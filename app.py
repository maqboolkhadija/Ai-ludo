import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw
import random

st.set_page_config(layout="wide")
st.title("Advanced Ludo Game")

# --- Configuration ---
GRID_SIZE = 15
CELL_SIZE = 40
BOARD_SIZE = GRID_SIZE * CELL_SIZE
PLAYER_COLORS = ["red", "green", "yellow", "blue"]
START_POSITIONS = {"red": (0,0), "green": (0,10), "yellow": (10,10), "blue": (10,0)}
SAFE_ZONES = [(6,0),(8,0),(14,6),(14,8),(8,14),(6,14),(0,8),(0,6)]
TRACK_PATH = [  # simplified linear path for demo
    (6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(5,6),(4,6),(3,6),(2,6),(1,6),(0,6),
    (0,7),(0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(6,9),(6,10),(6,11),(6,12),(6,13),(6,14),
    (7,14),(8,14),(8,13),(8,12),(8,11),(8,10),(8,9),(8,8),(9,8),(10,8),(11,8),(12,8),(13,8),(14,8),
    (14,7),(13,7),(12,7),(11,7),(10,7),(9,7),(8,7),(8,6),(8,5),(8,4),(8,3),(8,2),(8,1),(8,0),
    (7,0)  # loop back to start
]

# --- Initialize session state ---
if "board_image" not in st.session_state:
    # Create board image
    board = Image.new("RGB", (BOARD_SIZE, BOARD_SIZE), "white")
    draw = ImageDraw.Draw(board)

    # Draw grid
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x0 = i * CELL_SIZE
            y0 = j * CELL_SIZE
            x1 = x0 + CELL_SIZE
            y1 = y0 + CELL_SIZE
            draw.rectangle([x0, y0, x1, y1], outline="black", fill="white")

    # Draw safe zones
    for (i,j) in SAFE_ZONES:
        x0 = i*CELL_SIZE
        y0 = j*CELL_SIZE
        x1 = x0+CELL_SIZE
        y1 = y0+CELL_SIZE
        draw.rectangle([x0,y0,x1,y1], fill="lightgrey")

    # Draw homes
    for color,(i,j) in START_POSITIONS.items():
        for di in range(4):
            for dj in range(4):
                x0 = (i+di)*CELL_SIZE
                y0 = (j+dj)*CELL_SIZE
                x1 = x0+CELL_SIZE
                y1 = y0+CELL_SIZE
                draw.rectangle([x0,y0,x1,y1], fill=color)

    st.session_state.board_image = board
    st.session_state.turn = 0
    st.session_state.dice = 0
    st.session_state.positions = {color:[-1,-1,-1,-1] for color in PLAYER_COLORS}
    st.session_state.finished = []

# --- Display board ---
st.image(st.session_state.board_image)

# --- Dice roll ---
current_player = PLAYER_COLORS[st.session_state.turn % 4]
if st.button(f"{current_player.upper()} Roll Dice"):
    dice = random.randint(1,6)
    st.session_state.dice = dice
    st.write(f"{current_player.upper()} rolled {dice}")

# --- Move goti ---
dice = st.session_state.dice
if dice>0:
    goti_choice = st.radio(f"{current_player.upper()} choose goti to move", [1,2,3,4])
    if st.button(f"Move {current_player.upper()} goti"):
        idx = goti_choice-1
        pos = st.session_state.positions[current_player][idx]
        if pos==-1:
            if dice==6:
                pos=0
            else:
                st.warning("Need 6 to exit home")
        else:
            pos += dice
            if pos>=len(TRACK_PATH):
                pos = len(TRACK_PATH)-1  # finish
                st.session_state.finished.append(current_player)
        st.session_state.positions[current_player][idx] = pos
        # Reset dice
        st.session_state.dice = 0
        # Change turn unless dice==6
        if dice!=6:
            st.session_state.turn += 1

# --- Display positions ---
st.write("Current Positions:")
st.write(st.session_state.positions)
st.write("Finished Order:", st.session_state.finished)
