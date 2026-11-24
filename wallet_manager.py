import os
from solana.keypair import Keypair
from dotenv import load_dotenv

load_dotenv()

class WalletManager:
    def __init__(self):
        self._private_key = os.getenv('DEV_WALLET_PRIVATE_KEY')
        self._keypair = None
    
    @property
    def keypair(self):
        """Lazy loading of keypair - never expose the raw private key"""
        if not self._keypair:
            self._keypair = Keypair.from_base58_string(self._private_key)  # Fixed: was from_seed(self._private_key.encode()) which generates wrong keypair for base58 keys
        return self._keypair
    
    def get_public_key(self):
        """Safely get the public key without exposing private key"""
        return str(self.keypair.public_key)
    
    def __str__(self):
        """String representation never exposes the private key"""
        return f"Wallet(public_key={self.get_public_key()})"
