
def generate_answer_prompt_en(question, context):
    messages = {
        "messages": [
            {
            "content": """You are a helpful, respectful assistant. You will be given a HR Policy on user queries HR POLICY DETAILS, and QUESTION from user. Answer the following question in Thai language according to the HR POLICY DETAIL.""",
            "role": "system"
            },
            {
            "content": f"""
HR POLICY DETAILS: {context}
QUESTION: {question}
ANSWER:""",
            "role": "user"
            }
        ]
    }
    return messages["messages"]
  

# def generate_prompt_th(question, context):
#     output = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
# คุณเป็นผู้ช่วยที่ใจดี โปรดตอบคำถามอย่างใจดีและมีประโยชน์ที่สุดเสมอ พร้อมกับรักษาความปลอดภัย คำตอบของคุณไม่ควรมีเนื้อหาที่เป็นอันตราย ไม่ธรรมดา แบ่งแยกทางเชื้อชาติ ลำเอียงทางเพศ มีพิษ อันตราย หรือผิดกฎหมาย โปรดให้แน่ใจว่าคำตอบของคุณไม่มีอคติทางสังคมและเป็นบวกในธรรมชาติ ถ้าคำถามไม่มีเหตุผล หรือไม่สอดคล้องกับความเป็นจริง โปรดอธิบายเหตุผลแทนที่จะตอบคำถามที่ไม่ถูกต้อง ถ้าคุณไม่ทราบคำตอบของคำถาม โปรดอย่าแชร์ข้อมูลที่ผิด 
# คุณจะได้รับนโยบายทรัพยากรบุคคล ที่เป็นแหล่งฃ้อมูลในการคำถามจากผู้ใช้ จงตอบคำถามเป็นภาษาไทย

# รายละเอียดนโยบายทรัพยากรบุคคล:
# {context}

# คำถาม: {question}

# ตอบคำถามโดยใช้ลฃ้อมูลจาก "รายละเอียดนโยบายทรัพยากรบุคคล" อธิบายเหตุผลของคุณ
# หากคำถามไม่เกี่ยวข้องกับข้อมูลอ้างอิง โปรดตอบว่า “ฉันไม่ทราบคำตอบ, มันไม่ใช่ส่วนหนึ่งของนโยบายทรัพยากรบุคคลที่ได้รับ”
# <|eot_id|><|start_header_id|>user<|end_header_id|>
# {question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
#     return output  