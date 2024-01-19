import socket
import numpy as np
import matplotlib.pyplot as plt
import time


PORT = 5555

def send_query(ip, port, message, protocol=socket.SOCK_STREAM):
    with socket.socket(socket.AF_INET, protocol) as s:
        s.settimeout(5)
        try:
            s.connect((ip, port))
            s.sendall(message.encode() + b'\n')
            data = s.recv(1024)
            return data.decode()
        except socket.timeout:
            return "No response (timeout)"
        except socket.error as err:
            return f"Connection error: {err}"
def send_command(ip,port,message,protocol=socket.SOCK_STREAM):
    # same as above except do not expect a response
    with socket.socket(socket.AF_INET, protocol) as s:
        s.connect((ip, port))
        s.sendall(message.encode() + b'\n')
    return f"Command {message} sent"

# IP and port of the device
scope_ip = "10.245.26.153"
func_gen_ip = "10.245.26.150"

frequency = 800  # Frequency in Hz
command = f':SOUR1:FREQ {frequency}'

def set_frequency(function_generator_ip, frequency):
    command = f':SOUR1:FREQ {frequency}'
    send_command(function_generator_ip, PORT, command)    
    #Now check the frequency

def get_amplitude(oscope_ip) -> float:
    query = ':MEAS:VAMP? CHAN1'
    response = send_query(oscope_ip, PORT, query)
    print(f"Amplitude is {response} V")
    return float(response)

def get_phase(oscope_ip) -> float:
    query = ':MEAS:VPH?'
    response = send_query(oscope_ip, PORT, query)
    print(f"Phase is {response} deg")
    return float(response)
# Try with TCP
def bode_data(fg_ip, o_ip, start, stop, step):
    freq = np.arange(start, stop, step)
    amp = []
    phase = []
    for f in freq:
        set_frequency(fg_ip, f)
        time.sleep(0.1)
        amp.append(get_amplitude(o_ip))
        phase.append(get_phase(o_ip))
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

set_frequency(func_gen_ip, frequency)
get_amplitude(scope_ip)

# w0 = 723
#data = bode_data(func_gen_ip, scope_ip, 0, 2000, 1)
#plot_bode(data)