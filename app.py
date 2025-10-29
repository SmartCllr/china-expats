import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import uuid
from datetime import datetime

# إعداد صفحة Streamlit
st.set_page_config(page_title="تطبيق المغتربين في الصين", layout="wide")
st.title("🌍 تطبيق المغتربين في الصين - China Expat App - 中国外籍人士应用")

# جلسات Streamlit
if 'users' not in st.session_state:
    st.session_state.users = []
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}

# مدن الصين باللغات الثلاث
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
    "تشينغداو - Qingdao - 青岛": {"lat": 36.0671, "lon": 120.3826},
    "ودوهان - Wuhan - 武汉": {"lat": 30.5928, "lon": 114.3055},
    "تشنغدو - Chengdu - 成都": {"lat": 30.5728, "lon": 104.0668},
    "داليان - Dalian - 大连": {"lat": 38.9140, "lon": 121.6147},
    "شيامن - Xiamen - 厦门": {"lat": 24.4798, "lon": 118.0894},
    "هايكو - Haikou - 海口": {"lat": 20.0174, "lon": 110.3492}
}

# مجالات الخبرة
EXPERTISE_AREAS = {
    "مترجم صيني عربي": "language",
    "مترجم صيني انجليزي عربي": "language", 
    "خبير فحص منتجات": "inspection",
    "خبير فحص معدات صناعية": "inspection",
    "خبير معاملات حكومية": "government",
    "خبير سياحة ورحلات": "tourism",
    "خبير خدمات طلابية": "education",
    "سائق متاح سيارة": "transport",
    "خبير اشراف على الشحن": "shipping",
    "خبير فحص وتشغيل خطوط انتاج": "industrial",
    "خبير فحص مواد خام": "inspection",
    "خبير فحص وتوثيق مصانع وشركات": "inspection",
    "متاح معدات تصوير": "media"
}

def add_custom_city():
    st.sidebar.header("🏙️ إضافة مدينة جديدة")
    with st.sidebar.expander("➕ اضف مدينة غير موجودة"):
        city_ar = st.text_input("اسم المدينة بالعربية")
        city_en = st.text_input("اسم المدينة بالإنجليزية")
        city_zh = st.text_input("اسم المدينة بالصينية")
        lat = st.number_input("خط العرض (Latitude)", value=35.0, format="%.6f")
        lon = st.number_input("خط الطول (Longitude)", value=105.0, format="%.6f")
        
        if st.button("إضافة المدينة"):
            if city_ar and city_en and city_zh:
                city_key = f"{city_ar} - {city_en} - {city_zh}"
                CHINA_CITIES[city_key] = {"lat": lat, "lon": lon}
                st.success(f"تمت إضافة {city_key} بنجاح!")
            else:
                st.error("يرجى ملء جميع حقول اسم المدينة")

# بيانات افتراضية للمسجلين
def create_sample_users():
    return [
        {
            "id": str(uuid.uuid4()),
            "name": "أحمد محمد",
            "city": "بكين - Beijing - 北京",
            "lat": 39.9042,
            "lon": 116.4074,
            "status": "متاح",
            "contact_type": "واتساب",
            "contact_info": "+8613812345678",
            "details": "طالب دراسات عليا في جامعة بكين، متخصص في الهندسة المدنية",
            "language": "العربية, الإنجليزية, الصينية",
            "specialization": "هندسة مدنية",
            "expertise": ["مترجم صيني عربي", "خبير خدمات طلابية"],
            "registration_date": "2024-01-15 10:30",
            "color": [0, 255, 0],  # أخضر للمتاح
            "rating": 4.8,
            "reviews": 12
        },
        {
            "id": str(uuid.uuid4()),
            "name": "فاطمة علي", 
            "city": "شنغهاي - Shanghai - 上海",
            "lat": 31.2304,
            "lon": 121.4737,
            "status": "مشغول",
            "contact_type": "وي تشات",
            "contact_info": "Fatima_Shanghai",
            "details": "موظفة في شركة تقنية متعددة الجنسيات، خبرة 5 سنوات في التسويق الرقمي",
            "language": "العربية, الصينية, الإنجليزية",
            "specialization": "تسويق رقمي",
            "expertise": ["مترجم صيني انجليزي عربي", "خبير معاملات حكومية"],
            "registration_date": "2024-01-10 14:20",
            "color": [255, 165, 0],  # برتقالي للمشغول
            "rating": 4.9,
            "reviews": 8
        },
        {
            "id": str(uuid.uuid4()),
            "name": "خالد عبدالله",
            "city": "غوانغتشو - Guangzhou - 广州", 
            "lat": 23.1291,
            "lon": 113.2644,
            "status": "متاح",
            "contact_type": "هاتف",
            "contact_info": "+8613923456789",
            "details": "تاجر ومستورد، متخصص في الأجهزة الإلكترونية والمنتجات المنزلية",
            "language": "العربية, الإنجليزية, الصينية",
            "specialization": "تجارة واستيراد",
            "expertise": ["خبير فحص منتجات", "خبير اشراف على الشحن", "خبير فحص مصانع وشركات"],
            "registration_date": "2024-01-20 09:15",
            "color": [0, 255, 0],  # أخضر للمتاح
            "rating": 4.6,
            "reviews": 15
        },
        {
            "id": str(uuid.uuid4()),
            "name": "سارة أحمد",
            "city": "شينزين - Shenzhen - 深圳",
            "lat": 22.5431,
            "lon": 114.0579,
            "status": "غير متاح", 
            "contact_type": "بريد إلكتروني",
            "contact_info": "sara.tech@email.com",
            "details": "مصممة جرافيك ومطورة واجهات مستخدم، أعمل في شركة تقنية ناشئة",
            "language": "العربية, الصينية, الإنجليزية",
            "specialization": "تصميم جرافيك",
            "expertise": ["متاح معدات تصوير"],
            "registration_date": "2024-01-18 16:45",
            "color": [255, 0, 0],  # أحمر لغير المتاح
            "rating": 4.7,
            "reviews": 5
        }
    ]

# تحميل البيانات الافتراضية إذا لم تكن موجودة
if not st.session_state.users:
    st.session_state.users = create_sample_users()

def show_rating_system(user_id):
    """نظام التقييم"""
    if user_id not in st.session_state.ratings:
        st.session_state.ratings[user_id] = []
    
    st.subheader("⭐ تقييم الخدمة")
    
    with st.form(f"rating_form_{user_id}"):
        rating = st.slider("التقييم", 1, 5, 5, help="1 = سيء, 5 = ممتاز")
        review = st.text_area("تعليقك على الخدمة", placeholder="اكتب تعليقك عن الخدمة هنا...")
        
        submitted = st.form_submit_button("إرسال التقييم")
        
        if submitted:
            new_rating = {
                "id": str(uuid.uuid4()),
                "rating": rating,
                "review": review,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "user_id": user_id
            }
            st.session_state.ratings[user_id].append(new_rating)
            st.success("شكراً لتقييمك! ✅")
    
    # عرض التقييمات السابقة
    user_ratings = st.session_state.ratings.get(user_id, [])
    if user_ratings:
        st.subheader("📝 التقييمات السابقة")
        for rating in user_ratings[-5:]:  # عرض آخر 5 تقييمات
            with st.expander(f"⭐ {rating['rating']}/5 - {rating['date']}"):
                st.write(f"**التعليق:** {rating['review']}")

def calculate_user_rating(user_id):
    """حساب متوسط التقييم للمستخدم"""
    user_ratings = st.session_state.ratings.get(user_id, [])
    if not user_ratings:
        return 0, 0
    
    total_rating = sum(r['rating'] for r in user_ratings)
    average_rating = total_rating / len(user_ratings)
    return round(average_rating, 1), len(user_ratings)

def show_registration_form():
    st.header("📝 تسجيل مغترب جديد")
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("الاسم الكامل *")
            city = st.selectbox("المدينة *", list(CHINA_CITIES.keys()))
            
            contact_type = st.selectbox(
                "طريقة التواصل", 
                ["بريد إلكتروني", "واتساب", "هاتف", "وي تشات"]
            )
            
            contact_info = st.text_input("معلومات التواصل *")
            
        with col2:
            status = st.selectbox("الحالة *", ["متاح", "مشغول", "غير متاح"])
            
            language = st.multiselect(
                "اللغات المتحدث بها",
                ["العربية", "الإنجليزية", "الصينية", "الفرنسية", "الألمانية", "الإسبانية"]
            )
            
            details = st.text_area("تفاصيل عنك *", placeholder="مثال: طالب، موظف، تاجر...")
        
        specialization = st.text_input("التخصص أو المجال")
        
        # حقل مجالات الخبرة الإلزامي
        st.subheader("🛠️ مجالات الخبرة *")
        st.markdown("**يرجى اختيار مجال خبرتك (يمكن اختيار أكثر من مجال)**")
        
        expertise = st.multiselect(
            "اختر مجالات خبرتك:",
            options=list(EXPERTISE_AREAS.keys()),
            help="يمكنك اختيار أكثر من مجال خبرة"
        )
        
        # تحذير إذا لم يتم اختيار أي مجال خبرة
        if not expertise:
            st.warning("⚠️ يرجى اختيار مجال خبرة واحد على الأقل")
        
        submitted = st.form_submit_button("✅ تسجيل البيانات")
        
        if submitted:
            if name and contact_info and details and expertise:
                # إحداثيات المدينة المختارة
                lat = CHINA_CITIES[city]["lat"]
                lon = CHINA_CITIES[city]["lon"]
                
                # تحديد اللون حسب الحالة
                if status == "متاح":
                    color = [0, 255, 0]  # أخضر
                elif status == "مشغول":
                    color = [255, 165, 0]  # برتقالي
                else:
                    color = [255, 0, 0]  # أحمر
                
                new_user = {
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "city": city,
                    "lat": lat,
                    "lon": lon,
                    "status": status,
                    "contact_type": contact_type,
                    "contact_info": contact_info,
                    "details": details,
                    "language": ", ".join(language),
                    "specialization": specialization,
                    "expertise": expertise,
                    "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "color": color,
                    "rating": 0,
                    "reviews": 0
                }
                
                st.session_state.users.append(new_user)
                st.success("🎉 تم تسجيل بياناتك بنجاح!")
                st.balloons()
                
                # عرض البيانات المسجلة
                st.subheader("بياناتك المسجلة")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**الاسم:** {name}")
                    st.write(f"**المدينة:** {city}")
                    st.write(f"**الحالة:** {status}")
                    st.write(f"**مجالات الخبرة:** {', '.join(expertise)}")
                with col2:
                    st.write(f"**طريقة التواصل:** {contact_type}")
                    st.write(f"**معلومات التواصل:** {contact_info}")
                    st.write(f"**اللغات:** {', '.join(language)}")
            else:
                st.error("⚠️ يرجى ملء جميع الحقول الإلزامية (*) بما في ذلك مجالات الخبرة")

def create_pydeck_map(filtered_users):
    """إنشاء خريطة باستخدام PyDeck"""
    
    # تحويل البيانات إلى DataFrame
    map_data = []
    for user in filtered_users:
        avg_rating, total_reviews = calculate_user_rating(user['id'])
        map_data.append({
            'name': user['name'],
            'city': user['city'],
            'lat': user['lat'],
            'lon': user['lon'],
            'status': user['status'],
            'contact_type': user['contact_type'],
            'contact_info': user['contact_info'],
            'details': user['details'],
            'language': user.get('language', ''),
            'expertise': ', '.join(user.get('expertise', [])),
            'rating': avg_rating,
            'reviews': total_reviews,
            'coordinates': [user['lon'], user['lat']],
            'color': user.get('color', [255, 0, 0])
        })
    
    df = pd.DataFrame(map_data)
    
    if df.empty:
        return None
    
    # إعداد طبقة الخريطة
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=df,
        get_position='coordinates',
        get_fill_color='color',
        get_radius=50000,
        pickable=True,
        auto_highlight=True,
        radius_min_pixels=8,
        radius_max_pixels=15,
    )
    
    # إعداد عرض الخريطة
    view_state = pdk.ViewState(
        latitude=35.0,
        longitude=105.0,
        zoom=4,
        pitch=0,
        bearing=0
    )
    
    # إنشاء الخريطة
    map = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            'html': '''
                <b>الاسم:</b> {name}<br/>
                <b>المدينة:</b> {city}<br/>
                <b>الحالة:</b> {status}<br/>
                <b>التقييم:</b> {rating} ⭐ ({reviews} تقييم)<br/>
                <b>مجالات الخبرة:</b> {expertise}<br/>
                <b>التواصل:</b> {contact_type}: {contact_info}
            ''',
            'style': {
                'backgroundColor': 'white',
                'color': 'black',
                'direction': 'rtl',
                'textAlign': 'right'
            }
        }
    )
    
    return map

def show_map():
    st.header("🗺️ خريطة المغتربين في الصين")
    
    # إضافة مدينة جديدة
    add_custom_city()
    
    if not st.session_state.users:
        st.warning("⚠️ لا توجد بيانات لعرضها. يرجى تسجيل مستخدمين جدد.")
        return
    
    # الشريط الجانبي للتصفية
    st.sidebar.header("🔍 تصفية البحث")
    
    # تصفية حسب المدينة
    cities = list(set(user["city"] for user in st.session_state.users))
    selected_city = st.sidebar.selectbox("اختر المدينة", ["الكل"] + cities)
    
    # تصفية حسب الحالة
    status_filter = st.sidebar.selectbox("الحالة", ["الكل", "متاح", "مشغول", "غير متاح"])
    
    # تصفية حسب مجالات الخبرة
    st.sidebar.subheader("🛠️ تصفية حسب الخبرة")
    all_expertise = list(EXPERTISE_AREAS.keys())
    selected_expertise = st.sidebar.multiselect(
        "اختر مجالات الخبرة:",
        options=all_expertise,
        help="اختر مجالات الخبرة المطلوبة"
    )
    
    # تصفية حسب التقييم
    st.sidebar.subheader("⭐ تصفية حسب التقييم")
    min_rating = st.sidebar.slider("حد أدنى للتقييم", 0.0, 5.0, 0.0, 0.5)
    
    # تطبيق التصفية
    filtered_users = st.session_state.users
    
    if selected_city != "الكل":
        filtered_users = [u for u in filtered_users if u["city"] == selected_city]
    
    if status_filter != "الكل":
        filtered_users = [u for u in filtered_users if u["status"] == status_filter]
    
    if selected_expertise:
        filtered_users = [
            u for u in filtered_users 
            if any(expertise in u.get('expertise', []) for expertise in selected_expertise)
        ]
    
    # تصفية حسب التقييم
    filtered_users = [
        u for u in filtered_users 
        if calculate_user_rating(u['id'])[0] >= min_rating
    ]
    
    # عرض الخريطة
    st.subheader("الخريطة التفاعلية")
    st.markdown("انقر على أي نقطة في الخريطة لعرض معلومات المغترب")
    
    # إنشاء وعرض الخريطة
    map = create_pydeck_map(filtered_users)
    if map:
        st.pydeck_chart(map)
    else:
        st.error("❌ لا يمكن عرض الخريطة بسبب عدم وجود بيانات")
    
    # إحصائيات سريعة
    st.subheader("📊 إحصائيات سريعة")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_users = len(st.session_state.users)
        st.metric("إجمالي المسجلين", total_users)
    
    with col2:
        available_count = len([u for u in st.session_state.users if u["status"] == "متاح"])
        st.metric("المتاحون", available_count)
    
    with col3:
        cities_count = len(set(u["city"] for u in st.session_state.users))
        st.metric("المدن المغطاة", cities_count)
    
    with col4:
        filtered_count = len(filtered_users)
        st.metric("نتائج البحث", filtered_count)
    
    # عرض قائمة مفصلة
    st.subheader("👥 قائمة المغتربين المفصلة")
    
    if filtered_users:
        for user in filtered_users:
            # حساب التقييم الحالي
            avg_rating, total_reviews = calculate_user_rating(user['id'])
            
            # تحديد الأيقونة حسب الحالة
            if user["status"] == "متاح":
                status_icon = "🟢"
            elif user["status"] == "مشغول":
                status_icon = "🟡"
            else:
                status_icon = "🔴"
            
            city_ar = user["city"].split(" - ")[0]
            
            with st.expander(f"{status_icon} {user['name']} - {city_ar} - ⭐ {avg_rating} ({total_reviews} تقييم)"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**معلومات الاتصال:**")
                    st.write(f"📞 **{user['contact_type']}:** {user['contact_info']}")
                    st.write(f"🗣️ **اللغات:** {user.get('language', 'غير محدد')}")
                    st.write(f"⭐ **التقييم:** {avg_rating}/5 ({total_reviews} تقييم)")
                    st.write(f"📍 **الإحداثيات:** {user['lat']:.4f}, {user['lon']:.4f}")
                
                with col2:
                    st.write("**الحالة والموقع:**")
                    st.write(f"**{user['status']}**")
                    st.write(f"🏙️ **المدينة:** {user['city']}")
                    st.write(f"📅 **تاريخ التسجيل:** {user.get('registration_date', 'غير محدد')}")
                    if user.get('specialization'):
                        st.write(f"🎯 **التخصص:** {user['specialization']}")
                
                st.write("**🛠️ مجالات الخبرة:**")
                expertise_list = user.get('expertise', [])
                if expertise_list:
                    for expertise in expertise_list:
                        st.write(f"• {expertise}")
                else:
                    st.write("لا توجد مجالات خبرة محددة")
                
                st.write("**التفاصيل:**")
                st.info(user['details'])
                
                # نظام التقييم
                show_rating_system(user['id'])
    else:
        st.warning("⚠️ لا توجد نتائج تطابق معايير البحث")

def show_statistics():
    st.header("📊 إحصائيات المنصة")
    
    if not st.session_state.users:
        st.warning("لا توجد بيانات كافية للإحصائيات")
        return
    
    total_users = len(st.session_state.users)
    available_users = len([u for u in st.session_state.users if u["status"] == "متاح"])
    busy_users = len([u for u in st.session_state.users if u["status"] == "مشغول"])
    unavailable_users = len([u for u in st.session_state.users if u["status"] == "غير متاح"])
    
    # إحصائيات عامة
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("إجمالي المغتربين", total_users)
    with col2:
        st.metric("المتاحون", available_users)
    with col3:
        st.metric("المشغولون", busy_users)
    with col4:
        st.metric("غير المتاحين", unavailable_users)
    
    # إحصائيات التقييمات
    st.subheader("⭐ إحصائيات التقييمات")
    all_ratings = []
    for user_ratings in st.session_state.ratings.values():
        all_ratings.extend([r['rating'] for r in user_ratings])
    
    if all_ratings:
        avg_platform_rating = sum(all_ratings) / len(all_ratings)
        total_reviews = len(all_ratings)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("متوسط تقييم المنصة", f"{avg_platform_rating:.1f}/5")
        with col2:
            st.metric("إجمالي التقييمات", total_reviews)
    
    # توزيع مجالات الخبرة
    st.subheader("🛠️ توزيع مجالات الخبرة")
    expertise_counts = {}
    for user in st.session_state.users:
        for expertise in user.get('expertise', []):
            expertise_counts[expertise] = expertise_counts.get(expertise, 0) + 1
    
    if expertise_counts:
        expertise_df = pd.DataFrame(list(expertise_counts.items()), columns=['مجال الخبرة', 'العدد'])
        expertise_df = expertise_df.sort_values('العدد', ascending=False)
        st.bar_chart(expertise_df.set_index('مجال الخبرة'))
    
    # أفضل المسجلين تقييماً
    st.subheader("🏆 أفضل المسجلين تقييماً")
    user_ratings = []
    for user in st.session_state.users:
        avg_rating, total_reviews = calculate_user_rating(user['id'])
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

def main():
    # شريط التنقل
    st.sidebar.title("🌍 التنقل")
    
    page_options = {
        "الخريطة التفاعلية": show_map,
        "تسجيل جديد": show_registration_form,
        "الإحصائيات": show_statistics
    }
    
    selected_page = st.sidebar.radio("اختر الصفحة:", list(page_options.keys()))
    
    # معلومات سريعة في الشريط الجانبي
    st.sidebar.markdown("---")
    st.sidebar.header("ℹ️ معلومات سريعة")
    st.sidebar.write(f"**إجمالي المسجلين:** {len(st.session_state.users)}")
    
    available_count = len([u for u in st.session_state.users if u["status"] == "متاح"])
    st.sidebar.write(f"**المتاحون الآن:** {available_count}")
    
    # إجمالي التقييمات
    total_reviews = sum(len(ratings) for ratings in st.session_state.ratings.values())
    st.sidebar.write(f"**إجمالي التقييمات:** {total_reviews}")
    
    # عرض الصفحة المختارة
    page_options[selected_page]()

if __name__ == "__main__":
    main()