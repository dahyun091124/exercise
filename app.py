import streamlit as st
import os
import pandas as pd

# 페이지 기본 설정
st.set_page_config(
    page_title="EXERCISE 스마트스토어",
    page_icon="💪🏼",
    layout="wide",
    initial_sidebar_state="collapsed" # 기본으로 사이드바(햄버거 메뉴)를 가려 메인 브랜딩 강조
)

# 스마트스토어 & 러쉬 감성 커스텀 CSS
st.markdown("""
<style>
    .stApp, body, html {
        background-color: #ffffff !important;
        color: #111111 !important;
    }
    
    h1, h2, h3, h4, h5, h6, p, div, span, label, strong {
        color: #111111 !important;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }

    /* 사이드바 메뉴 스타일링 */
    section[data-testid="stSidebar"] {
        background-color: #f9f9f9 !important;
        border-right: 1px solid #eeeeee !important;
    }

    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] > input,
    textarea {
        background-color: #ffffff !important;
        color: #1e1e1e !important;
        border: 1px solid #cccccc !important;
        border-radius: 6px !important;
    }
    
    /* 파일 업로더 화이트 톤 */
    [data-testid="stFileUploader"] {
        background-color: #f8f9fa !important;
        border: 2px dashed #03C75A !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: #ffffff !important;
        border: none !important;
    }

    [data-testid="stFileUploaderDropzone"] > div {
        background-color: #ffffff !important;
        color: #111111 !important;
    }

    [data-testid="stFileUploader"] button {
        background-color: #ffffff !important;
        border: 1.5px solid #03C75A !important;
        color: #03C75A !important;
        font-weight: bold !important;
        box-shadow: none !important;
    }

    [data-testid="stFileUploader"] button:hover {
        background-color: #03C75A !important;
        color: #ffffff !important;
    }

    [data-testid="stFileUploader"] * {
        color: #222222 !important;
    }

    /* 상단 브랜드 로고 및 헤더 */
    .brand-header {
        text-align: center;
        padding: 5px 0 15px 0;
        width: 100%;
    }
    .brand-title {
        font-size: clamp(60px, 9vw, 120px);
        font-weight: 950;
        letter-spacing: -2px;
        line-height: 1.0;
        color: #111111 !important;
        text-transform: uppercase;
        width: 100%;
        display: block;
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
    
    .price-text {
        font-size: 20px;
        font-weight: 800;
        color: #03C75A !important;
    }
    
    .stButton > button {
        border-radius: 6px !important;
        border: 1px solid #e0e0e0 !important;
        background-color: #ffffff !important;
        color: #111111 !important;
    }
    .stButton > button[kind="primary"] {
        background-color: #03C75A !important;
        color: white !important;
        border: none !important;
    }

    /* 차트 영역 배경 및 스타일 최적화 */
    div[data-testid="stVegaLiteChart"] {
        background-color: #ffffff !important;
        border-radius: 8px !important;
        padding: 10px !important;
        border: 1px solid #e0e0e0 !important;
    }

    /* 러쉬 스타일 타이포그래피 */
    .lush-section-title {
        font-size: clamp(26px, 3.2vw, 40px);
        font-weight: 900;
        line-height: 1.25;
        letter-spacing: -1.5px;
        color: #111111 !important;
        margin-bottom: 20px;
        word-break: keep-all;
    }
    .lush-section-desc {
        font-size: 16px;
        line-height: 1.75;
        color: #444444 !important;
        word-break: keep-all;
    }
    .lush-tag {
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #03C75A !important;
        margin-bottom: 10px;
    }

    /* 푸터 스타일 */
    .footer-container {
        margin-top: 50px;
        padding: 30px 0 10px 0;
        border-top: 1px solid #eeeeee;
        color: #888888;
        font-size: 13px;
        line-height: 1.6;
    }
    .footer-title {
        font-weight: bold;
        color: #333333 !important;
        font-size: 14px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 이미지 로드 안전 함수
def safe_image(img):
    if img is not None:
        if isinstance(img, str):
            if os.path.exists(img):
                st.image(img, use_container_width=True)
            else:
                st.image("https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=500&auto=format&fit=crop&q=60", use_container_width=True)
        else:
            st.image(img, use_container_width=True)
    else:
        st.image("https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=500&auto=format&fit=crop&q=60", use_container_width=True)

# 1. 세션 상태 초기화
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

if 'orders' not in st.session_state:
    st.session_state['orders'] = []

if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

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

# C2C 상품 목록 초기화
if 'c2c_products' not in st.session_state:
    st.session_state['c2c_products'] = [
        {
            "id": 101,
            "name": "폴리모프 커스텀 지압 악력기", 
            "price": 12000, 
            "comment": "판매자: 정예나 | 손 모양 맞춤 지압 구조",
            "img": "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=500&auto=format&fit=crop&q=60",
            "desc_title": "구매자 정예나 님이 제작한 custom 지압 악력기",
            "desc_detail": "EXERCISE DIY 키트의 폴리모프와 지압판 재료를 활용하여 손바닥 곡선에 딱 맞게 제작한 수제 악력기입니다.",
            "components": "폴리모프 커스텀 성형 악력 프레임, 결합형 지압 돌기",
            "feature": "제작자 맞춤형 손 그립감 구현"
        }
    ]

# 공식 키트 데이터
kits = [
    {
        "id": 1,
        "name": "EXERCISE 커스텀 DIY 운동 키트", 
        "price": 15000, 
        "comment": "라텍스밴드 + 지압판 + 폴리모프 구성 / 나만의 맞춤형 운동 기구",
        "img": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=500&auto=format&fit=crop&q=60",
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
        "img": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=500&auto=format&fit=crop&q=60",
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
        "img": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500&auto=format&fit=crop&q=60",
        "desc_title": "소멸 위기 지역 특산물로 만드는 건강 수분 보충 음료",
        "desc_detail": "지역 상생의 의미를 담아 건강하고 맛있게 수분과 전해질을 보충하는 이온음료 키트입니다.",
        "components": "꿀유자믹스 스틱, 오미자 스틱, 전용 소주잔 세트",
        "feature": "100% 지역 특산물 활용 / 빠른 수분 및 에너지 충전 효과"
    }
]

# 장바구니 담기 처리
def add_to_cart(item_name, item_price):
    st.session_state['cart'].append({"name": item_name, "price": item_price})
    st.session_state['added_item'] = item_name
    st.session_state['show_modal'] = True

# -------------------------------------------------------------------
# 햄버거 메뉴 (사이드바 드로어 네비게이션)
# -------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 👤 회원 계정")
    if st.session_state['user'] is None:
        st.caption("로그인 후 맞춤 혜택을 받아보세요.")
        if st.button("🔑 로그인 / 회원가입", use_container_width=True):
            st.session_state['page'] = 'login'
            st.rerun()
    else:
        st.success(f"**{st.session_state['user']}**님 환영합니다!")
        if st.button("🚪 로그아웃", use_container_width=True):
            st.session_state['user'] = None
            st.rerun()

    st.divider()

    st.markdown("### 🧭 메뉴 탐색")
    if st.button("🏢 EXERCISE 브랜드 소개", use_container_width=True):
        st.session_state['page'] = 'about'
        st.rerun()

    if st.button("🛍️ 스마트스토어 (메인)", use_container_width=True):
        st.session_state['page'] = 'home'
        st.rerun()

    if st.button("🛒 장바구니 보기", use_container_width=True):
        st.session_state['page'] = 'cart'
        st.rerun()

    st.divider()

    st.markdown("### ⚙️ 시스템")
    if st.button("🔐 관리자 페이지", use_container_width=True):
        st.session_state['page'] = 'admin'
        st.rerun()

# -------------------------------------------------------------------
# 메인 상단 헤더 (우측 상단에 장바구니만 깔끔하게배치)
# -------------------------------------------------------------------
col_hdr1, col_hdr2 = st.columns([5, 1])
with col_hdr1:
    st.markdown("""
    <div class="brand-header">
        <div class="brand-title">EXERCISE</div>
        <p style="color:#666; font-size:16px; margin-top:4px; font-weight:500;">“운동에는 하나의 정답이 없다”</p>
    </div>
    """, unsafe_allow_html=True)

with col_hdr2:
    st.write("")
    cart_cnt = len(st.session_state['cart'])
    btn_text = f"🛒 장바구니 ({cart_cnt})" if cart_cnt > 0 else "🛒 장바구니"
    if st.button(btn_text, type="primary", use_container_width=True):
        st.session_state['page'] = 'cart'
        st.rerun()

# 장바구니 담김 알림 상자
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
# 화면 0: 로그인 / 회원가입 페이지
# -------------------------------------------------------------------
if st.session_state['page'] == 'login':
    st.divider()
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.markdown("<h2 style='text-align: center;'>🔐 회원 로그인</h2>", unsafe_allow_html=True)
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
                        st.success(f"{st.session_state['user']}님, 성공적으로 로그인되었습니다!")
                        st.session_state['page'] = 'home'
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
# 화면 1: 기업/브랜드 소개 페이지 (러쉬 감성 레이아웃)
# -------------------------------------------------------------------
elif st.session_state['page'] == 'about':
    st.divider()
    
    # [섹션 1]
    col_img1, col_txt1 = st.columns([1.1, 1], gap="large")
    with col_img1:
        st.image("https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=1200&auto=format&fit=crop&q=80", use_container_width=True)
    with col_txt1:
        st.write("")
        st.markdown('<div class="lush-tag">01. INNOVATION</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="lush-section-title">
            EXERCISE는 커스텀 DIY 키트,<br>
            맞춤형 에어셀 쿠션과 같은<br>
            기발하고 혁신적인<br>
            운동 솔루션을 선보입니다.
        </div>
        <div class="lush-section-desc">
            정형화된 공장형 기구의 틀을 깨고, 개인의 독특한 손 모양과 체형에 완벽히 피팅되는 
            다양한 '커스터마이징(Customizing)' 키트를 개발하여 헬스 케어 및 웰니스 시장에 혁명을 일으킵니다.
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.divider()
    st.write("")

    # [섹션 2] (운동/상생 컨셉 이미지)
    col_txt2, col_img2 = st.columns([1, 1.1], gap="large")
    with col_txt2:
        st.write("")
        st.markdown('<div class="lush-tag">02. COMMUNITY & ECO</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="lush-section-title">
            나만의 기구를 직접 만들고,<br>
            지역 특산물로 수분을 채우며,<br>
            가치를 함께 공유합니다.
        </div>
        <div class="lush-section-desc">
            지방 소멸 위기 지역의 특산물을 활용한 건강 이온음료부터, 
            구매자들이 직접 제작한 아이디어를 서로 거래하는 C2C 마켓까지. 
            EXERCISE는 지속 가능한 건강 생태계와 지역 상생의 가치를 만들어갑니다.
        </div>
        """, unsafe_allow_html=True)
    with col_img2:
        st.image("https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=1200&auto=format&fit=crop&q=80", use_container_width=True)

    st.write("")
    st.divider()
    st.write("")

    # [섹션 3] (덤벨/운동 기구 이미지)
    col_img3, col_txt3 = st.columns([1.1, 1], gap="large")
    with col_img3:
        st.image("https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=1200&auto=format&fit=crop&q=80", use_container_width=True)
    with col_txt3:
        st.write("")
        st.markdown('<div class="lush-tag">03. PERFECT FITTING</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="lush-section-title">
            표준화된 규격에 몸을 맞추지 마세요.<br>
            당신의 몸에 기구를 맞추세요.
        </div>
        <div class="lush-section-desc">
            사람마다 손가락의 길이, 관절의 유연성, 발바닥 아치의 높이는 모두 다릅니다.<br>
            체온에 맞춰 자율 변경되는 폴리모프 성형 기술을 통해 오직 단 한 사람만을 위한 
            인체공학적 그립감을 제공합니다.
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.divider()
    st.write("")

    if st.button("EXERCISE 전체 상품 라인업 둘러보기 ➔", type="primary", use_container_width=True):
        st.session_state['page'] = 'home'
        st.rerun()

# -------------------------------------------------------------------
# 화면 2: 장바구니 및 결제 페이지
# -------------------------------------------------------------------
elif st.session_state['page'] == 'cart':
    if st.button("⬅ 쇼핑 계속하기"):
        st.session_state['page'] = 'home'
        st.rerun()
        
    st.divider()
    st.markdown("## 🛒 장바구니 및 주문결제")
    
    if not st.session_state['cart']:
        st.info("장바구니가 비어 있습니다. 마음에 드는 상품을 담아보세요!")
    else:
        col_c1, col_c2 = st.columns([3, 2])
        
        with col_c1:
            st.markdown("### 📦 담은 상품 목록")
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
                    if pay_submitted:
                        if name and phone and address:
                            new_order = {
                                "id": len(st.session_state['orders']) + 1,
                                "name": name,
                                "phone": phone,
                                "address": address,
                                "pay_method": pay_method,
                                "items": [item['name'] for item in st.session_state['cart']],
                                "total_price": total_price
                            }
                            st.session_state['orders'].append(new_order)
                            st.success(f"주문이 완료되었습니다!\n[{pay_method}] 로 {total_price:,}원 결제 성공.")
                            st.session_state['cart'] = []
                        else:
                            st.error("배송지 및 주문자 정보를 입력해 주세요.")

# -------------------------------------------------------------------
# 화면 3: 상품 상세 페이지
# -------------------------------------------------------------------
elif st.session_state['page'] == 'detail' and st.session_state['selected_product'] is not None:
    p = st.session_state['selected_product']
    
    if st.button("⬅ 목록으로 돌아가기"):
        st.session_state['page'] = 'home'
        st.session_state['selected_product'] = None
        st.rerun()
        
    st.divider()
    
    col_d1, col_d2 = st.columns([1, 1])
    with col_d1:
        safe_image(p['img'])
    with col_d2:
        st.markdown(f"## {p['name']}")
        st.caption(p.get('comment', ''))
        st.markdown(f"<p class='price-text' style='font-size:26px;'>{p['price']:,} 원</p>", unsafe_allow_html=True)
        st.write("---")
        
        if st.button("🛒 장바구니 담기", type="primary", use_container_width=True):
            add_to_cart(p['name'], p['price'])
            st.rerun()
            
    st.divider()
    st.markdown("### 상품 상세 설명")
    
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        st.markdown("#### 개요")
        st.write(p.get('desc_title', ''))
        
        st.markdown("#### 💡 상품 특징 및 노하우")
        st.write(p.get('desc_detail', ''))
        
        st.markdown("#### 📦 구성 품목")
        st.write(p.get('components', ''))
        
        st.markdown("#### 💥 핵심 가치")
        st.write(p.get('feature', ''))

# -------------------------------------------------------------------
# 화면 4: 관리자 페이지
# -------------------------------------------------------------------
elif st.session_state['page'] == 'admin':
    if st.button("⬅ 메인으로 돌아가기"):
        st.session_state['page'] = 'home'
        st.rerun()
        
    st.divider()
    st.markdown("## ⚙️ EXERCISE 관리자 페이지")
    
    if not st.session_state['admin_authenticated']:
        with st.form("admin_login"):
            pw = st.text_input("관리자 비밀번호를 입력하세요", type="password")
            login_btn = st.form_submit_button("로그인", type="primary")
            if login_btn:
                if pw == "1234":
                    st.session_state['admin_authenticated'] = True
                    st.success("인증되었습니다.")
                    st.rerun()
                else:
                    st.error("비밀번호가 올바르지 않습니다. (비밀번호: 1234)")
    else:
        st.subheader("📊 항목별 구매 통계")
        if not st.session_state['orders']:
            st.info("접수된 주문 내역이 없습니다.")
        else:
            all_items = []
            for order in st.session_state['orders']:
                all_items.extend(order['items'])
            
            df_counts = pd.Series(all_items).value_counts().reset_index()
            df_counts.columns = ['상품명', '판매 수량']
            df_counts = df_counts.set_index('상품명')
            st.bar_chart(df_counts, horizontal=True, color="#03C75A")

# -------------------------------------------------------------------
# 화면 5: 메인 쇼핑몰 홈 화면
# -------------------------------------------------------------------
else:
    tab1, tab2 = st.tabs(["전체 상품", "구매자 창작 마켓"])
    
    # TAB 1: 전체 공식 상품
    with tab1:
        st.markdown("<h3 style='margin-bottom:20px;'>전체 공식 상품</h3>", unsafe_allow_html=True)
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

    # TAB 2: C2C 창작 마켓
    with tab2:
        st.markdown("### 구매자 창작 물품 거래소")
        st.caption("소비자가 직접 만든 완성품을 자유롭게 공유하고 거래하는 공간입니다.")
        
        with st.expander("➕ 내 창작물 직접 판매 등록하기", expanded=False):
            with st.form("c2c_add_form"):
                st.markdown("#### 📝 상품 정보 입력")
                c_title = st.text_input("상품명", placeholder="예: 폴리모프 악력 스트레처")
                c_seller = st.text_input("판매자 닉네임", placeholder="예: 홍길동")
                c_price = st.number_input("판매 가격 (원)", min_value=0, step=1000, value=10000)
                c_img_file = st.file_uploader("🖼️ 대표 이미지 파일 선택", type=["jpg", "jpeg", "png", "webp"])
                c_desc_title = st.text_input("한 줄 개요")
                c_desc_detail = st.text_area("상세설명 및 제작 노하우")
                
                c_submit = st.form_submit_button("등록하기", type="primary", use_container_width=True)
                if c_submit:
                    if c_title and c_seller:
                        selected_img = c_img_file if c_img_file is not None else "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=500&auto=format&fit=crop&q=60"
                        new_c2c = {
                            "id": len(st.session_state['c2c_products']) + 200,
                            "name": f"[C2C] {c_title}",
                            "price": c_price,
                            "comment": f"판매자: {c_seller} | {c_desc_title}",
                            "img": selected_img,
                            "desc_title": c_desc_title,
                            "desc_detail": c_desc_detail,
                            "components": "커스텀 조합 구성",
                            "feature": "독창적 C2C 커스텀 아이템"
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
# 공통 푸터
# -------------------------------------------------------------------
st.markdown("""
<div class="footer-container">
    <div class="footer-title">EXERCISE 스마트스토어</div>
    <p>
        상호명: EXERCISE | 대표: 정예나 | 사업자등록번호: 000-00-00000<br>
        통신판매업신고: 제2026-서울강남-0000호 | 고객센터: 1588-0000 (평일 09:00 ~ 18:00)<br>
        주소: 경기도 고양시 일산동구 위시티4로 112<br>
        Copyright © EXERCISE Inc. All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)
