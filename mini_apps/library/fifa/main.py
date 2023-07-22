import pandas as pd
import sys, signal, os

## Show AVG
def avg(data,index):
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
def show_player(data,index):
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
def search(data,index):
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

def limitation(datas):
    showing = True
    first_index = 0
    last_index = 10

    while showing:
        if len(datas) < 10:
                print(datas.to_markdown(index=False))
        else:
            choose = input('\n\nNext[1], Back[2], Exit[3]\nYour choice: ')
            os.system('cls')
            if int(choose) == 1:
                first_index = last_index
                last_index += 10
                show = datas[first_index:last_index].to_markdown(index=False)
                if len(show) < 10:
                    print(show, '\n\nThis is the end\n')
                    showing = False     
                else:
                    print(show)
            elif int(choose) == 2:
                os.system('cls')
                showing = False
            elif int(choose) == 3:
                os._exit(os.EX_OK)
            else:
                print("\nThat is not a valid number.")

## Menu
def main():
    os.system('cls')
    signal.signal(signal.SIGINT, signal_handler)
    #print("")
    menu = True
    while menu:
        data = pd.read_csv("E:\\Latihan\\script\\Fifa\\data\\FIFA-21.csv", sep = ";").drop("player_id", axis=1).sort_values("potential", ascending=False)
        input_1 = int(input("Show AVG[1]\nShow Player[2]\nSearch by[3]\nYour Choice : "))
        os.system('cls')
        menu2 = True
        while menu2:
            input_2 = input("\nFiller By : ").lower()
            if input_2 in ["name", "nationality", "position", "overall", "age", "potential", "team"]:
                if input_1 == 1:
                    os.system('cls')
                    limitation(avg(data,input_2))
                elif input_1 == 2:
                    os.system('cls')
                    limitation(show_player(data,input_2))
                elif input_1 == 3:
                    os.system('cls')
                    limitation(search(data,input_2))
                elif input_1 == 99:
                    sys.exit(1)
                else:
                    os.system('cls')
                    print('That is not a valid number.\n')
                menu2 = False
            else :
                    os.system('cls')
                    print('That is not a valid number.\n')

main()