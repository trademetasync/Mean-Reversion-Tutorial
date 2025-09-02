import requests
import pandas as pd
import logging
from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetasyncClient:
    def __init__(self):
        self.base_url = f"https://{config.RAPIDAPI_HOST}"
        self.headers = config.api_headers
        
    def _make_request(self, method: str, endpoint: str, **kwargs):
        """CORRECT request method for RapidAPI"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            # Use requests.request with proper parameters
            response = requests.request(
                method, 
                url, 
                headers=self.headers, 
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error {e.response.status_code}: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None
    
    def get_ohlc_data(self, symbol: str, timeframe: str, date_from: str, date_to: str):
        """CORRECT endpoint usage: /ohlc with params"""
        logger.info(f"Fetching OHLC for {symbol} {timeframe} from {date_from} to {date_to}")
        
        params = {
            "symbol": symbol,
            "timeframe": timeframe,
            "date_from": date_from,
            "date_to": date_to
        }
        
        result = self._make_request("GET", "/ohlc", params=params)
        
        if result:
            try:
                df = pd.DataFrame(result)
                if not df.empty:
                    df['time'] = pd.to_datetime(df['time'])
                    numeric_cols = ['open', 'high', 'low', 'close']
                    for col in numeric_cols:
                        if col in df.columns:
                            df[col] = pd.to_numeric(df[col], errors='coerce')
                    df = df.sort_values('time').reset_index(drop=True)
                    logger.info(f"✅ Retrieved {len(df)} candles")
                    return df
            except Exception as e:
                logger.error(f"Error processing data: {e}")
        return None

    def get_current_tick(self, symbol: str):
        """CORRECT tick endpoint"""
        params = {"symbol": symbol}
        return self._make_request("GET", "/tick", params=params)

# Global client instance
client = MetasyncClient()