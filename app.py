# app.py
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

st.title("AI Ludo Game")

# Image load karna (same folder mein)
try:
    board_image = Image.open("chat_ludo.png")
    st.image(board_image, caption="Ludo Board")
except FileNotFoundError:
    st.error("Error: 'chat_ludo.png' file not found. Please upload the board image.")

# Canvas setup
canvas_result = st_canvas(
    fill_color="rgba(0,0,0,0)",   # transparent initially
    stroke_width=2,
    stroke_color="#000000",
    background_image=board_image if 'board_image' in locals() else None,
    height=500,
    width=500,
    drawing_mode="freedraw",
    key="canvas",
)

# Optional: show drawing data
if canvas_result.image_data is not None:
    st.image(canvas_result.image_data, caption="Canvas Output")
