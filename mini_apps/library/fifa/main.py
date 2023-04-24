import pandas as pd
import sys, signal, os

## Show AVG
def avg(data):
    index = input(str("Filter by: ")).lower()
    unique = data[index].unique() 
    result = []
    for i in unique:
        j = format(data.loc[data[index] == i].overall.mean(), ".2f")
        k = format(data.loc[data[index] == i].potential.mean(), ".2f")
        result.append([i, j, k])
    return pd.DataFrame(result,
                        columns=[
        index.capitalize(), "Overall", "Potential"
                        ])

## Show Player
def show_player(data):
    index = input(str("Filter by: ")).lower()
    unique = data[index].unique()
    result = []
    for i in unique:
        j = data.loc[data[index] == i]
        result.append([j.name, j.age, j.nationality, j.position, j.overall, j.potential, j.team])
    return pd.DataFrame(result, 
                        columns=[
        "Name", "Age", "Nationality", "Position", "Overall", "Potential", "Team"
                        ])

## Search
def search(data):
    index = input(str("Filter by: ")).lower()
    result = []
    for i in data.loc[data[index]]:
        result.append([i.name, i.nationality, i.position, i.overall, i.age, i.potential, i.team])
    return pd.DataFrame(result,
                        columns=[
        "Name", "Nationality", "Position", "Overall", "Age", "Potential", "Team"
                        ])                        

## Ctrl+C trigger
def signal_handler(signal, frame):
    print("\n==================")
    print("Execution aborted by User")
    print("====================")
    sys.exit(1)

## Menu
def menu():
    signal.signal(signal.SIGINT, signal_handler)
    print(1)
    menu = False
    while menu == False:
        data = pd.read_csv("E:\\Latihan\\script\\Fifa\\data\\FIFA-21.csv", sep = ";")
        input_1 = int(input("Show AVG[1]\nShow Player[2]\nSearch by[3]\nYour Choice : "))
        if input_1 == 1:
            datas = avg(data)
            print(datas.sort_values("Potential", ascending=False).to_markdown(index=False))
        elif input_1 == 2:
            datas = show_player(data)
            print(datas.sort_values("Potential", ascending=False).to_markdown(index=False))
        elif input_1 == 3:
            datas = search(data)
            print(datas.sort_values("Potential", ascending=False).to_markdown(index=False))
        elif input_1 == 99:
            sys.exit(1)
        else:
            print('\nThat is not a valid number.')

menu()