import streamlit as st
import pandas as pd

# =========================================================
# CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================================================
# CSS GIAO DIỆN
# =========================================================
st.markdown(
    """
    <style>
    .main-title {
        font-size: 36px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }

    .sub-title {
        text-align: center;
        color: #666;
        margin-bottom: 25px;
    }

    .result-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #f7f9fc;
        border: 1px solid #e1e5eb;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================
def format_money(value):
    return f"{value:,.0f} VNĐ"


# =========================================================
# HÀM TÍNH LÃI
# =========================================================
def tinh_lai(
    tien_gui,
    ky_han_thang,
    lai_suat_nam,
    loai_lai,
    hinh_thuc_nhan_lai
):
    """
    Parameters
    ----------
    tien_gui : float
        Số tiền gửi ban đầu.

    ky_han_thang : int
        Kỳ hạn gửi tính theo tháng.

    lai_suat_nam : float
        Lãi suất %/năm.

    loai_lai : str
        "Lãi đơn" hoặc "Lãi kép".

    hinh_thuc_nhan_lai : str
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ".

    Returns
    -------
    dict
        Kết quả tính toán.
    """

    # Chuyển lãi suất từ % về số thập phân
    lai_suat_nam_decimal = lai_suat_nam / 100

    # -----------------------------------------------------
    # XÁC ĐỊNH SỐ THÁNG CỦA MỘT KỲ
    # -----------------------------------------------------
    if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":
        so_thang_moi_ky = 1

    elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":
        so_thang_moi_ky = 3

    else:
        so_thang_moi_ky = ky_han_thang

    # -----------------------------------------------------
    # TRƯỜNG HỢP LÃNH LÃI CUỐI KỲ
    # -----------------------------------------------------
    if hinh_thuc_nhan_lai == "Lãnh lãi cuối kỳ":

        # -------------------------------
        # LÃI ĐƠN
        # -------------------------------
        if loai_lai == "Lãi đơn":

            tong_lai = (
                tien_gui
                * lai_suat_nam_decimal
                * ky_han_thang
                / 12
            )

            tong_tien = tien_gui + tong_lai

            bang_chi_tiet = pd.DataFrame([
                {
                    "Kỳ": "Cuối kỳ",
                    "Tiền gốc": tien_gui,
                    "Tiền lãi": tong_lai,
                    "Tổng gốc + lãi": tong_tien
                }
            ])

        # -------------------------------
        # LÃI KÉP
        # -------------------------------
        else:

            # Ghép lãi theo tháng
            lai_suat_thang = lai_suat_nam_decimal / 12

            tong_tien = tien_gui * (
                1 + lai_suat_thang
            ) ** ky_han_thang

            tong_lai = tong_tien - tien_gui

            bang_chi_tiet = pd.DataFrame([
                {
                    "Kỳ": "Cuối kỳ",
                    "Tiền gốc": tien_gui,
                    "Tiền lãi": tong_lai,
                    "Tổng gốc + lãi": tong_tien
                }
            ])

        return {
            "lai_dinh_ky": tong_lai,
            "tong_lai": tong_lai,
            "tong_tien": tong_tien,
            "bang_chi_tiet": bang_chi_tiet
        }

    # =====================================================
    # LÃI THEO THÁNG / QUÝ
    # =====================================================

    # Số kỳ đầy đủ
    so_ky = ky_han_thang // so_thang_moi_ky

    # Số tháng còn dư
    thang_le = ky_han_thang % so_thang_moi_ky

    # Lãi suất của một kỳ
    lai_suat_ky = (
        lai_suat_nam_decimal
        * so_thang_moi_ky
        / 12
    )

    # Vốn hiện tại
    von_hien_tai = tien_gui

    tong_lai = 0

    chi_tiet = []

    # =====================================================
    # TÍNH TỪNG KỲ
    # =====================================================
    for ky in range(1, so_ky + 1):

        von_dau_ky = von_hien_tai

        if loai_lai == "Lãi đơn":

            # Lãi đơn: luôn tính trên gốc ban đầu
            tien_lai = tien_gui * lai_suat_ky

            von_cuoi_ky = von_dau_ky

        else:

            # Lãi kép: lãi nhập vào vốn
            tien_lai = von_hien_tai * lai_suat_ky

            von_hien_tai = von_hien_tai + tien_lai

            von_cuoi_ky = von_hien_tai

        tong_lai += tien_lai

        chi_tiet.append(
            {
                "Kỳ": ky,
                "Thời gian": f"Đến tháng {ky * so_thang_moi_ky}",
                "Tiền gốc đầu kỳ": von_dau_ky,
                "Tiền lãi": tien_lai,
                "Tiền cuối kỳ": von_cuoi_ky
            }
        )

    # =====================================================
    # XỬ LÝ PHẦN THÁNG LẺ
    # =====================================================
    if thang_le > 0:

        lai_suat_thang_le = (
            lai_suat_nam_decimal
            * thang_le
            / 12
        )

        von_dau_ky = von_hien_tai

        if loai_lai == "Lãi đơn":

            tien_lai_le = (
                tien_gui
                * lai_suat_thang_le
            )

            von_cuoi_ky = von_dau_ky

        else:

            tien_lai_le = (
                von_hien_tai
                * lai_suat_thang_le
            )

            von_hien_tai += tien_lai_le

            von_cuoi_ky = von_hien_tai

        tong_lai += tien_lai_le

        chi_tiet.append(
            {
                "Kỳ": "Kỳ lẻ",
                "Thời gian": f"Đến tháng {ky_han_thang}",
                "Tiền gốc đầu kỳ": von_dau_ky,
                "Tiền lãi": tien_lai_le,
                "Tiền cuối kỳ": von_cuoi_ky
            }
        )

    # =====================================================
    # TÍNH TỔNG CUỐI CÙNG
    # =====================================================
    if loai_lai == "Lãi đơn":
        tong_tien = tien_gui + tong_lai
    else:
        tong_tien = von_hien_tai

    # Tiền lãi định kỳ
    if len(chi_tiet) > 0:
        lai_dinh_ky = tong_lai / len(chi_tiet)
    else:
        lai_dinh_ky = 0

    bang_chi_tiet = pd.DataFrame(chi_tiet)

    return {
        "lai_dinh_ky": lai_dinh_ky,
        "tong_lai": tong_lai,
        "tong_tien": tong_tien,
        "bang_chi_tiet": bang_chi_tiet
    }


# =========================================================
# TIÊU ĐỀ
# =========================================================
st.markdown(
    '<div class="main-title">💰 TÍNH LÃI TIỀN GỬI TIẾT KIỆM</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Tính lãi đơn và lãi kép theo tháng, quý hoặc cuối kỳ'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# NHẬP DỮ LIỆU
# =========================================================
st.header("📋 Thông tin khoản tiền gửi")

col1, col2 = st.columns(2)

with col1:

    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=360,
        value=12,
        step=1
    )

    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1,
        format="%.2f"
    )

with col2:

    loai_lai = st.selectbox(
        "Phương thức tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

    hinh_thuc_nhan_lai = st.selectbox(
        "Hình thức nhận lãi",
        [
            "Lãnh lãi theo tháng",
            "Lãnh lãi theo quý",
            "Lãnh lãi cuối kỳ"
        ]
    )


# =========================================================
# THÔNG TIN QUY ƯỚC
# =========================================================
with st.expander("ℹ️ Quy ước tính toán"):

    st.write(
        """
        - Lãi suất được nhập theo **%/năm**.
        - **Lãi đơn:** tiền lãi luôn tính trên số tiền gốc ban đầu.
        - **Lãi kép:** tiền lãi được cộng vào vốn sau mỗi kỳ tính lãi.
        - Lãnh lãi tháng: 1 kỳ = 1 tháng.
        - Lãnh lãi quý: 1 kỳ = 3 tháng.
        - Lãnh lãi cuối kỳ: toàn bộ tiền lãi được tính đến ngày đáo hạn.
        """
    )


# =========================================================
# NÚT TÍNH
# =========================================================
st.divider()

tinh_button = st.button(
    "🧮 TÍNH TIỀN LÃI",
    type="primary",
    use_container_width=True
)


# =========================================================
# XỬ LÝ KẾT QUẢ
# =========================================================
if tinh_button:

    if tien_gui <= 0:
        st.error("❌ Số tiền gửi phải lớn hơn 0.")
        st.stop()

    if ky_han <= 0:
        st.error("❌ Kỳ hạn phải lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("❌ Lãi suất không được âm.")
        st.stop()

    ket_qua = tinh_lai(
        tien_gui=tien_gui,
        ky_han_thang=ky_han,
        lai_suat_nam=lai_suat,
        loai_lai=loai_lai,
        hinh_thuc_nhan_lai=hinh_thuc_nhan_lai
    )

    lai_dinh_ky = ket_qua["lai_dinh_ky"]
    tong_lai = ket_qua["tong_lai"]
    tong_tien = ket_qua["tong_tien"]
    bang_chi_tiet = ket_qua["bang_chi_tiet"]


    # =====================================================
    # KẾT QUẢ CHÍNH
    # =====================================================
    st.header("📊 Kết quả")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            format_money(lai_dinh_ky)
        )

    with c2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(tong_lai)
        )

    with c3:
        st.metric(
            "💰 Tổng gốc + lãi",
            format_money(tong_tien)
        )


    # =====================================================
    # THÔNG TIN KHOẢN GỬI
    # =====================================================
    st.subheader("📝 Thông tin khoản gửi")

    thong_tin = pd.DataFrame({
        "Thông tin": [
            "Số tiền gửi",
            "Kỳ hạn",
            "Lãi suất",
            "Phương thức tính lãi",
            "Hình thức nhận lãi"
        ],
        "Giá trị": [
            format_money(tien_gui),
            f"{ky_han} tháng",
            f"{lai_suat:.2f}%/năm",
            loai_lai,
            hinh_thuc_nhan_lai
        ]
    })

    st.table(thong_tin)


    # =====================================================
    # CHI TIẾT TỪNG KỲ
    # =====================================================
    st.subheader("📋 Chi tiết tiền lãi từng kỳ")

    bang_hien_thi = bang_chi_tiet.copy()

    bang_hien_thi["Tiền gốc đầu kỳ"] = (
        bang_hien_thi["Tiền gốc đầu kỳ"]
        .apply(format_money)
    )

    bang_hien_thi["Tiền lãi"] = (
        bang_hien_thi["Tiền lãi"]
        .apply(format_money)
    )

    bang_hien_thi["Tiền cuối kỳ"] = (
        bang_hien_thi["Tiền cuối kỳ"]
        .apply(format_money)
    )

    st.dataframe(
        bang_hien_thi,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # CÔNG THỨC
    # =====================================================
    with st.expander("📐 Xem công thức tính"):

        if loai_lai == "Lãi đơn":

            st.markdown("### Lãi đơn")

            st.latex(
                r"""
                Lãi = Tiền\ gốc \times Lãi\ suất\ năm
                \times \frac{Số\ tháng}{12}
                """
            )

            st.write(
                "Tiền lãi không được cộng vào vốn để tạo ra lãi ở kỳ sau."
            )

        else:

            st.markdown("### Lãi kép")

            st.latex(
                r"""
                A = P(1+r)^n
                """
            )

            st.write(
                """
                Trong đó:
                - P: số tiền gốc ban đầu
                - r: lãi suất của một kỳ
                - n: số kỳ tính lãi
                - A: tổng tiền gốc và lãi
                """
            )


# =========================================================
# FOOTER
# =========================================================
st.divider()

st.caption(
    "💡 Công cụ mang tính tham khảo. "
    "Lãi suất và phương pháp tính thực tế có thể khác tùy ngân hàng "
    "và sản phẩm tiền gửi."
)
