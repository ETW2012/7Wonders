import streamlit as st


players = st.selectbox(
    "Select number of players:",
    options = ["2 Players", "3 Players", "4 Players", "5 Players", "6 Players", "7 Players"]
)

point_types = ["Number of coins", "Wonder Points", "Military Points (Red)", "Science Points (Green)", "Guild Points (Purple)", "Victory Points (Blue)", "Economic Points (Yellow)"]


for player in range(int(players.split()[0])):
    st.write("_______________________________________________________")
    for point_type in point_types:
        st.text_input(f"Player {player+1} {point_type}") 

st.write("_______________________________________________________")

for player in range(int(players.split()[0])):
    for point_type in point_types:
        total_points = {str("Player"+str(player+1)+" "+point_type)}
        st.write(f"Player {player+1} Got a total of: {total_points} points")


    


