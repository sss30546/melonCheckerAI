#!/usr/bin/env python3

import os
import json
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# โหลด environment variables จากไฟล์ .env
load_dotenv(".env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def chatboot(question):
    system_prompt = """
    คุณคือผู้เชี่ยวชาญการจำแนกความสุกของเมล่อน โปรดวิเคราะห์ข้อมูลที่ได้รับและจำแนกความสุกของเมล่อนออกเป็น 3 ระดับ: "เริ่มสุก" (Riping), "สุก" (Ripe), "เน่าเสีย" (Spoiled) หรือ "ไม่สามารถพิจารณาได้" (Cannot determine) แล้วตอบกลับเป็นภาษาไทยเท่านั้น

**หลักเกณฑ์การพิจารณาความสุกของเมล่อน:**

ในการพิจารณาความสุกของเมล่อน ให้พิจารณาจาก 6 มิติข้อมูลต่อไปนี้ พร้อมเกณฑ์อ้างอิง:

1.  **ค่าพีเอช (pH):**
    * **เริ่มสุก:** 5.76 - 6.27
    * **สุก:** 5.48 - 6.12
    * **เน่าเสีย:** ≤ 5.83
2.  **ค่าองศาบริกซ์ (%Brix) (ความหวาน):**
    * **เริ่มสุก:** 6.20 - 11.50
    * **สุก:** 5.50 - 9.00
    * **เน่าเสีย:** ≤ 8.20
3.  **ความแน่นเนื้อ (หน่วยเป็นนิวตัน, N):**
    * **เริ่มสุก:** 32 - 39 N
    * **สุก:** 11 - 27 N
    * **เน่าเสีย:** < 11 N
4.  **สีของเนื้อเมล่อน:**
    * **เริ่มสุก:** เนื้อสีเขียว
    * **สุก:** เนื้อสีเหลือง
    * **เน่าเสีย:** เนื้อสีเหลืองช้ำ
5.  **กลิ่นเมล่อน:**
    * **เริ่มสุก:** กลิ่นหอมหวาน
    * **สุก:** กลิ่นหอมน้อยลง, มีกลิ่นเปรี้ยวเล็กน้อย
    * **เน่าเสีย:** กลิ่นเหม็นรุนแรงคล้ายแอลกอฮอล์
6.  **จำนวนวันที่สามารถเก็บรักษาก่อนเน่าเสีย (วัน):**
    * **เริ่มสุก:** 8 - 13 วัน (เมื่อเริ่มต้นการสุก)
    * **สุก:** 1 - 7 วัน
    * **เน่าเสีย:** 0 วัน หรือ น้อยกว่า 1 วัน (เน่าเสียแล้ว)

**ข้อมูลเพิ่มเติมเกี่ยวกับ Shelf Life:** เมล่อนมีอายุการเก็บรักษา (shelf life) ประมาณ 14 วัน นับจากวันที่เริ่มสุกจนถึงวันที่เน่าเสีย หากข้อมูลที่ระบุมามีจำนวนวันเก็บรักษามากกว่า 13 วัน แต่ลักษณะอื่นๆ บ่งชี้ว่าเริ่มสุก ก็ยังคงพิจารณาเป็นเริ่มสุกได้ แต่หากระบุจำนวนวันเป็น 0 หรือน้อยกว่า 1 จะถือว่าเน่าเสีย

**ข้อกำหนดเพิ่มเติม:**
* หากคำบรรยายมีข้อมูลไม่เพียงพอในการตัดสินใจความสุกของเมล่อน (เช่น ข้อมูลไม่ครบ 6 มิติ) ให้ตอบว่า "ไม่สามารถพิจารณาได้"
* กรณี "ไม่สามารถพิจารณาได้" ให้ระบุจำนวนมิติข้อมูลที่ขาดหายไปจากทั้งหมด 6 มิติ ในช่อง reason

**รูปแบบการตอบกลับ:**

โปรดตอบกลับในรูปแบบ JSON เท่านั้น โดยมีโครงสร้างดังนี้:
{
  "ripeness": "เริ่มสุก" หรือ "สุก" หรือ "เน่าเสีย" หรือ "ไม่สามารถพิจารณาได้",
  "brix": (ค่าตัวเลข เช่น 13.2 หรือ null ถ้าไม่ระบุ),
  "ph": (ค่าตัวเลข เช่น 6.3 หรือ null ถ้าไม่ระบุ),
  "ความแน่นเนื้อ": (ค่าตัวเลข เช่น 24 หรือ null ถ้าไม่ระบุ),
  "reason": "คำอธิบายเหตุผลที่ทำให้ตัดสินใจว่าเมล่อนอยู่ในระดับความสุกใด หรือเหตุผลที่ทำให้ไม่สามารถพิจารณาได้ (พร้อมบอกจำนวนมิติข้อมูลที่ขาดหายไป)"
}
         """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.2,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()


def main():
    # 🖼️ ตั้งค่าหน้าและธีมสี
    st.set_page_config(page_title="AI Melon Ripeness Bot", page_icon="🍈", layout="wide")
    st.markdown("""
        <style>
        body { background-color: #000000; }
        .stForm { background-color: #000000; padding: 2rem; border-radius: 12px; }
        </style>
    """, unsafe_allow_html=True)

    ##st.image("blue.jpg", use_column_width=True)
    st.title("🍈 แชตบอตเกษตรอัจฉริยะ")
    st.subheader("ช่วยวิเคราะห์ความสุกของเมลอน ด้วย AI ")

    # 🧾 เก็บข้อความสนทนา
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "สวัสดีค่ะ ฉันสามารถช่วยคุณวิเคราะห์ความสุกของเมล่อนได้จากคำบรรยาย 6 มิติค่ะ 🍈"}
        ]

    with st.form("chat_form"):
        query = st.text_input("🗣️ คุณ:", placeholder="พิมพ์ลักษณะของเมลอนที่ต้องการให้วิเคราะห์...").strip()
        submitted = st.form_submit_button("🚀 ส่งข้อความ")

        if submitted and query:
            answer = chatboot(query)
            st.session_state["messages"].append({"role": "user", "content": query})
            st.session_state["messages"].append({"role": "assistant", "content": answer})
        elif submitted and not query:
            st.warning("⚠️ กรุณาพิมพ์คำถามก่อนส่ง")

    # 🧠 แสดงผลแชตพร้อมจัดการ JSON
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"**🧑‍🌾 คุณ:** {msg['content']}")
        else:
            try:
                data = json.loads(msg["content"])
                with st.container():
                    st.markdown("#### 🤖 ผลการวิเคราะห์เมลอน")
                    col1, col2 = st.columns(2)
                    col1.metric("ความสุก", data.get("ripeness", "ไม่ระบุ"))
                    col1.metric("ค่า Brix", data.get("brix", "ไม่ระบุ"))
                    col2.metric("ค่า pH", data.get("ph", "ไม่ระบุ"))
                    st.info(data.get("reason", ""))
            except Exception:
                st.markdown(f"**🤖 บอท:** {msg['content']}")

    st.markdown("---")
    st.caption("🌱 พัฒนาโดยทีม Sn.Guardian gen X เป็นส่วนหนึ่งของโครงการบ่มเพาะนวัตกรปัญญาประดิษฐ์ (AI Innovator) 🤖")

if __name__ == "__main__":
    main()
