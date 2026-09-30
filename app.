```python
import streamlit as st
import math

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ"


# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 Tính lãi tiền gửi tiết kiệm")

st.write(
    "Ứng dụng tính toán tiền lãi theo **lãi đơn** hoặc **lãi kép**, "
    "với các hình thức nhận lãi theo tháng, theo quý hoặc cuối kỳ."
)

st.divider()


# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:
    so_tien_gui = st.number_input(
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
        "Hình thức tính lãi",
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


# =========================
# TÍNH TOÁN
# =========================
def tinh_lai(
    tien_goc,
    so_thang,
    lai_suat_nam,
    loai_lai,
    hinh_thuc_nhan_lai
):
    """
    Tính tiền lãi tiết kiệm.

    Quy ước:
    - Lãi suất nhập vào là %/năm.
    - Lãi theo tháng = lãi suất năm / 12.
    - Lãi theo quý = lãi suất năm / 4.
    - Với lãi đơn: tiền lãi được tính trên tiền gốc ban đầu.
    - Với lãi kép: tiền lãi được nhập vào gốc sau mỗi kỳ nhận lãi.
    """

    lai_suat_nam = lai_suat_nam / 100

    # Xác định số tháng của một kỳ nhận lãi
    if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":
        thang_moi_ky = 1
    elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":
        thang_moi_ky = 3
    else:
        thang_moi_ky = so_thang

    # =========================
    # TRƯỜNG HỢP LÃNH CUỐI KỲ
    # =========================
    if hinh_thuc_nhan_lai == "Lãnh lãi cuối kỳ":

        if loai_lai == "Lãi đơn":
            tong_lai = tien_goc * lai_suat_nam * so_thang / 12
            tong_tien = tien_goc + tong_lai

        else:
            # Lãi kép: ghép lãi theo tháng
            lai_thang = lai_suat_nam / 12
            tong_tien = tien_goc * ((1 + lai_thang) ** so_thang)
            tong_lai = tong_tien - tien_goc

        return {
            "lai_dinh_ky": tong_lai,
            "tong_lai": tong_lai,
            "tong_tien": tong_tien,
            "chi_tiet": [
                {
                    "Kỳ": "Cuối kỳ",
                    "Số tháng": so_thang,
                    "Tiền gốc": tien_goc,
                    "Tiền lãi": tong_lai,
                    "Tổng tiền": tong_tien
                }
            ]
        }

    # =========================
    # LÃNH LÃI THEO THÁNG / QUÝ
    # =========================

    # Số kỳ nhận lãi
    so_ky = so_thang // thang_moi_ky

    # Nếu kỳ hạn không chia hết cho kỳ nhận lãi,
    # phần tháng lẻ sẽ được xử lý ở cuối.
    thang_con_lai = so_thang % thang_moi_ky

    chi_tiet = []

    tong_lai = 0
    tien_hien_tai = tien_goc

    # Lãi suất cho một kỳ
    lai_suat_ky = lai_suat_nam * thang_moi_ky / 12

    for ky in range(1, so_ky + 1):

        if loai_lai == "Lãi đơn":
            # Lãi luôn tính trên tiền gốc ban đầu
            tien_lai = tien_goc * lai_suat_ky

            # Với lãi đơn, tiền lãi được trả ra ngoài,
            # không cộng vào gốc.
            tien_cuoi_ky = tien_goc + tien_lai

        else:
            # Lãi kép
            tien_lai = tien_hien_tai * lai_suat_ky

            # Lãi nhập vào gốc
            tien_hien_tai += tien_lai

            tien_cuoi_ky = tien_hien_tai

        tong_lai += tien_lai

        chi_tiet.append(
            {
                "Kỳ": ky,
                "Số tháng": ky * thang_moi_ky,
                "Tiền gốc": tien_goc if loai_lai == "Lãi đơn" else tien_hien_tai - tien_lai,
                "Tiền lãi": tien_lai,
                "Tổng tiền": tien_cuoi_ky
            }
        )

    # =========================
    # XỬ LÝ THÁNG LẺ
    # =========================
    if thang_con_lai > 0:

        lai_suat_le = lai_suat_nam * thang_con_lai / 12

        if loai_lai == "Lãi đơn":
            tien_lai_le = tien_goc * lai_suat_le
            tien_cuoi_ky = tien_goc + tien_lai_le
        else:
            tien_lai_le = tien_hien_tai * lai_suat_le
            tien_hien_tai += tien_lai_le
            tien_cuoi_ky = tien_hien_tai

        tong_lai += tien_lai_le

        chi_tiet.append(
            {
                "Kỳ": f"{so_ky + 1} (lẻ)",
                "Số tháng": so_thang,
                "Tiền gốc": (
                    tien_goc
                    if loai_lai == "Lãi đơn"
                    else tien_hien_tai - tien_lai_le
                ),
                "Tiền lãi": tien_lai_le,
                "Tổng tiền": tien_cuoi_ky
            }
        )

    # =========================
    # KẾT QUẢ CUỐI
    # =========================
    if loai_lai == "Lãi đơn":
        tong_tien = tien_goc + tong_lai
    else:
        tong_tien = tien_hien_tai

    # Tiền lãi định kỳ
    if so_ky > 0:
        lai_dinh_ky = (
            tong_lai / so_ky
            if thang_con_lai == 0
            else tong_lai / len(chi_tiet)
        )
    else:
        lai_dinh_ky = tong_lai

    return {
        "lai_dinh_ky": lai_dinh_ky,
        "tong_lai": tong_lai,
        "tong_tien": tong_tien,
        "chi_tiet": chi_tiet
    }


# =========================
# NÚT TÍNH TOÁN
# =========================
st.divider()

if st.button(
    "🧮 TÍNH TIỀN LÃI",
    type="primary",
    use_container_width=True
):

    if so_tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    ket_qua = tinh_lai(
        tien_goc=so_tien_gui,
        so_thang=ky_han,
        lai_suat_nam=lai_suat,
        loai_lai=loai_lai,
        hinh_thuc_nhan_lai=hinh_thuc_nhan_lai
    )

    lai_dinh_ky = ket_qua["lai_dinh_ky"]
    tong_lai = ket_qua["tong_lai"]
    tong_tien = ket_qua["tong_tien"]


    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.subheader("📊 Kết quả tính toán")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            format_money(lai_dinh_ky)
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(tong_lai)
        )

    with col3:
        st.metric(
            "💰 Tổng gốc + lãi",
            format_money(tong_tien)
        )


    # =========================
    # THÔNG TIN TÓM TẮT
    # =========================
    st.divider()

    st.subheader("📝 Thông tin khoản gửi")

    thong_tin = {
        "Số tiền gửi": format_money(so_tien_gui),
        "Kỳ hạn": f"{ky_han} tháng",
        "Lãi suất": f"{lai_suat:.2f}%/năm",
        "Hình thức tính": loai_lai,
        "Hình thức nhận lãi": hinh_thuc_nhan_lai
    }

    for key, value in thong_tin.items():
        col1, col2 = st.columns([1, 2])

        with col1:
            st.write(f"**{key}**")

        with col2:
            st.write(value)


    # =========================
    # BẢNG CHI TIẾT
    # =========================
    st.divider()

    st.subheader("📋 Chi tiết tiền lãi")

    # Tạo dữ liệu hiển thị đẹp hơn
    bang_hien_thi = []

    for item in ket_qua["chi_tiet"]:
        bang_hien_thi.append(
            {
                "Kỳ": item["Kỳ"],
                "Số tháng": item["Số tháng"],
                "Tiền gốc": format_money(item["Tiền gốc"]),
                "Tiền lãi": format_money(item["Tiền lãi"]),
                "Tổng tiền": format_money(item["Tổng tiền"])
            }
        )

    st.dataframe(
        bang_hien_thi,
        use_container_width=True,
        hide_index=True
    )


    # =========================
    # GIẢI THÍCH
    # =========================
    with st.expander("ℹ️ Xem cách tính"):

        if loai_lai == "Lãi đơn":
            st.write(
                "### Lãi đơn"
            )

            st.latex(
                r"Lãi = Tiền\ gốc \times Lãi\ suất\ năm \times "
                r"\frac{Số\ tháng}{12}"
            )

            st.write(
                "Với lãi đơn, tiền lãi của mỗi kỳ được tính dựa trên "
                "số tiền gốc ban đầu. Tiền lãi không được nhập vào gốc."
            )

        else:
            st.write(
                "### Lãi kép"
            )

            st.latex(
                r"Tổng\ tiền = Tiền\ gốc \times (1 + r)^n"
            )

            st.write(
                "Với lãi kép, tiền lãi sau mỗi kỳ được cộng vào tiền gốc "
                "và tiếp tục được dùng để tính lãi cho kỳ tiếp theo."
            )


# =========================
# FOOTER
# =========================
st.divider()

st.caption(
    "💡 Công cụ mang tính chất tham khảo. "
    "Lãi thực tế của ngân hàng có thể phụ thuộc vào quy định, "
    "phương pháp tính lãi và điều kiện của từng sản phẩm tiền gửi."
)
```
