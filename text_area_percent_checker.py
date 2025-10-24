import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="Kiểm tra phần trăm văn bản trong ảnh", layout="wide")

st.title("📊 Kiểm tra phần trăm vùng chứa văn bản trong ảnh")

# --------------------------
# Bước 1: Upload ảnh
# --------------------------
uploaded_file = st.file_uploader("📤 Tải ảnh lên (JPG, PNG...)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Đọc ảnh
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Ảnh gốc", use_column_width=True)

    st.markdown("### ✏️ Bước 2: Vẽ vùng chứa văn bản trong ảnh")
    st.info("👉 Dùng chuột để vẽ vùng chữ (có thể vẽ nhiều vùng). Khi xong, nhấn nút bên dưới để tính phần trăm.")

    # Chuyển ảnh sang mảng NumPy
    img_array = np.array(image)

    # Kích thước canvas
    width, height = image.size

    # Vẽ vùng chọn
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",  # Màu vùng chọn
        stroke_width=2,
        stroke_color="#FF0000",
        background_image=image,
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode="rect",
        key="canvas",
    )

    # --------------------------
    # Bước 3: Tính phần trăm vùng được chọn
    # --------------------------
    if st.button("📈 Tính phần trăm vùng được chọn"):
        if canvas_result.json_data is not None:
            objects = canvas_result.json_data["objects"]
            total_area = width * height
            selected_area = 0

            for obj in objects:
                if obj["type"] == "rect":
                    rect_width = obj["width"] * obj["scaleX"]
                    rect_height = obj["height"] * obj["scaleY"]
                    selected_area += rect_width * rect_height

            percent = (selected_area / total_area) * 100
            st.success(f"🟩 Phần trăm vùng chứa văn bản: **{percent:.2f}%**")
        else:
            st.warning("⚠️ Bạn chưa vẽ vùng nào trên ảnh!")

else:
    st.info("⬆️ Hãy tải lên một ảnh để bắt đầu.")
