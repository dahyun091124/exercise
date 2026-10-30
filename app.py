        st.write("---")

        if st.button("🛒 장바구니 담기", type="primary", use_container_width=True):
            add_to_cart(p['name'], p['price'])

    st.write("<br><br>", unsafe_allow_html=True)
    st.divider()

    # 상품 상세 설명 구획
    st.markdown("### 상품 상세 설명")

    # [0.05, 0.95] 비율로 살짝 오른쪽 들여쓰기 효과 유지
    indent_space, content_col = st.columns([0.05, 0.95])
    with content_col:
        st.markdown("#### 📌 개요")
        st.write(p.get('desc_title', ''))

        st.markdown("#### 💡 상품 특징")
        st.write(p.get('desc_detail', ''))

        st.markdown("#### 📦 구성 품목")
        st.write(p.get('components', ''))

        st.markdown("#### 💥 핵심 가치")
        st.write(p.get('feature', ''))

# -------------------------------------------------------------------
# 6. 관리자 페이지
# -------------------------------------------------------------------
elif st.session_state['page'] == 'admin':
    st.button("⬅ 메인으로 돌아가기", on_click=set_page, args=('about',))

    st.divider()
    st.markdown("## 관리자 페이지")
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

            max_val = int(df_counts['수량'].max()) if not df_counts.empty else 1

            chart = alt.Chart(df_counts).mark_bar(color='#03C75A').encode(
                x=alt.X('수량:Q', title='판매 수량', axis=alt.Axis(values=list(range(0, max_val + 2)), format='d')),
                y=alt.Y('상품명:N', title='상품명', sort='-x'),
                tooltip=['상품명', '수량']
            ).properties(
                height=max(150, len(df_counts) * 40)
            )

            st.altair_chart(chart, use_container_width=True)

            st.divider()
            st.subheader("📋 전체 주문 정보")

            for o in st.session_state['orders']:
                st.write("---")
                col_left, col_right = st.columns([1, 1])

                with col_left:
                    st.markdown(f"**주문번호:** ORD-{o['id']:04d}")
                    st.markdown(f"**이름:** {o.get('name', '-')}")
                    st.markdown(f"**연락처:** {o.get('phone', '-')}")
                    st.markdown(f"**주소:** {o.get('address', '-')}")

                with col_right:
                    # 1. 주문 내역 처리 (2개 이상일 경우 세로 정렬)
                    order_items = o.get('items', [])
                    if len(order_items) >= 2:
                        items_formatted = "<br>".join([f"&nbsp;&nbsp;{i+1}. {item}" for i, item in enumerate(order_items)])
                        items_html = f"<div style='margin-top: 4px;'>{items_formatted}</div>"
                    elif len(order_items) == 1:
                        items_html = f" {order_items[0]}"
                    else:
                        items_html = " -"

                    # 2. 주문 내역 및 결제 금액 글씨 크기 확대 출력
                    st.markdown(
                        f"<div style='font-size: 18px; font-weight: bold; margin-bottom: 8px; line-height: 1.5;'>"
                        f"주문 내역:{items_html}"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"<div style='font-size: 18px; font-weight: bold; color: #03C75A;'>"
                        f"결제 금액: {o.get('total_price', 0):,} 원"
                        f"</div>",
                        unsafe_allow_html=True
                    )
            st.write("---")
        else:
            st.info("등록된 주문 내역이 없습니다.")

# -------------------------------------------------------------------
# 푸터
# -------------------------------------------------------------------
st.markdown("""
<div class="footer-container">
    <div style="font-weight: bold; color: #111111; font-size: 14px; margin-bottom: 8px;">EXERCISE 공식 사이트</div>
    <p>
        상호명: EXERCISE | 대표: 정예나 | 사업자등록번호: 000-00-00000<br>
        Copyright © EXERCISE Inc. All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)
