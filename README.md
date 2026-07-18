# rsa_encryptor

> A Python implementation of the RSA encryption algorithm for secure message transmission.

## Overview

rsa_encryptor is an open-source project that provides a secure way to encrypt and decrypt messages using the widely accepted RSA encryption algorithm. With the rise of digital communication, secure data transmission has become increasingly important. rsa_encryptor addresses this need by offering a Python implementation of RSA encryption, allowing developers to easily integrate secure message transmission into their applications. This project includes key generation, encryption, decryption, and signature verification, making it a valuable tool for anyone working with secure data.

## Features

- **Key Generation**: Generate public and private RSA keys for secure encryption.
- **Encryption**: Encrypt messages using the public key and decrypt messages using the private key.
- **Decryption**: Decrypt encrypted messages using the private key.
- **Signature Verification**: Verify the authenticity of messages using digital signatures.
- **Secure Data Transmission**: Safely transmit sensitive information using RSA encryption.
- **Flexible Key Sizes**: Support various key sizes to balance security and performance.
- **Clear API**: Easy-to-use public interface for encryption and decryption operations.

## Getting Started

### Prerequisites

- Python (3.8+)
- pip (latest version)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/rsa_encryptor.git

# Navigate to the project directory
cd rsa_encryptor

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Generate a public and private key pair
python src/main.py generate_key

# Encrypt a message
python src/main.py encrypt message.txt public_key.pem

# Decrypt the encrypted message
python src/main.py decrypt encrypted_message.txt private_key.pem
```

## Architecture

rsa_encryptor is structured into four main files:

- `src/main.py`: The entry point for the project, handling key generation, encryption, and decryption operations.
- `src/rsa.py`: Contains the RSA encryption and decryption functions.
- `src/utils.py`: Provides utility functions for key handling and file operations.
- `tests/test_rsa.py`: Contains unit tests for the RSA encryption and decryption functions.

## API Reference

rsa_encryptor exposes a simple API for encryption and decryption operations:

```python
from rsa_encryptor import encrypt, decrypt

# Encrypt a message
encrypted_message = encrypt(message="Hello, World!", public_key=public_key)

# Decrypt the encrypted message
decrypted_message = decrypt(encrypted_message, private_key=private_key)
```

## Testing

```bash
# Run unit tests
python -m unittest tests/test_rsa.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push and open a PR

## License

rsa_encryptor is licensed under the MIT License.