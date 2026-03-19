import streamlit as st
from PIL import Image
import random

st.set_page_config(layout="wide")
st.title("🎲 Full Advanced Ludo Game")

# --- Load Images ---
try:
    board_img = Image.open("board.png").convert("RGBA")
    tok_red = Image.open("token_red.png").convert("RGBA")
    tok_green = Image.open("token_green.png").convert("RGBA")
    tok_yellow = Image.open("token_yellow.png").convert("RGBA")
    tok_blue = Image.open("token_blue.png").convert("RGBA")
except:
    st.error("⚠️ Please make sure all images (board + 4 tokens) are in the project folder.")
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

# --- Simplified track coordinates (15x15 grid) ---
TRACK = [
    (6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(5,6),(4,6),(3,6),(2,6),(1,6),(0,6),
    (0,7),(0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(6,9),(6,10),(6,11),(6,12),(6,13),(6,14),
    (7,14),(8,14),(8,13),(8,12),(8,11),(8,10),(8,9),(8,8),(9,8),(10,8),(11,8),(12,8),(13,8),(14,8),
    (14,7),(13,7),(12,7),(11,7),(10,7),(9,7),(8,7),(8,6),(8,5),(8,4),(8,3),(8,2),(8,1),(8,0),
    (7,0)
]

# --- Display Board with Tokens ---
canvas = board_img.copy()
for player in players:
    for idx, step in enumerate(st.session_state.pos[player]):
        if step >= 0 and step < len(TRACK):
            x, y = TRACK[step]
            px = x*40 + 5  # adjust token offset
            py = y*40 + 5
            token_img = token_images[player].resize((30,30))
            canvas.paste(token_img, (px, py), token_img)

st.image(canvas, caption="Board with Tokens", use_column_width=True)

# --- Dice Roll & Move ---
col1, col2 = st.columns([1,2])
current_player = players[st.session_state.turn % 4]

with col1:
    if st.button(f"🎲 {current_player.upper()} Roll Dice"):
        st.session_state.dice = random.randint(1,6)
        st.write(f"{current_player.upper()} rolled {st.session_state.dice}")

    dice = st.session_state.dice
    if dice > 0:
        goti_choice = st.radio(f"{current_player.upper()} choose goti to move", [1,2,3,4])
        if st.button("➡ Move"):
            idx = goti_choice - 1
            pos = st.session_state.pos[current_player][idx]
            if pos == -1:
                if dice == 6:
                    pos = 0
                else:
                    st.warning("Need 6 to bring goti out!")
            else:
                pos += dice
                if pos >= len(TRACK):
                    pos = len(TRACK)-1
                    if current_player not in st.session_state.finished:
                        st.session_state.finished.append(current_player)
            st.session_state.pos[current_player][idx] = pos
            st.session_state.dice = 0
            if dice != 6:
                st.session_state.turn += 1

with col2:
    st.write("🔢 Positions:", st.session_state.pos)
    st.write("🏁 Finished:", st.session_state.finished)
