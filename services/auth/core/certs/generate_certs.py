from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from pathlib import Path
import shutil


class GeneratorCerts:
    def __init__(self, certs_path: Path):
        self.crts_path: Path = certs_path
        # self.remove_directory_with_contents()
        self.create_directory()
        self.generate_certs()

    # def __del__(self):
    #     self.remove_directory_with_contents()

    def remove_directory_with_contents(self) -> None:
        directory = Path(self.crts_path)
        try:
            if directory.exists() and directory.is_dir():
                shutil.rmtree(directory)
                print(f"The directory {self.crts_path} is deleted")
            else:
                print(f"The directory {self.crts_path} is not exist")
        except OSError as e:
            print(f"ERROR by delete directory {self.crts_path}: {e}")

    def create_directory(self) -> None:
        try:
            self.crts_path.mkdir(parents=True, exist_ok=True)
            print(f"The directory {self.crts_path} is created or already exist")
        except Exception as e:
            print(f"ERROR by created directory {self.crts_path}: {e}")

    def generate_certs(self):
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # Get public key from private key
        public_key = private_key.public_key()

        # Сериализация секретного ключа в PEM формате
        pem_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Сериализация публичного ключа в PEM формате
        pem_public = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Write public key and private key in directory
        with open(self.crts_path.joinpath("jwt-private-key.pem"), "wb") as file:
            file.write(pem_private)

        with open(self.crts_path.joinpath("jwt-public-key.pem"), "wb") as file:
            file.write(pem_public)
