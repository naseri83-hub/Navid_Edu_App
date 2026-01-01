import streamlit as st
import json
import os
import pandas as pd
import jdatetime
from groq import Groq

# --- ۱. تنظیمات صفحه ---
st.set_page_config(page_title="نوید پژوهش | پورتال جامع آموزشی", layout="wide", page_icon="🎓")

# --- ۲. استایل گرافیکی (تم روشن و مدرن) ---
def apply_edu_ui():
    bg_url = "https://img.freepik.com/free-vector/white-abstract-background_23-2148810353.jpg"
    st.markdown(f"""
    <style>
    .stApp {{ background: url("{bg_url}"); background-size: cover; }}
    .main-box {{
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px; padding: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        color: #2c3e50; border: 1px solid #f0f0f0;
    }}
    .course-card {{
        background: #ffffff; border-right: 6px solid #1a2a6c;
        padding: 15px; border-radius: 10px; margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    h1, h2, h3 {{ color: #1a2a6c !important; }}
    .stButton>button {{ border-radius: 20px; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

apply_edu_ui()

# --- ۳. هوش مصنوعی ---
client = None
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- ۴. دیتابیس و اطلاعات ---
def load_db(f): return json.load(open(f, "r", encoding="utf-8")) if os.path.exists(f) else {}
def save_db(f, d): json.dump(d, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=4)

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "u_type": None, "u_name": None})

# --- ۵. منوی کناری (ارتباطات و اطلاعات سریع) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=100)
    st.title("نوید پژوهش")
    
    if st.session_state.auth:
        st.success(f"خوش آمدید، {st.session_state.u_name}")
        if st.button("🚪 خروج از حساب"):
            st.session_state.auth = False
            st.rerun()
    
    st.divider()
    st.markdown("### 📞 پل‌های ارتباطی")
    st.write("💬 **ایتا:** 09364744796 (فقط پیام)")
    st.write("📸 **اینستاگرام:** [navid_pazhoohesh](https://instagram.com/navid_pazhoohesh)")
    
    st.divider()
    st.markdown("### 📍 شعب حضوری")
    st.caption("شهریار: آموزشگاه نوید پژوهش، پژوهش‌سرا، فرهنگسراها")
    st.caption("اندیشه: سراهای محله فازها")
    st.info("🌐 دوره‌های آنلاین: سراسر کشور و جهان")

# --- ۶. محتوای اصلی (Tabs) ---
tab_home, tab_courses, tab_shop, tab_content, tab_about = st.tabs([
    "🏠 صفحه اصلی", "📚 دوره‌های آموزشی", "🛒 محصولات فیزیکی", "🎬 محتوای آموزشی", "👨‍🏫 درباره ما"
])

# --- بخش درباره ما ---
with tab_about:
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)
    col_img, col_text = st.columns([1, 3])
    with col_text:
        st.header("مهندس نوید ناصری")
        st.write("🎓 **کارشناسی مهندسی کامپیوتر نرم‌افزار**")
        st.write("🎓 **کارشناسی ارشد مکاترونیک (ارتباطات جنبی انسان، ماشین و کامپیوتر)**")
        st.write("🚀 **مؤسس گروه آموزشی نوید پژوهش**")
        st.write("🏫 **مدرس رسمی آموزش و پرورش در مقطع هنرستان**")
        st.write("👥 **تیم آموزشی:** بهره‌مندی از تیمی مجرب با بیش از ۵۰ مدرس و همکار متخصص")
    st.markdown("</div>", unsafe_allow_html=True)

# --- بخش صفحه اصلی و ورود ---
with tab_home:
    if not st.session_state.auth:
        st.markdown("<h1>🎓 به مرکز نوید پژوهش خوش آمدید</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🔐 ورود به پنل")
            u = st.text_input("نام کاربری")
            p = st.text_input("رمز عبور", type="password")
            if st.button("ورود"):
                if u == "naseri" and p == "123":
                    st.session_state.update({"auth": True, "u_type": "admin", "u_name": "آقای ناصری"})
                    st.rerun()
                # چک کردن یوزرهای عادی در دیتابیس اینجا...
        with col2:
            st.subheader("📝 عضویت سریع")
            st.write("برای مشاهده جزئیات بیشتر و ثبت‌نام در دوره‌ها، عضو شوید.")
            # فرم ثبت نام اینجا...
    else:
        st.balloons()
        st.header("پنل کاربری فعال است")
        st.info("از تب‌های بالا برای دسترسی به بخش‌های مختلف استفاده کنید.")

# --- بخش محصولات (فروشگاه) ---
with tab_shop:
    st.header("🛒 فروشگاه تجهیزات")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("<div class='course-card'><h4>📦 پک‌های رباتیک</h4><p>انواع بسته‌های آموزشی مکانیک و الکترونیک برای سنین مختلف</p></div>", unsafe_allow_html=True)
    with col_p2:
        st.markdown("<div class='course-card'><h4>💻 سیستم‌های کامپیوتری</h4><p>فروش و مشاوره خرید سیستم‌های مناسب برنامه‌نویسی و گرافیک</p></div>", unsafe_allow_html=True)
    st.warning("⚠️ بخش خرید آنلاین به زودی فعال می‌شود. فعلاً از طریق ایتا سفارش دهید.")

# --- بخش محتوا ---
with tab_content:
    st.header("🎬 محتوای آموزشی و جزوات")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("### 📽 فیلم‌های آفلاین")
        st.write("- آموزش مقدماتی اسکرچ")
        st.write("- مبانی مکاترونیک")
    with col_c2:
        st.markdown("### 📑 جزوات آموزشی")
        st.write("- جزوه برنامه‌نویسی پایتون")
        st.write("- راهنمای ساخت ربات")

# بخش دوره‌ها (مشابه قبل با گروه‌بندی)
with tab_courses:
    st.header("📚 لیست دوره‌های فعال")
    st.write("ویژه ۴ الی ۲۰ سال | شهریه ۶۰۰ الی ۸۰۰ هزار تومان")
    # کدهای مربوط به نمایش دوره‌ها و دکمه ثبت‌نام اینجا قرار می‌گیرد...