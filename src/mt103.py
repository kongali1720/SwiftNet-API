# src/mt103.py
import json

def create_mt103_transaction():
    return {
        "transaction": "MT103",
        "amount": 1000,
        "currency": "USD",
        "sender": "Bank A",
        "receiver": "Bank B"
    }

if __name__ == "__main__":
    tx = create_mt103_transaction()
    print("Generated MT103 Transaction:")
    print(json.dumps(tx, indent=4))
