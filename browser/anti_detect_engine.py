def inject(context, fingerprint):

    # 1. WebDriver removal
    context.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    """)

    # 2. Languages
    lang = fingerprint.get("language", "en-US")
    context.add_init_script(f"""
    Object.defineProperty(navigator, 'languages', {{ get: () => ['{lang}', '{lang.split('-')[0]}'] }});
    """)

    # 3. Platform
    platform = fingerprint.get("platform", "Win32")
    context.add_init_script(f"""
    Object.defineProperty(navigator, 'platform', {{ get: () => '{platform}' }});
    """)

    # 4. WebRTC Leak Protection (Spoofing IP)
    context.add_init_script("""
    const rtcConfig = { get: () => undefined };
    Object.defineProperty(window, 'RTCPeerConnection', rtcConfig);
    Object.defineProperty(window, 'webkitRTCPeerConnection', rtcConfig);
    """)

    # 5. Canvas Noise
    noise = fingerprint.get("canvas_noise", 1)
    context.add_init_script(f"""
    const getImageData = CanvasRenderingContext2D.prototype.getImageData;
    CanvasRenderingContext2D.prototype.getImageData = function() {{
        const data = getImageData.apply(this, arguments);
        data.data[0] += {noise};
        return data;
    }}
    """)

    # 6. WebGL Vendor/Renderer
    vendor = fingerprint.get("webgl_vendor", "Intel Inc.")
    renderer = fingerprint.get("webgl_renderer", "Intel Iris OpenGL Engine")
    context.add_init_script(f"""
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter){{
        if(parameter === 37445) return "{vendor}";
        if(parameter === 37446) return "{renderer}";
        return getParameter(parameter);
    }}
    """)

    # 7. Screen Resolution consistency
    res = fingerprint.get("resolution", "1920x1080").split("x")
    w, h = res[0], res[1]
    context.add_init_script(f"""
    Object.defineProperty(screen, 'width', {{ get: () => {w} }});
    Object.defineProperty(screen, 'height', {{ get: () => {h} }});
    Object.defineProperty(screen, 'availWidth', {{ get: () => {w} }});
    Object.defineProperty(screen, 'availHeight', {{ get: () => {h} }});
    Object.defineProperty(window, 'innerWidth', {{ get: () => {w} }});
    Object.defineProperty(window, 'innerHeight', {{ get: () => {h} }});
    """)