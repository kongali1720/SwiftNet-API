import socket
import json
from src.crypto import AESCipher

HOST = '127.0.0.1'
PORT = 65432
KEY = "supersecretkey1234"  # 16 bytes, harus sama dengan server

def send_mt103(message_dict):
    cipher = AESCipher(KEY)
    json_message = json.dumps(message_dict)  # ubah dict ke string JSON
    encrypted_msg = cipher.encrypt(json_message)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(encrypted_msg.encode('utf-8'))
        response = s.recv(1024).decode('utf-8')
        print(f"Response from server: {response}")

if __name__ == "__main__":
    mt103_sample = {
        "transaction": "MT103",
        "amount": 1000,
        "currency": "USD",
        "sender": "Bank A",
        "receiver": "Bank B"
    }
    send_mt103(mt103_sample)
