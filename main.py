import os
import tempfile
from pathlib import Path
import requests
import marimo

# GitHub repository and notebook details
GITHUB_REPO = "Tiru-Kaggundi/DistrictsExports"
NOTEBOOK_NAME = "state_port_country.py"

def download_github_file(repo: str, file_path: str) -> tuple[str, str]:
    """Download a specific file from GitHub repo."""
    api_url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
    response = requests.get(api_url)
    response.raise_for_status()
    content = requests.get(response.json()["download_url"]).text
    return file_path, content

# Download the notebook
file_path, content = download_github_file(GITHUB_REPO, NOTEBOOK_NAME)

# Setup Marimo server
server = marimo.create_asgi_app()
tmp_dir = tempfile.TemporaryDirectory()

# Save the notebook locally
local_path = Path(tmp_dir.name) / NOTEBOOK_NAME
local_path.parent.mkdir(parents=True, exist_ok=True)
local_path.write_text(content)

# Add the notebook as an app
server = server.with_app(path="/", root=str(local_path))  # Set root path to "/"

# Build and serve the app
app = server.build()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860, log_level="info")
