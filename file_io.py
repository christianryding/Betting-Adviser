import os

# create files needed for program
def create_files():
    if os.path.exists('bets.csv') == False:
        print('bets.csv dont exist!, lets create it..')
        f= open("bets.csv","w+")
        if os.path.exists('bets.csv') == True:
            print('created bets.csv')
        f.close()
    
    if os.path.exists('bets_summary.csv') == False:
        print('bets_summary.csv dont exist!, lets create it..')
        f= open("bets_summary.csv","w+")
        if os.path.exists('bets_summary.csv') == True:
            print('created bets_summary.csv')
        f.close()