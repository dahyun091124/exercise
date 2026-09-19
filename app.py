import streamlit as st
import os
import pandas as pd

# 페이지 기본 설정
st.set_page_config(
    page_title="EXERCISE 스마트스토어",
    page_icon="💪🏼",
    layout="wide"
)

# 스마트스토어 감성 커스텀 CSS
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
    
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] > input,
    textarea {
        background-color: #ffffff !important;
        color: #1e1e1e !important;
        border: 1px solid #cccccc !important;
        border-radius: 6px !important;
    }
    
    /* 파일 업로더 완벽 화이트 톤 */
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

    /* 상단 브랜드 로고 */
    .brand-header {
        text-align: center;
        padding: 10px 0 10px 0;
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
    div[data-testid="stVegaLiteChart"] svg {
        background-color: #ffffff !important;
    }
    div[data-testid="stVegaLiteChart"] text {
        fill: #111111 !important;
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
            "img": "ganadi.jpg",
            "desc_title": "구매자 정예나 님이 제작한 custom 지압 악력기",
            "desc_detail": "EXERCISE DIY 키트의 폴리모프와 지압판 재료를 활용하여 손바닥 곡선에 딱 맞게 제작한 수제 악력기입니다. 손 전체에 골고루 지압 자극을 주어 손목 강화와 스트레칭에 매우 효과적입니다.",
            "components": "폴리모프 커스텀 성형 악력 프레임, 결합형 지압 돌기",
            "feature": "제작자 맞춤형 손 그립감 구현"
        }
    ]

# 기획서 기반 공식 키트 데이터
kits = [
    {
        "id": 1,
        "name": "EXERCISE 커스텀 DIY 운동 키트", 
        "price": 15000, 
        "comment": "라텍스밴드 + 지압판 + 폴리모프 구성 / 나만의 맞춤형 운동 기구",
        "img": "ganadi.jpg",
        "desc_title": "사용자의 신체와 취향에 딱 맞게 제작하는 DIY 키트",
        "desc_detail": "자신의 신체 조건과 운동 목적에 맞게 직접 형태를 변형할 수 있는 커스텀 운동 키트입니다. 체온에 반응해 자유롭게 형태를 잡을 수 있는 폴리모프 소재와 발/손 지압용 지압판, 근력 운동용 라텍스밴드가 포함되어 있어 세상에 하나뿐인 나만의 운동 기구를 만들어 사용할 수 있습니다.",
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
        "desc_detail": "상부 쿠션층 스펀지와 하부 지지층 스펀지, 그리고 공기량을 자유롭게 조절할 수 있는 에어셀 주머니 2개로 구성된 맞춤형 방석 키트입니다. 체중 분산과 자세 교정이 필요한 위치에 에어셀을 직접 배치하여 가장 편안한 착석감을 제공합니다.",
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
        "desc_detail": "지방 소멸 위기 지역의 대표 특산물인 꿀유자 믹스와 송원 오미자 스틱을 활용하여 제작된 이온음료 DIY 키트입니다. 운동 후 빠르게 수분과 전해질을 보충해 주며, 지역 상생의 의미를 담아 건강하고 맛있게 즐기실 수 있습니다.",
        "components": "꿀유자믹스 스틱, 오미자 스틱, 전용 소주잔 세트",
        "feature": "100% 지역 특산물 활용 / 빠른 수분 및 에너지 충전 효과"
    }
]

# 장바구니 담기 처리
def add_to_cart(item_name, item_price):
    st.session_state['cart'].append({"name": item_name, "price": item_price})
    st.session_state['added_item'] = item_name
    st.session_state['show_modal'] = True

# 2. 상단 버튼 레이아웃 (장바구니 전용)
col_top_btns1, col_top_btns2 = st.columns([5, 1])
with col_top_btns2:
    cart_cnt = len(st.session_state['cart'])
    btn_text = f"🛒 {cart_cnt}" if cart_cnt > 0 else "🛒"
    if st.button(btn_text, type="primary", use_container_width=True):
        st.session_state['page'] = 'cart'
        st.rerun()

st.markdown("""
<div class="brand-header">
    <div class="brand-title">EXERCISE</div>
    <p style="color:#666; font-size:16px; margin-top:4px; font-weight:500;">“운동에는 하나의 정답이 없다”</p>
</div>
""", unsafe_allow_html=True)

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
# 화면 1: 장바구니 화면
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
            delete_index = None
            for idx, item in enumerate(st.session_state['cart']):
                with st.container(border=True):
                    mc1, mc2, mc3 = st.columns([3, 2, 1])
                    with mc1:
                        st.markdown(f"**{item['name']}**")
                    with mc2:
                        st.markdown(f"<p class='price-text'>{item['price']:,} 원</p>", unsafe_allow_html=True)
                    with mc3:
                        if st.button("삭제", key=f"big_cart_del_{idx}"):
                            delete_index = idx
                    total_price += item['price']
            
            if delete_index is not None:
                st.session_state['cart'].pop(delete_index)
                st.rerun()
            
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
# 화면 2: 상품 상세 페이지
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
    
    st.markdown("### 상품 상세 설명")
    st.caption("EXERCISE 제작 가이드")
    
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
        
        st.divider()
        safe_image(p['img'])

# -------------------------------------------------------------------
# 화면 3: 관리자 모드
# -------------------------------------------------------------------
elif st.session_state['page'] == 'admin':
    if st.button("⬅ 메인 쇼핑몰로 돌아가기"):
        st.session_state['page'] = 'home'
        st.rerun()
        
    st.divider()
    st.markdown("## ⚙️ EXERCISE 관리자 페이지")
    
    # 관리자 인증 체크
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
                    st.error("비밀번호가 올바르지 않습니다. (기본 비밀번호: 1234)")
    else:
        st.subheader("📊 항목별 구매 통계")
        
        if not st.session_state['orders']:
            st.info("현재 접수된 주문 내역이 없어 통계를 출력할 수 없습니다.")
        else:
            all_items = []
            for order in st.session_state['orders']:
                all_items.extend(order['items'])
            
            df_counts = pd.Series(all_items).value_counts().reset_index()
            df_counts.columns = ['상품명', '판매 수량']
            df_counts = df_counts.set_index('상품명')
            
            st.bar_chart(df_counts, horizontal=True, color="#03C75A")
            
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.metric("총 주문 건수", f"{len(st.session_state['orders'])} 건")
            with col_stat2:
                total_sales = sum([o['total_price'] for o in st.session_state['orders']])
                st.metric("총 누적 매출액", f"{total_sales:,} 원")
                
        st.divider()
        st.subheader("📋 실시간 상세 주문 내역")
        
        if st.session_state['orders']:
            for order in reversed(st.session_state['orders']):
                with st.container(border=True):
                    col_o1, col_o2 = st.columns([2, 3])
                    with col_o1:
                        st.markdown(f"**주문 번호 #NO-{order['id']}**")
                        st.markdown(f"**수령인:** {order['name']}")
                        st.markdown(f"**연락처:** {order['phone']}")
                        st.markdown(f"**배송지:** {order['address']}")
                        st.markdown(f"**결제 방식:** {order['pay_method']}")
                    with col_o2:
                        st.markdown("**주문 상품 목록:**")
                        for item in order['items']:
                            st.write(f"- {item}")
                        st.markdown(f"**총 결제 금액:** <span class='price-text'>{order['total_price']:,} 원</span>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# 화면 4: 메인 쇼핑몰 홈 화면
# -------------------------------------------------------------------
else:
    tab1, tab2 = st.tabs(["전체 상품", "구매자 창작 마켓"])
    
    # --- TAB 1: 전체 상품 ---
    with tab1:
        st.markdown("<h3 style='margin-bottom:20px;'>전체 상품</h3>", unsafe_allow_html=True)
        
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

    # --- TAB 2: C2C 창작 마켓 ---
    with tab2:
        st.markdown("### 구매자 창작 물품 거래소")
        st.caption("키트를 구매한 소비자들이 직접 만든 완성품을 판매하는 공간입니다.")
        
        with st.expander("➕ 내 창작물 직접 판매 등록하기", expanded=False):
            with st.form("c2c_add_form"):
                st.markdown("#### 📝 상품 정보 입력")
                c_title = st.text_input("상품명", placeholder="예: 폴리모프 악력 스트레처")
                c_seller = st.text_input("판매자 닉네임", placeholder="예: 홍길동")
                c_price = st.number_input("판매 가격 (원)", min_value=0, step=1000, value=10000)
                
                c_img_file = st.file_uploader("🖼️ 대표 이미지 파일 선택 (노트북 파일 선택)", type=["jpg", "jpeg", "png", "webp"])
                
                c_desc_title = st.text_input("한 줄 개요", placeholder="예: 키트의 폴리모프 재료를 활용한 스트레칭 기구")
                c_desc_detail = st.text_area("상세설명 및 제작 노하우", placeholder="예: 손 모양에 딱 맞춰 굳힌 맞춤형 악력기입니다.")
                c_components = st.text_input("구성품", placeholder="예: 수제 폴리모프 성형 기구 1개")
                c_feature = st.text_input("핵심 가치", placeholder="예: 맞춤형 그립감 제공")
                
                c_submit = st.form_submit_button("등록하기", type="primary", use_container_width=True)
                
                if c_submit:
                    if c_title and c_seller and c_desc_title:
                        selected_img = c_img_file if c_img_file is not None else "ganadi.jpg"
                        
                        new_c2c = {
                            "id": len(st.session_state['c2c_products']) + 200,
                            "name": f"[C2C] {c_title}" if not c_title.startswith("[C2C]") else c_title,
                            "price": c_price,
                            "comment": f"판매자: {c_seller} | {c_desc_title}",
                            "img": selected_img,
                            "desc_title": c_desc_title,
                            "desc_detail": c_desc_detail,
                            "components": c_components,
                            "feature": c_feature
                        }
                        st.session_state['c2c_products'].append(new_c2c)
                        st.success("성공적으로 등록되었습니다!")
                        st.rerun()
                    else:
                        st.error("상품명, 판매자 닉네임, 한 줄 개요를 반드시 입력해 주세요.")
                        
        st.divider()
        
        c2c_list = st.session_state['c2c_products']
        
        if not c2c_list:
            st.info("현재 등록된 창작 물품이 없습니다. 첫 작품을 올려보세요!")
        else:
            cols_c2c = st.columns(2)
            for idx, c_item in enumerate(c2c_list):
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
# 푸터 영역 (페이지 공통 하단 & 관리자 이동 링크 포함)
# -------------------------------------------------------------------
st.markdown("""
<div class="footer-container">
    <div class="footer-title">EXERCISE 스마트스토어</div>
    <p>
        상호명: EXERCISE | 대표: 정예나 | 사업자등록번호: 012-34-56789<br>
        통신판매업신고: 제2026-서울강남-1234호 | 고객센터: 9876-5432 (평일 09:00 ~ 18:00)<br>
        주소: 경기도 고양시 일산동구 위시티4로 112<br>
        Copyright © EXERCISE Inc. All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)

# 푸터 맨 밑에 깔끔하게 넣은 <관리자> 이동 링크 버튼
if st.button("<관리자>", key="footer_admin_btn"):
    st.session_state['page'] = 'admin'
    st.rerun()
