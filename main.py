'''
@author: Christian Ryding
'''
import time
from bets_api import find_events, get_ended_events
from file_io import create_files
from calc import calc_sum

# create necessary files
create_files()

test = True
while(test == True):
    x = 0
    print("Program is running.....{}".format(x))
    find_events()
    get_ended_events()
    x=x+1
    calc_sum()
    time.sleep(240)      
