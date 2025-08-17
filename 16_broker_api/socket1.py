from alpaca.data.live.crypto import CryptoDataStream

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# import os
# import certifi
# #for windows ssl error
# os.environ['SSL_CERT_FILE'] = certifi.where()

import pendulum as dt
time_zone="UTC"
print(dt.now(time_zone))


# Fetch keys from environment
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")

crypto_data_stream_client=CryptoDataStream(api_key,secret_key)
async def sample(data):
    print(data)
    print(dt.now(time_zone))
# symbol=['BTC/USD','ETH/USD']
# symbol=['BTC/USD','ETH/USD']
symbol=['AAVE/USD']
# crypto_data_stream_client.subscribe_trades(crypto_data_stream_handler, *symbol)

crypto_data_stream_client.subscribe_quotes(sample, *symbol)
crypto_data_stream_client.run()