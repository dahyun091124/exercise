import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="EXERCISE 스마트스토어",
    page_icon="🛍️",
    layout="wide"
)

# 스마트스토어 커스텀 CSS (시인성 강화 및 네이버 스타일)
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background-color: #f5f6f8;
    }
    
    /* 텍스트 시인성 보장 */
    h1, h2, h3, h4, h5, h6, p, div, span {
        color: #1e1e1e !important;
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
    
    /* 안내 배너 */
    .info-banner {
        background-color: #ffffff;
        border: 1px solid #03C75A;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 1. 세션 상태 초기화 (장바구니 및 C2C 데이터)
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

if 'c2c_products' not in st.session_state:
    st.session_state['c2c_products'] = [
        {
            "title": "폴리모프 커스텀 지압 악력기", 
            "seller": "정예나", 
            "price": 12000, 
            "desc": "키트 재료로 손 모양에 딱 맞게 제작한 지압 악력기입니다.",
            "img": "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=500&auto=format&fit=crop&q=60"
        }
    ]

# 공식 키트 데이터 (임의 이미지 연결)
kits = [
    {
        "id": 1,
        "name": "DIY 운동 기구 풀키트", 
        "price": 15000, 
        "desc": "라텍스밴드, 지압판, 폴리모프로 자유롭게 내 맞춤형 기구를 제작합니다.",
        "img": "https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": 2,
        "name": "공기방석 에어셀 제작 키트", 
        "price": 18500, 
        "desc": "에어셀 주머니와 스펀지로 자세 교정에 효과적인 커스텀 방석을 만듭니다.",
        "img": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": 3,
        "name": "특산물 이온음료 DIY 키트", 
        "price": 9800, 
        "desc": "소멸위기 지역 대표 특산물 믹스로 나만의 건강 이온음료를 제작합니다.",
        "img": "https://images.unsplash.com/photo-1556881286-fc6915169721?w=500&auto=format&fit=crop&q=60"
    }
]

# 2. 사이드바 - 장바구니 및 결제 창
with st.sidebar:
    st.title("🛒 장바구니 & 결제")
    st.divider()
    
    if not st.session_state['cart']:
        st.info("장바구니가 비어 있습니다.")
    else:
        total_price = 0
        for idx, item in enumerate(st.session_state['cart']):
            col_s1, col_s2 = st.columns([3, 1])
            with col_s1:
                st.write(f"**{item['name']}**")
                st.caption(f"{item['price']:,} 원")
            with col_s2:
                if st.button("삭제", key=f"del_{idx}"):
                    st.session_state['cart'].pop(idx)
                    st.rerun()
            total_price += item['price']
            st.divider()
            
        st.markdown(f"### 총 결제 금액: **{total_price:,} 원**")
        
        # 결제 Form
        with st.form("checkout_form"):
            st.subheader("💳 주문자 정보")
            name = st.text_input("수령인 이름")
            phone = st.text_input("연락처")
            address = st.text_input("배송지 주소")
            pay_method = st.radio("결제 수단", ["N Pay (네이버페이)", "신용/체크카드", "계좌이체"])
            
            pay_submitted = st.form_submit_button("💳 결제하기", type="primary")
            if pay_submitted:
                if name and phone and address:
                    st.success(f"🎉 주문이 완료되었습니다!\n[{pay_method}] 로 {total_price:,}원 결제 완료.")
                    st.session_state['cart'] = []
                else:
                    st.error("배송지 및 주문자 정보를 모두 입력해 주세요.")

# 3. 메인 상단 헤더
st.markdown("""
<div class="store-header">
    <span class="naver-badge">N SMART STORE</span>
    <div class="store-title">EXERCISE 공식 스토어</div>
    <div class="store-sub">“운동에는 하나의 정답이 없다” | 나만의 DIY 운동 기구 & C2C 창작 마켓</div>
</div>
""", unsafe_allow_html=True)

# 4. 탭 구성
tab1, tab2, tab3 = st.tabs(["🏠 스토어 홈", "📦 공식 DIY 키트", "🔄 구매자 창작 마켓 (C2C)"])

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
                st.image(kit["img"], use_container_width=True)
                st.markdown(f"### {kit['name']}")
                st.caption(kit['desc'])
                st.markdown(f"<p class='price-text'>{kit['price']:,} 원</p>", unsafe_allow_html=True)
                if st.button("장바구니 담기", key=f"home_cart_{kit['id']}", type="primary"):
                    st.session_state['cart'].append(kit)
                    st.toast(f"'{kit['name']}'이(가) 장바구니에 담겼습니다!")
                    st.rerun()

# --- TAB 2: 공식 키트 ---
with tab2:
    st.subheader("📦 공식 DIY 키트 전체 보기")
    
    for kit in kits:
        with st.container(border=True):
            col_a, col_b = st.columns([1, 2])
            with col_a:
                st.image(kit["img"], use_container_width=True)
            with col_b:
                st.markdown(f"## {kit['name']}")
                st.write(kit['desc'])
                st.markdown(f"<p class='price-text'>{kit['price']:,} 원</p>", unsafe_allow_html=True)
                
                if st.button("🛒 장바구니에 추가", key=f"kit_cart_{kit['id']}", type="primary"):
                    st.session_state['cart'].append(kit)
                    st.toast(f"'{kit['name']}'이(가) 장바구니에 담겼습니다!")
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
                        "img": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=500&auto=format&fit=crop&q=60"
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
                st.image(item.get("img", "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=500&auto=format&fit=crop&q=60"), use_container_width=True)
                st.caption(f"👤 판매자: {item['seller']}")
                st.markdown(f"### {item['title']}")
                st.write(item['desc'])
                st.markdown(f"<p class='price-text'>{item['price']:,} 원</p>", unsafe_allow_html=True)
                
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    if st.button("🛒 장바구니 담기", key=f"c2c_cart_{idx}"):
                        st.session_state['cart'].append({"name": f"[C2C] {item['title']}", "price": item['price']})
                        st.toast("장바구니에 담겼습니다!")
                        st.rerun()
                with col_c2:
                    st.button("💬 1:1 톡톡 문의", key=f"chat_{idx}")
