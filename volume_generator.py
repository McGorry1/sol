import os
import random
import asyncio
from rug_executor import RugExecutor
from position_monitor import PositionMonitor

class VolumeGenerator:
    def __init__(self, bundle_manager, rpc_url):
        self.bundle_manager = bundle_manager
        self.rpc_url = rpc_url
        self.is_running = False
    
    async def start_volume_cycles(self, token_mint, sol_amount_per_buy=0.1):
        """Start automated volume generation cycles"""
        self.is_running = True
        monitor = PositionMonitor(self.rpc_url)
        
        while self.is_running:
            # Get 3 random wallets from the bundle
            wallets = self.bundle_manager.get_random_wallets(count=3)
            
            # Execute buy from wallet 1
            executor1 = RugExecutor(wallets[0]['private_key'], self.rpc_url)
            # Use a random amount between 0.05 and 0.2 SOL
            buy_amount = random.uniform(0.05, 0.2)
            tx_hash, status = await executor1.execute_buy(token_mint, buy_amount)
            print(f"Buy from {wallets[0]['public_key']}: {status}")
            
            # Wait for random interval (1-5 minutes)
            await asyncio.sleep(random.randint(60, 300))
            
            # Execute sell from wallet 2
            executor2 = RugExecutor(wallets[1]['private_key'], self.rpc_url)
            balance = await monitor.get_token_balance(wallets[1]['public_key'], token_mint)
            if balance > 0:
                sell_percentage = min(random.uniform(5, 15), 100)
                tx_hash, status = await executor2.execute_swap(token_mint, sell_percentage)
                print(f"Sell from {wallets[1]['public_key']}: {status}")
            
            # Wait for random interval (1-5 minutes)
            await asyncio.sleep(random.randint(60, 300))
            
            # Execute small sell from wallet 3
            executor3 = RugExecutor(wallets[2]['private_key'], self.rpc_url)
            balance3 = await monitor.get_token_balance(wallets[2]['public_key'], token_mint)
            if balance3 > 0:
                sell_percentage3 = min(random.uniform(1, 5), 100)
                tx_hash, status = await executor3.execute_swap(token_mint, sell_percentage3)
                print(f"Sell from {wallets[2]['public_key']}: {status}")
    
    def stop_volume_cycles(self):
        """Stop the volume generation cycles"""
        self.is_running = False
