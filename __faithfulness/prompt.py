def faithfulness_divide_answer_prompt_EN(answer):
    messages = {
        "messages": [
            {
            "content": """Break down the complex Thai sentences into specific, simpler, understandable Thai sentences. Provide the answers in an array format. If the original sentence is simple, return an array containing the original sentence. 
For example: 
Original Sentence: อัลเบิร์ต ไอน์สไตน์เป็นนักฟิสิกส์ทฤษฎีชาวเยอรมันมาแต่โดยกำเนิด ซึ่งเป็นที่ยอมรับกันอย่างกว้างขวางว่าเป็นหนึ่งในนักฟิสิกส์ที่ยิ่งใหญ่ที่สุดตลอดกาล เขาได้เป็นที่รู้จักกันในการพัฒนาทฤษฎีสัมพัทธภาพ แต่เขายังมีส่วนสำคัญในการพัฒนาทฤษฎีกลศาสตร์ควอนตัม,
Simple Sentences: ["อัลเบิร์ต ไอน์สไตน์เป็นนักฟิสิกส์ทฤษฎีชาวเยอรมันมาแต่โดยกำเนิด", "อัลเบิร์ต ไอน์สไตน์เป็นที่ยอมรับกันอย่างกว้างขวางว่าเป็นหนึ่งในนักฟิสิกส์ที่ยิ่งใหญ่ที่สุดตลอดกาล", "อัลเบิร์ต ไอน์สไตน์เป็นที่รู้จักกันในการพัฒนาทฤษฎีสัมพัทธภาพ", "อัลเบิร์ต ไอน์สไตน์มีส่วนสำคัญในการพัฒนาทฤษฎีกลศาสตร์ควอนตัม"] 
Original Sentence: หากพนักงานมีวันลาสะสมน้อยกว่า 18 วันในหนึ่งปี จะต้องใช้วันลาเพิ่มเติมเพื่อให้บรรลุวัตถุประสงค์ของการรักษาสมดุลชีวิตการทำงาน ตามนโยบายการลาของบริษัท ซึ่งกำหนดให้พนักงานต้องใช้วันลา 18 วันในหนึ่งปี โดยแบ่งเป็น EL 12 วันและ CL 6 วัน
Simple Sentences: ["หากพนักงานมีวันลาสะสมน้อยกว่า 18 วันในหนึ่งปี จะต้องใช้วันลาเพิ่มเติม", "พนักงานจะต้องบรรลุวัตถุประสงค์ของการรักษาสมดุลชีวิตการทำงาน ตามนโยบายการลาของบริษัท", "นโยบายการลาของบริษัทกำหนดให้พนักงานต้องใช้วันลา 18 วันในหนึ่งปี", "วันลา 18 วันในหนึ่งปีแบ่งเป็น EL 12 วันและ CL 6 วัน"] 
Original Sentence: ไม่ การลาชั่วคราวไม่สามารถนำไปสู้ปีถัดไปได้ ตามนโยบายการลาชั่วคราวของบริษัท
Simple Sentences: ["ไม่ การลาชั่วคราวไม่สามารถนำไปสู้ปีถัดไปได้ ตามนโยบายการลาชั่วคราวของบริษัท"] 
Original Sentence: ถ้าพนักงานไม่แน่ใจว่าจะขยายการลาต่อเนื่องกันหรือไม่ ควรแจ้งผู้จัดการที่รายงานล่วงหน้าเพื่อขออนุมัติและรอผลการตัดสินใจจากผู้จัดการที่รายงานก่อนจะขยายการลาเพิ่มเติม
Simple Sentences: ["ถ้าพนักงานไม่แน่ใจว่าจะขยายการลาต่อเนื่องกันหรือไม่ ควรแจ้งผู้จัดการที่รายงานล่วงหน้าเพื่อขออนุมัติ", "ถ้าพนักงานควรรอผลการตัดสินใจจากผู้จัดการที่รายงานก่อนจะขยายการลาเพิ่มเติม”] 
Original Sentence: ถ้าฉันใช้จ่ายเงิน 2,500 ดอลลาร์ในธุรกรรมเดียวที่ร้านค้าที่เข้าร่วมของ XYZ Corporation จะได้รับคะแนนสะสม
Simple Sentences: ["ถ้าฉันใช้จ่ายเงิน 2,500 ดอลลาร์ในธุรกรรมเดียวที่ร้านค้าที่เข้าร่วมของ XYZ Corporation จะได้รับคะแนนสะสม"] 
Original Sentence: เงื่อนไขเป็นไปตามที่บริษัทฯ กำหนด และขอสงวนสิทธิ์ในการเปลี่ยนแปลงเงื่อนไข หรือยกเลิกโดยไม่ต้องแจ้งให้ทราบล่วงหน้า
Simple Sentences: ["เงื่อนไขเป็นไปตามที่บริษัทฯ กำหนด", "ขอสงวนสิทธิ์ในการเปลี่ยนแปลงเงื่อนไข", "ขอสงวนสิทธิ์ในการยกเลิกโดยไม่ต้องแจ้งให้ทราบล่วงหน้า"] 
""",
            "role": "system"
            },
            {
            "content": f"""Here is the actual Original Sentence I want you to break down the information from. Only use the information from this New Original Sentence. Answer in array of strings that can directly be turned into array.: 
New Original Sentence: {answer}""",
            "role": "user"
            },
            {
            "content": "Simple Sentences: [\"",
            "role": "assistant"
            },
        ]
    }
    return messages["messages"]

def faithfulness_evaluation_prompt_EN(context, answer):
    messages = {
        "messages": [
            {
            "content": "Your task is to judge the faithfulness of a statements in Thai based on a given context in Thai. For each statement you must return verdict as {1} if the statement can be directly inferred based on the context, or {0} if the statement can not be directly inferred based on the context.",         
            "role": "system"
            },
            {
            "content": f"""Statement: {answer}
Context: {context}""",
            "role": "user"
            },
            {
            "content": "Answer: {",
            "role": "assistant"
            },
        ]
    }
    return messages["messages"]