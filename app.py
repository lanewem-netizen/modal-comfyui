import modal

app = modal.App("comfyui")

image = (
    modal.Image.debian_slim()
    .apt_install("git")
    .pip_install("torch", "torchvision", "torchaudio")
    .run_commands(
        "git clone https://github.com/comfyanonymous/ComfyUI.git /root/ComfyUI",
        "cd /root/ComfyUI && pip install -r requirements.txt"
    )
)

@app.function(
    gpu="L4",
    image=image,
    scaledown_window=300,
    timeout=3600,
)
@modal.web_server(8188, startup_timeout=600)
def ui():
    import subprocess

    subprocess.run(
        [
            "python",
            "/root/ComfyUI/main.py",
            "--listen",
            "0.0.0.0",
            "--port",
            "8188",
        ]
    )
