import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
    RAPIDAPI_HOST = "metasyc.p.rapidapi.com"
    
    # Trading Settings
    SYMBOL = "EURUSD"
    TIMEFRAME = "M30"
    LOT_SIZE = 0.01
    
    # Strategy Parameters
    BB_PERIOD = 20
    BB_DEVIATION = 2
    
    # Risk Management
    STOP_LOSS_PIPS = 50
    TAKE_PROFIT_PIPS = 30

    @property
    def api_headers(self):
        """CORRECT headers format for RapidAPI"""
        return {
            "x-rapidapi-key": self.RAPIDAPI_KEY,
            "x-rapidapi-host": self.RAPIDAPI_HOST,
            "Content-Type": "application/json"
        }

config = Config()
