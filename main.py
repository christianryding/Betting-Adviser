'''
@author: Christian Ryding
'''
import time
from bets_api import find_events, get_ended_events
from file_io import create_files

# # create necessary files
create_files()

print('Program is running.....')

test = True
while(test == True):
    find_events()
    get_ended_events()
    time.sleep(240)                 
