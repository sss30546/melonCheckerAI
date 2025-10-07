                 #!/usr/bin/env python3

import os
import json
import datetime
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

st.set_page_config(page_title="AI Melon Ripeness Bot", page_icon="🍈", layout="wide")

# โหลดค่า API KEY จาก Secrets หรือ .env
load_dotenv(".env")
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
client = Groq(api_key=GROQ_API_KEY)

# ฟังก์ชันคำนวณวันคงเหลือ
def คำนวณวันคงเหลือ(จำนวนวันที่เก็บแล้ว):
    อายุรวม = 14
    try:
        วันเก็บแล้ว = int(จำนวนวันที่เก็บแล้ว)
        คงเหลือ = max(0, อายุรวม - วันเก็บแล้ว)
        return คงเหลือ
    except:
        return None

# ฟังก์ชันแชตกับ Groq
def chatboot(question):
    system_prompt = """ 
คุณคือผู้เชี่ยวชาญการจำแนกความสุกของเมล่อน... (ขอย่อไว้ในตัวอย่างนะครับ แต่คุณสามารถใส่ system_prompt เต็มได้เหมือนเดิม)
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",  # ✅ แก้ตรงนี้
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.2,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()

# ฟังก์ชันคำนวณคงเหลือจากวันที่เริ่มสุก
def คงเหลือก่อนเน่าเสีย(วันที่เริ่มสุก):
    วันนี้ = datetime.date.today()
    วันผ่านไป = (วันนี้ - วันที่เริ่มสุก).days
    รวมวันก่อนเน่า = 13 + 7
    คงเหลือ = max(0, รวมวันก่อนเน่า - วันผ่านไป)
    return คงเหลือ

# main app
def main():
    st.markdown("""
        <style>
        body { background-color: #000000; }
        .stForm { background-color: #000000; padding: 2rem; border-radius: 12px; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🍈 แชตบอตเกษตรอัจฉริยะ")
    st.subheader("ช่วยวิเคราะห์ความสุกของเมลอน ด้วย AI")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "สวัสดีจ้าว... (ข้อความแนะนำ)"}
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

    # แสดงผลแชต
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
                    col1.metric("ความหวาน", data.get("brix", "ไม่ระบุ"))
                    col1.metric("สี", data.get("สีของเนื้อเมลอน", "ไม่ระบุ"))
                    col2.metric("ความแน่นเนื้อ", data.get("ความแน่นเนื้อ", "ไม่ระบุ"))
                    col2.metric("ค่า pH", data.get("ph", "ไม่ระบุ"))
                    วันคงเหลือ = คำนวณวันคงเหลือ(data.get("อายุการเก็บรักษาก่อนเน่าเสีย"))
                    col2.metric("คงเหลือก่อนเน่าเสีย", f"{วันคงเหลือ} วัน" if วันคงเหลือ is not None else "ไม่ระบุ")
                    col2.metric("กลิ่น", data.get("กลิ่นเมล่อน", "ไม่ระบุ"))
                    st.info(data.get("reason", "ไม่พบเหตุผล"))
            except:
                st.markdown(f"**🤖 อองตอง:** {msg['content']}")

    st.markdown("---")
    st.caption("🌱 พัฒนาโดยทีม Sn.Guardian gen X...")

if __name__ == "__main__":
    main()

