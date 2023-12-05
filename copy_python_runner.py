import subprocess 

script_path = "copy_file.sh"

script_arguments =  ["887e293336dc162e486d86a4e3681c0d5bb6b8dc8ff562a2be8864cc6d580120","amal"]

try :
    subprocess.run(['sh',script_path]+script_arguments, check= True)
    print("Shell script executed successfully")
except subprocess.CalledProcessError as e:
    print(f"Error executing shell script: {e}")