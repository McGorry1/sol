import os
import requests
import json
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class PositionMonitor:
    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url
        self.headers = {
            "Content-Type": "application/json",
            "Helius-Api-Key": os.getenv('HELIUS_API_KEY')
        }
    
    def get_token_balance(self, wallet_address: str, token_mint: str) -> float:
        """Get token balance for a specific wallet"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getTokenAccountsByOwner",
                "params": [
                    wallet_address,
                    {"mint": token_mint},
                    {"encoding": "jsonParsed"}
                ]
            }
            
            response = requests.post(self.rpc_url, json=payload, headers=self.headers)
            data = response.json()
            
            if "result" in data and data["result"]["value"]:
                account = data["result"]["value"]⁰
                amount = account["account"]["data"]["parsed"]["info"]["tokenAmount"]["amount"]
                decimals = account["account"]["data"]["parsed"]["info"]["tokenAmount"]["decimals"]
                return float(amount) / (10 ** decimals)
            
            return 0.0
        except Exception as e:
            print(f"Error getting token balance: {e}")
            return 0.0
    
    def get_sol_balance(self, wallet_address: str) -> float:
        """Get SOL balance for a specific wallet"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getBalance",
                "params": [wallet_address]
            }
            
            response = requests.post(self.rpc_url, json=payload, headers=self.headers)
            data = response.json()
            
            if "result" in data:
                lamports = data["result"]["value"]
                return lamports / 1_000_000_000  # Convert lamports to SOL
            
            return 0.0
        except Exception as e:
            print(f"Error getting SOL balance: {e}")
            return 0.0
    
    def get_pool_info(self, token_mint: str) -> Dict[str, Any]:
        """Get pool information for a token (Simplified for development)"""
        try:
            # In a real bot, you would query Jupiter or Raydium API here
            return {
                "price_usd": 0.00012345,
                "liquidity_usd": 1000.0,
                "volume_24h": 5000.0,
                "price_change_24h": 5.2,
                "holders": 150,
                "marketcap": 10000.0
            }
        except Exception as e:
            print(f"Error getting pool info: {e}")
            return {}
    
    def calculate_maximum_extractable(self, pool_info: Dict[str, Any], wallet_address: str) -> float:
        """Calculate maximum amount that can be extracted without major price impact"""
        liquidity = pool_info.get('liquidity_usd', 0)
        max_extract = liquidity * 0.25  # 25% of liquidity before major impact
        return max_extract

    def get_rug_metrics(self, token_mint: str) -> Dict[str, Any]:
        """Calculate advanced metrics for rug strategy optimization"""
        pool_info = self.get_pool_info(token_mint)
        
        price = pool_info.get('price_usd', 0)
        liquidity = pool_info.get('liquidity_usd', 0)
        price_liquidity_ratio = price / liquidity if liquidity > 0 else float('inf')
        
        volume = pool_info.get('volume_24h', 0)
        volume_liquidity_ratio = volume / liquidity if liquidity > 0 else 0
        
        holders = pool_info.get('holders', 0)
        is_rug_worthy = holders < 1000 and price_liquidity_ratio < 0.01
        
       return {
            "price_liquidity_ratio": price_liquidity_ratio,
            "volume_liquidity_ratio": volume_liquidity_ratio,
            "is_rug_worthy": is_rug_worthy,
            "current_metrics": pool_info
        }

    def check_token_lifecycle_stage(self, token_mint: str) -> str:
        """Check if token has migrated to Raydium"""
        pool_info = self.get_pool_info(token_mint)
        
        # In a real implementation, you would check if the pool is on Raydium
        # For now, we'll simulate with a condition based on liquidity
        if pool_info.get('liquidity_usd', 0) > 5000:  # Mock threshold
            return "migrated_to_raydium"
        else:
            return "on_pump_fun"
