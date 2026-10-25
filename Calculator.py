import base64
from itertools import groupby
from pathlib import Path
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.title("7 Wonders Score Calculator", text_alignment="center")

background_image = base64.b64encode(
    Path("C:/Users/User/Downloads/7 wonders banner.jpg").read_bytes()
).decode("ascii")

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

players = st.selectbox(
    "Select number of players:",
    options = ["2 Players", "3 Players", "4 Players", "5 Players", "6 Players", "7 Players"]
)

player_count = int(players.split()[0])
player_names = [""] * player_count

for start in range(0, player_count, 3):
    name_columns = st.columns(3)
    for player in range(start, min(start + 3, player_count)):
        with name_columns[player - start]:
            player_names[player] = st.text_input(f"Player {player+1} Name:")

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
    
    with first_row[0]:
        coin_input = st.text_input(
            label = f"{name(player+1)}'s Number of Coins:",
            placeholder = "Not points from coins")
    
    with first_row[1]:
        point_inputs.append(st.text_input(
            label = f"{name(player+1)}'s {point_types[0]}",
            placeholder = card_colours[0]))
    
    with first_row[2]:
        point_inputs.append(st.text_input(
            label = f"{name(player+1)}'s {point_types[1]}",
            placeholder = card_colours[1]))
        
    try:
        coins = int(coin_input)
    except ValueError:
        coins = 0
    total_points += coins // 3

    second_row = st.columns(3)
    for index, column in enumerate(second_row, start=2):
        with column:
            point_inputs.append(st.text_input(
                label = f"{name(player+1)}'s {point_types[index]}",
                placeholder = card_colours[index]))

    for user_input in point_inputs:
        try:
            total_points += int(user_input)
        except ValueError:
            total_points += 0

    st.write(f"{name(player+1)}'s Sciences (green):")

    image_1, compass, image_2, gear, image_3, tablet = st.columns(6)
    with image_1:
        st.write("")
        st.image("C:/Users/User/Downloads/hackclub things/3.png", width = 135)
    with compass:
        Compass_input = st.text_input(
            "", 
            placeholder = "Green cards", 
            key = f"{player + 1} compasses")
        
    with image_2:
        st.write("")
        st.image("C:/Users/User/Downloads/hackclub things/2.png", width = 135)
    with gear:
        Gear_input = st.text_input(
            "",
            placeholder = "Green cards", 
            key = f"{player + 1} gears")
    
    with image_3:
        st.write("")
        st.image("C:/Users/User/Downloads/hackclub things/1.png", width = 135)
    with tablet:
        Tablet_input = st.text_input(
            "",
            placeholder = "Green cards", 
            key = f"{player + 1} tablets")
    
    compass_points = test_if_integer_and_square(Compass_input)
    gear_points = test_if_integer_and_square(Gear_input)
    tablet_points = test_if_integer_and_square(Tablet_input)
    squared_points = compass_points + gear_points + tablet_points
    try:
        complete_sets = min(int(Compass_input), int(Gear_input), int(Tablet_input))
    except ValueError:
        complete_sets = 0
    set_bonus_points = complete_sets * 7
    try:
        total_points += squared_points + set_bonus_points
    except ValueError:
        total_points += 0
    players_total_points.update({str(player+1): total_points})
    players_coins.update({str(player+1): coins})
    players_total_points.update({str(player+1): total_points})

make_line()
 
Calculate_score = st.button("Calculate Score")

if Calculate_score:
    for player in range(int(players.split()[0])):
        player_number = player + 1
        if players_total_points[str(player_number)] == 1:
            st.subheader(f'{name(player_number)} - {players_total_points[str(player_number)]} point')
        else:
            st.subheader(f'{name(player_number)} - {players_total_points[str(player_number)]} points')
    
    make_line()

    st.subheader("Final standings:")
    sorted_players = sorted(
        players_total_points.items(),
        key=lambda player_score: (
            player_score[1],
            players_coins[player_score[0]]
        ),
        reverse=True
    )
    standing_groups = [
        (score_and_coins, list(tied_players))
        for score_and_coins, tied_players in groupby(
            sorted_players,
            key=lambda player_score: (
                player_score[1],
                players_coins[player_score[0]]
            )
        )
    ]

    podium_places = {}
    place = 1
    for (score, coins), tied_players in standing_groups:
        if place <= 3:
            podium_places[place] = (score, coins, tied_players)
        place += len(tied_players)

    podium_columns = st.columns(3, vertical_alignment="bottom")
    box_heights = {1: 240, 2: 180, 3: 140}
    for column, place_number, medal, place_label in [
        (podium_columns[0], 2, "🥈", "Second place"),
        (podium_columns[1], 1, "🥇", "First place"),
        (podium_columns[2], 3, "🥉", "Third place"),
    ]:
        with column:
            with st.container(height=box_heights[place_number], border=True):
                st.subheader(f"{medal} {place_label}")
                podium_group = podium_places.get(place_number)
                if podium_group:
                    score, coins, tied_players = podium_group
                    for player_number, _ in tied_players:
                        st.write(name(player_number))
                    points_label = "point" if score == 1 else "points"
                    st.write(f"**{score} {points_label}**")
                    st.caption(f"{coins} coins")
                else:
                    st.write("No player in this place")

    place_names = {1: "first", 2: "second", 3: "third"}
    place = 1

    for (score, coins), tied_players in standing_groups:
        if place <= 3:
            place += len(tied_players)
            continue

        tied_names = [name(player_number) for player_number, _ in tied_players]
        
        if len(tied_names) == 1:
            display_names = tied_names[0]
        else:
            display_names = f"{', '.join(tied_names[:-1])} and {tied_names[-1]}"

        place_name = place_names.get(place, f"{place}th")
        points_label = "point" if score == 1 else "points"

        if place == 1 and len(tied_names) > 1:
            st.header(
                f"{display_names} are tied for first place with {score} "
                f"{points_label}!"
            )
        elif place == 1:
            st.header(f"{display_names} is the winner with {score} {points_label}!")
        
        elif len(tied_names) > 1:
            st.header(
                f"{display_names} are tied for {place_name} place with "
                f"{score} {points_label}!"
            )
        else:
            st.header(
                f"{display_names} is in {place_name} place with "
                f"{score} {points_label}!"
            )

        place += len(tied_players)

    make_line()

if st.button("Reset"):
    #Reloads borwser
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

make_line()

st.write("By: Elliot Wijoyo")
