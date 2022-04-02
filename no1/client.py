import socket
import json
import logging
import threading
import datetime
import random
from tabulate import tabulate

server_address = ('172.16.16.104', 12000)

def make_socket(destination_address='localhost',port=12000):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)
        return sock
    except Exception as ee:
        logging.warning(f"error {str(ee)}")

def deserealisasi(s):
    logging.warning(f"deserialisasi {s.strip()}")
    return json.loads(s)
    

def send_command(command_str):
    alamat_server = server_address[0]
    port_server = server_address[1]
    sock = make_socket(alamat_server,port_server)

    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        data_received="" #empty string
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = deserialisasi(data_received)
        logging.warning("data received from server:")
        return hasil
    except Exception as ee:
        logging.warning(f"error during data receiving {str(ee)}")
        return False

def get_data_player(nomor=0):
    cmd=f"get_data_player {nomor}\r\n\r\n"
    hasil = send_command(cmd)
    if (hasil):
        pass
    else:
        print("kegagalan pada data transfer")
    return hasil

def version_check():
    cmd=f"versi \r\n\r\n"
    hasil = send_command(cmd)
    return hasil

def get_data_player_multithread(total_request, data_table):
    total_response = 0
    texec = dict()
    catat_awal = datetime.datetime.now()

    for k in range(total_request):
        texec[k] = threading.Thread(
            target=get_data_player, args=(random.randint(1, 20),))
        texec[k].start()

    for k in range(total_request):
        if (texec[k] != -1):
            total_response += 1
        else: 
            continue
        texec[k].join()
        

    catat_akhir = datetime.datetime.now()
    selesai = catat_akhir - catat_awal
    data_table.append([total_request, total_request, total_response, selesai])
    

if __name__ == '__main__':
    h = version_check()
    if (h):
        print(h)
    
    total_request = [1, 5, 10, 20]
    data_table = []
    
    for request in total_request:
        get_data_player_multithread(request, data_table)
        
    table_header = ["Sum of Thread", "Sum of Request", "Sum of Response", "Latency"]
    print(tabulate(data_table, headers=table_header, tablefmt="fancy_grid"))
