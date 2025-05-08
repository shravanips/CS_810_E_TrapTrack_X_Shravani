# fingerprint_dectector.py

def inject_fingerprint_detection(page):
    js_code = """
    (() => {
        const results = {};

        // Canvas fingerprint
        try {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = 'red';
            ctx.fillRect(10, 10, 100, 100);
            results.canvas = canvas.toDataURL();
        } catch (e) {
            results.canvas = 'error';
        }

        // WebGL fingerprint
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl');
            results.webgl = gl.getSupportedExtensions();
        } catch (e) {
            results.webgl = 'error';
        }

        // AudioContext fingerprint
        try {
            const context = new (window.AudioContext || window.webkitAudioContext)();
            results.audio = context.sampleRate;
        } catch (e) {
            results.audio = 'error';
        }

        // Store result
        window._fp_results = results;
    })();
    """

    try:
        page.evaluate(js_code)
        print("[✔] Fingerprint detection script injected.")
    except Exception as e:
        print(f"[!] Failed to inject fingerprint detector: {e}")
