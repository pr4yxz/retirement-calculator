import streamlit as st

def format_years_months(months):
    years = months // 12
    months = months % 12
    if years and months:
        return f"{years} ปี {months} เดือน"
    elif years:
        return f"{years} ปี"
    else:
        return f"{months} เดือน"

def calculate_retirement_fund_with_return(age, retire_age, life_expectancy, monthly_expense, annual_return):
    months_saving = (retire_age - age) * 12
    months_using = (life_expectancy - retire_age) * 12

    # เงินที่ต้องใช้ตอนเกษียณรวมทั้งหมด (ไม่รวมดอกเบี้ย)
    needed_at_retirement = monthly_expense * months_using

    # คำนวณเงินที่ต้องเก็บต่อเดือน โดยสมมติว่าเงินที่เก็บมีผลตอบแทนแบบดอกเบี้ยทบต้น
    # สูตรเงินสะสม (Future Value of Annuity) FV = P * [((1 + r)^n -1)/r]
    # เราต้องการ FV = needed_at_retirement, r = monthly_return, n = months_saving
    # แก้สมการหาค่า P (เงินเก็บต่อเดือน)
    monthly_return = annual_return / 100 / 12
    if monthly_return > 0 and months_saving > 0:
        monthly_saving = needed_at_retirement * monthly_return / ((1 + monthly_return)**months_saving - 1)
    else:
        # กรณีไม่มีดอกเบี้ยหรือเดือนเก็บเงิน = 0
        monthly_saving = needed_at_retirement / months_saving if months_saving > 0 else 0

    return {
        "needed_at_retirement": needed_at_retirement,
        "monthly_saving": monthly_saving,
        "months_saving": months_saving,
        "months_using": months_using
    }

st.title("โปรแกรมคำนวณเงินเกษียณ พร้อมผลตอบแทนการลงทุน 💰")

age = st.number_input("อายุปัจจุบันของคุณ (ปี)", min_value=0, max_value=100, value=30)
retire_age = st.number_input("อายุที่ต้องการเกษียณ (ปี)", min_value=age+1, max_value=120, value=60)
life_expectancy = st.number_input("คาดหวังอายุขัย (ปี)", min_value=retire_age+1, max_value=150, value=85)
monthly_expense = st.number_input("ค่าใช้จ่ายต่อเดือนในช่วงเกษียณ (บาท)", min_value=0.0, value=50000.0, step=1000.0)
annual_return = st.number_input("อัตราผลตอบแทนเฉลี่ยต่อปี (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1)

if st.button("คำนวณ"):
    result = calculate_retirement_fund_with_return(age, retire_age, life_expectancy, monthly_expense, annual_return)

    st.subheader("📊 ผลลัพธ์การคำนวณ:")
    st.write(f"- เงินที่ต้องมีตอนเกษียณ: {result['needed_at_retirement']:,.2f} บาท")
    st.write(f"- เงินที่ต้องเก็บต่อเดือน: {result['monthly_saving']:,.2f} บาท")
    st.write(f"- ระยะเวลาเก็บเงิน (เดือน): {format_years_months(result['months_saving'])}")
    st.write(f"- ระยะเวลาใช้เงินหลังเกษียณ (เดือน): {format_years_months(result['months_using'])}")

    st.subheader("💬 สรุป:")
    st.write(f"คุณต้องเก็บเงินเดือนละ {result['monthly_saving']:,.2f} บาท เป็นเวลา {format_years_months(result['months_saving'])}")
    st.write(f"เพื่อให้มีเงินใช้เดือนละ {monthly_expense:,.2f} บาท ตลอดช่วงเกษียณ {format_years_months(result['months_using'])}")
    st.write(f"โดยสมมติผลตอบแทนเฉลี่ย {annual_return:.2f}% ต่อปี")