import socket
import threading
import queue
import time
import json
import logging
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Setup logging
logging.basicConfig(filename='snl_log.txt', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# AES encryption/decryption key (must be 16, 24 or 32 bytes)
AES_KEY = b'ThisIsASecretKey'  

message_queue = queue.Queue()

def encrypt_message(message):
    cipher = AES.new(AES_KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    iv = cipher.iv
    return iv + ct_bytes  # prepend IV for decryption

def decrypt_message(ciphertext):
    iv = ciphertext[:AES.block_size]
    ct = ciphertext[AES.block_size:]
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode()

def validate_mt103(msg_dict):
    required_fields = ['TransactionReference', 'BankOperationCode', 'InstructionCode', 
                       'Amount', 'Currency', 'OrderingCustomer', 'BeneficiaryCustomer']
    for field in required_fields:
        if field not in msg_dict:
            return False, f"Missing field: {field}"
    return True, "Valid MT103"

def snl_server(host='127.0.0.1', port=65432):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"SNL Server running on {host}:{port}")
    while True:
        conn, addr = server.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_client, args=(conn,)).start()

def handle_client(conn):
    with conn:
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break
                # decrypt message
                decrypted_msg = decrypt_message(data)
                print(f"Received decrypted message: {decrypted_msg}")
                logging.info(f"Received message: {decrypted_msg}")

                # parse json
                msg_dict = json.loads(decrypted_msg)

                # validate MT103 format
                valid, msg = validate_mt103(msg_dict)
                if not valid:
                    response = f"ERROR: {msg}"
                    conn.sendall(encrypt_message(response))
                    continue

                # enqueue message
                message_queue.put(msg_dict)
                conn.sendall(encrypt_message("ACK"))
            except Exception as e:
                logging.error(f"Error in client handler: {e}")
                break

def snl_client(msg_dict, host='127.0.0.1', port=65432, retry=3):
    msg_json = json.dumps(msg_dict)
    encrypted_msg = encrypt_message(msg_json)
    attempt = 0

    while attempt < retry:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(encrypted_msg)
                data = s.recv(4096)
                decrypted_resp = decrypt_message(data)
                print(f"Server reply: {decrypted_resp}")
                if decrypted_resp == "ACK":
                    return True
                else:
                    print("Server error:", decrypted_resp)
                    return False
        except Exception as e:
            print(f"Connection failed, attempt {attempt+1}: {e}")
            attempt += 1
            time.sleep(2)
    return False

def process_messages():
    while True:
        if not message_queue.empty():
            msg = message_queue.get()
            logging.info(f"Processing message: {msg}")
            print(f"Processing message: {msg}")
            # Simulasi delay pemrosesan
            time.sleep(2)
        else:
            time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=snl_server, daemon=True).start()
    threading.Thread(target=process_messages, daemon=True).start()

    # Contoh pesan MT103 sederhana
    sample_mt103 = {
        "TransactionReference": "ABC123456789",
        "BankOperationCode": "CRED",
        "InstructionCode": "PHON",
        "Amount": "5000000",
        "Currency": "USD",
        "OrderingCustomer": "John Doe",
        "BeneficiaryCustomer": "Jane Smith"
    }

    print("SNL Client Simulator")
    while True:
        send = input("Send MT103? (yes/quit): ").lower()
        if send == 'quit':
            break
        elif send == 'yes':
            success = snl_client(sample_mt103)
            if success:
                print("Message sent successfully!")
            else:
                print("Failed to send message.")
