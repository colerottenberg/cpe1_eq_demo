import socket
import numpy as np
import matplotlib.pyplot as plt
import time


PORT = 5555
SCOPE_IP = "10.245.26.153"
FUNC_GEN_IP = "10.245.26.150"

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

# IP and port of the device

frequency = 800  # Frequency in Hz
command = f':SOUR1:FREQ {frequency}'

def set_frequency(s, frequency):
    command = f':SOUR1:FREQ {frequency}'
    send_command(s, command)    
    #Now check the frequency

def get_amplitude(s) -> float:
    query = ':MEAS:VAMP? CHAN1'
    response = send_query(s, query)
    print(f"Amplitude is {response} V")
    return float(response)

# Connect to devices
scope_socket = connect_to_device(scope_ip, PORT)
func_gen_socket = connect_to_device(func_gen_ip, PORT)

# Send commands and queries
# ...


# Try with TCP
def bode_data(fg_s, o_s, start, stop, step):
    freq = np.arange(start, stop, step)
    amp = []
    phase = []
    for f in freq:
        set_frequency(fg_s, f)
        time.sleep(0.1)
        amp.append(get_amplitude(o_s))
        time.sleep(0.1)
    return {'freq': freq, 'amp': amp, 'phase': phase}

def plot_bode(data):
    fig, ax = plt.subplots(2, 1, sharex=True)
    ax[0].semilogx(data['freq'], data['amp'])
    ax[0].set_ylabel('Amplitude (V)')
    ax[1].semilogx(data['freq'], data['phase'])
    ax[1].set_ylabel('Phase (deg)')
    ax[1].set_xlabel('Frequency (Hz)')
    return fig, ax

set_frequency(func_gen_socket, frequency)
get_amplitude(scope_socket)

# Disconnect from devices
disconnect_from_device(scope_socket)
disconnect_from_device(func_gen_socket)