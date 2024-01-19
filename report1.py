import socket


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

frequency = 900  # Frequency in Hz
command = f':SOUR1:FREQ {frequency}'

def set_frequency(function_generator_ip, frequency):
    command = f':SOUR1:FREQ {frequency}'
    send_command(function_generator_ip, PORT, command)    
    #Now check the frequency
    query = ':SOUR1:FREQ?'
    response = send_query(func_gen_ip, PORT, query)
    print(f"Frequency set to {response} Hz")
    assert float(response) == float(frequency), "Frequency not set correctly"
    return float(response)
    
def get_amplitude(oscope_ip) -> float:
    query = ':MEAS:VAMP?'
    response = send_query(oscope_ip, PORT, query)
    print(f"Amplitude is {response} V")
    return float(response)
# Try with TCP
set_frequency(func_gen_ip, frequency)
get_amplitude(scope_ip)