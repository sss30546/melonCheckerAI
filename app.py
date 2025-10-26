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
   - แผลแข็งและมีลักษณะหยาบ เมื่อส่องดูจากด้านหลังใบจะนูนขึ้น  
   - พบได้ทั้งใบ กิ่ง และผล  
   - ผลมีแผลสีน้ำตาลเข้มเป็นวงกลม  
   - สาเหตุ: แบคทีเรีย *Xanthomonas citri*  
   - แนวทางจัดการ: ตัดแต่งกิ่งที่เป็นโรค, ใช้สารคอปเปอร์, หลีกเลี่ยงฝนสาด

2. **โรคสแคบ (Citrus Scab)**  
   - ใบและผลอ่อนมีตุ่มนูนคล้ายสะเก็ด  
   - แผลมีสีครีมหรือสีเหลืองอ่อน ต่อมาจะเปลี่ยนเป็นสีน้ำตาล  
   - ด้านล่างใบอาจมีจุดนูนสีน้ำตาลขนาดเล็ก  
   - สาเหตุ: เชื้อรา *Elsinoë fawcetti*  
   - แนวทางจัดการ: พ่นสารป้องกันกำจัดเชื้อรา เช่น แมนโคเซบ หรือ คอปเปอร์

3. **โรคแอนแทรคโนส (Anthracnose)**  
   - พบได้ที่ใบ กิ่ง และผล โดยเฉพาะผลแก่  
   - มีจุดช้ำสีน้ำตาลดำหรือสีส้ม แผลแห้ง凋เหี่ยว  
   - สาเหตุ: เชื้อรา *Colletotrichum gloeosporioides*  
   - แนวทางจัดการ: เก็บผลที่เป็นโรคออก, พ่นสารป้องกันเชื้อรา, ปรับการระบายอากาศ

**รูปแบบการตอบกลับ:**
ให้ตอบกลับเป็น JSON ภาษาไทย ตามโครงสร้างนี้:

{
  "disease": "โรคแคงเกอร์" หรือ "โรคสแคบ" หรือ "โรคแอนแทรคโนส" หรือ "ไม่สามารถระบุได้",
  "สาเหตุ": "ชื่อเชื้อสาเหตุหรือไม่ทราบ",
  "อาการที่พบ": "สรุปอาการหลักตามที่ผู้ใช้บรรยาย",
  "แนวทางจัดการเบื้องต้น": "คำแนะนำสำหรับเกษตรกร",
  "reason": "เหตุผลที่วิเคราะห์ว่าเป็นโรคนั้น หรือเหตุผลที่ยังไม่สามารถระบุได้"
}
หากข้อมูลไม่เพียงพอ ให้ตอบว่า "ไม่สามารถระบุได้" พร้อมแนะนำว่าควรบอกเพิ่มเติมเช่น ลักษณะของแผล, สี, ตำแหน่งที่พบ, ฯลฯ
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
    st.title("🍋 แชตบอตวิเคราะห์โรคในเลมอน (AI Lemon Disease Bot)")
    st.subheader("ให้บรรยายอาการของเลมอน แล้วให้ AI ช่วยวิเคราะห์ว่าเป็นโรคอะไร")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "สวัสดีจ้า 🍋 ฉันเป็นแชตบอตผู้ช่วยวิเคราะห์โรคในเลมอน เช่น แคงเกอร์ สแคบ และแอนแทรคโนส บอกฉันได้เลยว่าพบอาการแบบไหน เช่น 'ใบเป็นจุดนูนสีเหลือง' หรือ 'ผลมีรอยดำแห้ง' แล้วฉันจะช่วยวิเคราะห์ให้นะ"}
        ]

    with st.form("chat_form"):
        query = st.text_input("🗣️ คุณ:", placeholder="พิมพ์อาการของเลมอนที่พบ เช่น 'ใบเป็นจุดนูนสีน้ำตาล มีวงเหลืองรอบๆ'").strip()
        submitted = st.form_submit_button("🚀 ส่งข้อความ")

        if submitted and query:
            answer = chatboot(query)
            st.session_state["messages"].append({"role": "user", "content": query})
            st.session_state["messages"].append({"role": "assistant", "content": answer})
        elif submitted and not query:
            st.warning("⚠️ กรุณาพิมพ์อาการก่อนส่ง")

    # แสดงข้อความโต้ตอบ
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"**🧑‍🌾 คุณ:** {msg['content']}")
        else:
            try:
                data = json.loads(msg["content"])
                st.markdown("#### 🤖 ผลการวิเคราะห์โรคในเลมอน")
                col1, col2 = st.columns(2)
                col1.metric("โรคที่เป็นไปได้", data.get("disease", "ไม่ระบุ"))
                col1.metric("สาเหตุ", data.get("สาเหตุ", "ไม่ระบุ"))
                col2.metric("อาการที่พบ", data.get("อาการที่พบ", "ไม่ระบุ"))
                st.info(f"🧩 แนวทางจัดการเบื้องต้น: {data.get('แนวทางจัดการเบื้องต้น', 'ไม่ระบุ')}")
                st.success(f"🔍 เหตุผล: {data.get('reason', 'ไม่ระบุ')}")
            except Exception:
                st.markdown(f"**🤖 เลมอนบอต:** {msg['content']}")

    st.markdown("---")
    st.caption("🌱 พัฒนาโดยทีม future lab | ระบบแชตบอตวิเคราะห์โรคในเลมอน (Citrus AI Expert)")

if __name__ == "__main__":
    main()
