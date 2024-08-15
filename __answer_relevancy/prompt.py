def answer_relevancy_predict_questions_prompt_EN(answer):
    messages = {
        "messages": [
            {
            "content": """You will be given a Given Answer to an unknown Thai question with its supported context, you task is to predict 3 most reasonable Questions that would match the given answer in an array format. Please predict the question in Thai language. Do not provide further explanation or translation'
For example: 
Given Answer: อัลเบิร์ต ไอน์สไตน์เป็นนักฟิสิกส์ทฤษฎีชาวเยอรมันมาแต่โดยกำเนิด ซึ่งเป็นที่ยอมรับกันอย่างกว้างขวางว่าเป็นหนึ่งในนักฟิสิกส์ที่ยิ่งใหญ่ที่สุดตลอดกาล เขาได้เป็นที่รู้จักกันในการพัฒนาทฤษฎีสัมพัทธภาพ แต่เขายังมีส่วนสำคัญในการพัฒนาทฤษฎีกลศาสตร์ควอนตัม
Predicted Questions: ["อัลเบิร์ต ไอน์สไตน์เป็นใคร", "ใครคืออัลเบิร์ต ไอน์สไตน์", "อัลเบิร์ต ไอน์สไตน์ทำอาชีพอะไร"] 
""",
            "role": "system"
            },
            {
            "content": f"""Here is the actual Given Answer I want you to 3 most reasonable Questions that would match the given answer in Thai language. Only use the information from this New Given Answer. Answer in array of strings that can directly be turned into array: 
New Given Answer: {answer}""",
            "role": "user"
            },
            {
            "content": "Predicted Questions: [\"",
            "role": "assistant"
            },
        ]
    }
    return messages["messages"]



# Given Answer: หากพนักงานมีวันลาสะสมน้อยกว่า 18 วันในหนึ่งปี จะต้องใช้วันลาเพิ่มเติมเพื่อให้บรรลุวัตถุประสงค์ของการรักษาสมดุลชีวิตการทำงาน ตามนโยบายการลาของบริษัท ซึ่งกำหนดให้พนักงานต้องใช้วันลา 18 วันในหนึ่งปี โดยแบ่งเป็น EL 12 วันและ CL 6 วัน
# Predicted Questions: ["หากพนักงานมีวันลาสะสมน้อยกว่า 18 วันในหนึ่งปี จะต้องลาเพิ่มเติมกี่วัน", "พนักงานจะต้องบรรลุวัตถุประสงค์ของการรักษาสมดุลชีวิตการทำงาน ตามนโยบายการลาของบริษัท", "นโยบายการลาของบริษัทกำหนดให้พนักงานต้องใช้วันลา 18 วันในหนึ่งปี", "วันลา 18 วันในหนึ่งปีแบ่งเป็น EL 12 วันและ CL 6 วัน"] 
# Given Answer: ไม่ การลาชั่วคราวไม่สามารถนำไปสู้ปีถัดไปได้ ตามนโยบายการลาชั่วคราวของบริษัท
# Predicted Questions: ["การลาชั่วคราวสามารถนำไปสู้ปีถัดไปได้หรือไม่", ""] 
# Given Answer: ถ้าฉันใช้จ่ายเงิน 2,500 ดอลลาร์ในธุรกรรมเดียวที่ร้านค้าที่เข้าร่วมของ XYZ Corporation จะได้รับคะแนนสะสม
# Predicted Questions: ["ถ้าฉันใช้จ่ายเงิน 2,500 ดอลลาร์ในธุรกรรมเดียวที่ร้านค้าที่เข้าร่วมของ XYZ Corporation จะได้รับคะแนนสะสมหรือไม่"] 
# Given Answer: เงื่อนไขเป็นไปตามที่บริษัทฯ กำหนด และขอสงวนสิทธิ์ในการเปลี่ยนแปลงเงื่อนไข หรือยกเลิกโดยไม่ต้องแจ้งให้ทราบล่วงหน้า
# Predicted Questions: ["เงื่อนไขเป็นไปตามที่บริษัทฯ กำหนด", "ขอสงวนสิทธิ์ในการเปลี่ยนแปลงเงื่อนไข", "ขอสงวนสิทธิ์ในการยกเลิกโดยไม่ต้องแจ้งให้ทราบล่วงหน้า"] 
