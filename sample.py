import docker

def stop_container(container_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        print(f"Container {container_name} stopped successfully.")
    except docker.errors.NotFound:
        print(f"Container {container_name} not found.")
    except docker.errors.APIError as e:
        print(f"Error stopping container {container_name}: {e}")

# Replace 'my-vscode-server' with the actual name or ID of your container
stop_container('76cf77e91d0aa6c0174693b67fff2be88399346b39575496d056684294f84c1a')
