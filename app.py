import streamlit as st
import os
import pandas as pd

# 페이지 기본 설정
st.set_page_config(
    page_title="EXERCISE 브랜드몰",
    page_icon="💪🏼",
    layout="wide"
)

# 커스텀 CSS (깔끔한 백그라운드 & 러쉬 감성 폰트)
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

    /* 브랜드 타이틀 스타일 */
    .brand-header {
        text-align: center;
        padding: 0px 0 10px 0;
        width: 100%;
    }
    .brand-title {
        font-size: clamp(50px, 8vw, 100px);
        font-weight: 950;
        letter-spacing: -2px;
        line-height: 1.0;
        color: #111111 !important;
        text-transform: uppercase;
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

    /* 러쉬 스타일 타이포그래피 */
    .lush-section-title {
        font-size: clamp(24px, 3vw, 36px);
        font-weight: 900;
        line-height: 1.3;
        letter-spacing: -1.5px;
        color: #111111 !important;
        margin-bottom: 15px;
        word-break: keep-all;
    }
    .lush-section-desc {
        font-size: 15px;
        line-height: 1.7;
        color: #444444 !important;
        word-break: keep-all;
    }
    .lush-tag {
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #03C75A !important;
        margin-bottom: 8px;
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

# 안전한 이미지 처리 함수
def safe_image(img_path):
    if img_path and os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        # 파일이 없을 경우 깨지지 않도록 플레이스홀더 출력
        st.image("https://via.placeholder.com/600x400?text=EXERCISE+IMAGE", use_container_width=True)

# 1. 세션 상태 초기화 (첫 화면을 브랜드 소개 'about'으로 설정)
if 'page' not in st.session_state:
    st.session_state['page'] = 'about'

if 'menu_open' not in st.session_state:
    st.session_state['menu_open'] = False

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

# 원본 C2C 상품 목록
if 'c2c_products' not in st.session_state:
    st.session_state['c2c_products'] = [
        {
            "id": 101,
            "name": "폴리모프 커스텀 지압 악력기", 
            "price": 12000, 
            "comment": "판매자: 정예나 | 손 모양 맞춤 지압 구조",
            "img": "ganadi.jpg",
            "desc_title": "구매자 정예나 님이 제작한 custom 지압 악력기",
            "desc_detail": "EXERCISE DIY 키트의 폴리모프와 지압판 재료를 활용하여 손바닥 곡선에 딱 맞게 제작한 수제 악력기입니다.",
            "components": "폴리모프 커스텀 성형 악력 프레임, 결합형 지압 돌기",
            "feature": "제작자 맞춤형 손 그립감 구현"
        }
    ]

# 원본 공식 키트 데이터
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

def add_to_cart(item_name, item_price):
    st.session_state['cart'].append({"name": item_name, "price": item_price})
    st.session_state['added_item'] = item_name
    st.session_state['show_modal'] = True

# -------------------------------------------------------------------
# 최상단 헤더 (≡ 햄버거 메뉴 토글 버튼 + 브랜드 로고 + 장바구니)
# -------------------------------------------------------------------
col_hdr1, col_hdr2, col_hdr3 = st.columns([1, 4, 1])

with col_hdr1:
    if st.button("≡ 메뉴", key="toggle_menu_btn", use_container_width=True):
        st.session_state['menu_open'] = not st.session_state['menu_open']

with col_hdr2:
    st.markdown("""
    <div class="brand-header">
        <div class="brand-title">EXERCISE</div>
    </div>
    """, unsafe_allow_html=True)

with col_hdr3:
    cart_cnt = len(st.session_state['cart'])
    btn_text = f"🛒 ({cart_cnt})" if cart_cnt > 0 else "🛒 장바구니"
    if st.button(btn_text, type="primary", use_container_width=True):
        st.session_state['page'] = 'cart'
        st.rerun()

# -------------------------------------------------------------------
# 햄버거 메뉴 누르면 열리는 슬라이드/네비게이션 창
# -------------------------------------------------------------------
if st.session_state['menu_open']:
    with st.container(border=True):
        st.markdown("### 🧭 전체 메뉴")
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        
        with m_col1:
            if st.button("🏢 기업/브랜드 소개", use_container_width=True):
                st.session_state['page'] = 'about'
                st.session_state['menu_open'] = False
                st.rerun()
        with m_col2:
            if st.button("🛍️ 스마트스토어", use_container_width=True):
                st.session_state['page'] = 'store'
                st.session_state['menu_open'] = False
                st.rerun()
        with m_col3:
            if st.button("🔐 로그인 / 회원가입", use_container_width=True):
                st.session_state['page'] = 'login'
                st.session_state['menu_open'] = False
                st.rerun()
        with m_col4:
            if st.button("⚙️ 관리자", use_container_width=True):
                st.session_state['page'] = 'admin'
                st.session_state['menu_open'] = False
                st.rerun()

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
# 1. 기업/브랜드 소개 페이지 (접속 시 첫 화면)
# -------------------------------------------------------------------
if st.session_state['page'] == 'about':
    st.markdown("<p style='text-align:center; color:#666; font-size:18px; font-weight:500;'>“운동에는 하나의 정답이 없다”</p>", unsafe_allow_html=True)
    st.divider()

    # [섹션 1]
    col_img1, col_txt1 = st.columns([1, 1], gap="large")
    with col_img1:
        safe_image("ganadi.jpg")
    with col_txt1:
        st.write("")
        st.markdown('<div class="lush-tag">01. INNOVATION</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="lush-section-title">
            EXERCISE는 커스텀 DIY 키트,<br>
            맞춤형 에어셀 쿠션과 같은<br>
            혁신적인 운동 솔루션을 선보입니다.
        </div>
        <div class="lush-section-desc">
            정형화된 공장형 기구의 틀을 깨고, 개인의 독특한 손 모양과 체형에 완벽히 피팅되는 
            다양한 '커스터마이징' 키트를 개발합니다.
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # [섹션 2]
    col_txt2, col_img2 = st.columns([1, 1], gap="large")
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
            지방 소멸 위기 지역 특산물을 활용한 건강 이온음료부터 C2C 마켓까지,
            EXERCISE는 지속 가능한 건강 생태계와 지역 상생의 가치를 만들어갑니다.
        </div>
        """, unsafe_allow_html=True)
    with col_img2:
        safe_image("usagi.jpg")

    st.divider()

    # [섹션 3]
    col_img3, col_txt3 = st.columns([1, 1], gap="large")
    with col_img3:
        safe_image("hachiware.jpg")
    with col_txt3:
        st.write("")
        st.markdown('<div class="lush-tag">03. PERFECT FITTING</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="lush-section-title">
            표준화된 규격에 몸을 맞추지 마세요.<br>
            당신의 몸에 기구를 맞추세요.
        </div>
        <div class="lush-section-desc">
            체온에 맞춰 자율 변경되는 폴리모프 성형 기술을 통해 오직 단 한 사람만을 위한 
            인체공학적 그립감을 제공합니다.
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    if st.button("🛍️ 스마트스토어로 이동하여 상품 보기 ➔", type="primary", use_container_width=True):
        st.session_state['page'] = 'store'
        st.rerun()

# -------------------------------------------------------------------
# 2. 로그인 / 회원가입 페이지
# -------------------------------------------------------------------
elif st.session_state['page'] == 'login':
    st.divider()
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
                        st.success(f"{st.session_state['user']}님, 로그인되었습니다!")
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
                        "img": c_img_file if c_img_file else "ganadi.jpg",
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
# 푸터
# -------------------------------------------------------------------
st.markdown("""
<div class="footer-container">
    <div class="footer-title">EXERCISE 스마트스토어</div>
    <p>
        상호명: EXERCISE | 대표: 정예나 | 사업자등록번호: 000-00-00000<br>
        Copyright © EXERCISE Inc. All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)
