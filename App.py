import streamlit as st
import pickle
import numpy as np

# --- ส่วน CSS: ปรับพื้นหลังใหญ่แผ่นเดียวและองค์ประกอบกลมมน ---
def pink_full_background_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap');
    
    /* ปรับฟอนต์และพื้นหลังใหญ่สุด */
    html, body, [class*="css"] {
        font-family: 'Kanit', sans-serif;
    }

    /* สร้างกรอบพื้นหลังใหญ่ครอบคลุมพื้นที่ทั้งหมด */
    .main {
        background-color: #FFF0F5; /* สีชมพูอ่อนมากสำหรับพื้นหลัง */
        padding: 20px;
    }

    /* ปรับแต่ง Container หลักให้เป็นกรอบสีชมพูใหญ่แผ่นเดียว */
    [data-testid="stAppViewContainer"] {
        background-color: #FFF0F5;
    }
    
    [data-testid="stVerticalBlock"] {
        background-color: #ffffffaa; /* สีขาวโปร่งแสงเพื่อให้เห็นพื้นหลังชมพู */
        padding: 40px;
        border-radius: 40px;
        box-shadow: 0 10px 30px rgba(255, 182, 193, 0.3);
        border: 2px solid #FFB1CF;
    }

    /* ปรับแต่ง Dropdown และ Slider ให้ดูเข้ากัน */
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 20px !important;
    }
    
    /* ปุ่มกดทรงมนยาว (Pill Shape) */
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 3.5em;
        background: linear-gradient(45deg, #FF74B1, #FF9BCC);
        color: white;
        border: none;
        font-weight: 600;
        font-size: 18px;
        transition: 0.4s;
        box-shadow: 0 4px 15px rgba(255, 116, 177, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 116, 177, 0.5);
    }

    /* กล่องผลลัพธ์ทรงมนสวยๆ */
    .prediction-card {
        padding: 25px;
        border-radius: 40px;
        background: white;
        border: 3px solid #FF74B1;
        margin-top: 25px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# เรียกใช้ CSS
pink_full_background_style()

# --- โค้ดเดิม (ห้ามเปลี่ยน Logic) ---
model = pickle.load(open('commute_model.pkl', 'rb'))

st.set_page_config(page_title="Commute Time Predictor", layout="centered", page_icon="🌸")

# ส่วนหัวเรื่อง
st.markdown("<h1 style='text-align: center; color: #FF74B1;'>🌸 Travel discrepancies</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; margin-bottom: 30px;'>วิเคราะห์ความคลาดเคลื่อนในการเดินทาง</p>", unsafe_allow_html=True)

# ส่วนกรอกข้อมูล (ไม่มีกรอบแยกแล้ว จะลอยอยู่บนพื้นหลังใหญ่แผ่นเดียว)
col1, col2 = st.columns(2)
with col1:
    day = st.selectbox("📅 ประเภทวัน", options=[(1, "วันธรรมดา (จ-ศ)"), (0, "วันเสาร์-อาทิตย์")], format_func=lambda x: x[1])
    rain = st.selectbox("🌧️ สภาพอากาศ", options=[(1, "ฝนตก"), (0, "ฝนไม่ตก")], format_func=lambda x: x[1])
    mode = st.selectbox("🚌 วิธีการเดินทาง", options=[(1, "รถเมล์"), (0, "รถไฟฟ้า")], format_func=lambda x: x[1])

with col2:
    hour = st.slider("⏰ ช่วงเวลาเดินทาง (นาฬิกา)", 6, 22, 8)
    crowd = st.slider("👥 ความหนาแน่นของคน (1-5)", 1, 5, 3)

st.write("") 

# ปุ่มทำนายผล
if st.button("💖 เริ่มคำนวณเลย"):
    input_data = np.array([[day[0], rain[0], mode[0], hour, crowd]])
    prediction = model.predict(input_data)
    
    buffer_time = max(0, prediction[0])
    
    st.markdown(f"""
        <div class="prediction-card">
            <h3 style='margin:0; color: #D81B60;'>⏳ ผลพยากรณ์</h3>
            <p style='font-size: 28px; font-weight: bold; color: #FF4B91;'>ควรเผื่อเวลาเพิ่ม {buffer_time:.0f} นาทีนะคะ</p>
        </div>
    """, unsafe_allow_html=True)

    if buffer_time > 30:
        st.warning("⚠️ แนะนำให้เผื่อเวลามากเป็นพิเศษนะคะ")
    else:
        st.success("✅ การเดินทางค่อนข้างเสถียรค่ะ")