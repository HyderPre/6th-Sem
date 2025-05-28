from cryptography.fernet import Fernet
import os

# Load the encryption key
KEY_PATH = 'encryption_key.key'

# Check if the key exists
if not os.path.exists(KEY_PATH):
    print("Encryption key not found.")
    exit()

# Read the encryption key
with open(KEY_PATH, 'rb') as key_file:
    encryption_key = key_file.read()

# Initialize the Fernet cipher with the encryption key
fernet = Fernet(encryption_key)

# Specify the encrypted file path
encrypted_folder = 'encrypted_files'
encrypted_filename = input("Enter the encrypted file name (with extension): ")
encrypted_file_path = os.path.join(encrypted_folder, encrypted_filename)

# Check if the file exists
if not os.path.exists(encrypted_file_path):
    print(f"Encrypted file '{encrypted_filename}' not found.")
    exit()

# Read the encrypted file
with open(encrypted_file_path, 'rb') as encrypted_file:
    encrypted_data = encrypted_file.read()

# Decrypt the file
try:
    decrypted_data = fernet.decrypt(encrypted_data)
    
    # Save the decrypted file
    decrypted_filename = f"decrypted_{encrypted_filename}"
    decrypted_file_path = os.path.join(encrypted_folder, decrypted_filename)

    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)
    
    print(f"File decrypted successfully! Saved as {decrypted_filename}")
except Exception as e:
    print(f"Error decrypting file: {e}")
