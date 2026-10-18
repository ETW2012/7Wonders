import streamlit as st

st.markdown(
    """
    <style>
    .big-font {
        font-size:30px !important;
        color:#A9A9A9;
   </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .medium-font {
        font-size:20px !important;
        color:#A9A9A9;
   </style>
    """,
    unsafe_allow_html=True
)

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

def place_index(index):
    return int(sorted(players_total_points.values(), reverse=True)[index])

for player in range(int(players.split()[0])):
    if players_total_points[str(player+1)] == 1:
        st.markdown(f"<p class='medium-font'>Player {player+1} got a total of {players_total_points[str(player+1)]} point</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p class='medium-font'>Player {player+1} got a total of {players_total_points[str(player+1)]} points</p>", unsafe_allow_html=True)


winner = sorted(players_total_points, key=players_total_points.get, reverse=True)[0]
second_place = sorted(players_total_points, key=players_total_points.get, reverse=True)[1]
third_place = sorted(players_total_points, key=players_total_points.get, reverse=True)[2]

def write_winner():
     st.markdown(f'<p class="big-font">Player {winner} is the winner with {players_total_points[winner]} points!</p>', unsafe_allow_html=True)
def write_second_place():
    st.markdown(f'<p class="big-font">Player {second_place} is in second place with {players_total_points[second_place]} points!</p>', unsafe_allow_html=True)
def write_third_place():
    st.markdown(f'<p class="big-font">Player {third_place} is in third place with {players_total_points[third_place]} points!</p>', unsafe_allow_html=True)

if int(players.split()[0]) > 1:
        if place_index(0) == place_index(1):
            if place_index(0) == place_index(2):
                st.markdown(f'<p class="big-font">Players {winner}, {second_place} and {third_place} are all tied for first place with {players_total_points[second_place]} points each!</p>', unsafe_allow_html=True)
            else:
                st.markdown(f'<p class="big-font">Player {winner} and Player {second_place} are tied for first place with {players_total_points[winner]} points each!</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="big-font">Player {third_place} is in third place with {players_total_points[third_place]} points!</p>', unsafe_allow_html=True)
        else:
            write_winner()
            write_second_place()
            write_third_place()
else:
    write_winner()
    write_second_place()