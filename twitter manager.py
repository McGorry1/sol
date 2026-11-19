import os
import time
import tweepy
from dotenv import load_dotenv

load_dotenv()

class TwitterManager:
    def __init__(self):
        # Authenticate with Twitter
        auth = tweepy.OAuthHandler(
            os.getenv('TWITTER_API_KEY'), 
            os.getenv('TWITTER_API_SECRET')
        )
        auth.set_access_token(
            os.getenv('TWITTER_ACCESS_TOKEN'), 
            os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )
        self.twitter = tweepy.API(auth)
        
        # Token information
        self.token_name = os.getenv('TOKEN_NAME', 'Your Token')
        self.token_symbol = os.getenv('TOKEN_SYMBOL', 'TOKEN')
        self.contract_address = os.getenv('TARGET_TOKEN_MINT')
        
        # Milestone tracking
        self.last_marketcap_milestone = 0
        self.last_holders_milestone = 0
    
    def post_with_retry(self, message, max_retries=3):
        """Post with retry logic for rate limits"""
        for attempt in range(max_retries):
            try:
                return self.twitter.update_status(message)
            except tweepy.errors.TweepyException as e:
                if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                    time.sleep(15 * (attempt + 1))  # Exponential backoff
                    continue
                raise
    
    def post_token_launch(self):
        """Post token launch announcement"""
        message = f"""🚀 {self.token_name} ({self.token_symbol}) is now LIVE on Solana!

🔥 Contract: {self.contract_address[:8]}...{self.contract_address[-8:]}
💧 Liquidity: Locked & Verified
📈 Ready to moon!

Join our Telegram: https://t.me/yourgroup
#Solana #DeFi #Crypto #Airdrop"""
        
        try:
            self.post_with_retry(message)
            return True
        except Exception as e:
            print(f"Twitter error: {e}")
            return False
    
    def post_price_update(self, current_price, price_change):
        """Post price update"""
        emoji = "📈" if price_change > 0 else "📉"
        message = f"""{emoji} {self.token_name} Price Update!

Current Price: ${current_price:.8f}
24h Change: {price_change:+.2f}%

🔥 Still early! Get in before the pump!
Join: https://t.me/yourgroup
#Solana #DeFi"""
        
        try:
            self.post_with_retry(message)
            return True
        except Exception as e:
            print(f"Twitter error: {e}")
            return False
    
    def post_milestone(self, milestone_type, value):
        """Post project milestone"""
        if milestone_type == "holders":
            message = f"""🎉 {value} holders and counting!

{self.token_name} community is growing fast!
🚀 Next stop: {int(value) * 2} holders

Join now: https://t.me/yourgroup
#Solana #Crypto"""
        elif milestone_type == "marketcap":
            message = f"""💰 Market Cap: ${value:,}!

{self.token_name} is gaining momentum!
📈 Still room to grow before major exchange listing

Join: https://t.me/yourgroup
#Solana #DeFi"""
        elif milestone_type == "extraction":
            message = f"""🔥 Strategic liquidity optimization completed!

${value:,.2f} reinvested for growth
📈 Stronger foundation for next pump

Join: https://t.me/yourgroup
#Solana #DeFi"""
        
        try:
            self.post_with_retry(message)
            return True
        except Exception as e:
            print(f"Twitter error: {e}")
            return False
    
    def engage_with_hashtags(self, hashtags):
        """Engage with posts using specific hashtags"""
        for hashtag in hashtags:
            try:
                tweets = self.twitter.search_tweets(q=f"#{hashtag} -filter:retweets", count=5)  # Fixed: search() removed in Tweepy v4+, correct method is search_tweets()
                for tweet in tweets:
                    # Reply to relevant tweets with your token info
                    reply_text = f"Check out {self.token_name} ({self.token_symbol})! 🔥\n\nJoin: https://t.me/yourgroup"
                    self.twitter.update_status(
                        reply_text, 
                        in_reply_to_status_id=tweet.id
                    )
                    time.sleep(30)  # Avoid rate limiting
            except Exception as e:
                print(f"Hashtag engagement error: {e}")
    
    def post_community_update(self, update_type):
        """Post community updates"""
        if update_type == "new_features":
            message = f"""🚀 New features coming to {self.token_name}!

Our dev team is working hard to bring you exciting updates!
🔥 Stay tuned for major announcements!

Join: https://t.me/yourgroup
#Solana #DeFi"""
        elif update_type == "partnership":
            message = f"""🤝 Exciting partnership discussions underway!

{self.token_name} is expanding its ecosystem!
📈 Big things coming soon!

Join: https://t.me/yourgroup
#Solana #DeFi"""
        else:
            print(f"Unknown update_type: {update_type}")  # Fixed: missing else guard caused UnboundLocalError when unknown update_type passed to post_with_retry(message)
            return False
        
        try:
            self.post_with_retry(message)
            return True
        except Exception as e:
            print(f"Twitter error: {e}")
            return False
