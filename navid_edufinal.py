import streamlit as st
import json
import os
import pandas as pd
import jdatetime
from groq import Groq

# --- ۱. تنظیمات صفحه ---
st.set_page_config(page_title="آموزشگاه نوید پژوهش", layout="wide", page_icon="🎓")

# --- ۲. استایل گرافیکی ---
def apply_edu_ui():
    bg_url = "https://images.unsplash.com/photo-1531482615713-2afd69097998?q=80&w=2070&auto=format&fit=crop"
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), url("{bg_url}");
        background-size: cover; background-attachment: fixed;
    }}
    div.stTabs, div.stForm, section[data-testid="stSidebar"] > div, .stTable {{
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px); border-radius: 20px; padding: 25px;
    }}
    h1 {{ color: white !important; text-align: center; text-shadow: 2px 2px 4px #000; }}
    .course-card {{
        background-color: #f0f2f6; padding: 20px; border-radius: 15px;
        border-right: 8px solid #007bff; margin-bottom: 15px; color: #333;
    }}
    </style>
    """, unsafe_allow_html=True)

apply_edu_ui()

# --- ۳. تنظیمات امنیتی هوش مصنوعی (Secrets) ---
# در این نسخه، کلید مستقیم حذف شده تا امنیت شما حفظ شود
client = None
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.warning("⚠️ کلید هوش مصنوعی در تنظیمات (Secrets) یافت نشد.")

# --- ۴. مدیریت دیتابیس محلی ---
USERS_FILE = "edu_users.json"
REG_FILE = "course_registrations.json"

def load_db(f): return json.load(open(f, "r", encoding="utf-8")) if os.path.exists(f) else {}
def save_db(f, d): json.dump(d, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=4)

COURSES = {
    "🤖 رباتیک و مکاترونیک": {"teacher": "مهندس راد", "age": "۷ تا ۱۵ سال", "fee": "۳,۵۰۰,۰۰۰ تومان"},
    "💻 پایتون و هوش مصنوعی": {"teacher": "دکتر ناصری", "age": "۱۲ سال به بالا", "fee": "۴,۸۰۰,۰۰۰ تومان"},
    "🧮 چرتکه و محاسبات ذهنی": {"teacher": "خانم رضایی", "age": "۵ تا ۱۲ سال", "fee": "۲,۹۰۰,۰۰۰ تومان"},
    "🎲 روبیک و بازی‌های فکری": {"teacher": "مهندس علوی", "age": "آزاد", "fee": "۱,۵۰۰,۰۰۰ تومان"}
}

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "u_type": None, "u_name": None})

# --- ۵. صفحه ورود ---
if not st.session_state.auth:
    st.markdown("<h1>🎓 آموزشگاه نوید پژوهش</h1>")
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        tab_login, tab_signup = st.tabs(["🔐 ورود", "📝 ثبت‌نام"])
        with tab_login:
            u = st.text_input("نام کاربری")
            p = st.text_input("رمز عبور", type="password")
            if st.button("ورود"):
                db = load_db(USERS_FILE)
                if u == "naseri" and p == "123":
                    st.session_state.update({"auth": True, "u_type": "admin", "u_name": "آقای ناصری"})
                    st.rerun()
                elif u in db and db[u]['password'] == p:
                    st.session_state.update({"auth": True, "u_type": "student", "u_name": u})
                    st.rerun()
                else: st.error("نام کاربری یا کلمه عبور اشتباه است.")
        with tab_signup:
            nu, npw = st.text_input("نام کاربری جدید"), st.text_input("رمز جدید", type="password")
            fn, ph = st.text_input("نام دانش‌آموز"), st.text_input("تلفن")
            if st.button("تأیید عضویت"):
                db = load_db(USERS_FILE); db[nu] = {"password": npw, "full_name": fn, "phone": ph}
                save_db(USERS_FILE, db); st.success("حساب ساخته شد.")

# --- ۶. پنل اصلی ---
else:
    with st.sidebar:
        st.write(f"کاربر: **{st.session_state.u_name}**")
        if st.button("🚪 خروج"):
            st.session_state.auth = False; st.rerun()

    if st.session_state.u_type == "admin":
        st.title("📋 لیست ثبت‌نام کنندگان")
        regs = load_db(REG_FILE); users = load_db(USERS_FILE)
        if regs:
            data = [{"نام": users.get(uid, {}).get("full_name", uid), "تلفن": users.get(uid, {}).get("phone", "-"), "دوره": r['course'], "تاریخ": r['date']} for uid, ur in regs.items() for r in ur]
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
        else: st.info("لیست خالی است.")
    else:
        st.title("📚 دوره‌های آموزشی")
        for name, info in COURSES.items():
            with st.container():
                st.markdown(f"<div class='course-card'><h3>{name}</h3><p>مدرس: {info['teacher']} | شهریه: {info['fee']}</p></div>", unsafe_allow_html=True)
                if st.button(f"پیش‌ثبت‌نام در {name}", key=name):
                    regs = load_db(REG_FILE)
                    if st.session_state.u_name not in regs: regs[st.session_state.u_name] = []
                    if not any(item['course'] == name for item in regs[st.session_state.u_name]):
                        regs[st.session_state.u_name].append({"course": name, "date": jdatetime.datetime.now().strftime("%Y/%m/%d")})
                        save_db(REG_FILE, regs); st.balloons(); st.success(f"ثبت شد.")
                    else: st.warning("قبلاً انتخاب شده است.")

        if client:
            st.divider(); st.subheader("🤖 گفتگو با نویدبات")
            msg = st.chat_input("سوال خود را بپرسید...")
            if msg:
                res = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": msg}])
                st.write(res.choices[0].message.content)