import docker
import socket
from flask import Flask, request, jsonify 
from flask_apscheduler import APScheduler
import flask
from flask_cors import CORS
import subprocess 
from UiSample import samlpe ,create_lab_template , open_lab_template , opener as open_page

from database import vlab_db as database

import datetime



import git

app = Flask(__name__)
CORS(app)
scheduler = APScheduler()

app.config['SCHEDULER_API_ENABLED'] = True
app.config['SCHEDULER_JOB_DEFAULTS'] = {'misfire_grace_time': 5}

def scheduled_task():
    data= database.get_live_containers()
    for i in data :
        # if remove_container_by_id(container_id=i):
        #     print("container removed : ", i)
        pass
    print(f"Task executed at {datetime.datetime.utcnow()}")
    print(data)


scheduler.add_job(id='scheduled_task', func=scheduled_task, trigger='interval', seconds=1)
scheduler.start()

def is_git_repo(url):
    try:
        git.Repo.clone_from(url, 'temp_clone_directory', depth=1)
        return True
    except git.exc.GitCommandError:
        return False



# function to check image is exist or not 
def image_exists(client , image_name ):
    try : 
        client.images.get(image_name)
        return True 
    except docker.errors.ImageNotFound:
        return False 





def get_free_tcp_port():
    # Create a socket to find an available port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 0))
        return s.getsockname()[1]

def create_vscode_container(repo_url):
    client = docker.from_env()
    image_name = "vs-code-python"

    if  not image_exists(client, image_name):
        # Build the Docker image
        image, _ = client.images.build(path='.', tag=image_name, dockerfile='Sample')
        print("image created")

    # Find an available port
    port = get_free_tcp_port()

    # Create and run the Docker container
    container = client.containers.run(
        image_name,
        detach=True,
        ports={f'{port}/tcp': port},
        environment={'GIT_REPO': repo_url, 'PORT': port},
        tty=True,
    )
    return container.id, port


def open_vscode_container(repo_url ,filepath):
    client = docker.from_env()
    image_name = filepath
    build_args = {'FOLDER': filepath}
    # if  not image_exists(client, image_name):
    #     # Build the Docker image
    image, _ = client.images.build(path='.', tag=image_name, dockerfile='PythonOpenContainer',buildargs=build_args)
    print("image created")

    # Find an available port
    port = get_free_tcp_port()

    # Create and run the Docker container
    container = client.containers.run(
        image_name,
        detach=True,
        ports={f'{port}/tcp': port},
        environment={'GIT_REPO': repo_url, 'PORT': port, 'FOLDER' : filepath},
        tty=True,
    )
    return container.id, port


def create_vscode_container_node(repo_url):
    image_name="vs-code-nodejs"
    client = docker.from_env()

    # Build the Docker image
    image, _ = client.images.build(path='.', tag=image_name, dockerfile='Dockerfile')

    # Find an available port
    port = get_free_tcp_port()

    # Create and run the Docker container
    container = client.containers.run(
        image_name,
        detach=True,
        ports={f'{port}/tcp': port},
        environment={'GIT_REPO': repo_url, 'PORT': port},
        tty=True,
    )
    return container.id, port

def create_jupiter_container(repo_url):
    client = docker.from_env()
    # Build the Docker image
    image, _ = client.images.build(path='.', tag='my-vscode-server', dockerfile='Dockerfile')
    # Find an available port
    port = get_free_tcp_port()
    # Create and run the Docker container
    container = client.containers.run(
        image,
        detach=True,
        ports={f'{port}/tcp': port},
        environment={'GIT_REPO': repo_url, 'PORT': port},
        tty=True,
    )
    return container.id, port

def remove_container_by_id(container_id):
    client = docker.from_env()
    try :
        container = client.containers.get(container_id)
        container.stop()
        container.remove()
        database.update_container_log(container_id=container_id)
        return True
    except docker.errors.NotFound :
        return False


def copy_file_to_container(container_id, name , assingment_id , course_id):
    script_path = "copy_file.sh"
    script_arguments =  [container_id,name+"_"+assingment_id+"_"+course_id]
    try :
        subprocess.run(['sh',script_path]+script_arguments, check= True)
        return True
    except subprocess.CalledProcessError as e:
        return False


@app.route("/savetoserver", methods=['POST'])
def post_save():
    if request.method == 'POST' : 
        data = request.get_json()
        username  = data["username"]
        container_id = data["container_id"]
        print(container_id)
        assingment_id = data["assignment_id"]
        course_id= data["course_id"]
        if (copy_file_to_container(container_id,username,assingment_id,course_id)):
            database.create_log(username= data["username"],usertype = "student" , action="saved", course= data["course_id"], assingment= data["assignment_id"])
            result={"error" : False , "message" : "data copied"}
            return jsonify(result)
        else :
            result={"error" : True , "message" : "Some Error"}
            return jsonify(result)

@app.route("/update/time")
def container_time_updater(method=["POST"]):
    if request.method ==  "GET" :
        data = request.get_json()
        print("data")
        container_id = data["container_id"]
        if database.update_conatiner_time(container_id) :
            result = {"message" : "upadted data"}
        else :
            result = {"message" : "contaner not exist"}
        return jsonify(result)
@app.route('/create/lab', methods=['POST'])
def post_example():
    if request.method == 'POST':
        data = request.get_json()
        print(data["repo"])
        # Do something with the posted data
        if (not("repo" in data)):
            result={"error" : True , "message" : "please the repo"}
            return jsonify(result)
        elif (not("username" in data)):
            result =  {"error" :  True , "message" :  "please enter the username"}
            return jsonify(result)
        
        elif (not("course_id" in data)) : 
            result =  {"error" :  True , "meesage" : "please enter the course"}
            return jsonify(result)
        elif (not("assignment_id" in data)) :
            result = {"error" : True , "message" : "please enter the assingment"}
            return jsonify(result)
        else :
            # if(not is_git_repo(data["repo"])):
            #     result = {"error" : True , "message" : "not valid reopository"}
            #     return jsonify(result)

            print(data["repo"])
            container_id, allocated_port = create_vscode_container(data["repo"])
            database.create_log(username= data["username"],usertype = "student" , action="create and open ", course= data["course_id"], assingment= data["assignment_id"])
            database.create_container_log(container_id=container_id, type="Create" , status="Live")
            result =  {"error" : False  ,"container_id":container_id, "port" : allocated_port}
            return jsonify(result)


@app.route('/open/lab/python', methods=['POST'])
def open_python_lab():
    if request.method == 'POST':
        data = request.get_json()
        # Do something with the posted data
        username = data["username"]
        assingment_id = data["assingment_id"]
        course_id = data["course_id"]
        filepath="files/"+username+"_"+assingment_id+"_"+course_id
        print("/"+username+"_"+assingment_id+"_"+course_id)

        container_id, allocated_port = open_vscode_container(data["repo"],filepath)
        result =  {"error" : False  ,"container_id":container_id, "port" : allocated_port}
        response = flask.jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/create/lab/node', methods=['POST'])
def node_example():
    if request.method == 'POST':
        data = request.get_json()
        # Do something with the posted data
        if (not("repo" in data)):
            result={"error" : True , "message" : "please the repo"}
            return jsonify(result)
        else :
            container_id, allocated_port = create_vscode_container_node(data["repo"])
            result =  {"error" : False  ,"container_id":container_id, "port" : allocated_port}
            return jsonify(result)

@app.route('/create/jupiter', methods=['POST'])
def post_jupiter():
    if request.method == 'POST':
        data = request.get_json()
        # Do something with the posted data
        if (not("repo" in data)):
            result={"error" : True , "message" : "please the repo"}
            return jsonify(result)
        else :
            container_id, allocated_port = create_jupiter_container(data["repo"])
            result =  {"error" : False  ,"container_id":container_id, "port" : allocated_port}
            return jsonify(result)

@app.route('/copy/data', methods=['POST'])
def copy_data():
    data = request.get_json()
    if (not ("container_id" in data)):
        result = {"error" : True , "message" : "please enter container id"}
        return jsonify(result)
    else :
        script_path = "copy_file.sh"
        script_arguments =  [data["container_id"],data["name"]]
        try :
            subprocess.run(['sh',script_path]+script_arguments, check= True)
            result = {"error" : False  , "message" : "created successfully"}
            return jsonify(result)
        except subprocess.CalledProcessError as e:
            result = {"error" : True , "error_details" : e}
            return jsonify(result)

@app.route("/remove", methods= ["POST"])
def remove_container(): 
    data = request.get_json()
    if (not ("container_id" in data)): 
        return jsonify({"error" : True , "message" : "container id not found"})
    elif (not ("username" in data)) :
        return jsonify({"error"  : True , "message" : "username not found"})
    elif (not ("course_id" in data)) :
        return jsonify({"error" : True , "message" :  "course_id not found "})
    elif (not ("assignment_id" in data)) : 
        return jsonify({"error" :  True , "message" :  "assignment_id not found"})
    elif (not ("user_type" in data)):
        return jsonify({"error" : True , "message" : "user_type not found"  })
    else :
        container_id = data["container_id"]
        if remove_container_by_id(container_id):
            database.create_log(username= data["username"],usertype = data["user_type"] , action="container closed", course= data["course_id"], assingment= data["assignment_id"])
            result = {"error" :False , "message" :  "removed successfully"}
            return jsonify(result)
        else :
            result = {"error" :True , "message" :  "not valid container id "}
            return jsonify(result)
@app.route('/', methods=['GET'])
def hello():
    return 'Hello, World!'


@app.route('/render')
def render():
    return samlpe(request)

@app.route("/labcreater")
def creater():
    return create_lab_template(request)

@app.route("/opener")
def ui_opener():
    return open_page(request)
@app.route("/openvscode/<port_no>/<container_id>")
def opener(port_no,container_id):
    return open_lab_template(request,port_no,container_id)

if __name__ == "__main__":
    
    api_port = 3005
    app.run(host='0.0.0.0', port=api_port,debug=True)

    # Create the VS Code Server container


