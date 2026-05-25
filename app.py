import modal

app = modal.App("comfyui")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install(
        "git",
        "ffmpeg",
        "libgl1",
    )
    .pip_install(
        "torch",
        "torchvision",
        "torchaudio",
        "fastapi",
        "uvicorn",
    )
    .run_commands(
        "git clone https://github.com/comfyanonymous/ComfyUI /root/ComfyUI",
        "cd /root/ComfyUI && pip install -r requirements.txt",
    )
)

@app.function(
    image=image,
    gpu="T4",
    timeout=60 * 60,
    scaledown_window=300,
)
@modal.asgi_app()
def ui():
    import os
    import subprocess
    import time
    from fastapi import FastAPI
    from fastapi.responses import RedirectResponse

    os.chdir("/root/ComfyUI")

    subprocess.Popen(
        [
            "python",
            "main.py",
            "--listen",
            "0.0.0.0",
            "--port",
            "8188",
        ]
    )

    time.sleep(15)

    web_app = FastAPI()

    @web_app.get("/")
    async def root():
        return RedirectResponse(url="http://127.0.0.1:8188")

    return web_app
