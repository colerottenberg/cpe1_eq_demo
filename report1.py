import socket
import numpy as np
import matplotlib.pyplot as plt
import time

PORT = 5555
SCOPE_IP = "10.245.26.102"
FUNC_GEN_IP = "10.245.26.230"

def connect_to_device(ip, port, protocol=socket.SOCK_STREAM):
    s = socket.socket(socket.AF_INET, protocol)
    s.settimeout(5)
    try:
        s.connect((ip, port))
        return s
    except socket.error as err:
        print(f"Connection error: {err}")
        return None

def disconnect_from_device(s):
    s.close()

def send_query(s, message):
    try:
        s.sendall(message.encode() + b'\n')
        data = s.recv(1024)
        return data.decode()
    except socket.timeout:
        return "No response (timeout)"
    except socket.error as err:
        return f"Connection error: {err}"

def send_command(s, message):
    s.sendall(message.encode() + b'\n')
    return f"Command {message} sent"


def set_frequency(s, frequency):
    command = f':SOUR1:FREQ {frequency}'
    send_command(s, command)    
    #Now check the frequency

def get_amplitude(s) -> float:
    query = ':MEAS:VAMP? CHAN1'
    response = send_query(s, query)
    print(f"Amplitude is {response} V")
    return float(response)

def bode_data(fg_s, o_s, start, stop, step):
    freq = np.arange(start, stop, step)
    amp = []
    for f in freq:
        set_frequency(fg_s, f)
        amp.append(get_amplitude(o_s))
        time.sleep(0.1)
    return {'freq': freq, 'amp': amp}

def plot_bode(data):
    plt.plot(data['freq'], np.log(data['amp']))
    plt.ylabel('Power (dB)')
    plt.xlabel('Frequency (Hz)')
    plt.title('Bode Plot')
    plt.savefig('bode.png')
    plt.show() 

# IP and port of the device

# Connect to devices
scope_socket = connect_to_device(SCOPE_IP, PORT)
func_gen_socket = connect_to_device(FUNC_GEN_IP, PORT)

# frequency = 800  # Frequency in Hz
# command = f':SOUR1:FREQ {frequency}'

#set_frequency(func_gen_socket, frequency)
#get_amplitude(scope_socket)

data = bode_data(func_gen_socket, scope_socket, 100, 3000, 25)

plot_bode(data)

# Disconnect from devices
disconnect_from_device(scope_socket)
disconnect_from_device(func_gen_socket)