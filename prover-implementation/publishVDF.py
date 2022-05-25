import time
import requests

from consts import url, headers
from helpers import nBitRandom, getGaussianPrime, squareRoot, encodeBigInt, encodeCollBigInt

# Generate prime p
p = getGaussianPrime(120)
# Get seed n
n = nBitRandom(120)
# If square root does not exist on n, then it must exist for -n,
# given p as Gaussian Prime
if squareRoot(n,p) == -1:
    n = -n

checkpoints = [encodeBigInt(n)]
start = time.process_time()

# Initialise transaction_to_sign dictionary
transaction_to_sign = \
    {
        "requests": [],
        "fee": 1000000,
        "inputsRaw": []
    }

for _ in range(25):
    for _ in range(200):
        for _ in range(int(178)):
            n = squareRoot(n,p)
        checkpoints.append(encodeBigInt(n))
    obj_to_append = \
                {
                    "address": "3n7QCt34e6s7VwzLXVq3je1HMJQexGLM2vdRifkmVbPu8nVq8G1o8kJGExy8YRajbsmoMX4fdxhg4opmBz3KeS5nCvyCpBP5TP8HxbhiYAMpNmtTwGAzPPefo1cBeF37hSYWVXd1YeWczufwcz6Lq54hmJB57C5hbJjqVRYW4",
                    "value": 3000000,
                    "assets": [
                    ],
                    "registers": {
                        "R4": encodeCollBigInt(checkpoints),
                        "R5": "06" + encodeBigInt(p),
                        "R6": "0eb20101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101"
                    }
                }
    checkpoints = [checkpoints[-1]]
    transaction_to_sign['requests'].append(obj_to_append)


print(transaction_to_sign)
transaction_id = requests.post(url + "wallet/transaction/send", json=transaction_to_sign,
                               headers=headers).text
print(transaction_id)

