# app.py
import streamlit as st
from PIL import Image
import os
from streamlit_drawable_canvas import st_canvas
import random

st.title("AI Ludo - Interactive Canvas Prototype")

# -------------------------------
# Board image
# -------------------------------
BASE_DIR = os.path.dirname(__file__)
board_file_name = "chat ludo.png"  # ya rename karke board.png
board_path = os.path.join(BASE_DIR, board_file_name)

try:
    board = Image.open(board_path)
except FileNotFoundError:
    st.error(f"Error: '{board_path}' file not found. Please upload the board image.")
    st.stop()

# -------------------------------
# Initialize game state
# -------------------------------
if "players" not in st.session_state:
    # 4 players, 4 gotiyan each, positions as (x, y)
    st.session_state.players = {
        "Red": [(20, 20), (60, 20), (20, 60), (60, 60)],
        "Blue": [(320, 20), (360, 20), (320, 60), (360, 60)],
        "Green": [(20, 320), (60, 320), (20, 360), (60, 360)],
        "Yellow": [(320, 320), (360, 320), (320, 360), (360, 360)],
    }
    st.session_state.turn_order = ["Red", "Blue", "Green", "Yellow"]
    st.session_state.current_turn = 0
    st.session_state.dice_roll = 0

# -------------------------------
# Dice roll
# -------------------------------
if st.button("Roll Dice"):
    st.session_state.dice_roll = random.randint(1, 6)
    player = st.session_state.turn_order[st.session_state.current_turn]
    st.write(f"{player}'s turn: You rolled {st.session_state.dice_roll}")

# -------------------------------
# Draw canvas
# -------------------------------
canvas_result = st_canvas(
    fill_color="rgba(0,0,0,0)",   # transparent initially
    stroke_width=2,
    background_image=board,       # board image as background
    height=400,
    width=400,
    drawing_mode="circle",
    key="canvas",
)

# -------------------------------
# Move logic (simple horizontal move)
# -------------------------------
player = st.session_state.turn_order[st.session_state.current_turn]
dice = st.session_state.dice_roll

if dice > 0:
    # Move first goti of current player as example
    x, y = st.session_state.players[player][0]
    new_x = x + dice * 10  # simple horizontal move
    st.session_state.players[player][0] = (new_x, y)

    # Reset dice and next turn
    st.session_state.dice_roll = 0
    st.session_state.current_turn = (st.session_state.current_turn + 1) % 4

# -------------------------------
# Draw all gotiyan over canvas
# -------------------------------
if canvas_result:
    for color, positions in st.session_state.players.items():
        for pos in positions:
            x, y = pos
            canvas_result.circle(x=x, y=y, r=10, fill=color.lower())

# -------------------------------
# Display positions for debug
# -------------------------------
st.write("Current positions (x, y):")
st.write(st.session_state.players)
