import random
import json

# ===============================
# USER AGENTS
# ===============================

USER_AGENTS = [

"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",

"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",

]

# ===============================
# SCREEN RESOLUTION
# ===============================

RESOLUTIONS = [

"1920x1080",
"1366x768",
"1536x864",
"1440x900",
"1600x900"

]

# ===============================
# TIMEZONE
# ===============================

TIMEZONES = [

"Asia/Ho_Chi_Minh",
"Asia/Bangkok",
"Asia/Singapore",
"Asia/Tokyo",
"Asia/Shanghai"

]

# ===============================
# LANGUAGE
# ===============================

LANGUAGES = [

"vi-VN",
"en-US",
"en-GB",
"th-TH",
"zh-CN"

]

# ===============================
# PLATFORM
# ===============================

PLATFORMS = [

"Win32",
"Win64",
"MacIntel"

]

# ===============================
# WEBGL VENDOR
# ===============================

WEBGL_VENDORS = [

"Intel Inc.",
"NVIDIA Corporation",
"AMD"

]

# ===============================
# WEBGL RENDERER
# ===============================

WEBGL_RENDERERS = [

"Intel Iris OpenGL Engine",
"NVIDIA GeForce GTX 1050",
"AMD Radeon RX 580"

]

# ===============================
# FONTS
# ===============================

FONTS = [

"Arial",
"Calibri",
"Times New Roman",
"Verdana",
"Segoe UI"

]


# ===============================
# RANDOM FUNCTIONS
# ===============================

def random_user_agent():
    return random.choice(USER_AGENTS)


def random_resolution():
    return random.choice(RESOLUTIONS)


def random_timezone():
    return random.choice(TIMEZONES)


def random_language():
    return random.choice(LANGUAGES)


def random_platform():
    return random.choice(PLATFORMS)


def random_webgl_vendor():
    return random.choice(WEBGL_VENDORS)


def random_webgl_renderer():
    return random.choice(WEBGL_RENDERERS)


def random_fonts():
    return random.sample(FONTS, random.randint(2, 4))


def random_canvas_noise():
    return random.randint(1, 10)


def random_audio_noise():
    return random.uniform(0.0001, 0.001)


# ===============================
# GENERATE FULL FINGERPRINT
# ===============================

def generate_fingerprint():

    fingerprint = {

        "user_agent": random_user_agent(),

        "resolution": random_resolution(),

        "timezone": random_timezone(),

        "language": random_language(),

        "platform": random_platform(),

        "webgl_vendor": random_webgl_vendor(),

        "webgl_renderer": random_webgl_renderer(),

        "fonts": random_fonts(),

        "canvas_noise": random_canvas_noise(),

        "audio_noise": random_audio_noise()

    }

    return fingerprint


# ===============================
# EXPORT JSON
# ===============================

def fingerprint_to_json():

    fingerprint = generate_fingerprint()

    return json.dumps(fingerprint)