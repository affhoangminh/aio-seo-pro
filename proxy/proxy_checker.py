import requests
import time
from concurrent.futures import ThreadPoolExecutor


TEST_URL = "https://api.ipify.org"


def check_proxy(proxy):

    host = proxy[1]
    port = proxy[2]
    user = proxy[3]
    password = proxy[4]

    if user and password:
        proxy_str = f"http://{user}:{password}@{host}:{port}"
    else:
        proxy_str = f"http://{host}:{port}"

    proxies = {
        "http": proxy_str,
        "https": proxy_str
    }

    start = time.time()

    try:

        r = requests.get(TEST_URL, proxies=proxies, timeout=8)

        latency = round(time.time() - start, 2)

        if r.status_code == 200:
            return ("LIVE", latency)

    except:
        pass

    return ("DEAD", 0)


def check_proxy_list(proxy_list, callback):

    def worker(proxy):

        status, speed = check_proxy(proxy)

        callback(proxy, status, speed)

    with ThreadPoolExecutor(max_workers=50) as executor:

        for proxy in proxy_list:
            executor.submit(worker, proxy)