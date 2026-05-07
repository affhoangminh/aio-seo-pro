import time
import requests
import socket
from playwright.sync_api import sync_playwright


TEST_URL = "https://vnexpress.net"

PROXY = "http://random:random@160.191.177.17:11214"


def test_dns():

    print("\n=== DNS TEST ===")

    start = time.time()

    ip = socket.gethostbyname("ipinfo.io")

    end = time.time()

    print("Resolved IP:", ip)
    print("DNS Time:", round(end - start, 3), "seconds")


def test_proxy_requests():

    print("\n=== PROXY REQUEST TEST ===")

    proxies = {
        "http": PROXY,
        "https": PROXY
    }

    start = time.time()

    r = requests.get(TEST_URL, proxies=proxies)

    end = time.time()

    print("Status:", r.status_code)
    print("Response Time:", round(end - start, 3), "seconds")


def test_playwright():

    print("\n=== PLAYWRIGHT TEST ===")

    start_browser = time.time()

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            proxy={
                "server": "http://160.191.177.17:11214",
                "username": "random",
                "password": "random"
            }
        )

        page = browser.new_page()

        end_browser = time.time()

        start_page = time.time()

        page.goto(TEST_URL)

        end_page = time.time()

        print("Browser Startup:", round(end_browser - start_browser, 3), "seconds")
        print("Page Load Time:", round(end_page - start_page, 3), "seconds")

        browser.close()


def test_no_proxy():

    print("\n=== NO PROXY TEST ===")

    start = time.time()

    r = requests.get(TEST_URL)

    end = time.time()

    print("Response Time:", round(end - start, 3), "seconds")


if __name__ == "__main__":

    print("\nBROWSER / PROXY BENCHMARK\n")

    test_dns()

    test_no_proxy()

    test_proxy_requests()

    test_playwright()

    print("\nBenchmark finished.\n")