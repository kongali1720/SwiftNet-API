import socket
from src.crypto import AESCipher
from src.mt103 import parse_mt103
from src.logger import setup_logger

HOST = '127.0.0.1'
PORT = 65432
KEY = "supersecretkey1234"  # 16 bytes (harus valid untuk AES)

logger = setup_logger()

def start_server():
    cipher = AESCipher(KEY)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server started on {HOST}:{PORT}")
        logger.info(f"SNL Server running on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                logger.info(f"Connection from {addr}")
                encrypted_msg = conn.recv(4096).decode()
                try:
                    decrypted_msg = cipher.decrypt(encrypted_msg)
                    logger.info(f"Received decrypted message: {decrypted_msg}")
                    mt103_data = parse_mt103(decrypted_msg)  # parsing JSON di sini sekali saja
                    logger.info(f"Processing message: {mt103_data}")
                    conn.sendall("ACK".encode())
                except Exception as e:
                    logger.error(f"Error: {e}")
                    conn.sendall(f"ERR {e}".encode())

if __name__ == "__main__":
    start_server()
