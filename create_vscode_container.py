import docker
import socket
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess 



app = Flask(__name__)
CORS(app)


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

def create_vscode_container_node(repo_url):
    client = docker.from_env()

    # Build the Docker image
    image, _ = client.images.build(path='.', tag='my-vscode-server', dockerfile='Dockerfile')

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
        assingment_id = data["assingment_id"]
        course_id= data["course_id"]
        if (copy_file_to_container(container_id,username,assingment_id,course_id)):
            result={"error" : False , "message" : "data copied"}
            return jsonify(result)
        else :
            result={"error" : True , "message" : "Some Error"}
            return jsonify(result)


@app.route('/create/lab', methods=['POST'])
def post_example():
    if request.method == 'POST':
        data = request.get_json()
        # Do something with the posted data
        if (not("repo" in data)):
            result={"error" : True , "message" : "please the repo"}
            return jsonify(result)
        else :
            container_id, allocated_port = create_vscode_container(data["repo"])
            result =  {"error" : False  ,"container_id":container_id, "port" : allocated_port}
            return jsonify(result)

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
    container_id = data["container_id"]
    if remove_container_by_id(container_id):
        result = {"error" :False , "message" :  "removed successfully"}
        return jsonify(result)
    else :
        result = {"error" :True , "message" :  "connot removed "}
        return jsonify(result)
@app.route('/', methods=['GET'])
def hello():
    return 'Hello, World!'
if __name__ == "__main__":
    # Set the Git repository URL, container name
    repo_url = "https://github.com/vimalprakash404/python.git"
    container_name = "vscode-containers-4569"
    api_port = 3005
    app.run(host='0.0.0.0', port=api_port)

    # Create the VS Code Server container


