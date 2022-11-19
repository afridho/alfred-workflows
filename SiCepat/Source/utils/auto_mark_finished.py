import json
from datetime import datetime
import os
from utils import crud

## variables
time_format = "%Y-%m-%d %H:%M"
parse_time_now = datetime.now()
time_now = parse_time_now.strftime(time_format)

class doCheck:    
    @staticmethod
    def compare_time(no_resi=None, last_update=None, days=None): # mark finished after days variable
        if last_update and int(days) != 0:
            d1 = datetime.strptime(get_time_value(no_resi), time_format)
            d2 = datetime.strptime(time_now, time_format)
            hoursOfDays = ((d2-d1).days)
            if hoursOfDays >= int(days):
                remove_file(no_resi)
                crud.markFinishedData(no_resi)
                return True
            else:
                return False
        else:
            return False
        
def get_time_value(no_resi=None):
        with open(crud.fileName) as f:
            data = json.load(f)
            list1 = list ((p_id.get('last_update') for p_id in data if p_id.get('no_resi') == no_resi)) 
            return ''.join(list1)           

def remove_file(no_resi=None):
    if os.path.exists(f"./Cache/{no_resi}.json"):
        os.remove(f"./Cache/{no_resi}.json")

# be = doCheck()
# print(be.compare_time("003079501392","2022-08-21 09:56", "3"))



