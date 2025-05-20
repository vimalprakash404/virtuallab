from database.connection import client , database 
from database.schema import log 
import datetime
from bson import ObjectId  # Add this import at the top

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



def create_container_log(username,container_id , status, type , assignmentId , courseId , port):
    data = {
        'username' : username ,
        "container_id" : container_id ,
        "type" : type ,
        "status" : status ,
        "start_time" : datetime.datetime.utcnow(),
        "end_time" : None,
        "time" : datetime.datetime.utcnow(),
        "assignmentId" : assignmentId,
        "courseId" : courseId,
        "port" : port
    }

    container_log = database["container_log"]
    result = container_log.insert_one(data)
    return result.inserted_id

def get_container_log(_id):
    container_log = database["container_log"]
    try:
        query = {"_id": ObjectId(_id)}
    except Exception:
        query = {"_id": _id}
    result = container_log.find_one(query)
    if result and "_id" in result:
        result["_id"] = str(result["_id"])
    return result


def update_container_log(container_id, additional_data=None):
    container_log = database["container_log"]
    print("updateing container_id",container_id)
    query = {"container_id": container_id, "end_time": None}
    update_data = {"$set": {"end_time": datetime.datetime.utcnow(), "status" : "Stop"}}
    if additional_data:
        update_data["$set"].update(additional_data)
    container_log.update_one(query, update_data)


def get_live_containers():
    container_log = database["container_log"]

    # Calculate the start time 5 seconds ago from the current time
    start_time_limit = datetime.datetime.utcnow() - datetime.timedelta(seconds=10)

    # Query to find documents with status "Live" and start time within the last 5 seconds
    query = {
        "status": "Live",
        "time": {"$lte": start_time_limit}
    }

    # Projection to include only the "container_id" field in the result
    projection = {"_id": 0, "container_id": 1}

    # Find documents with the specified query and projection
    result = container_log.find(query, projection)

    # Extract container_id values from the result
    container_ids = [doc["container_id"] for doc in result]

    return container_ids

def update_conatiner_time(container_id):
    print("containerid", container_id)
    container_log = database["container_log"]
    print("updateing container_id",container_id)
    query = {"container_id": container_id}
    update_data = {"$set": {"time": datetime.datetime.utcnow()}}
    if container_log.find_one({"container_id": container_id}):
        container_log.update_one(query, update_data)
        return True
    else :
        return False

