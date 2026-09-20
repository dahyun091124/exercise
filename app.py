import streamlit as st
import os
import pandas as pd

# -------------------------------------------------------------------
# 페이지 기본 설정 (사이드바 기본 닫힘 상태: collapsed)
# -------------------------------------------------------------------
st.set_page_config(
    page_title="EXERCISE 브랜드몰",
    page_icon="💪🏼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 세션 상태로 사이드바 열림/닫힘 제어
if 'sidebar_state' not in st.session_state:
    st.session_state['sidebar_state'] = 'collapsed'

# -------------------------------------------------------------------
# 러쉬(LUSH) 스타일 커스텀 CSS
# -------------------------------------------------------------------
st.markdown("""
<style>
    /* 전체 백그라운드 & 폰트 설정 */
    .stApp, body, html {
        background-color: #ffffff !important;
        color: #111111 !important;
    }
    
    * {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif !important;
    }

    /* 사이드바(메뉴창) 내 메뉴 버튼 스타일 */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #eeeeee !important;
    }
    [data-testid="stSidebar"] * {
        color: #111111 !important;
    }
    [data-testid="stSidebar"] .stButton > button {
        background-color: #f8f9fa !important;
        color: #111111 !important;
        border: 1px solid #e9ecef !important;
        font-weight: 600 !important;
        margin-bottom: 8px;
        text-align: left !important;
        padding-left: 15px !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #111111 !important;
        color: #ffffff !important;
    }

    /* 러쉬 헤더 레이아웃 (중앙 정렬 로고) */
    .lush-logo-center {
        font-size: 32px;
        font-weight: 950;
        letter-spacing: -1.5px;
        color: #000000;
        text-transform: uppercase;
        text-align: center;
        width: 100%;
    }

    /* 러쉬 브랜드 메인 서두 스타일 */
    .lush-quote-box {
        text-align: center;
        padding: 50px 20px 40px 20px;
        max-width: 900px;
        margin: 0 auto 30px auto;
    }
    .lush-quote-title {
        font-size: clamp(22px, 3.2vw, 34px);
        font-weight: 900;
        line-height: 1.45;
        letter-spacing: -1.5px;
        color: #111111;
        margin-bottom: 20px;
        word-break: keep-all;
    }
    .lush-quote-desc {
        font-size: 15px;
        line-height: 1.8;
        color: #666666;
        word-break: keep-all;
    }

    /* 러쉬 원형 아이콘 그리드 스타일 */
    .circle-card {
        background-color: #111111;
        width: 170px;
        height: 170px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 0 auto 15px auto;
        color: #ffffff !important;
        text-align: center;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    .circle-card-title {
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #ffffff !important;
        margin-top: 6px;
    }
    .circle-card-icon {
        font-size: 28px;
    }

    /* 상세 섹션 스타일 */
    .lush-section-title {
        font-size: clamp(22px, 2.8vw, 34px);
        font-weight: 900;
        line-height: 1.35;
        letter-spacing: -1.5px;
        color: #111111 !important;
        margin-bottom: 15px;
        word-break: keep-all;
    }
    .lush-section-desc {
        font-size: 15px;
        line-height: 1.75;
        color: #555555 !important;
        word-break: keep-all;
    }
    
    /* 초록색 태그 강조 (#03C75A) */
    .lush-tag {
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #03C75A !important;
        margin-bottom: 8px;
    }

    /* 가격 및 버튼 스타일 */
    .price-text {
        font-size: 20px;
        font-weight: 800;
        color: #03C75A !important;
    }
    .rank-badge {
        position: absolute;
        top: 10px;
        left: 10px;
        background-color: #000000;
        color: #ffffff !important;
        font-weight: bold;
        padding: 4px 10px;
        font-size: 14px;
        z-index: 10;
    }
    
    .stButton > button {
        border-radius: 4px !important;
        border: 1px solid #dddddd !important;
        background-color: #ffffff !important;
        color: #111111 !important;
    }
    .stButton > button[kind="primary"] {
        background-color: #111111 !important;
        color: #ffffff !important;
        border: none !important;
    }

    /* 푸터 스타일 */
    .footer-container {
        margin-top: 80px;
        padding: 40px 0 20px 0;
        border-top: 1px solid #eeeeee;
        color: #888888;
        font-size: 13px;
        line-height: 1.7;
    }
</style>
""", unsafe_allow_html=True)

# 안전한 이미지 로딩 함수
def safe_image(img_src):
    if isinstance(img_src, str):
        if os.path.exists(img_src) or img_src.startswith("http"):
            st.image(img_src, use_container_width=True)
        else:
            st.image("https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=800&auto=format&fit=crop&q=80", use_container_width=True)
    else:
        st.image(img_src, use_container_width=True)

# -------------------------------------------------------------------
# 세션 상태 초기화
# -------------------------------------------------------------------
if 'page' not in st.session_state:
    st.session_state['page'] = 'about'

if 'cart' not in st.session_state:
    st.session_state['cart'] = []

if 'orders' not in st.session_state:
    st.session_state['orders'] = []

if 'user' not in st.session_state:
    st.session_state['user'] = None

if 'show_modal' not in st.session_state:
    st.session_state['show_modal'] = False

if 'added_item' not in st.session_state:
    st.session_state['added_item'] = ""

if 'selected_product' not in st.session_state:
    st.session_state['selected_product'] = None

if 'admin_authenticated' not in st.session_state:
    st.session_state['admin_authenticated'] = False

# 감성 이미지 리스트
about_images = [
    "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=1000&auto=format&fit=crop&q=80",
    "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=1000&auto=format&fit=crop&q=80",
    "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=1000&auto=format&fit=crop&q=80",
    "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=1000&auto=format&fit=crop&q=80",
    "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1000&auto=format&fit=crop&q=80"
]

# 스마트스토어 상품 목록
kits = [
    {
        "id": 1,
        "name": "EXERCISE 커스텀 DIY 운동 키트", 
        "price": 15000, 
        "comment": "라텍스밴드 + 지압판 + 폴리모프 구성 / 나만의 맞춤형 운동 기구",
        "img": "ganadi.jpg",
        "desc_title": "사용자의 신체와 취향에 딱 맞게 제작하는 DIY 키트",
        "desc_detail": "자신의 신체 조건과 운동 목적에 맞게 직접 형태를 변형할 수 있는 커스텀 운동 키트입니다.",
        "components": "라텍스밴드, 지압판, 폴리모프 왁스",
        "feature": "손 모양이나 발 모양에 맞춰 자유롭게 성형 가능한 커스텀 구조"
    },
    {
        "id": 2,
        "name": "맞춤형 공기방석 에어셀 제작 키트", 
        "price": 18500, 
        "comment": "에어셀 주머니(2개) + 상부 쿠션 스펀지 + 외부 커버 구성",
        "img": "usagi.jpg",
        "desc_title": "장시간 앉아있는 현대인을 위한 골반 및 척추 균형 방석",
        "desc_detail": "공기량을 자유롭게 조절할 수 있는 에어셀 주머니 2개로 구성된 맞춤형 방석 키트입니다.",
        "components": "상부 쿠션층 스펀지, 하부 지지층 스펀지, 에어셀 주머니 2개, 외부 커버",
        "feature": "공기압 조절을 통한 맞춤형 자세 교정 및 체중 분산 기능"
    },
    {
        "id": 3,
        "name": "소멸위기 지역 특산물 이온음료 DIY 키트", 
        "price": 9800, 
        "comment": "지방 소멸 위기 지역 대표 특산물(꿀유자, 오미자) 활용 음료",
        "img": "hachiware.jpg",
        "desc_title": "소멸 위기 지역 특산물로 만드는 건강 수분 보충 음료",
        "desc_detail": "지역 상생의 의미를 담아 건강하고 맛있게 수분과 전해질을 보충하는 이온음료 키트입니다.",
        "components": "꿀유자믹스 스틱, 오미자 스틱, 전용 소주잔 세트",
        "feature": "100% 지역 특산물 활용 / 빠른 수분 및 에너지 충전 효과"
    }
]

if 'c2c_products' not in st.session_state:
    st.session_state['c2c_products'] = [
        {
            "id": 101,
            "name": "폴리모프 커스텀 지압 악력기", 
            "price": 12000, 
            "comment": "판매자: 정예나 | 손 모양 맞춤 지압 구조",
            "img": about_images[3],
            "desc_title": "구매자 정예나 님이 제작한 custom 지압 악력기",
            "desc_detail": "EXERCISE DIY 키트의 폴리모프와 지압판 재료를 활용하여 손바닥 곡선에 딱 맞게 제작한 수제 악력기입니다.",
            "components": "폴리모프 커스텀 성형 악력 프레임, 결합형 지압 돌기",
            "feature": "제작자 맞춤형 손 그립감 구현"
        }
    ]

def add_to_cart(item_name, item_price):
    st.session_state['cart'].append({"name": item_name, "price": item_price})
    st.session_state['added_item'] = item_name
    st.session_state['show_modal'] = True

# -------------------------------------------------------------------
# 왼쪽에 세로로 뜨는 사이드바 메뉴 (≡ 메뉴 클릭 시 토글형으로 열림)
# -------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧭 NAVIGATION")
    st.write("---")
    
    if st.button("🏢 기업소개", use_container_width=True):
        st.session_state['page'] = 'about'
        st.rerun()

    if st.button("🛍️ 스마트스토어", use_container_width=True):
        st.session_state['page'] = 'store'
        st.rerun()

    if st.button("🔑 로그인 / 회원가입", use_container_width=True):
        st.session_state['page'] = 'login'
        st.rerun()

    if st.button("⚙️ 관리자 페이지", use_container_width=True):
        st.session_state['page'] = 'admin'
        st.rerun()

    cart_cnt = len(st.session_state['cart'])
    cart_label = f"🛒 장바구니 ({cart_cnt})" if cart_cnt > 0 else "🛒 장바구니"
    if st.button(cart_label, use_container_width=True):
        st.session_state['page'] = 'cart'
        st.rerun()

# -------------------------------------------------------------------
# [요청사항 반영] 맨 왼쪽: ≡ 메뉴 / 가운데: EXERCISE 로고 헤더
# -------------------------------------------------------------------
col_left_btn, col_center_logo, col_right_empty = st.columns([1, 4, 1])

with col_left_btn:
    # 클릭하면 왼쪽 사이드바가 열리거나 닫히는 토글 동작
    if st.button("≡ 메뉴", use_container_width=True):
        st.session_state['sidebar_state'] = 'expanded' if st.session_state['sidebar_state'] == 'collapsed' else 'collapsed'
        # Streamlit 사이드바 열림 제어
        st.set_page_config(initial_sidebar_state=st.session_state['sidebar_state'])
        st.rerun()

with col_center_logo:
    st.markdown("<div class='lush-logo-center'>EXERCISE</div>", unsafe_allow_html=True)

with col_right_empty:
    st.write("") # 우측 대칭용 여백

st.write("---")

# 장바구니 알림 모달
if st.session_state['show_modal']:
    with st.container(border=True):
        st.success(f"🛒 **'{st.session_state['added_item']}'** 상품이 장바구니에 담겼습니다.")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            if st.button("🛍️ 계속 둘러보기", use_container_width=True):
                st.session_state['show_modal'] = False
                st.rerun()
        with col_m2:
            if st.button("🛒 장바구니로 이동", type="primary", use_container_width=True):
                st.session_state['show_modal'] = False
                st.session_state['page'] = 'cart'
                st.rerun()

# -------------------------------------------------------------------
# 1. 기업/브랜드 소개 페이지
# -------------------------------------------------------------------
if st.session_state['page'] == 'about':
    
    # [러쉬 서두] 메인 브랜드 선언문
    st.markdown("""
    <div class="lush-quote-box">
        <div class="lush-quote-title">
            “ EXERCISE는 모든 신체가 가진 고유한 가능성을 믿으며,<br>
            자신의 몸에 완벽하게 맞춰진 정직한 운동 경험을 손으로 만듭니다. ”
        </div>
        <div class="lush-quote-desc">
            획일화된 공장형 기구의 틀에서 벗어나 개인 맞춤형 커스텀 DIY 키트부터 지역 상생 헬스 케어,<br>
            그리고 구매자의 아이디어가 상품이 되는 가치 공유 플랫폼까지 지속 가능한 웰니스 생태계를 만들어갑니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # [러쉬 6개 원형 아이콘 그리드 (3열 x 2행)]
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        st.markdown("""
        <div class="circle-card">
            <div class="circle-card-icon">🧩</div>
            <div class="circle-card-title">CUSTOM DIY</div>
        </div>
        """, unsafe_allow_html=True)
    with col_g2:
        st.markdown("""
        <div class="circle-card">
            <div class="circle-card-icon">💨</div>
            <div class="circle-card-title">AIR-CELL CUSHION</div>
        </div>
        """, unsafe_allow_html=True)
    with col_g3:
        st.markdown("""
        <div class="circle-card">
            <div class="circle-card-icon">🍊</div>
            <div class="circle-card-title">LOCAL RECOVERY</div>
        </div>
        """, unsafe_allow_html=True)

    col_g4, col_g5, col_g6 = st.columns(3)
    with col_g4:
        st.markdown("""
        <div class="circle-card">
            <div class="circle-card-icon">🖐️</div>
            <div class="circle-card-title">POLYMORPH</div>
        </div>
        """, unsafe_allow_html=True)
    with col_g5:
        st.markdown("""
        <div class="circle-card">
            <div class="circle-card-icon">🤝</div>
            <div class="circle-card-title">ETHICAL C2C</div>
        </div>
        """, unsafe_allow_html=True)
    with col_g6:
        st.markdown("""
        <div class="circle-card">
            <div class="circle-card-icon">🌱</div>
            <div class="circle-card-title">SUSTAINABLE</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("<br><br>", unsafe_allow_html=True)
    st.divider()

    # [상세 특징 5가지 (지그재그 감성 이미지/텍스트)]
    
    # 01. CUSTOM DIY KIT
    col_img1, col_txt1 = st.columns([1, 1], gap="large")
    with col_img1:
        safe_image(about_images[0])
    with col_txt1:
        st.write("")
        st.markdown('<div class="lush-tag">01. CUSTOM DIY KIT</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="lush-section-title">
            자신의 신체 조건과 목적에<br>
            완벽하게 맞추는 커스텀 키트
        </div>
        <div class="lush-section-desc">
            정형화된 기구의 틀을 깨고, 개인의 손 모양과 체형에 정확히 맞춤 피팅되는 
            커스터마이징 키트를 통해 나만의 효율적인 움직임을 만들어갑니다.
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # 02. AIR-CELL BALANCING
    col_txt2, col_img2 = st.columns([1, 1], gap="large")
    with col_txt2:
        st.write("")
        st.markdown('<div class="lush-tag">02. AIR-CELL BALANCING</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="lush-section-title">
            장시간 앉아있는 현대인을 위한<br>
            골반 및 척추 균형 솔루션
        </div>
        <div class="lush-section-desc">
            공기량을 자율 조절할 수 있는 에어셀 구조를 적용하여 바른 자세 유지와 
            체중 분산 효과를 극대화한 인체공학적 방석을 제작합니다.
        </div>
        """, unsafe_allow_html=True)
    with col_img2:
        safe_image(about_images[1])

    st.divider()

    # 03. LOCAL RECOVERY DRINK
    col_img3, col_txt3 = st.columns([1, 1], gap="large")
    with col_img3:
        safe_image(about_images[2])
    with col_txt3:
        st.write("")
        st.markdown('<div class="lush-tag">03. LOCAL RECOVERY DRINK</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="lush-section-title">
            소멸 위기 지역 특산물로<br>
            건강하게 채우는 수분과 전해질
        </div>
        <div class="lush-section-desc">
            꿀유자, 오미자 등 지방 소멸 위기 지역의 특산물을 활용하여 
            운동 후 필요한 수분과 에너지를 건강하게 충전하는 상생형 음료입니다.
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # 04. POLYMORPH ERGONOMICS
    col_txt4, col_img4 = st.columns([1, 1], gap="large")
    with col_txt4:
        st.write("")
        st.markdown('<div class="lush-tag">04. POLYMORPH ERGONOMICS</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="lush-section-title">
            내 손바닥 곡선에 딱 맞게<br>
            변형되는 맞춤형 지압 구조
        </div>
        <div class="lush-section-desc">
            체온과 열에 반응해 형태를 자유롭게 몰딩하는 폴리모프 기술을 적용하여 
            세상에 단 하나뿐인 최고의 그립감과 자극을 제공합니다.
        </div>
        """, unsafe_allow_html=True)
    with col_img4:
        safe_image(about_images[3])

    st.divider()

    # 05. SHARED COMMUNITY
    col_img5, col_txt5 = st.columns([1, 1], gap="large")
    with col_img5:
        safe_image(about_images[4])
    with col_txt5:
        st.write("")
        st.markdown('<div class="lush-tag">05. SHARED COMMUNITY</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="lush-section-title">
            구매자의 아이디어가 상품이 되는<br>
            C2C 가치 공유 커뮤니티
        </div>
        <div class="lush-section-desc">
            사용자가 직접 개발한 창작 운동기구를 등록하고 공유할 수 있는 
            선순환 C2C 마켓플레이스를 지향합니다.
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    if st.button("🛍️ EXERCISE 스마트스토어 바로가기 ➔", type="primary", use_container_width=True):
        st.session_state['page'] = 'store'
        st.rerun()

# -------------------------------------------------------------------
# 2. 로그인 / 회원가입 페이지
# -------------------------------------------------------------------
elif st.session_state['page'] == 'login':
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.markdown("<h2 style='text-align: center;'>🔐 회원 로그인 / 회원가입</h2>", unsafe_allow_html=True)
        st.write("")
        
        tab_log1, tab_log2 = st.tabs(["로그인", "회원가입"])
        
        with tab_log1:
            with st.form("login_form"):
                user_id = st.text_input("아이디 또는 이메일", placeholder="example@exercise.com")
                user_pw = st.text_input("비밀번호", type="password")
                submit_login = st.form_submit_button("로그인하기", type="primary", use_container_width=True)
                
                if submit_login:
                    if user_id and user_pw:
                        st.session_state['user'] = user_id.split('@')[0]
                        st.success(f"{st.session_state['user']}님, 환영합니다!")
                        st.session_state['page'] = 'store'
                        st.rerun()
                    else:
                        st.error("아이디와 비밀번호를 모두 입력해 주세요.")
                        
        with tab_log2:
            with st.form("signup_form"):
                new_name = st.text_input("이름")
                new_id = st.text_input("아이디(이메일)")
                new_pw = st.text_input("비밀번호 설정", type="password")
                submit_signup = st.form_submit_button("가입완료", type="primary", use_container_width=True)
                
                if submit_signup:
                    if new_name and new_id and new_pw:
                        st.success("회원가입이 완료되었습니다! 로그인해 주세요.")
                    else:
                        st.error("모든 항목을 입력해야 합니다.")

# -------------------------------------------------------------------
# 3. 스마트스토어 메인 페이지
# -------------------------------------------------------------------
elif st.session_state['page'] == 'store':
    tab1, tab2 = st.tabs(["전체 상품", "구매자 창작 마켓"])
    
    with tab1:
        st.markdown("<h3 style='margin-bottom:20px;'>전체 상품 목록</h3>", unsafe_allow_html=True)
        cols = st.columns(3)
        for idx, kit in enumerate(kits):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"<span class='rank-badge'>{idx + 1}</span>", unsafe_allow_html=True)
                    safe_image(kit["img"])
                    st.markdown(f"**{kit['name']}**")
                    st.caption(kit['comment'])
                    st.markdown(f"<p class='price-text'>{kit['price']:,} 원</p>", unsafe_allow_html=True)
                    
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        if st.button("상세보기", key=f"detail_{kit['id']}", use_container_width=True):
                            st.session_state['selected_product'] = kit
                            st.session_state['page'] = 'detail'
                            st.rerun()
                    with col_b2:
                        if st.button("담기", key=f"home_cart_{kit['id']}", type="primary", use_container_width=True):
                            add_to_cart(kit['name'], kit['price'])
                            st.rerun()

    with tab2:
        st.markdown("### 구매자 창작 물품 거래소")
        st.caption("구매자들이 직접 만든 완성품을 공유하고 거래하는 공간입니다.")
        
        with st.expander("➕ 내 창작물 직접 판매 등록하기", expanded=False):
            with st.form("c2c_add_form"):
                c_title = st.text_input("상품명")
                c_seller = st.text_input("판매자 닉네임")
                c_price = st.number_input("판매 가격 (원)", min_value=0, step=1000, value=10000)
                c_img_file = st.file_uploader("대표 이미지 선택", type=["jpg", "jpeg", "png"])
                c_desc_title = st.text_input("한 줄 개요")
                c_desc_detail = st.text_area("상세설명 및 제작 노하우")
                
                c_submit = st.form_submit_button("등록하기", type="primary", use_container_width=True)
                if c_submit and c_title and c_seller:
                    new_c2c = {
                        "id": len(st.session_state['c2c_products']) + 200,
                        "name": f"[C2C] {c_title}",
                        "price": c_price,
                        "comment": f"판매자: {c_seller} | {c_desc_title}",
                        "img": c_img_file if c_img_file else about_images[3],
                        "desc_title": c_desc_title,
                        "desc_detail": c_desc_detail,
                        "components": "커스텀 조합",
                        "feature": "맞춤형 그립"
                    }
                    st.session_state['c2c_products'].append(new_c2c)
                    st.success("등록되었습니다!")
                    st.rerun()

        st.divider()
        cols_c2c = st.columns(2)
        for idx, c_item in enumerate(st.session_state['c2c_products']):
            with cols_c2c[idx % 2]:
                with st.container(border=True):
                    safe_image(c_item['img'])
                    st.markdown(f"**{c_item['name']}**")
                    st.caption(c_item['comment'])
                    st.markdown(f"<p class='price-text'>{c_item['price']:,} 원</p>", unsafe_allow_html=True)
                    
                    col_cb1, col_cb2 = st.columns(2)
                    with col_cb1:
                        if st.button("상세보기", key=f"c2c_detail_{c_item['id']}_{idx}", use_container_width=True):
                            st.session_state['selected_product'] = c_item
                            st.session_state['page'] = 'detail'
                            st.rerun()
                    with col_cb2:
                        if st.button("담기", key=f"c2c_cart_{c_item['id']}_{idx}", type="primary", use_container_width=True):
                            add_to_cart(c_item['name'], c_item['price'])
                            st.rerun()

# -------------------------------------------------------------------
# 4. 장바구니 페이지
# -------------------------------------------------------------------
elif st.session_state['page'] == 'cart':
    if st.button("⬅ 이전으로 돌아가기"):
        st.session_state['page'] = 'store'
        st.rerun()
        
    st.divider()
    st.markdown("## 🛒 장바구니 및 주문결제")
    
    if not st.session_state['cart']:
        st.info("장바구니가 비어 있습니다.")
    else:
        col_c1, col_c2 = st.columns([3, 2])
        with col_c1:
            total_price = 0
            delete_index = None
            for idx, item in enumerate(st.session_state['cart']):
                with st.container(border=True):
                    mc1, mc2, mc3 = st.columns([3, 2, 1])
                    with mc1:
                        st.markdown(f"**{item['name']}**")
                    with mc2:
                        st.markdown(f"<p class='price-text'>{item['price']:,} 원</p>", unsafe_allow_html=True)
                    with mc3:
                        if st.button("삭제", key=f"cart_del_{idx}"):
                            delete_index = idx
                    total_price += item['price']
            
            if delete_index is not None:
                st.session_state['cart'].pop(delete_index)
                st.rerun()
            st.markdown(f"### 총 결제 예정 금액: **{total_price:,} 원**")

        with col_c2:
            with st.container(border=True):
                st.markdown("### 💳 주문 정보 입력")
                with st.form("checkout_form"):
                    name = st.text_input("수령인 이름", value=st.session_state['user'] if st.session_state['user'] else "")
                    phone = st.text_input("연락처")
                    address = st.text_input("배송지 주소")
                    pay_method = st.radio("결제 수단", ["N Pay (네이버페이)", "신용/체크카드", "계좌이체"])
                    pay_submitted = st.form_submit_button("💳 결제하기", type="primary", use_container_width=True)
                    
                    if pay_submitted and name and phone and address:
                        new_order = {
                            "id": len(st.session_state['orders']) + 1,
                            "name": name,
                            "items": [item['name'] for item in st.session_state['cart']],
                            "total_price": total_price
                        }
                        st.session_state['orders'].append(new_order)
                        st.success("주문 결제가 완료되었습니다!")
                        st.session_state['cart'] = []

# -------------------------------------------------------------------
# 5. 상품 상세 페이지
# -------------------------------------------------------------------
elif st.session_state['page'] == 'detail' and st.session_state['selected_product'] is not None:
    p = st.session_state['selected_product']
    if st.button("⬅ 목록으로 돌아가기"):
        st.session_state['page'] = 'store'
        st.rerun()
        
    st.divider()
    col_d1, col_d2 = st.columns([1, 1])
    with col_d1:
        safe_image(p['img'])
    with col_d2:
        st.markdown(f"## {p['name']}")
        st.caption(p.get('comment', ''))
        st.markdown(f"<p class='price-text' style='font-size:26px;'>{p['price']:,} 원</p>", unsafe_allow_html=True)
        if st.button("🛒 장바구니 담기", type="primary", use_container_width=True):
            add_to_cart(p['name'], p['price'])
            st.rerun()

# -------------------------------------------------------------------
# 6. 관리자 페이지
# -------------------------------------------------------------------
elif st.session_state['page'] == 'admin':
    if st.button("⬅ 메인으로 돌아가기"):
        st.session_state['page'] = 'about'
        st.rerun()
        
    st.divider()
    st.markdown("## ⚙️ EXERCISE 관리자 페이지")
    if not st.session_state['admin_authenticated']:
        with st.form("admin_login"):
            pw = st.text_input("관리자 비밀번호", type="password")
            if st.form_submit_button("로그인", type="primary"):
                if pw == "1234":
                    st.session_state['admin_authenticated'] = True
                    st.rerun()
                else:
                    st.error("비밀번호 불일치 (기본값: 1234)")
    else:
        st.subheader("📊 구매 통계")
        if st.session_state['orders']:
            all_items = [item for o in st.session_state['orders'] for item in o['items']]
            df_counts = pd.Series(all_items).value_counts().reset_index()
            df_counts.columns = ['상품명', '수량']
            st.bar_chart(df_counts.set_index('상품명'))

# -------------------------------------------------------------------
# 러쉬 스타일 푸터
# -------------------------------------------------------------------
st.markdown("""
<div class="footer-container">
    <div style="font-weight: bold; color: #111111; font-size: 14px; margin-bottom: 8px;">EXERCISE 공식 스토어</div>
    <p>
        상호명: EXERCISE | 대표: 정예나 | 사업자등록번호: 000-00-00000<br>
        Copyright © EXERCISE Inc. All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)
