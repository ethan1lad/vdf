import time
import requests

from consts import url, headers
from helpers import nBitRandom, getGaussianPrime, squareRoot, encodeBigInt, encodeCollBigInt, encodeInt

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

for i in range(25):
    for _ in range(200):
        for _ in range(int(178)):
            n = squareRoot(n,p)
        checkpoints.append(encodeBigInt(n))
    obj_to_append = \
                {
                    "address": "KeFFWP5NAKZ5aiL6N65KZWZMvuN86BzinYvPwpjkqc8xU9FSNNA4gp6bKwBFMhgB3LRkf1jBzyr3uHS9YidBgeb2U4uA7kHrFXUhpDxun29jeHhQSZ1ZsmK6JJeUiXu8sCi86umPukXBXBLGheBWFAPeYaV62AqqjisaN3wWq5PRvM3Qg8e7SHBcBXJMNfAaecPddJxQQHDDr6oUYeNKDp6YvDmpSnaxTeZAJiSomjPEtsVi4DjrgUf114mCRMywMSijZgFBYEZS1Y7KoP5UGCSM4QbEoCvemdq5nK7NymkNT",
                    "value": 3000000,
                    "assets": [
                        {
                        "tokenId": "5d1f057b01ee6f6d83683a87da418d31c4d82c548e3eeed1687120f1adbad745",
                        "amount": 1
                        }
                    ],
                    "registers": {
                        "R4": encodeCollBigInt(checkpoints),
                        "R5": "06" + encodeBigInt(p),
                        "R6": "0eb20101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101",
                        "R7": encodeInt(i)
                    }
                }
    checkpoints = [checkpoints[-1]]
    transaction_to_sign['requests'].append(obj_to_append)


print(transaction_to_sign)
transaction_id = requests.post(url + "wallet/transaction/send", json=transaction_to_sign,
                               headers=headers).text
print(transaction_id)

