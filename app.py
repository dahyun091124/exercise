import streamlit as st
import os

# 페이지 기본 설정
st.set_page_config(
    page_title="EXERCISE 스마트스토어",
    page_icon="🛍️",
    layout="wide"
)

# 스마트스토어 감성 커스텀 CSS
st.markdown("""
<style>
    /* 전체 배경 화이트 고정 */
    .stApp {
        background-color: #ffffff !important;
    }
    
    /* 폰트 및 시인성 보장 */
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #111111 !important;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
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
    
    /* 상단 브랜드 로고 */
    .brand-header {
        text-align: center;
        padding: 10px 0;
    }
    .brand-title {
        font-size: 32px;
        font-weight: 900;
        letter-spacing: -0.5px;
    }
    
    /* 쿠폰 혜택 배너 */
    .coupon-banner {
        background-color: #f7f8f9;
        border: 1px solid #e1e4e6;
        border-radius: 8px;
        padding: 14px;
        text-align: center;
        font-size: 14px;
        margin-bottom: 25px;
    }
    .coupon-badge {
        background-color: #03C75A;
        color: white !important;
        padding: 4px 8px;
        font-size: 12px;
        font-weight: bold;
        border-radius: 4px;
        margin-left: 8px;
    }

    /* 상품 베스트 순위 뱃지 */
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
    
    /* 가격 텍스트 */
    .price-text {
        font-size: 20px;
        font-weight: 800;
        color: #03C75A !important;
    }
    
    /* 감성 상세페이지 스타일 */
    .detail-section {
        text-align: center;
        padding: 30px 0;
    }
    .detail-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 4px;
        letter-spacing: 1px;
    }
    .detail-sub {
        font-size: 15px;
        color: #666666 !important;
        margin-bottom: 24px;
    }
    
    /* 버튼 스타일 */
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

if 'page' not in st.session_state:
    st.session_state['page'] = 'home' # 'home', 'detail', 'cart'

if 'show_modal' not in st.session_state:
    st.session_state['show_modal'] = False

if 'added_item' not in st.session_state:
    st.session_state['added_item'] = ""

if 'selected_product' not in st.session_state:
    st.session_state['selected_product'] = None

# 키트 데이터 세팅
kits = [
    {
        "id": 1,
        "name": "EXERCISE 커스텀 운동 기구 풀키트", 
        "price": 15000, 
        "comment": "라텍스밴드 + 지압판 + 폴리모프 조합 / 나만의 맞춤 기구",
        "img": "ganadi.jpg",
        "color": "black, mint, beige",
        "size": "free size",
        "fabric": "latex, polymorph, rubber",
        "model_size": "yena / 165cm / top 55 / bottom 26\n(손 모양에 맞춰 제작 가능한 커스텀 구조)"
    },
    {
        "id": 2,
        "name": "공기방석 에어셀 자세교정 키트", 
        "price": 18500, 
        "comment": "에어셀 주머니 + 고밀도 스펀지 / 척추 균형 서포트",
        "img": "usagi.jpg",
        "color": "ivory, gray",
        "size": "40cm x 40cm (표준 방석 사이즈)",
        "fabric": "air-cell urethane, sponge, mesh cover",
        "model_size": "dahyun / 158cm / top 44 / bottom 25\n(장시간 착석 시 골반 불균형 완화)"
    },
    {
        "id": 3,
        "name": "소멸위기 지역 특산물 이온음료 DIY 키트", 
        "price": 9800, 
        "comment": "지역 특산 믹스 / 수분 보충 & 유기농 과즙",
        "img": "hachiware.jpg",
        "color": "natural citrus, berry",
        "size": "10포 / 15포 세트 선택 가능",
        "fabric": "organic local extract powder",
        "model_size": "exercise team / 매일 운동 후 섭취 추천"
    }
]

# 장바구니 담기 처리
def add_to_cart(item_name, item_price):
    st.session_state['cart'].append({"name": item_name, "price": item_price})
    st.session_state['added_item'] = item_name
    st.session_state['show_modal'] = True

# 2. 최상단 우측 장바구니 이모지 버튼 & 로고
col_head1, col_head2 = st.columns([6, 1])

with col_head1:
    st.markdown("""
    <div class="brand-header">
        <div class="brand-title">EXERCISE</div>
        <p style="color:#666; font-size:14px; margin-top:2px;">“운동에는 하나의 정답이 없다”</p>
    </div>
    """, unsafe_allow_html=True)

with col_head2:
    st.write("") # 여백 조절
    cart_cnt = len(st.session_state['cart'])
    btn_text = f"🛒 {cart_cnt}" if cart_cnt > 0 else "🛒"
    if st.button(btn_text, type="primary", use_container_width=True):
        st.session_state['page'] = 'cart'
        st.rerun()

# 혜택 배너
st.markdown("""
<div class="coupon-banner">
    <b>EXERCISE 고객님을 위한 혜택</b> &nbsp;|&nbsp; 첫 구매 고객 전 품목 <b>3,000원 장바구니 할인 쿠폰</b> 제공 <span class="coupon-badge">COUPON ⬇</span>
</div>
""", unsafe_allow_html=True)

# 장바구니 담김 알림 상자 (네모 박스 두 개)
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
# 화면 1: 장바구니 화면 (우측 상단 🛒 클릭 시 전환되는 큰 화면)
# -------------------------------------------------------------------
if st.session_state['page'] == 'cart':
    if st.button("⬅ 메인 쇼핑몰로 돌아가기"):
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
            for idx, item in enumerate(st.session_state['cart']):
                with st.container(border=True):
                    mc1, mc2, mc3 = st.columns([3, 2, 1])
                    with mc1:
                        st.markdown(f"**{item['name']}**")
                    with mc2:
                        st.markdown(f"<p class='price-text'>{item['price']:,} 원</p>", unsafe_allow_html=True)
                    with mc3:
                        if st.button("삭제", key=f"big_cart_del_{idx}"):
                            st.session_state['cart'].pop(idx)
                            st.rerun()
                    total_price += item['price']
            
            st.markdown(f"### 총 결제 예정 금액: **{total_price:,} 원**")

        with col_c2:
            with st.container(border=True):
                st.markdown("### 💳 주문 정보 입력")
                with st.form("checkout_big_form"):
                    name = st.text_input("수령인 이름")
                    phone = st.text_input("연락처")
                    address = st.text_input("배송지 주소")
                    pay_method = st.radio("결제 수단", ["N Pay (네이버페이)", "신용/체크카드", "계좌이체"])
                    
                    pay_submitted = st.form_submit_button("💳 결제하기", type="primary", use_container_width=True)
                    if pay_submitted:
                        if name and phone and address:
                            st.balloons()
                            st.success(f"🎉 주문이 완료되었습니다!\n[{pay_method}] 로 {total_price:,}원 결제 성공.")
                            st.session_state['cart'] = []
                        else:
                            st.error("배송지 및 주문자 정보를 입력해 주세요.")

# -------------------------------------------------------------------
# 화면 2: 상품 상세 페이지 (상품 클릭 시 이동)
# -------------------------------------------------------------------
elif st.session_state['page'] == 'detail' and st.session_state['selected_product'] is not None:
    p = st.session_state['selected_product']
    
    if st.button("⬅ 전체 상품 목록으로 돌아가기"):
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
    
    # 상세페이지 정보
    st.markdown("""
    <div style="text-align: center; margin-top: 40px;">
        <h2 style="font-weight: 800;">PRODUCT DETAIL</h2>
        <p style="color:#888;">EXERCISE 제작 가이드 및 사양 정보</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        st.markdown(f"""
        <div class="detail-section">
            <div class="detail-title">color</div>
            <div class="detail-sub">{p.get('color', 'N/A')}</div>
            
            <div class="detail-title">size</div>
            <div class="detail-sub">{p.get('size', 'FREE')}</div>
            
            <div class="detail-title">fabric</div>
            <div class="detail-sub">{p.get('fabric', 'N/A')}</div>
            
            <div class="detail-title">model size / note</div>
            <div class="detail-sub" style="white-space: pre-line;">{p.get('model_size', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        safe_image(p['img'])

# -------------------------------------------------------------------
# 화면 3: 메인 쇼핑몰 홈 화면
# -------------------------------------------------------------------
else:
    tab1, tab2 = st.tabs(["🔥 베스트 상품", "🔄 구매자 창작 마켓 (C2C)"])
    
    # --- TAB 1: 베스트 상품 ---
    with tab1:
        st.markdown("<h3 style='margin-bottom:20px;'>베스트 상품</h3>", unsafe_allow_html=True)
        
        cols = st.columns(3)
        for idx, kit in enumerate(kits):
            with cols[idx]:
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

    # --- TAB 2: C2C 창작 마켓 ---
    with tab2:
        st.markdown("### 🔄 구매자 창작 물품 거래소")
        st.caption("키트를 구매한 소비자들이 직접 만든 완성품을 판매하는 공간입니다.")
        
        cols = st.columns(2)
        c2c_item = {
            "id": 99,
            "name": "[C2C] 폴리모프 커스텀 지압 악력기", 
            "price": 12000, 
            "comment": "판매자: 정예나 | 손 모양 맞춤 지압 구조",
            "img": "ganadi.jpg",
            "color": "custom white",
            "size": "맞춤형 사이즈",
            "fabric": "polymorph thermo-plastic",
            "model_size": "정예나 제작자 직용 모델\n손 악력 및 지압 강화에 최적화된 형태"
        }
        
        with cols[0]:
            with st.container(border=True):
                safe_image(c2c_item['img'])
                st.markdown(f"**{c2c_item['name']}**")
                st.caption(c2c_item['comment'])
                st.markdown(f"<p class='price-text'>{c2c_item['price']:,} 원</p>", unsafe_allow_html=True)
                
                col_cb1, col_cb2 = st.columns(2)
                with col_cb1:
                    if st.button("상세보기", key="c2c_detail", use_container_width=True):
                        st.session_state['selected_product'] = c2c_item
                        st.session_state['page'] = 'detail'
                        st.rerun()
                with col_cb2:
                    if st.button("담기", key="c2c_cart", type="primary", use_container_width=True):
                        add_to_cart(c2c_item['name'], c2c_item['price'])
                        st.rerun()
