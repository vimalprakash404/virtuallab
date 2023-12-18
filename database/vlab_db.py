from database.connection import client , database 
from database.schema import log 
import datetime

def create_log(username,usertype, action, course , assingment):
    data  ={ 
        "username" : username ,
        "usertype"  : usertype ,
        "action" :  action ,
        "course" :  course ,
        "assingment" :  assingment,
        "time" : datetime.datetime.utcnow()
    }
    log = database["log"]

    log.insert_one(data) 
    return 

