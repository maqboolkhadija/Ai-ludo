import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io

st.title("AI Ludo Game")

# Step 1: Upload your Ludo board image
uploaded_file = st.file_uploader("Upload your Ludo board image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Convert uploaded file to PIL Image
    board_image = Image.open(uploaded_file)

    # Save image to bytes buffer (Streamlit Canvas compatible)
    img_bytes = io.BytesIO()
    board_image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    st.image(board_image, caption="Ludo Board", use_column_width=True)

    # Step 2: Setup canvas
    canvas_result = st_canvas(
        fill_color="rgba(0,0,0,0)",   # transparent initially
        stroke_width=2,
        stroke_color="#FF0000",
        background_image=Image.open(img_bytes),  # use bytes object
        height=500,
        width=500,
        drawing_mode="freedraw",
        key="canvas",
    )

    # Step 3: Show canvas output
    if canvas_result.image_data is not None:
        st.image(canvas_result.image_data, caption="Canvas Output")
else:
    st.warning("Please upload the board image to start.")
