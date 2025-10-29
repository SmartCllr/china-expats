import streamlit as st
import uuid
from datetime import datetime

# إعدادات السيرفر
st.set_page_config(
    page_title="تطبيق المغتربين في الصين",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 تطبيق المغتربين في الصين")

# جلسات Streamlit
if 'users' not in st.session_state:
    st.session_state.users = []
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}

# مدن الصين
CHINA_CITIES = [
    "بكين - Beijing - 北京",
    "شنغهاي - Shanghai - 上海", 
    "غوانغتشو - Guangzhou - 广州",
    "شينزين - Shenzhen - 深圳",
    "هونغ كونغ - Hong Kong - 香港",
    "تيانجين - Tianjin - 天津",
    "شيان - Xi'an - 西安",
    "نانجينغ - Nanjing - 南京",
    "هانغتشو - Hangzhou - 杭州",
    "تشينغداو - Qingdao - 青岛"
]

# مجالات الخبرة
EXPERTISE_AREAS = [
    "مترجم صيني عربي",
    "مترجم صيني انجليزي عربي", 
    "خبير فحص منتجات",
    "خبير فحص معدات صناعية",
    "خبير معاملات حكومية",
    "خبير سياحة ورحلات",
    "خبير خدمات طلابية",
    "سائق متاح سيارة",
    "خبير اشراف على الشحن",
    "خبير فحص وتشغيل خطوط انتاج",
    "خبير فحص مواد خام", 
    "خبير فحص وتوثيق مصانع وشركات",
    "متاح معدات تصوير"
]

# بيانات افتراضية
def create_sample_users():
    return [
        {
            "id": "1",
            "name": "أحمد محمد",
            "city": "بكين - Beijing - 北京",
            "status": "متاح",
            "contact_type": "واتساب",
            "contact_info": "+8613812345678",
            "details": "طالب دراسات عليا في جامعة بكين، متخصص في الهندسة المدنية",
            "language": "العربية, الإنجليزية, الصينية",
            "specialization": "هندسة مدنية",
            "expertise": ["مترجم صيني عربي", "خبير خدمات طلابية"],
            "registration_date": "2024-01-15 10:30"
        },
        {
            "id": "2",
            "name": "فاطمة علي", 
            "city": "شنغهاي - Shanghai - 上海",
            "status": "مشغول",
            "contact_type": "وي تشات",
            "contact_info": "Fatima_Shanghai",
            "details": "موظفة في شركة تقنية متعددة الجنسيات، خبرة 5 سنوات في التسويق الرقمي",
            "language": "العربية, الصينية, الإنجليزية",
            "specialization": "تسويق رقمي",
            "expertise": ["مترجم صيني انجليزي عربي", "خبير معاملات حكومية"],
            "registration_date": "2024-01-10 14:20"
        }
    ]

if not st.session_state.users:
    st.session_state.users = create_sample_users()

# نظام التقييم
def show_rating_system(user_id):
    if user_id not in st.session_state.ratings:
        st.session_state.ratings[user_id] = []
    
    st.subheader("⭐ تقييم الخدمة")
    
    with st.form(f"rating_form_{user_id}"):
        rating = st.select_slider("التقييم", options=[1, 2, 3, 4, 5], value=5)
        review = st.text_area("تعليقك على الخدمة")
        
        if st.form_submit_button("إرسال التقييم"):
            new_rating = {
                "id": str(uuid.uuid4()),
                "rating": rating,
                "review": review,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "user_id": user_id
            }
            st.session_state.ratings[user_id].append(new_rating)
            st.success("شكراً لتقييمك! ✅")

def calculate_user_rating(user_id):
    user_ratings = st.session_state.ratings.get(user_id, [])
    if not user_ratings:
        return 0, 0
    
    total_rating = sum(r['rating'] for r in user_ratings)
    average_rating = total_rating / len(user_ratings)
    return round(average_rating, 1), len(user_ratings)

# صفحة التسجيل
def show_registration():
    st.header("📝 تسجيل مغترب جديد")
    
    with st.form("registration_form"):
        name = st.text_input("الاسم الكامل *")
        city = st.selectbox("المدينة *", CHINA_CITIES)
        
        col1, col2 = st.columns(2)
        with col1:
            contact_type = st.selectbox("طريقة التواصل", ["بريد إلكتروني", "واتساب", "هاتف", "وي تشات"])
            contact_info = st.text_input("معلومات التواصل *")
            status = st.selectbox("الحالة *", ["متاح", "مشغول", "غير متاح"])
        
        with col2:
            language = st.multiselect("اللغات المتحدث بها", ["العربية", "الإنجليزية", "الصينية", "الفرنسية"])
            specialization = st.text_input("التخصص أو المجال")
        
        details = st.text_area("تفاصيل عنك *")
        expertise = st.multiselect("مجالات الخبرة *", EXPERTISE_AREAS)
        
        if st.form_submit_button("✅ تسجيل البيانات"):
            if name and contact_info and details and expertise:
                new_user = {
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "city": city,
                    "status": status,
                    "contact_type": contact_type,
                    "contact_info": contact_info,
                    "details": details,
                    "language": ", ".join(language),
                    "specialization": specialization,
                    "expertise": expertise,
                    "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.users.append(new_user)
                st.success("🎉 تم التسجيل بنجاح!")
            else:
                st.error("⚠️ يرجى ملء جميع الحقول الإلزامية")

# صفحة البحث والعرض
def show_search():
    st.header("🔍 البحث عن مغتربين")
    
    # خيارات التصفية
    col1, col2, col3 = st.columns(3)
    with col1:
        city_filter = st.selectbox("المدينة", ["الكل"] + CHINA_CITIES)
    with col2:
        status_filter = st.selectbox("الحالة", ["الكل", "متاح", "مشغول", "غير متاح"])
    with col3:
        expertise_filter = st.multiselect("مجالات الخبرة", EXPERTISE_AREAS)
    
    # تطبيق التصفية
    filtered_users = st.session_state.users.copy()
    
    if city_filter != "الكل":
        filtered_users = [u for u in filtered_users if u["city"] == city_filter]
    
    if status_filter != "الكل":
        filtered_users = [u for u in filtered_users if u["status"] == status_filter]
    
    if expertise_filter:
        filtered_users = [u for u in filtered_users if any(expertise in u["expertise"] for expertise in expertise_filter)]
    
    # عرض النتائج
    st.subheader(f"📊 النتائج ({len(filtered_users)} مغترب)")
    
    for user in filtered_users:
        rating, reviews_count = calculate_user_rating(user["id"])
        
        with st.expander(f"{user['name']} - {user['city'].split(' - ')[0]} - ⭐ {rating} ({reviews_count})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**معلومات الاتصال:**")
                st.write(f"📞 {user['contact_type']}: {user['contact_info']}")
                st.write(f"🗣️ اللغات: {user.get('language', 'غير محدد')}")
                st.write(f"📅 تاريخ التسجيل: {user['registration_date']}")
            
            with col2:
                st.write("**الحالة والتخصص:**")
                st.write(f"🟢 الحالة: {user['status']}")
                if user.get('specialization'):
                    st.write(f"🎯 التخصص: {user['specialization']}")
                
                st.write("**مجالات الخبرة:**")
                for exp in user["expertise"]:
                    st.write(f"• {exp}")
            
            st.write("**التفاصيل:**")
            st.info(user['details'])
            
            show_rating_system(user["id"])

# صفحة الإحصائيات
def show_stats():
    st.header("📈 إحصائيات المنصة")
    
    total_users = len(st.session_state.users)
    available = len([u for u in st.session_state.users if u["status"] == "متاح"])
    busy = len([u for u in st.session_state.users if u["status"] == "مشغول"])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي المسجلين", total_users)
    col2.metric("المتاحون", available)
    col3.metric("المشغولون", busy)
    
    # توزيع المدن
    st.subheader("🏙️ توزيع المدن")
    city_counts = {}
    for user in st.session_state.users:
        city = user["city"]
        city_counts[city] = city_counts.get(city, 0) + 1
    
    for city, count in city_counts.items():
        st.write(f"{city}: {count} مغترب")
    
    # توزيع الخبرات
    st.subheader("🛠️ توزيع مجالات الخبرة")
    expertise_counts = {}
    for user in st.session_state.users:
        for expertise in user["expertise"]:
            expertise_counts[expertise] = expertise_counts.get(expertise, 0) + 1
    
    for expertise, count in expertise_counts.items():
        st.write(f"{expertise}: {count}")

# التنقل الرئيسي
def main():
    st.sidebar.title("🌍 التنقل")
    
    page = st.sidebar.radio(
        "اختر الصفحة:",
        ["الرئيسية", "تسجيل جديد", "البحث", "الإحصائيات"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("معلومات سريعة")
    st.sidebar.write(f"المسجلين: {len(st.session_state.users)}")
    st.sidebar.write(f"المتاحون: {len([u for u in st.session_state.users if u['status'] == 'متاح'])}")
    
    if page == "الرئيسية":
        st.header("مرحباً بك في تطبيق المغتربين في الصين")
        st.write("هذا التطبيق يساعد المغتربين في الصين على التواصل وتبادل الخبرات")
        st.write("### المميزات:")
        st.write("• 📝 تسجيل بيانات المغتربين")
        st.write("• 🔍 البحث والتصفية المتقدم") 
        st.write("• ⭐ نظام التقييمات")
        st.write("• 📊 إحصائيات مفصلة")
        
    elif page == "تسجيل جديد":
        show_registration()
    elif page == "البحث":
        show_search()
    elif page == "الإحصائيات":
        show_stats()

if __name__ == "__main__":
    main()