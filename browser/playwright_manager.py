import asyncio
from playwright.sync_api import sync_playwright

playwright = None
chromium = None


def start_playwright():
    # Fix: It looks like you are using Playwright Sync API inside the asyncio loop
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If a loop is running, we might be in trouble with sync API
            # but usually in a separate thread, get_event_loop() might raise an error or return a new one
            pass
    except RuntimeError:
        # No event loop in this thread, which is good for sync API
        pass
    
    # Force clear event loop for this thread to satisfy Playwright Sync API
    asyncio.set_event_loop(asyncio.new_event_loop())

    pw = sync_playwright().start()
    return pw, pw.chromium



def stop_playwright():

    global playwright

    if playwright:
        playwright.stop()