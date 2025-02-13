import time

import requests


for _ in range(3):
    time.sleep(5)
    res = requests.post('http://server:8000/send/?message=hello')
    print(res.json())
