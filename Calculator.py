import streamlit as st

st.title("7 Wonders Score Calculator")

def make_line():
    st.write("_______________________________________________________")

make_line()

players = st.selectbox(
    "Select number of players:",
    options = ["2 Players", "3 Players", "4 Players", "5 Players", "6 Players", "7 Players"]
)

point_types = [
    "Wonder Points (Board)",
    "Military Points (Red)",
    "Guild Points (Purple)",
    "Victory Points (Blue)",
    "Economic Points (Yellow)"
]

players_total_points = {}

def test_if_integer_and_square(value):
    try:
        value = int(value)
        return value ** 2
    except ValueError:
        return 0

for player in range(int(players.split()[0])):
    make_line()
    total_points = 0
    coin_input =st.text_input(f"Player {player+1} Number of coins (Not points from coins)")
    try:
        total_points += int(coin_input)//3
    except ValueError:
        total_points += 0
    Compass_input = st.text_input(f"Player {player+1} Number of Compass")
    Gear_input = st.text_input(f"Player {player+1} Number of Gears")
    Tablet_input = st.text_input(f"Player {player+1} Number of Tablets")
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

    for point_type in point_types:
        user_input =st.text_input(f"Player {player+1} {point_type}")
        try:
            total_points += int(user_input)
        except ValueError:
            total_points += 0
    players_total_points.update({str(player+1): total_points})

make_line()
 
Calculate_score = st.button("Calculate Score")

if (Calculate_score):
    def players_rank(index):
        return int(sorted(players_total_points.values(), reverse=True)[index])

    for player in range(int(players.split()[0])):
        if players_total_points[str(player+1)] == 1:
                st.subheader(f'Player {player+1} got a total of {players_total_points[str(player+1)]} point')
        else:
            st.subheader(f'Player {player+1} got a total of {players_total_points[str(player+1)]} points')

    make_line()

    winner = sorted(players_total_points, key=players_total_points.get, reverse=True)[0]
    second_place = sorted(players_total_points, key=players_total_points.get, reverse=True)[1]

    def point_or_points (place):
        return [point if players_total_points[place] == 1 else points for point, points in [("point", "points")]][0]

    def write_winner():
        st.header(f"Player {winner} is the winner with {players_total_points[winner]} {point_or_points(winner)}!")
    def write_second_place():
        st.header(f"Player {second_place} is in second place with {players_total_points[second_place]} {point_or_points(second_place)}!")
    def write_third_place():
        st.header(f"Player {third_place} is in third place with {players_total_points[third_place]} {point_or_points(third_place)}!")
    def write_tied_players_for_first_place():
        st.header(f"Players {winner} and {second_place} are tied for first place with {players_total_points[winner]} {point_or_points(winner)} each!")
    def all_tied_players():
        st.header(f"Players {winner}, {second_place} and {third_place} are all tied for first place with {players_total_points[second_place]} {point_or_points(second_place)} each!")
    def write_tied_players_for_second_place():
        st.header(f"Players {second_place} and {third_place} are tied for second place with {players_total_points[second_place]} {point_or_points(second_place)} each!")

    if int(players.split()[0]) > 2:
        third_place = sorted(players_total_points, key=players_total_points.get, reverse=True)[2]
        if players_rank(0) == players_rank(1):
            if players_rank(0) == players_rank(2):
                all_tied_players()
            else:
                write_tied_players_for_first_place()
                write_third_place()
                
        elif players_rank(1) == players_rank(2):
            write_winner()
            write_tied_players_for_second_place()
        
        else:
            write_winner()
            write_second_place()
            write_third_place()

    elif players_rank(0) == players_rank(1):
        write_tied_players_for_first_place()

    else:
        write_winner()
        write_second_place()