import base64
from pathlib import Path

import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.title("7 Wonders Score Calculator")

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
    st.write("_______________________________________________________")

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
            player_names[player] = st.text_input(f"Player {player+1} Name")

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

    with first_row[0]:
        coin_input = st.text_input(
            label = f"{name(player+1)}'s Number of coins:",
            placeholder = "Not points from coins")
    point_inputs = []
    with first_row[1]:
        point_inputs.append(st.text_input(
            label = f"{name(player+1)}'s {point_types[0]}",
            placeholder = card_colours[0]))
    with first_row[2]:
        point_inputs.append(st.text_input(
            label = f"Player {name(player+1)}'s {point_types[1]}",
            placeholder = card_colours[1]))
    try:
        total_points += int(coin_input)//3
    except ValueError:
        total_points += 0

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

    st.write("")

    compass, gear, tablet = st.columns(3)
    with compass:
        Compass_input = st.text_input(
            label = f"{name(player+1)}'s Sciences (green):",
            placeholder = f"{name(player+1)}'s number of compasses")
    with gear:
        Gear_input = st.text_input(
            label = "",
            placeholder = f"{name(player+1)}'s number of gears")
    with tablet:
        Tablet_input = st.text_input(
            label = "",
            placeholder = f"{name(player+1)}'s number of tablets")
    
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

make_line()
 
Calculate_score = st.button("Calculate Score")

if (Calculate_score):
    def players_rank(index):
        return int(sorted(players_total_points.values(), reverse=True)[index])

    def point_or_points(place):
        return [point if players_total_points[place] == 1 else points for point, points in [("point", "points")]][0]


    for player in range(int(players.split()[0])):
        player_number = player + 1
        if players_total_points[str(player_number)] == 1:
            st.subheader(f'{name(player_number)} got a total of {players_total_points[str(player_number)]} point')
        else:
            st.subheader(f'{name(player_number)} got a total of {players_total_points[str(player_number)]} points')
    
    make_line()

    places = ["winner", "second place", "third place"]

    winner = sorted(players_total_points, key=players_total_points.get, reverse=True)[0]
    second_place = sorted(players_total_points, key=players_total_points.get, reverse=True)[1]

    def write_winner():
        st.header(f"{name(winner)} is the winner with {players_total_points[winner]} {point_or_points(winner)}!")
    def write_second_place():
        st.header(f"{name(second_place)} is in second place with {players_total_points[second_place]} {point_or_points(second_place)}!")
    def write_third_place():
        st.header(f"{name(third_place)} is in third place with {players_total_points[third_place]} {point_or_points(third_place)}!")
    def write_tied_for_first_place():
        st.header(f"{name(winner)} and {name(second_place)} are tied for first place with {players_total_points[winner]} {point_or_points(winner)} each!")
    def all_tied_players():
        st.header(f"{name(winner)}, {name(second_place)} and {name(third_place)} are all tied for first place with {players_total_points[second_place]} {point_or_points(second_place)} each!")
    def write_tied_for_second_place():
        st.header(f"{name(second_place)} and {name(third_place)} are tied for second place with {players_total_points[second_place]} {point_or_points(second_place)} each!")
    def write_tied_for_third():
        st.header(f"{name(third_place)} and {name(fourth_place)} are tied for thrid place with {players_total_points[third_place]} {point_or_points(third_place)} each!")

    if int(players.split()[0]) > 2:
        third_place = sorted(players_total_points, key=players_total_points.get, reverse=True)[2]
        if int(players.split()[0]) > 3:
            fourth_place = sorted(players_total_points, key=players_total_points.get, reverse=True)[3]
        
        if players_rank(0) == players_rank(1):
            if players_rank(0) == players_rank(2):
                all_tied_players()
            
            elif players_rank(2) == players_rank(3):
                write_tied_for_first_place()
                write_tied_for_third()
            
            else:
                write_tied_for_first_place()
                write_third_place()
                
        elif players_rank(1) == players_rank(2):
            write_winner()
            write_tied_for_second_place()

        else:
            if players_rank(2) == players_rank(3):
                write_winner()
                write_second_place()
                write_tied_for_third()
            else:
                write_winner()
                write_second_place()
                write_third_place()

    elif players_rank(0) == players_rank(1):
        write_tied_for_first_place()

    else:
        write_winner()
        write_second_place()

if st.button("Reset"):
    #Reloads borwser
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

st.write("By: Elliot Wijoyo")