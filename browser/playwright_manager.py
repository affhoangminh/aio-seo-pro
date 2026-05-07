from playwright.sync_api import sync_playwright

playwright = None
chromium = None


def start_playwright():
    pw = sync_playwright().start()
    return pw, pw.chromium


def stop_playwright():

    global playwright

    if playwright:
        playwright.stop()