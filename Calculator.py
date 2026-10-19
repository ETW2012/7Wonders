import streamlit as st

st.title("7 Wonders Score Calculator")

players = st.selectbox(
    "Select number of players:",
    options = ["2 Players", "3 Players", "4 Players", "5 Players", "6 Players", "7 Players"]
)

point_types = [
    "Wonder Points (Board)",
    "Military Points (Red)",
    "Science Points (Green)",
    "Guild Points (Purple)",
    "Victory Points (Blue)",
    "Economic Points (Yellow)"
]

players_total_points = {}

for player in range(int(players.split()[0])):
    st.write("_______________________________________________________")
    total_points = 0
    user_input =st.text_input(f"Player {player+1} Number of coins (Not points from coins)")
    try:
        total_points += int(user_input)//3
    except ValueError:
        total_points += 0
    for point_type in point_types:
        user_input =st.text_input(f"Player {player+1} {point_type}")
        try:
            total_points += int(user_input)
        except ValueError:
            total_points += 0
    players_total_points.update({str(player+1): total_points})

st.write("_______________________________________________________")

def players_rank(index):
    return int(sorted(players_total_points.values(), reverse=True)[index])

for player in range(int(players.split()[0])):
    if players_total_points[str(player+1)] == 1:
        st.subheader(f'Player {player+1} got a total of {players_total_points[str(player+1)]} point')
    else:
        st.subheader(f'Player {player+1} got a total of {players_total_points[str(player+1)]} points')

st.write("_______________________________________________________")

winner = sorted(players_total_points, key=players_total_points.get, reverse=True)[0]
second_place = sorted(players_total_points, key=players_total_points.get, reverse=True)[1]

def write_winner():
     st.header(f"Player {winner} is the winner with {players_total_points[winner]} points!")
def write_second_place():
    st.header(f"Player {second_place} is in second place with {players_total_points[second_place]} points!")
def write_third_place():
    st.header(f"Player {third_place} is in third place with {players_total_points[third_place]} points!")
def write_tied_players():
    st.header(f"Players {winner} and {second_place} are tied for first place with {players_total_points[winner]} points each!")
def all_tied_players():
    st.header(f"Players {winner}, {second_place} and {third_place} are all tied for first place with {players_total_points[second_place]} points each!")

if int(players.split()[0]) > 2:
        third_place = sorted(players_total_points, key=players_total_points.get, reverse=True)[2]
        if players_rank(0) == players_rank(1):
            if players_rank(0) == players_rank(2):
                all_tied_players()
            else:
                write_tied_players()
                write_third_place()
                
        else:
            write_winner()
            write_second_place()
            write_third_place()

elif players_rank(0) == players_rank(1):
    write_tied_players()

else:
    write_winner()
    write_second_place()