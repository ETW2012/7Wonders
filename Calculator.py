import base64
from itertools import groupby
from pathlib import Path
import streamlit as st
#from streamlit_js_eval import streamlit_js_eval
import pandas as pd

st.title("7 Wonders Score Calculator", text_alignment = "center")

image_dir = Path(__file__).resolve().parent / "images"

background_image = base64.b64encode(
    (image_dir / "7 wonders banner.jpg").read_bytes()
).decode("ascii")

#For background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image:
            linear-gradient(rgba(255, 255, 255, 0.55), rgba(255, 255, 255, 0.55)),
            url("data:image/jpeg;base64,{background_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

def make_line():
    st.write("________________________________________________________")

make_line()

# makes select box smaller
players_col1, players_col2, players_clo3 = st.columns(3)
with players_col1:
    players = st.selectbox(
        "Select number of players:",
        options = ["2 Players", "3 Players", "4 Players", "5 Players", "6 Players", "7 Players"]
    )

player_count = int(players.split()[0])
player_names = [""] * player_count

st.write("")
st.write("Player names:")


for start in range(0, player_count, 3):
    name_columns = st.columns(3)
    for player in range(start, min(start + 3, player_count)):
        with name_columns[player - start]:
            player_names[player] = st.text_input(label = "", placeholder = f"Player {player+1} Name")

def player_display_name(player_number):
    name = player_names[player_number - 1].strip()
    return name if name else f"Player {player_number}"

def name(place):
    return player_display_name(int(place))

point_types = [
    "Wonder Points:",
    "Military Points:",
    "Guild Points:",
    "Victory Points:",
    "Economic Points:"
]

card_colours = [
     "Board",
     "Victory tokens",
     "Purple cards",
     "Blue cards",
     "Yellow cards"
]

players_total_points = {}
players_coins = {}

def test_if_integer_and_square(value):
    try:
        value = int(value)
        return value ** 2
    except ValueError:
        return 0

for player in range(player_count):
    make_line()

    total_points = 0
    first_row = st.columns(3)
    point_inputs = []

    # Puts coins in column slot
    with first_row[0]:
        coin_input = st.number_input(
            label = f"{name(player+1)}'s Number of Coins:",
            placeholder = "Not points from coins",
            value = 0,
            step = 1,
            min_value = 0)

    # Adds second input box in first row
    with first_row[1]:
        point_inputs.append(st.number_input(
            label = f"{name(player+1)}'s {point_types[0]}",
            placeholder = card_colours[0],
            value = 0,
            step = 1,
            min_value = 0))

    # Adds third input box in first row
    with first_row[2]:
        point_inputs.append(st.number_input(
            label = f"{name(player+1)}'s {point_types[1]}",
            placeholder = card_colours[1],
            value = 0,
            step = 1,))

    # Calculates coin amount
    try:
        coins = int(coin_input)
    except ValueError:
        coins = 0
    total_points += coins // 3

    # Creates input boxes in second row
    second_row = st.columns(3)
    for index, column in enumerate(second_row, start = 2):
        with column:
            point_inputs.append(st.number_input(
                label = f"{name(player+1)}'s {point_types[index]}",
                placeholder = card_colours[index],
                value = 0,
                step = 1,
                min_value = 0))

    # Adda point from user input
    for user_input in point_inputs:
        try:
            total_points += int(user_input)
        except ValueError:
            total_points += 0

    st.write(f"{name(player+1)}'s Science Points:")

    image_1, compass, image_2, gear, image_3, tablet = st.columns(6)

    # Creates compass image and input box
    with image_1:
        st.write("")
        st.image(str(image_dir / "7 wonders compass.png"), width = 135)
    with compass:
        Compass_input = st.number_input(
            label = "", 
            placeholder = "Green cards", 
            key = f"{player + 1} compasses",
            value = 0,
            step = 1,
            min_value = 0)

    # Creates gear image and input box        
    with image_2:
        st.write("")
        st.image(str(image_dir / "7 wonders gear.png"), width = 135)
    with gear:
        Gear_input = st.number_input(
            label = "",
            placeholder = "Green cards", 
            key = f"{player + 1} gears",
            value = 0,
            step = 1,
            min_value = 0)

    # Creates tablet image and input box    
    with image_3:
        st.write("")
        st.image(str(image_dir / "7 wonders tablet.png"), width = 135)
    with tablet:
        Tablet_input = st.number_input(
            label = "",
            placeholder = "Green cards", 
            key = f"{player + 1} tablets",
            value = 0,
            step = 1,
            min_value = 0)

    # Tests and squares values
    compass_points = test_if_integer_and_square(Compass_input)
    gear_points = test_if_integer_and_square(Gear_input)
    tablet_points = test_if_integer_and_square(Tablet_input)
    squared_points = compass_points + gear_points + tablet_points

    # Adds up science points
    try:
        complete_sets = min(int(Compass_input), int(Gear_input), int(Tablet_input))
    except ValueError:
        complete_sets = 0
    set_bonus_points = complete_sets * 7

    # Adds up all the points
    try:
        total_points += squared_points + set_bonus_points
    except ValueError:
        total_points += 0

    # Updates players points
    players_total_points.update({str(player+1): total_points})
    players_coins.update({str(player+1): coins})
    players_total_points.update({str(player+1): total_points})

make_line()

# Moves button to the center
col1, col2, clo3 = st.columns(3)
with col2:
    Calculate_score = st.button("Calculate Score", width = "stretch")

if Calculate_score:

    st.subheader("Final standings:")

    # Sorts players into a list
    sorted_players = sorted(
        players_total_points.items(),
        key = lambda player_score: (
            player_score[1],
            players_coins[player_score[0]]
        ),
        reverse=True
    )

    # Sorts players into alist with tied players
    standing_groups = [
        (score_and_coins, list(tied_players))
        for score_and_coins, tied_players in groupby(
            sorted_players,
            key = lambda player_score: (
                player_score[1],
                players_coins[player_score[0]]
            )
        )
    ]

    podium_places = {}
    place = 1

    # Checks coins for ties    
    for (score, coins), tied_players in standing_groups:
        if place <= 3:
            podium_places[place] = (score, coins, tied_players)
        place += len(tied_players)

    # Sets medal emojis
    podium_columns = st.columns(3, vertical_alignment="bottom")
    box_heights = {1: 240, 2: 180, 3: 140}
    for column, place_number, medal, in [
        (podium_columns[0], 2, "🥈"),
        (podium_columns[1], 1, "🥇"),
        (podium_columns[2], 3, "🥉"),
    ]:

        # Creates podium
        with column:
            with st.container(height=box_heights[place_number], border=True):
                st.title(medal, text_alignment = "center")
                podium_group = podium_places.get(place_number)
                if podium_group:
                    score, coins, tied_players = podium_group
                    for player_number, _ in tied_players:
                        st.header(name(player_number), text_alignment = "center")
                
                else:
                    st.write("No player in this place")

    st.subheader("")

    names = []
    points = []

    # Creates table
    for player in range(int(players.split()[0])):
        player_number = player + 1
        names.append(name(player_number))
        if players_total_points[str(player_number)] == 1:
            points.append(f"{players_total_points[str(player_number)]} point")
        else:
            points.append(f"{players_total_points[str(player_number)]} points")    
    points_table = pd.DataFrame({
        "Names": names,
        "Points": points
    })

    # Removes unnessesary numbers
    points_table_no_index = points_table.reset_index(drop=True)

    st.table(points_table_no_index)
    
    #make_line()

# Moves button to the center
#reset_col1, reset_col2, reset_clo3 = st.columns(3)
#with reset_col2:
#    if st.button("Reset", width = "stretch"):
#        #Reloads borwser
#        streamlit_js_eval(js_expressions="parent.window.location.reload()")

make_line()

st.write("By: Elliot.W")
