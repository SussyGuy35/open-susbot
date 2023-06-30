import random

##### The responses are taken from susbot (legacy) v0.10 and ChatGPT #####
# Put on apostrophe ('): Take from susbot v0.10
# Put on quotation mark ("): Take from ChatGPT (thank LeiZanTheng)

ans = [	   
    'Hmmm tại sao mày lại hỏi tao cái này?',
	'Bạn không có đủ trình độ để hỏi con bot thông minh như tôi bruh',
	'Xin lỗi tôi đang bận',
	'Hỏi thừa à?',
	'Câu trả lời quá rõ ràng rồi má hỏi lắm',
	'*Server sập lol*',
	'Chắc chắn câu trả lời là có',
	'Không liên quan nhưng Đảng Cộng sản Việt Nam quang vinh muôn năm!',
	'Bạn muốn biết à ?',
	'Nếu đây là câu hỏi về thời gian thì đáp án là 2069, còn nếu không phải thì tôi chịu 🐧',
	'Đương nhiên',
	'Nếu có thắc mắc gì, hãy hỏi Google',
	'Đi mà hỏi thằng Bách ấy tôi bận rồi',
	':)',
	'Câu trả lời chắc chắn là không',
	'Hỏi dễ quá nên không muốn trả lời',
	'lol',
	'Bạn nên đi khám đi á',
    "Câu hỏi này quá dễ dàng, hãy thử cho tôi một câu hỏi khó hơn đi.",
    "Tôi đã nghe câu hỏi này quá nhiều lần, có gì đó thú vị hơn không?",
    "Tôi đã được lập trình để trả lời những câu hỏi khó hơn, nhưng câu hỏi này quá đơn giản.",
    "Câu hỏi này quá trẻ con đối với tôi. Hãy đặt một câu hỏi phức tạp hơn đi.",
    "Tôi biết câu trả lời, nhưng tôi muốn bạn tự tìm hiểu để trở nên thông minh hơn.",
    "Tôi có thể trả lời câu hỏi này, nhưng tôi nghĩ bạn có thể tìm hiểu nó dễ dàng hơn.",       
    "Câu hỏi này quá dễ dàng, tôi đã trả lời nó hàng trăm lần.",
    "Rất tiếc, tôi không thể tiết lộ câu trả lời cho câu hỏi này. Bạn có câu hỏi khác không?",
    "Tôi đã trả lời câu hỏi tương tự rất nhiều lần. Có gì đó thú vị hơn không?",
    "Tôi biết câu trả lời, nhưng tôi muốn bạn suy nghĩ và tìm hiểu nó bằng chính mình.",
    "Câu hỏi này quá đơn giản, hãy thử đặt một câu hỏi phức tạp hơn đi.",
    "Tôi đã được lập trình để trả lời những câu hỏi khó hơn. Có gì đó thách thức hơn không?",
    "Tôi biết câu trả lời, nhưng tôi muốn bạn có cơ hội tự tìm hiểu và khám phá.",
    "Câu hỏi này quá dễ dàng, tôi cần một thách thức lớn hơn.",
    "Rất tiếc, tôi không thể chia sẻ câu trả lời với bạn. Có câu hỏi khác mà tôi có thể giúp đỡ?",
    "Tôi đã trả lời câu hỏi tương tự rất nhiều lần. Bạn có câu hỏi thú vị hơn không?",
    "Câu hỏi này quá đơn giản, hãy thử đặt một câu hỏi phức tạp hơn để tôi đáp.",
    "Tôi đã nghe câu hỏi này rất nhiều lần. Có gì đó mới lạ hơn không?",
    "Tôi biết câu trả lời, nhưng tôi muốn bạn có cơ hội tự khám phá và học hỏi.",
    "Câu hỏi này quá dễ dàng cho tôi. Hãy đặt một câu hỏi phức tạp hơn để tôi thể hiện khả năng của mình."
]

def command_response(question):
    if question == '':
        return "Hỏi gì đi chứ ba"
    else:
        return random.choice(ans)