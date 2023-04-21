import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from api.app import app

# Load environment variables from secret.env file
load_dotenv('secret.env')

# Get the encryption key from the environment variables
encryption_key = os.getenv('ENCRYPTION_KEY')
print('Encryption key:', encryption_key)

# Decode the encryption key from a string to bytes
key = encryption_key.encode('utf-8')

# Perform a simple test using the encryption key
# Generate a random message
message = b'This is a test message'

# Encrypt the message using the encryption key
fernet = Fernet(key)
encrypted_message = fernet.encrypt(message)

# Decrypt the message using the encryption key
decrypted_message = fernet.decrypt(encrypted_message)

# Print the original message and the decrypted message
print('Original message:', message)
print('Decrypted message:', decrypted_message)

def main():
    # Create a new HTTP server
    http_server = HTTPServer(app())

    # Listen on port 8888
    http_server.listen(8888)

    # Start the I/O loop
    print("Running MyApp application")
    IOLoop.current().start()

if __name__ == "__main__":
    main()
