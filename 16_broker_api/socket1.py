from alpaca.data.live.crypto import CryptoDataStream

# import os
# import certifi
# #for windows ssl error
# os.environ['SSL_CERT_FILE'] = certifi.where()

import pendulum as dt
time_zone="UTC"
print(dt.now(time_zone))

api_key='PKE2TF3F7XPYTG8BBD3Z'
secret_key='zfYLU7dn3fdS3HfMf0kvS4XW1hG5C3a2NBhZQQuM'

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