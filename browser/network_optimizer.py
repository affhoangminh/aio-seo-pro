def chromium_args():

    return [

"--disable-background-networking",

"--disable-background-timer-throttling",
"--disable-renderer-backgrounding",

"--disable-backgrounding-occluded-windows",

# "--disable-http2",

"--max-connections-per-host=20",

"--enable-gpu",
"--ignore-gpu-blocklist",

"--no-sandbox",

"--disable-dev-shm-usage"

]