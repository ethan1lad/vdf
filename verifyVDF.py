import json
import requests

from consts import headers, url

resp = json.loads(requests.get("https://api.ergoplatform.com/api/v1/boxes/unspent/byAddress/3n7QCt34e6s7VwzLXVq3je1HMJQexGLM2vdRifkmVbPu8nVq8G1o8kJGExy8YRajbsmoMX4fdxhg4opmBz3KeS5nCvyCpBP5TP8HxbhiYAMpNmtTwGAzPPefo1cBeF37hSYWVXd1YeWczufwcz6Lq54hmJB57C5hbJjqVRYW4", params={'limit':500}).text)
for box in resp['items']:
    transaction_to_sign = \
        {
            "requests": [
                {
                    "address": "9hQziKQiyXYNcR4PUioFzkeTPxjaT8Ghu54do4k6no8yB6xpx3d",
                    "value": box['value'] - 1000000,
                    "assets": [
                    ],
                    "registers": {
                        "R4": "0428"
                    }

                }
            ],
            "fee": 1000000,
            "inputsRaw": [json.loads(requests.get(url+"utxo/byIdBinary/"+box['boxId']).text)['bytes']]
        }
    transaction_id = requests.post(url + "wallet/transaction/send", json=transaction_to_sign,
                                   headers=headers).text
    print(transaction_id)