import streamlit as st
import uuid
from datetime import datetime
import pandas as pd

# إعدادات السيرفر
st.set_page_config(
    page_title="تطبيق المغتربين في الصين",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 تطبيق المغتربين في الصين - China Expat App")

# جلسات Streamlit
if 'users' not in st.session_state:
    st.session_state.users = []
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}

# مدن الصين مع إحداثيات
CHINA_CITIES = {
    "بكين - Beijing - 北京": {"lat": 39.9042, "lon": 116.4074},
    "شنغهاي - Shanghai - 上海": {"lat": 31.2304, "lon": 121.4737},
    "غوانغتشو - Guangzhou - 广州": {"lat": 23.1291, "lon": 113.2644},
    "شينزين - Shenzhen - 深圳": {"lat": 22.5431, "lon": 114.0579},
    "هونغ كونغ - Hong Kong - 香港": {"lat": 22.3193, "lon": 114.1694},
    "تيانجين - Tianjin - 天津": {"lat": 39.3434, "lon": 117.3616},
    "شيان - Xi'an - 西安": {"lat": 34.3416, "lon": 108.9398},
    "نانجينغ - Nanjing - 南京": {"lat": 32.0603, "lon": 118.7969},
    "هانغتشو - Hangzhou - 杭州": {"lat": 30.2741, "lon": 120.1551},
    "تشينغداو - Qingdao - 青岛": {"lat": 36.0671, "lon": 120.3826}
}

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

# بيانات افتراضية كاملة
def create_sample_users():
    return [
        {
            "id": "1",
            "name": "أحمد محمد",
            "city": "بكين - Beijing - 北京",
            "lat": 39.9042,
            "lon": 116.4074,
            "status": "متاح",
            "contact_type": "واتساب",
            "contact_info": "+8613812345678",
            "details": "طالب دراسات عليا في جامعة بكين، متخصص في الهندسة المدنية. أساعد في الترجمة والخدمات الطلابية.",
            "language": "العربية, الإنجليزية, الصينية",
            "specialization": "هندسة مدنية",
            "expertise": ["مترجم صيني عربي", "خبير خدمات طلابية"],
            "registration_date": "2024-01-15 10:30"
        },
        {
            "id": "2",
            "name": "فاطمة علي", 
            "city": "شنغهاي - Shanghai - 上海",
            "lat": 31.2304,
            "lon": 121.4737,
            "status": "مشغول",
            "contact_type": "وي تشات",
            "contact_info": "Fatima_Shanghai",
            "details": "موظفة في شركة تقنية متعددة الجنسيات، خبرة 5 سنوات في التسويق الرقمي. أقدم استشارات في المعاملات الحكومية.",
            "language": "العربية, الصينية, الإنجليزية",
            "specialization": "تسويق رقمي",
            "expertise": ["مترجم صيني انجليزي عربي", "خبير معاملات حكومية"],
            "registration_date": "2024-01-10 14:20"
        },
        {
            "id": "3",
            "name": "خالد عبدالله",
            "city": "غوانغتشو - Guangzhou - 广州", 
            "lat": 23.1291,
            "lon": 113.2644,
            "status": "متاح",
            "contact_type": "هاتف",
            "contact_info": "+8613923456789",
            "details": "تاجر ومستورد، متخصص في الأجهزة الإلكترونية والمنتجات المنزلية. خبرة 8 سنوات في السوق الصينية.",
            "language": "العربية, الإنجليزية, الصينية",
            "specialization": "تجارة واستيراد",
            "expertise": ["خبير فحص منتجات", "خبير اشراف على الشحن", "خبير فحص مصانع وشركات"],
            "registration_date": "2024-01-20 09:15"
        },
        {
            "id": "4",
            "name": "سارة أحمد",
            "city": "شينزين - Shenzhen - 深圳",
            "lat": 22.5431,
            "lon": 114.0579,
            "status": "متاح", 
            "contact_type": "بريد إلكتروني",
            "contact_info": "sara.tech@email.com",
            "details": "مصممة جرافيك ومطورة واجهات مستخدم، أعمل في شركة تقنية ناشئة. أملك معدات تصوير محترفة.",
            "language": "العربية, الصينية, الإنجليزية",
            "specialization": "تصميم جرافيك",
            "expertise": ["متاح معدات تصوير"],
            "registration_date": "2024-01-18 16:45"
        },
        {
            "id": "5", 
            "name": "محمد حسن",
            "city": "هونغ كونغ - Hong Kong - 香港",
            "lat": 22.3193,
            "lon": 114.1694,
            "status": "مشغول",
            "contact_type": "واتساب",
            "contact_info": "+85291234567",
            "details": "مستشار مالي في بنك دولي، خبرة في الأسواق المالية الآسيوية. أقدم خدمات سياحية وترجمة.",
            "language": "العربية, الإنجليزية, الكانتونية",
            "specialization": "استشارات مالية",
            "expertise": ["خبير سياحة ورحلات", "سائق متاح سيارة"],
            "registration_date": "2024-01-22 11:30"
        }
    ]

if not st.session_state.users:
    st.session_state.users = create_sample_users()

# نظام التقييم
def show_rating_system(user_id):
    if user_id not in st.session_state.ratings:
        st.session_state.ratings[user_id] = []
    
    st.markdown("---")
    st.subheader("⭐ تقييم الخدمة")
    
    with st.form(f"rating_form_{user_id}"):
        rating = st.select_slider("التقييم", options=[1, 2, 3, 4, 5], value=5)
        review = st.text_area("تعليقك على الخدمة", placeholder="شاركنا تجربتك مع هذا المغترب...")
        
        submitted = st.form_submit_button("إرسال التقييم")
        if submitted:
            if review.strip():
                new_rating = {
                    "id": str(uuid.uuid4()),
                    "rating": rating,
                    "review": review,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "user_id": user_id
                }
                st.session_state.ratings[user_id].append(new_rating)
                st.success("شكراً لتقييمك! ✅")
            else:
                st.error("يرجى كتابة تعليق")

    # عرض التقييمات السابقة
    user_ratings = st.session_state.ratings.get(user_id, [])
    if user_ratings:
        st.subheader("📝 التقييمات السابقة")
        for i, rating_data in enumerate(user_ratings[-3:]):  # عرض آخر 3 تقييمات
            with st.container():
                stars = "⭐" * rating_data['rating']
                st.write(f"**{stars} - {rating_data['date']}**")
                st.write(f"**التعليق:** {rating_data['review']}")
                if i < len(user_ratings[-3:]) - 1:
                    st.markdown("---")

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
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("الاسم الكامل *", placeholder="أحمد محمد")
            city = st.selectbox("المدينة *", list(CHINA_CITIES.keys()))
            contact_type = st.selectbox("طريقة التواصل *", ["بريد إلكتروني", "واتساب", "هاتف", "وي تشات"])
            contact_info = st.text_input("معلومات التواصل *", placeholder="example@email.com أو +861231234567")
            
        with col2:
            status = st.selectbox("الحالة *", ["متاح", "مشغول", "غير متاح"])
            language = st.multiselect("اللغات المتحدث بها", ["العربية", "الإنجليزية", "الصينية", "الفرنسية", "الألمانية", "الإسبانية"])
            specialization = st.text_input("التخصص أو المجال", placeholder="هندسة، طب، تجارة، إلخ...")
        
        details = st.text_area("تفاصيل عنك *", placeholder="اخبرنا عن نفسك، خبراتك، خدماتك...", height=100)
        expertise = st.multiselect("مجالات الخبرة *", EXPERTISE_AREAS)
        
        submitted = st.form_submit_button("✅ تسجيل البيانات")
        
        if submitted:
            if name and contact_info and details and expertise:
                # الحصول على إحداثيات المدينة
                city_data = CHINA_CITIES[city]
                
                new_user = {
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "city": city,
                    "lat": city_data["lat"],
                    "lon": city_data["lon"],
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
                st.balloons()
                
                # عرض ملخص البيانات المسجلة
                st.subheader("ملخص بياناتك المسجلة:")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**الاسم:** {name}")
                    st.write(f"**المدينة:** {city}")
                    st.write(f"**الحالة:** {status}")
                    st.write(f"**مجالات الخبرة:** {', '.join(expertise)}")
                with col2:
                    st.write(f"**طريقة التواصل:** {contact_type}")
                    st.write(f"**معلومات التواصل:** {contact_info}")
                    st.write(f"**اللغات:** {', '.join(language) if language else 'غير محدد'}")
                    if specialization:
                        st.write(f"**التخصص:** {specialization}")
            else:
                st.error("⚠️ يرجى ملء جميع الحقول الإلزامية (*)")

# خريطة تفاعلية مبسطة
def show_interactive_map():
    st.header("🗺️ خريطة المغتربين في الصين")
    
    # إحصائيات سريعة
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("إجمالي المسجلين", len(st.session_state.users))
    with col2:
        available_count = len([u for u in st.session_state.users if u["status"] == "متاح"])
        st.metric("المتاحون", available_count)
    with col3:
        cities_count = len(set(u["city"] for u in st.session_state.users))
        st.metric("المدن المغطاة", cities_count)
    with col4:
        total_reviews = sum(len(ratings) for ratings in st.session_state.ratings.values())
        st.metric("إجمالي التقييمات", total_reviews)
    
    # عرض بيانات الخريطة في جدول تفاعلي
    st.subheader("📍 مواقع المغتربين")
    
    map_data = []
    for user in st.session_state.users:
        avg_rating, reviews_count = calculate_user_rating(user["id"])
        
        # تحديد لون الحالة
        status_color = {
            "متاح": "🟢",
            "مشغول": "🟡", 
            "غير متاح": "🔴"
        }.get(user["status"], "⚪")
        
        map_data.append({
            "الاسم": user["name"],
            "المدينة": user["city"].split(" - ")[0],
            "الحالة": f"{status_color} {user['status']}",
            "التقييم": f"⭐ {avg_rating} ({reviews_count})",
            "الإحداثيات": f"{user['lat']:.4f}, {user['lon']:.4f}",
            "التواصل": f"{user['contact_type']}",
            "المعلومات": user['contact_info'],
            "مجالات الخبرة": ", ".join(user["expertise"])
        })
    
    if map_data:
        df = pd.DataFrame(map_data)
        st.dataframe(df, use_container_width=True, height=400)
        
        # إرشادات استخدام الإحداثيات
        st.info("""
        **💡如何使用坐标：**
        - يمكنك نسخ الإحداثيات واستخدامها في تطبيقات الخرائط مثل Google Maps
        - مثال: 39.9042, 116.4074 (بكين)
        - أو استخدام الرابط: https://maps.google.com/?q=39.9042,116.4074
        """)
    else:
        st.warning("لا توجد بيانات لعرضها على الخريطة")

# صفحة البحث والعرض
def show_search():
    st.header("🔍 البحث عن مغتربين")
    
    # خيارات التصفية في الشريط الجانبي
    st.sidebar.header("🔍 خيارات البحث")
    
    with st.sidebar:
        # تصفية المدينة
        cities = list(set(user["city"] for user in st.session_state.users))
        city_filter = st.selectbox("المدينة", ["الكل"] + cities)
        
        # تصفية الحالة
        status_filter = st.selectbox("الحالة", ["الكل", "متاح", "مشغول", "غير متاح"])
        
        # تصفية مجالات الخبرة
        expertise_filter = st.multiselect("مجالات الخبرة", EXPERTISE_AREAS)
        
        # تصفية التقييم
        min_rating = st.slider("حد أدنى للتقييم", 0.0, 5.0, 0.0, 0.5)
    
    # تطبيق التصفية
    filtered_users = st.session_state.users.copy()
    
    if city_filter != "الكل":
        filtered_users = [u for u in filtered_users if u["city"] == city_filter]
    
    if status_filter != "الكل":
        filtered_users = [u for u in filtered_users if u["status"] == status_filter]
    
    if expertise_filter:
        filtered_users = [u for u in filtered_users if any(expertise in u["expertise"] for expertise in expertise_filter)]
    
    # تصفية حسب التقييم
    filtered_users = [u for u in filtered_users if calculate_user_rating(u["id"])[0] >= min_rating]
    
    # عرض النتائج
    st.subheader(f"📊 نتائج البحث ({len(filtered_users)} مغترب)")
    
    if filtered_users:
        for user in filtered_users:
            rating, reviews_count = calculate_user_rating(user["id"])
            
            # أيقونة الحالة
            status_icon = {
                "متاح": "🟢",
                "مشغول": "🟡",
                "غير متاح": "🔴"
            }.get(user["status"], "⚪")
            
            city_ar = user["city"].split(" - ")[0]
            
            with st.expander(f"{status_icon} {user['name']} - {city_ar} - ⭐ {rating} ({reviews_count} تقييم)"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📞 معلومات الاتصال:**")
                    st.write(f"**{user['contact_type']}:** {user['contact_info']}")
                    st.write(f"**🗣️ اللغات:** {user.get('language', 'غير محدد')}")
                    st.write(f"**⭐ التقييم:** {rating}/5 ({reviews_count} تقييم)")
                    st.write(f"**📍 الإحداثيات:** {user['lat']:.4f}, {user['lon']:.4f}")
                
                with col2:
                    st.write("**👤 الحالة والمعلومات:**")
                    st.write(f"**الحالة:** {user['status']}")
                    st.write(f"**🏙️ المدينة:** {user['city']}")
                    st.write(f"**📅 تاريخ التسجيل:** {user['registration_date']}")
                    if user.get('specialization'):
                        st.write(f"**🎯 التخصص:** {user['specialization']}")
                
                st.write("**🛠️ مجالات الخبرة:**")
                for expertise in user["expertise"]:
                    st.write(f"• {expertise}")
                
                st.write("**📝 التفاصيل:**")
                st.info(user['details'])
                
                # نظام التقييم
                show_rating_system(user["id"])
    else:
        st.warning("⚠️ لا توجد نتائج تطابق معايير البحث")

# صفحة الإحصائيات
def show_stats():
    st.header("📈 إحصائيات المنصة")
    
    total_users = len(st.session_state.users)
    available = len([u for u in st.session_state.users if u["status"] == "متاح"])
    busy = len([u for u in st.session_state.users if u["status"] == "مشغول"])
    unavailable = len([u for u in st.session_state.users if u["status"] == "غير متاح"])
    
    # الإحصائيات الأساسية
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("إجمالي المسجلين", total_users)
    col2.metric("المتاحون", available)
    col3.metric("المشغولون", busy)
    col4.metric("غير المتاحين", unavailable)
    
    # توزيع المدن
    st.subheader("🏙️ توزيع المدن")
    city_counts = {}
    for user in st.session_state.users:
        city = user["city"]
        city_counts[city] = city_counts.get(city, 0) + 1
    
    for city, count in city_counts.items():
        st.write(f"**{city}:** {count} مغترب")
    
    # توزيع الخبرات
    st.subheader("🛠️ توزيع مجالات الخبرة")
    expertise_counts = {}
    for user in st.session_state.users:
        for expertise in user["expertise"]:
            expertise_counts[expertise] = expertise_counts.get(expertise, 0) + 1
    
    # عرض الخبرات الأكثر شيوعاً
    sorted_expertise = sorted(expertise_counts.items(), key=lambda x: x[1], reverse=True)
    for expertise, count in sorted_expertise:
        st.write(f"**{expertise}:** {count} شخص")
    
    # إحصائيات التقييمات
    st.subheader("⭐ إحصائيات التقييمات")
    all_ratings = []
    for user_ratings in st.session_state.ratings.values():
        all_ratings.extend([r['rating'] for r in user_ratings])
    
    if all_ratings:
        avg_platform_rating = sum(all_ratings) / len(all_ratings)
        total_reviews = len(all_ratings)
        
        col1, col2 = st.columns(2)
        col1.metric("متوسط تقييم المنصة", f"{avg_platform_rating:.1f}/5")
        col2.metric("إجمالي التقييمات", total_reviews)
        
        # أفضل المسجلين تقييماً
        st.subheader("🏆 أفضل المسجلين تقييماً")
        user_ratings = []
        for user in st.session_state.users:
            avg_rating, total_reviews = calculate_user_rating(user["id"])
            if avg_rating > 0:
                user_ratings.append({
                    'name': user['name'],
                    'city': user['city'],
                    'rating': avg_rating,
                    'reviews': total_reviews
                })
        
        if user_ratings:
            user_ratings.sort(key=lambda x: x['rating'], reverse=True)
            for i, user in enumerate(user_ratings[:5], 1):
                city_ar = user['city'].split(' - ')[0]
                st.write(f"{i}. **{user['name']}** - {city_ar} - ⭐ {user['rating']} ({user['reviews']} تقييم)")

# التنقل الرئيسي
def main():
    st.sidebar.title("🌍 التنقل")
    
    page = st.sidebar.radio(
        "اختر الصفحة:",
        ["الرئيسية", "الخريطة", "تسجيل جديد", "البحث", "الإحصائيات"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ معلومات سريعة")
    st.sidebar.write(f"**المسجلين:** {len(st.session_state.users)}")
    
    available_count = len([u for u in st.session_state.users if u['status'] == 'متاح'])
    st.sidebar.write(f"**المتاحون:** {available_count}")
    
    total_reviews = sum(len(ratings) for ratings in st.session_state.ratings.values())
    st.sidebar.write(f"**التقييمات:** {total_reviews}")
    
    if page == "الرئيسية":
        st.header("🏠 مرحباً بك في تطبيق المغتربين في الصين")
        st.write("""
        ### 🌍 منصة تواصل للمغتربين في الصين
        
        هذه المنصة تساعد المغتربين العرب في الصين على:
        - **التواصل** وتبادل الخبرات
        - **البحث** عن خدمات متخصصة
        - **التسجيل** لعرض مهاراتهم
        - **التقييم** وبناء الثقة
        
        ### 🎯 المميزات:
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("""
            **📝 نظام التسجيل**
            - تسجيل بيانات كاملة
            - تحديد مجالات الخبرة
            - تحديث الحالة
            
            **🗺️ الخريطة التفاعلية**  
            - عرض مواقع المغتربين
            - إحداثيات دقيقة
            - تصفية حسب المدينة
            """)
            
        with col2:
            st.write("""
            **🔍 البحث المتقدم**
            - تصفية حسب المدينة
            - تصفية حسب الحالة
            - تصفية حسب الخبرة
            - تصفية حسب التقييم
            
            **⭐ نظام التقييم**
            - تقييم الخدمات
            - تعليقات المستخدمين
            - بناء السمعة
            """)
        
        st.info("💡 **نصيحة:** استخدم صفحة 'الخريطة' لرؤية جميع المغتربين على الخريطة، وصفحة 'البحث' للبحث المتقدم.")
        
    elif page == "الخريطة":
        show_interactive_map()
    elif page == "تسجيل جديد":
        show_registration()
    elif page == "البحث":
        show_search()
    elif page == "الإحصائيات":
        show_stats()

if __name__ == "__main__":
    main()