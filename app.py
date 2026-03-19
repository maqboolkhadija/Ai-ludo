import streamlit as st
from PIL import Image
import random

st.set_page_config(layout="wide")
st.title("🎲 Advanced Ludo Game")

# --- Load Images ---
try:
    board_img = Image.open("board.png")
    tok_red = Image.open("token_red.png")
    tok_green = Image.open("token_green.png")
    tok_yellow = Image.open("token_yellow.png")
    tok_blue = Image.open("token_blue.png")
except Exception as e:
    st.error("⚠️ Images not found! Upload board.png and token images.")
    st.stop()

token_images = {
    "red": tok_red,
    "green": tok_green,
    "yellow": tok_yellow,
    "blue": tok_blue
}

# --- Game Variables ---
players = ["red", "green", "yellow", "blue"]
if "turn" not in st.session_state:
    st.session_state.turn = 0
if "dice" not in st.session_state:
    st.session_state.dice = 0
if "pos" not in st.session_state:
    st.session_state.pos = {p: [-1,-1,-1,-1] for p in players}
if "finished" not in st.session_state:
    st.session_state.finished = []

# Simplified track coordinates
TRACK = [
    (6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(5,6),(4,6),(3,6),(2,6),(1,6),(0,6),
    (0,7),(0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(6,9),(6,10),(6,11),(6,12),(6,13),(6,14),
    (7,14),(8,14),(8,13),(8,12),(8,11),(8,10),(8,9),(8,8),(9,8),(10,8),(11,8),(12,8),(13,8),(14,8),
    (14,7),(13,7),(12,7),(11,7),(10,7),(9,7),(8,7),(8,6),(8,5),(8,4),(8,3),(8,2),(8,1),(8,0),
    (7,0)
]

# --- Display Board ---
st.image(board_img, caption="Ludo Board", use_column_width=True)

col1, col2 = st.columns([1,2])

with col1:
    current = players[st.session_state.turn % 4]
    if st.button(f"🎲 {current.upper()} Roll Dice"):
        d = random.randint(1,6)
        st.session_state.dice = d
        st.write(f"🎲 {current.upper()} rolled {d}")

    d = st.session_state.dice
    if d > 0:
        goti = st.radio("Choose Goti to Move", [1,2,3,4])
        if st.button("➡ Move"):
            idx = goti - 1
            pos = st.session_state.pos[current][idx]
            if pos == -1:
                if d == 6:
                    pos = 0
                else:
                    st.warning("Need 6 to bring goti out!")
            else:
                pos += d
                if pos >= len(TRACK):
                    pos = len(TRACK) - 1
                    if current not in st.session_state.finished:
                        st.session_state.finished.append(current)
            st.session_state.pos[current][idx] = pos
            st.session_state.dice = 0
            if d != 6:
                st.session_state.turn += 1

# --- Draw Token Overlay ---
canvas = board_img.copy()
draw = Image.new("RGBA", canvas.size)
for p in players:
    for i,step in enumerate(st.session_state.pos[p]):
        if step >= 0:
            x,y = TRACK[step]
            px = x * 40 + 10
            py = y * 40 + 10
            tok_img = token_images[p].resize((30,30))
            draw.paste(tok_img, (px,py), tok_img)

canvas.paste(draw, (0,0), draw)
st.image(canvas, caption="Board with Tokens")

with col2:
    st.write("🔢 Positions:", st.session_state.pos)
    st.write("🏁 Finished:", st.session_state.finished)
