from django.core.management.utils import get_random_secret_key

from backend.core.utils.cryptography import generate_key_pair


# Generate public/private key pair for signing
def generate_account():
    key_pair = generate_key_pair()
    print(f"Signing Key: {key_pair.private}")
    print(f"Account Number: {key_pair.public}")


# Generate secret key for Django
def generate_secret_key():
    secret_key = get_random_secret_key()
    print(f"SECRET_KEY: {secret_key}")


if __name__ == "__main__":
    generate_account()
    generate_secret_key()
