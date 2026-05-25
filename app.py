import modal

app = modal.App("comfyui")

image = (
    modal.Image.debian_slim()
    .apt_install("git", "wget")
    .pip_install("comfy-cli")
    .run_commands(
        "comfy --skip-prompt install"
    )
)

@app.function(
    gpu="L4",
    image=image,
    timeout=3600,
)
@modal.web_server(8188)
def ui():
    import subprocess

    subprocess.Popen(
        "comfy launch -- --listen 0.0.0.0 --port 8188",
        shell=True,
    )
