import streamlit as st
import pandas as pd
import joblib

# โหลดโมเดล
model = joblib.load("solar_wind_predictor_model.pkl")

st.set_page_config(page_title="Kp Index Predictor", layout="centered")
st.title("🔮 พยากรณ์ค่า Kp Index จากข้อมูลลมสุริยะ")
st.markdown("กรอกค่าที่ต้องการแล้วกดปุ่มเพื่อดูค่าพยากรณ์ Kp")

# แบบฟอร์มกรอกข้อมูล
with st.form("input_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        bz = st.number_input("Bz (nT)", value=-5.0, format="%.2f")
    with col2:
        speed = st.number_input("Speed (km/s)", value=400.0, format="%.2f")
    with col3:
        density = st.number_input("Density (N/cm³)", value=8.0, format="%.2f")

    submitted = st.form_submit_button("🔍 พยากรณ์ค่า Kp")

if submitted:
    new_data = pd.DataFrame([{"Bz": bz, "Speed": speed, "Density": density}])
    new_data["Speed_Density_Ratio"] = new_data["Speed"] / (new_data["Density"] + 1e-6)
    new_data["Bz_Squared"] = new_data["Bz"] ** 2
    new_data["Energy_Flux"] = (new_data["Speed"] ** 2) * new_data["Density"]

    prediction = model.predict(new_data)[0]

    st.success(f"ค่าพยากรณ์ Kp Index คือ: {prediction:.2f}")

    if prediction < 10:
        st.info("🟢 ระดับปลอดภัย")
    elif prediction < 30:
        st.warning("🟠 เริ่มมีความเสี่ยง")
    else:
        st.error("🔴 ระดับอันตรายสูง! ควรระวังผลกระทบจากพายุสุริยะ")
