import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="EXERCISE 스마트스토어",
    page_icon="🛍️",
    layout="wide"
)

# 스마트스토어 커스텀 CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f5f6f8;
    }
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
        color: #1e1e1e;
        margin-bottom: 4px;
    }
    .store-sub {
        font-size: 14px;
        color: #666;
    }
    .naver-badge {
        background-color: #03C75A;
        color: white;
        padding: 3px 8px;
        font-size: 11px;
        font-weight: bold;
        border-radius: 4px;
    }
    .price-text {
        font-size: 18px;
        font-weight: bold;
        color: #03C75A;
    }
</style>
""", unsafe_allow_html=True)

# 1. 헤더
st.markdown("""
<div class="store-header">
    <span class="naver-badge">N SMART STORE</span>
    <div class="store-title">EXERCISE 공식 스토어</div>
    <div class="store-sub">“운동에는 하나의 정답이 없다” | 나만의 DIY 운동 기구 & C2C 창작 마켓</div>
</div>
""", unsafe_allow_html=True)

# 2. 세션 상태 안전하게 초기화
if 'c2c_products' not in st.session_state:
    st.session_state['c2c_products'] = [
        {"title": "폴리모프 커스텀 지압 악력기", "seller": "정예나", "price": 12000, "desc": "키트 재료로 손 모양에 딱 맞게 제작한 지압 악력기입니다."}
    ]

# 3. 탭 구성
tab1, tab2, tab3 = st.tabs(["🏠 스토어 홈", "📦 공식 DIY 키트", "🔄 구매자 창작 마켓 (C2C)"])

# --- TAB 1: 스토어 홈 ---
with tab1:
    st.image("https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=1000&q=80", use_container_width=True, caption="나만의 맞춤형 운동 기구를 직접 만들어보세요!")
    
    st.subheader("🔥 베스트 추천 키트")
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("**[EXERCISE] 풀세트 DIY 운동 키트**")
            st.caption("라텍스밴드 + 지압판 + 폴리모프 구성")
            st.markdown("<p class='price-text'>15,000 원</p>", unsafe_allow_html=True)
            st.button("N Pay 구매하기", key="btn1", type="primary")
            
    with col2:
        with st.container(border=True):
            st.markdown("**[EXERCISE] 공기방석 에어셀 키트**")
            st.caption("맞춤형 자세 교정 공기방석 제작 키트")
            st.markdown("<p class='price-text'>18,500 원</p>", unsafe_allow_html=True)
            st.button("N Pay 구매하기", key="btn2", type="primary")

# --- TAB 2: 공식 키트 ---
with tab2:
    st.subheader("📦 공식 DIY 키트 목록")
    
    kits = [
        {"name": "DIY 운동 기구 풀키트", "price": "15,000원", "desc": "라텍스밴드, 지압판, 폴리모프로 자유롭게 제작"},
        {"name": "공기방석 제작 키트", "price": "18,500원", "desc": "에어셀 주머니와 스펀지로 만드는 커스텀 방석"},
        {"name": "특산물 이온음료 DIY 키트", "price": "9,800원", "desc": "소멸위기 지역 특산물 믹스로 만드는 나만의 이온음료"}
    ]
    
    for idx, kit in enumerate(kits):
        with st.container(border=True):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"### {kit['name']}")
                st.write(kit['desc'])
                st.markdown(f"<p class='price-text'>{kit['price']}</p>", unsafe_allow_html=True)
            with col_b:
                st.write("")
                st.button("장바구니", key=f"cart_{idx}")
                st.button("바로구매", key=f"buy_{idx}", type="primary")

# --- TAB 3: C2C 마켓 ---
with tab3:
    st.subheader("🔄 구매자 창작 물품 거래소")
    st.caption("키트를 구매한 다른 사용자들이 직접 만든 완제품을 거래하는 공간입니다.")
    
    with st.expander("➕ 내 창작물 판매 등록하기"):
        with st.form("sell_form"):
            title = st.text_input("작품 이름")
            seller = st.text_input("판매자 닉네임")
            price = st.number_input("판매 가격 (원)", min_value=0, step=1000)
            desc = st.text_area("작품 및 제작 노하우 설명")
            submitted = st.form_submit_button("스토어에 등록하기")
            
            if submitted:
                if title and seller:
                    st.session_state['c2c_products'].append({
                        "title": title, "seller": seller, "price": price, "desc": desc
                    })
                    st.success("성공적으로 등록되었습니다!")
                else:
                    st.warning("작품 이름과 판매자 닉네임을 입력해 주세요.")

    st.divider()
    
    cols = st.columns(2)
    for idx, item in enumerate(st.session_state['c2c_products']):
        with cols[idx % 2]:
            with st.container(border=True):
                st.caption(f"👤 판매자: {item['seller']}")
                st.markdown(f"#### {item['title']}")
                st.write(item['desc'])
                st.markdown(f"<p class='price-text'>{item['price']:,} 원</p>", unsafe_allow_html=True)
                st.button("💬 판매자와 1:1 톡톡 문의", key=f"chat_{idx}")
