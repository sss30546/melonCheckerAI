#!/usr/bin/env python3
import os
import json
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# โหลดค่า ENV
load_dotenv(".env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="🍋 Lemon Disease AI Bot", page_icon="🍋", layout="wide")

# ฟังก์ชันแชตบอต
def chatboot(question):
    system_prompt = """
คุณคือผู้เชี่ยวชาญด้านโรคพืช โดยเฉพาะ "โรคในเลมอน (Lemon)"  
โปรดวิเคราะห์อาการที่ผู้ใช้พิมพ์เข้ามา แล้วจำแนกว่าเลมอนอาจเป็นโรคใดใน 3 โรคหลักนี้  
พร้อมสรุปคำแนะนำในการจัดการเบื้องต้นให้เกษตรกรเข้าใจง่าย

**โรคที่ต้องจำแนกได้:**
1. **โรคแคงเกอร์ (Citrus Canker)**  
   - ใบอ่อนและผลอ่อนมีจุดนูนสีน้ำตาล ล้อมด้วยวงสีเหลือง  
   - แผลแข็งและหยาบ เมื่อลูบจะสากมือ  
   - สาเหตุ: แบคทีเรีย *Xanthomonas citri*  
   - แนวทางจัดการ: ตัดกิ่งที่เป็นโรค, ใช้สารคอปเปอร์

2. **โรคสแคบ (Citrus Scab)**  
   - ใบและผลอ่อนมีตุ่มนูนคล้ายสะเก็ด  
   - แผลสีครีมหรือเหลืองอ่อน เปลี่ยนเป็นสีน้ำตาลในภายหลัง  
   - สาเหตุ: เชื้อรา *Elsinoë fawcetti*  
   - แนวทางจัดการ: พ่นสารแมนโคเซบ หรือคอปเปอร์

3. **โรคแอนแทรคโนส (Anthracnose)**  
   - พบจุดสีน้ำตาลดำหรือส้ม แผลแห้ง ผลร่วงง่าย  
   - สาเหตุ: เชื้อรา *Colletotrichum gloeosporioides*  
   - แนวทางจัดการ: เก็บผลที่เป็นโรคออก, พ่นสารป้องกันเชื้อรา

**รูปแบบการตอบกลับ:**
ให้ตอบกลับเป็น JSON ภาษาไทย ตามโครงสร้างนี้:
{
  "disease": "ชื่อโรค" หรือ "ไม่สามารถระบุได้",
  "สาเหตุ": "ชื่อเชื้อสาเหตุหรือไม่ทราบ",
  "อาการที่พบ": "สรุปอาการหลักตามคำบรรยายของผู้ใช้",
  "แนวทางจัดการเบื้องต้น": "คำแนะนำที่เหมาะสม",
  "reason": "เหตุผลที่ใช้ในการวิเคราะห์"
}
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.3,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()


# ส่วนแสดงผลบนหน้าเว็บ
def main():
    st.markdown("""
        <style>
        /* จัดข้อความให้อยู่ในกล่องไม่ตกขอบ */
        .chat-bubble {
            background-color: #f0f2f6;
            padding: 12px 18px;
            border-radius: 12px;
            margin-bottom: 10px;
            word-wrap: break-word;
            white-space: pre-wrap;
            font-size: 16px;
            line-height: 1.5;
        }
        .chat-user {
            background-color: #e8ffe8;
        }
        .chat-bot {
            background-color: #fff6e6;
        }
        .stTextInput > div > div > input {
            font-size: 16px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🍋 Preliminary Lemon Disease Checker Chatbot")
    st.subheader("บรรยายลักษณะของเลมอน แล้วให้ AI วิเคราะห์ว่าอาจเป็นโรคอะไร")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": (
                "สวัสดีจ้า 🍋 ฉันเป็นแชตบอตผู้ช่วยวิเคราะห์โรคในเลมอน "
                "3 โรค ได้แก่ Citrus canker, Citrus scab, Anthracnose\n\n"
                "🟢 โปรดบอกอาการ เช่น:\n"
                "- ใบมีจุดนูนสีน้ำตาล ขอบเหลือง\n"
                "- ผลมีรอยแผลแห้งสีน้ำตาลเข้ม\n"
                "- กิ่งแห้งหรือยอดเหี่ยว\n\n"
                "จากนั้นฉันจะช่วยวิเคราะห์ให้เลย!"
            )}
        ]

    with st.form("chat_form"):
        query = st.text_input("🗣️ คุณ:", placeholder="เช่น 'ใบมีจุดนูนสีน้ำตาล มีขอบเหลืองรอบๆ'").strip()
        submitted = st.form_submit_button("🚀 ส่งข้อความ")

        if submitted and query:
            answer = chatboot(query)
            st.session_state["messages"].append({"role": "user", "content": query})
            st.session_state["messages"].append({"role": "assistant", "content": answer})
        elif submitted and not query:
            st.warning("⚠️ กรุณาพิมพ์อาการก่อนส่ง")

    # แสดงข้อความโต้ตอบในรูปแบบกล่องสวยงาม
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-bubble chat-user'><b>🧑‍🌾 คุณ:</b> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            try:
                data = json.loads(msg["content"])
                html = f"""
                <div class='chat-bubble chat-bot'>
                    <b>🤖 ผลการวิเคราะห์:</b><br>
                    <b>โรคที่เป็นไปได้:</b> {data.get("disease", "ไม่ระบุ")}<br>
                    <b>สาเหตุ:</b> {data.get("สาเหตุ", "ไม่ระบุ")}<br>
                    <b>อาการที่พบ:</b> {data.get("อาการที่พบ", "ไม่ระบุ")}<br>
                    <b>แนวทางจัดการเบื้องต้น:</b> {data.get("แนวทางจัดการเบื้องต้น", "ไม่ระบุ")}<br>
                    <b>เหตุผล:</b> {data.get("reason", "ไม่ระบุ")}
                </div>
                """
                st.markdown(html, unsafe_allow_html=True)
            except Exception:
                st.markdown(f"<div class='chat-bubble chat-bot'><b>🤖 น้องสตางค์:</b> {msg['content']}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("🌱 พัฒนาโดยทีม Future Lab | ระบบแชตบอตวิเคราะห์โรคในเลมอน (Citrus AI Expert)")

if __name__ == "__main__":
    main()
