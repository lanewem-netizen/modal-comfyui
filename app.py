import modal

app = modal.App("comfyui")

image = (
    modal.Image.debian_slim()
    .apt_install("git", "python3", "python3-pip")
    .run_commands(
        "git clone https://github.com/comfyanonymous/ComfyUI.git /root/ComfyUI",
        "cd /root/ComfyUI && pip install -r requirements.txt"
    )
)

@app.function(
    gpu="L4",
    image=image,
    timeout=3600,
)
@modal.web_server(8188)
def ui():
    import os

    os.chdir("/root/ComfyUI")

    os.system(
        "python main.py --listen 0.0.0.0 --port 8188"
    )
