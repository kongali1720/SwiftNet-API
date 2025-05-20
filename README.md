<<<<<<< HEAD
# SwiftNet-API
=======

# SwiftNet-API

Proyek ini adalah simulasi sederhana protokol komunikasi Swift MT103 dengan enkripsi AES.  
Server menerima pesan MT103 terenkripsi, mendekripsi, dan memprosesnya.  
Client mengirim pesan MT103 yang dienkripsi ke server.

## Fitur

- Enkripsi dan dekripsi pesan dengan AES
- Parsing pesan MT103 sederhana dalam format JSON
- Logging aktivitas server
- Contoh penggunaan client dan server

## Cara Pakai

1. Clone repo ini  
2. Buat virtual environment dan install dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install pycryptodome
    ```
3. Jalankan server:
    ```bash
    python3 -m src.server
    ```
4. Di terminal lain, jalankan client:
    ```bash
    python3 -m src.client
    ```

## Struktur Folder

- `src/crypto.py` - Modul enkripsi AES  
- `src/mt103.py` - Modul parsing dan contoh data MT103  
- `src/server.py` - Server TCP  
- `src/client.py` - Client TCP  
- `src/logger.py` - Setup logging  

---

### Buy Me A Coffee ☕

Jika kamu merasa proyek ini bermanfaat, traktir saya kopi lewat PayPal 💙

[https://www.paypal.com/paypalme/bungtempong99](https://www.paypal.com/paypalme/bungtempong99)
>>>>>>> 1907651 (Initial commit: SwiftNet-API with AES encryption, MT103 message, server and client)
