import csv
import statistics
import plotly.graph_objs as go
from plotly.offline import plot

matches = []  # List to hold tuples of matches

# Using DictReader to read CSV as a dictionary
with open("Match_stats.csv", mode="r") as csv_file:
    dataFrame = csv.DictReader(csv_file)  # Automatically maps header to dictionary keys

    for row in dataFrame:
        # Creating a tuple from the values of the row
        match = (
            row['Season'],              # index 0
            row['Date'],                # index 1
            row['Referee'],             # index 2
            row['HomeTeam'],            # index 3
            row['AwayTeam'],            # index 4
            row['FullTime'],            # index 5
            row['Halftime'],            # index 6
            row['HomeGoals'],           # index 7
            row['HomeGoalsHalfTime'],   # index 8
            row['HomeShots'],           # index 9
            row['HomeShotsOnTarget'],   # index 10
            row['HomeCorners'],         # index 11
            row['HomeFouls'],           # index 12
            row['HomeYellowCards'],     # index 13
            row['HomeRedCards'],        # index 14
            row['AwayGoals'],           # index 15
            row['AwayGoalsHalfTime'],   # index 16
            row['AwayShots'],           # index 17
            row['AwayShotsOnTarget'],   # index 18
            row['AwayCorners'],         # index 19
            row['AwayFouls'],           # index 20
            row['AwayYellowCards'],     # index 21
            row['AwayRedCards']         # index 22
        )
        matches.append(match)  # Append each match tuple to the list

# Function to prompt the user for input
def user_input():
    print("1. Red Cards Per Season")
    print("2. Goals Per Season")
    print("3. Average Yellow Cards Per Referee")
    print("4. Average Goals Per Match")
    print()
    user_input = int(input("Please input an option (1, 2, 3 or 4): "))
    return user_input

# Function to handle options based on user input
def options():
    option = user_input()  # Get the user's choice

    # Call the corresponding function based on the option selected
    if option == 1:
        red_cards_per_seasons()
    elif option == 2:
        goals_per_season()
    elif option == 3:
        average_yellows_per_ref()
    elif option == 4:
        average_goals_per_match()
    else:
        options()  # Recursively prompt the user if the input is invalid

# Helper function to extract the year from the 'Season' string
def getYear(yearStr):
    return int(yearStr[0:4])

# Function to calculate and display red cards per season
def red_cards_per_seasons():
    seasons = []
    redCards = []

    currentYear = 2010
    annualRedCards = 0

    # Iterate through all matches and calculate red cards per season
    for row in matches:
        if getYear(row[0]) == currentYear:
            annualRedCards += int(row[14]) + int(row[22])  # Add red cards for this match
        else:
            redCards.append(annualRedCards)
            seasons.append(currentYear)
            annualRedCards = 0
            annualRedCards += int(row[14]) + int (row[22])  # Reset for next season
            currentYear += 1  # Move to next season

    redCards.append(annualRedCards)
    seasons.append(currentYear)

    graph(seasons, redCards, "Red Cards Per Season", "Seasons", "Red Cards")  # Plot the graph

# Function to calculate the average yellow cards per referee
def average_yellows_per_ref():
    # Initialize lists for referees, yellow cards, and number of matches
    refList = []
    yellowCardsList = []
    matchesPerRef = []

    # Identify unique referees
    for row in matches:
        ref = row[2]  # Referee name
        if ref not in refList:
            refList.append(ref)
            yellowCardsList.append(0)  # Initialize yellow card count
            matchesPerRef.append(0)  # Initialize match count

    # Calculate yellow cards for each referee
    for row in matches:
        ref = row[2]
        yellowCards = int(row[13]) + int(row[21])  # Sum yellow cards

        index = refList.index(ref)  # Find the index of the referee in refList
        yellowCardsList[index] += yellowCards
        matchesPerRef[index] += 1

    # Compute average yellow cards per referee
    for i in range(len(refList)):
        if matchesPerRef[i] > 0:
            yellowCardsList[i] = round(yellowCardsList[i] / matchesPerRef[i], 2)  # Compute average

    graph(refList, yellowCardsList, "Average Yellow Cards Per Referee", "Referee", "Average Yellow Cards")  # Plot the graph

# Function to calculate goals per season
def goals_per_season():
    matchGoals = 0
    goalsPerMatchList = []
    
    for row in matches:
        matchGoals = int(row[7]) + int(row[15])  # Sum home and away goals for the match
        goalsPerMatchList.append(matchGoals)

    # Calculate the mean of goals per match
    meanGoals = statistics.mean(goalsPerMatchList)
    print("The average goals per game is: ", round(meanGoals, 2))

# Function to calculate goals per match for each season
def average_goals_per_match():
    seasons = []  # Various football seasons for graphing
    totalGoals = []  # Total goals per season
    
    currentYear = 2010
    annualGoalsTotal = 0
    
    for row in matches:
        if getYear(row[0]) == currentYear:
            annualGoalsTotal += int(row[7]) + int(row[15])  # Sum home and away goals
        else:
            totalGoals.append(annualGoalsTotal)
            seasons.append(currentYear)
            annualGoalsTotal = 0
            currentYear += 1  # Move to next season
            annualGoalsTotal += int(row[7]) + int(row[15])

    totalGoals.append(annualGoalsTotal)
    seasons.append(currentYear)

    graph(seasons, totalGoals, "Goals scored in various seasons", "Seasons", "Goals")  # Plot the graph

# Function to plot the graph
def graph(X, Y, Title, XTitle, YTitle):
    # Create the graph using Plotly
    data = [go.Bar(x=X, y=Y)]

    layout = go.Layout(
        title=Title,
        xaxis=dict(title=XTitle),
        yaxis=dict(title=YTitle),
    )

    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename="Bar_chart.html")  # Save the plot as an HTML file

# Call the options function to start the program
options()