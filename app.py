import modal

app = modal.App("comfyui")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "ffmpeg", "libgl1")
    .pip_install(
        "torch",
        "torchvision",
        "torchaudio",
    )
    .run_commands(
        "git clone https://github.com/comfyanonymous/ComfyUI /root/ComfyUI",
        "cd /root/ComfyUI && pip install -r requirements.txt"
    )
)

@app.function(
    image=image,
    gpu="T4",
    timeout=60 * 60,
    container_idle_timeout=300,
)

@modal.web_server(8188, startup_timeout=60 * 10)
def ui():
    import subprocess

    subprocess.Popen(
        "python /root/ComfyUI/main.py --listen 0.0.0.0 --port 8188",
        shell=True,
    )
