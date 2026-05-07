import requests

def check_proxy(proxy):

    try:

        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }

        r = requests.get(
            "https://api.ipify.org",
            proxies=proxies,
            timeout=5
        )

        return r.status_code == 200

    except:

        return False