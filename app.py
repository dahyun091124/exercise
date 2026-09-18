import streamlit as st
import os

# 페이지 기본 설정
st.set_page_config(
    page_title="EXERCISE 스마트스토어",
    page_icon="🛍️",
    layout="wide"
)

# 스마트스토어 커스텀 CSS (다크모드 완벽 방지 및 시인성 강화)
st.markdown("""
<style>
    /* 전체 라이트 모드 고정 */
    .stApp {
        background-color: #f5f6f8 !important;
    }
    
    /* 텍스트 시인성 보장 */
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #1e1e1e !important;
    }
    
    /* 입력창 및 폼 테마 강제 수정 (검은 배경 방지) */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] > input,
    textarea {
        background-color: #ffffff !important;
        color: #1e1e1e !important;
        border: 1px solid #cccccc !important;
        border-radius: 6px !important;
    }
    
    /* 일반 버튼 스타일 수정 (삭제 버튼 등 검은색 방지) */
    .stButton > button {
        background-color: #ffffff !important;
        color: #1e1e1e !important;
        border: 1px solid #d0d0d0 !important;
        border-radius: 6px !important;
    }
    
    .stButton > button:hover {
        border-color: #03C75A !important;
        color: #03C75A !important;
    }
    
    /* 강조 버튼 (NPay, 결제하기 등) */
    .stButton > button[kind="primary"] {
        background-color: #03C75A !important;
        color: #ffffff !important;
        border: none !important;
    }

    /* 스토어 상단 헤더 */
    .store-header {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        border-bottom: 3px solid #03C75A;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .store-title {
        font-size: 26px;
        font-weight: 800;
        color: #1e1e1e !important;
        margin-bottom: 4px;
    }
    .store-sub {
        font-size: 14px;
        color: #666666 !important;
    }
    .naver-badge {
        background-color: #03C75A;
        color: white !important;
        padding: 3px 8px;
        font-size: 11px;
        font-weight: bold;
        border-radius: 4px;
    }
    .price-text {
        font-size: 20px;
        font-weight: bold;
        color: #03C75A !important;
    }
    
    .info-banner {
        background-color: #ffffff;
        border: 1px solid #03C75A;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 이미지 로드 안전 함수
def safe_image(img_path):
    if img_path and os.path.exists(str(img_path)):
        st.image(img_path, use_container_width=True)
    else:
        st.image("https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=500&auto=format&fit=crop&q=60", use_container_width=True)

# 1. 세션 상태 초기화
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = 0

if 'show_modal' not in st.session_state:
    st.session_state['show_modal'] = False

if 'added_item' not in st.session_state:
    st.session_state['added_item'] = ""

if 'c2c_products' not in st.session_state:
    st.session_state['c2c_products'] = [
        {
            "title": "폴리모프 커스텀 지압 악력기", 
            "seller": "정예나", 
            "price": 12000, 
            "desc": "키트 재료로 손 모양에 딱 맞게 제작한 지압 악력기입니다.",
            "img": "ganadi.jpg"
        }
    ]

# 공식 키트 데이터
kits = [
    {
        "id": 1,
        "name": "DIY 운동 기구 풀키트", 
        "price": 15000, 
        "desc": "라텍스밴드, 지압판, 폴리모프로 자유롭게 내 맞춤형 기구를 제작합니다.",
        "img": "ganadi.jpg"
    },
    {
        "id": 2,
        "name": "공기방석 에어셀 제작 키트", 
        "price": 18500, 
        "desc": "에어셀 주머니와 스펀지로 자세 교정에 효과적인 커스텀 방석을 만듭니다.",
        "img": "usagi.jpg"
    },
    {
        "id": 3,
        "name": "특산물 이온음료 DIY 키트", 
        "price": 9800, 
        "desc": "소멸위기 지역 대표 특산물 믹스로 나만의 건강 이온음료를 제작합니다.",
        "img": "hachiware.jpg"
    }
]

# 장바구니 담기 처리 함수
def add_to_cart(item_name, item_price):
    st.session_state['cart'].append({"name": item_name, "price": item_price})
    st.session_state['added_item'] = item_name
    st.session_state['show_modal'] = True

# 2. 메인 상단 헤더
st.markdown("""
<div class="store-header">
    <span class="naver-badge">N SMART STORE</span>
    <div class="store-title">EXERCISE 공식 스토어</div>
    <div class="store-sub">“운동에는 하나의 정답이 없다” | 나만의 DIY 운동 기구 & C2C 창작 마켓</div>
</div>
""", unsafe_allow_html=True)

# 장바구니 담김 안내 상자 (네모 박스 두 개 선택 창)
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
                st.session_state['active_tab'] = 3
                st.rerun()

# 3. 메인 탭 구성
cart_count = len(st.session_state['cart'])
cart_label = f"🛒 장바구니 & 결제 ({cart_count})" if cart_count > 0 else "🛒 장바구니 & 결제"

tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 스토어 홈", 
    "📦 공식 DIY 키트", 
    "🔄 구매자 창작 마켓 (C2C)", 
    cart_label
])

# --- TAB 1: 스토어 홈 ---
with tab1:
    st.markdown("""
    <div class="info-banner">
        <h3>💡 EXERCISE 스토어 안내</h3>
        <p>자신의 신체와 취향에 딱 맞는 DIY 운동 키트를 구매하고, 직접 만든 개성 있는 운동 기구를 다른 사람들과 자유롭게 거래해 보세요!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🔥 베스트 추천 키트")
    cols = st.columns(3)
    for idx, kit in enumerate(kits):
        with cols[idx]:
            with st.container(border=True):
                safe_image(kit["img"])
                st.markdown(f"### {kit['name']}")
                st.caption(kit['desc'])
                st.markdown(f"<p class='price-text'>{kit['price']:,} 원</p>", unsafe_allow_html=True)
                if st.button("장바구니 담기", key=f"home_cart_{kit['id']}", type="primary", use_container_width=True):
                    add_to_cart(kit['name'], kit['price'])
                    st.rerun()

# --- TAB 2: 공식 키트 ---
with tab2:
    st.subheader("📦 공식 DIY 키트 전체 보기")
    
    for kit in kits:
        with st.container(border=True):
            col_a, col_b = st.columns([1, 2])
            with col_a:
                safe_image(kit["img"])
            with col_b:
                st.markdown(f"## {kit['name']}")
                st.write(kit['desc'])
                st.markdown(f"<p class='price-text'>{kit['price']:,} 원</p>", unsafe_allow_html=True)
                
                if st.button("🛒 장바구니에 추가", key=f"kit_cart_{kit['id']}", type="primary"):
                    add_to_cart(kit['name'], kit['price'])
                    st.rerun()

# --- TAB 3: 구매자 창작 마켓 (C2C) ---
with tab3:
    st.subheader("🔄 구매자 창작 물품 거래소")
    st.caption("키트를 구매한 소비자들이 직접 만든 완성품을 판매 및 구매하는 공간입니다.")
    
    with st.expander("➕ 내 창작물 판매 등록하기"):
        with st.form("sell_form"):
            title = st.text_input("작품 이름")
            seller = st.text_input("판매자 닉네임")
            price = st.number_input("판매 가격 (원)", min_value=0, step=1000)
            desc = st.text_area("작품 설명 및 제작 팁")
            submitted = st.form_submit_button("작품 등록하기")
            
            if submitted:
                if title and seller:
                    st.session_state['c2c_products'].append({
                        "title": title, 
                        "seller": seller, 
                        "price": price, 
                        "desc": desc,
                        "img": "ganadi.jpg"
                    })
                    st.success("성공적으로 등록되었습니다!")
                    st.rerun()
                else:
                    st.warning("작품 이름과 판매자 닉네임을 작성해 주세요.")

    st.divider()
    
    cols = st.columns(2)
    for idx, item in enumerate(st.session_state['c2c_products']):
        with cols[idx % 2]:
            with st.container(border=True):
                safe_image(item.get("img", "ganadi.jpg"))
                st.caption(f"👤 판매자: {item['seller']}")
                st.markdown(f"### {item['title']}")
                st.write(item['desc'])
                st.markdown(f"<p class='price-text'>{item['price']:,} 원</p>", unsafe_allow_html=True)
                
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    if st.button("🛒 장바구니 담기", key=f"c2c_cart_{idx}", use_container_width=True):
                        add_to_cart(f"[C2C] {item['title']}", item['price'])
                        st.rerun()
                with col_c2:
                    st.button("💬 1:1 톡톡 문의", key=f"chat_{idx}", use_container_width=True)

# --- TAB 4: 장바구니 & 주문 결제 ---
with tab4:
    st.subheader("🛒 장바구니 및 주문/결제")
    
    if not st.session_state['cart']:
        st.info("장바구니가 비어 있습니다. 원하는 키트를 장바구니에 담아보세요!")
    else:
        col_cart, col_pay = st.columns([3, 2])
        
        with col_cart:
            st.markdown("### 📦 담은 상품 목록")
            total_price = 0
            for idx, item in enumerate(st.session_state['cart']):
                with st.container(border=True):
                    c1, c2, c3 = st.columns([3, 2, 1])
                    with c1:
                        st.markdown(f"**{item['name']}**")
                    with c2:
                        st.markdown(f"<p class='price-text'>{item['price']:,} 원</p>", unsafe_allow_html=True)
                    with c3:
                        if st.button("삭제", key=f"tab_del_{idx}"):
                            st.session_state['cart'].pop(idx)
                            st.rerun()
                    total_price += item['price']
            
            st.markdown(f"## 총 주문 금액: **{total_price:,} 원**")

        with col_pay:
            with st.container(border=True):
                st.markdown("### 💳 주문 및 결제 정보")
                with st.form("checkout_tab_form"):
                    name = st.text_input("수령인 이름")
                    phone = st.text_input("연락처")
                    address = st.text_input("배송지 주소")
                    pay_method = st.radio("결제 수단", ["N Pay (네이버페이)", "신용/체크카드", "계좌이체"])
                    
                    pay_submitted = st.form_submit_button("💳 결제하기", type="primary", use_container_width=True)
                    if pay_submitted:
                        if name and phone and address:
                            st.balloons()
                            st.success(f"🎉 주문이 완료되었습니다!\n[{pay_method}] 로 {total_price:,}원 결제 완료.")
                            st.session_state['cart'] = []
                        else:
                            st.error("배송지 및 주문자 정보를 모두 입력해 주세요.")
