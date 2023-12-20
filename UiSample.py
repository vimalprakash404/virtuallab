from flask import Flask , render_template
import time 
def samlpe(request):
    current_domain = request.url_root
    host_with_port = request.host
    print(host_with_port)
    # Split the host and port
    host, port = host_with_port.split(':', 1) if ':' in host_with_port else (host_with_port, None)
    print(host)
    return render_template('front.html', message='Hello from Flask!'+current_domain, domain=current_domain, host= "http://"+host)



def create_lab_template(request):
    current_domain = request.url_root
    host_with_port = request.host
    print(host_with_port)
    # Split the host and port
    host, port = host_with_port.split(':', 1) if ':' in host_with_port else (host_with_port, None)
    print(host)
    return render_template('front.html', message='Hello from Flask!'+current_domain, domain=current_domain, host= "http://"+host)

def open_lab_template(request,port_no,container_id):
    current_domain = request.url_root
    host_with_port = request.host
    print(host_with_port)
    # Split the host and port
    host, port = host_with_port.split(':', 1) if ':' in host_with_port else (host_with_port, None)
    print(host)
    time.sleep(5)
    return render_template('VLabView.html', message='Hello from Flask!'+current_domain, domain=current_domain, host= "http://"+host+":"+port_no ,container_id = container_id)


def opener(request):
    current_domain = request.url_root
    host_with_port = request.host
    print(host_with_port)
    # Split the host and port
    host, port = host_with_port.split(':', 1) if ':' in host_with_port else (host_with_port, None)
    print(host)
    return render_template('opener.html', message='Hello from Flask!'+current_domain, domain=current_domain, host= "http://"+host)