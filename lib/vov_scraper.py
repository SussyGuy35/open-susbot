import asyncio
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

# In-memory cache to avoid scraping multiple times a day
# Format: { "station_key": { "timestamp": float, "schedule": [(time, program), ...] } }
_cache = {}
_tz = pytz.timezone("Asia/Ho_Chi_Minh")
CACHE_TTL = 3600  # 1 hour in seconds

async def _fetch_html(url: str) -> str:
    """Fetch HTML content from a URL."""
    import socket
    connector = aiohttp.TCPConnector(family=socket.AF_INET)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url, timeout=15) as response:
            response.raise_for_status()
            return await response.text()

async def _scrape_vov3() -> list[tuple[str, str]]:
    url = "https://vov3.vov.vn/lich-phat-song"
    html = await _fetch_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    
    results = []
    seen_times = set()
    
    for li in soup.find_all('li', class_='sidebar-nav-item'):
        time_span = li.find('span', class_='view-field-airtime')
        title_span = li.find('span', class_='views-field-title')
        
        if time_span and title_span:
            time_text = time_span.text.strip()
            title_text = title_span.text.strip()
            
            if time_text and time_text not in seen_times:
                seen_times.add(time_text)
                results.append((time_text, title_text))
                
    return results

async def _scrape_vovgt(region: str) -> list[tuple[str, str]]:
    url = f"https://vovgiaothong.vn/lich-phat-song-{region}/"
    html = await _fetch_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    
    results = []
    seen_times = set()
    
    for tr in soup.find_all('tr', class_='trlps'):
        tds = tr.find_all('td')
        if len(tds) >= 2:
            time_text = tds[0].text.strip()
            title_span = tds[1].find('span', class_='titletable')
            
            if title_span:
                title_text = title_span.text.strip()
                if time_text and time_text not in seen_times:
                    seen_times.add(time_text)
                    results.append((time_text, title_text))
                    
    return results

async def get_schedule(station_key: str) -> list[tuple[str, str]] | None:
    """
    Get the schedule for a given station key.
    Returns a list of (time_str, program_name_str) or None if unsupported/error.
    """
    now_ts = datetime.now(_tz).timestamp()
    
    # Check cache
    if station_key in _cache:
        cached_data = _cache[station_key]
        if now_ts - cached_data["timestamp"] < CACHE_TTL:
            return cached_data["schedule"]

    # Scrape if not in cache or outdated
    schedule = None
    try:
        if station_key == "vov3":
            schedule = await _scrape_vov3()
        elif station_key == "vovgt_hn":
            schedule = await _scrape_vovgt("hn")
        elif station_key == "vovgt_hcm":
            schedule = await _scrape_vovgt("hcm")
    except Exception as e:
        print(f"[vov_scraper] Error scraping {station_key}: {e}")
        return None

    if schedule:
        _cache[station_key] = {
            "timestamp": now_ts,
            "schedule": schedule
        }
        
    return schedule

def get_current_program(schedule: list[tuple[str, str]]) -> str | None:
    """Find the currently playing program based on the current time."""
    now = datetime.now(_tz)
    current_mins = now.hour * 60 + now.minute
    
    for time_str, program in schedule:
        clean_str = time_str.replace(" ", "").replace(":", "h")
        if "-" not in clean_str:
            continue
        try:
            start_str, end_str = clean_str.split("-")
            start_mins = int(start_str.split("h")[0]) * 60 + int(start_str.split("h")[1])
            end_mins = int(end_str.split("h")[0]) * 60 + int(end_str.split("h")[1])
            
            # Handle cases like 23h00-00h00 (crosses midnight)
            if end_mins == 0:
                end_mins = 1440
                
            if start_mins <= current_mins < end_mins:
                return f"{time_str} - {program}"
        except Exception:
            continue
            
    return None
