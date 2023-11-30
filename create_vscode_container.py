import docker
import socket
from flask import Flask, request, jsonify



app = Flask(__name__)
def get_free_tcp_port():
    # Create a socket to find an available port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 0))
        return s.getsockname()[1]

def create_vscode_container(repo_url):
    client = docker.from_env()

    # Build the Docker image
    image, _ = client.images.build(path='.', tag='my-vscode-server', dockerfile='Sample')

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
        

if __name__ == "__main__":
    # Set the Git repository URL, container name
    repo_url = "https://github.com/vimalprakash404/python.git"
    container_name = "vscode-containers-4569"
    api_port = 3001
    app.run(host='0.0.0.0', port=api_port)

    # Create the VS Code Server container

