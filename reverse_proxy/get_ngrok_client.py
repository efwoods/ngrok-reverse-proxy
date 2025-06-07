import asyncio
import httpx
import os
from pyngrok import ngrok

_ngrok_url = None
_ngrok_tunnel = None
_ngrok_lock = asyncio.Lock()

NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GIST_ID = os.getenv("GIST_ID")

async def get_ngrok_client():
    global _ngrok_url, _ngrok_tunnel
    async with _ngrok_lock:
        if _ngrok_tunnel is None:
            try:
                ngrok.set_auth_token(NGROK_AUTH_TOKEN)
                _ngrok_tunnel = ngrok.connect(8000, "http", bind_tls=True)

                timeout = 10
                while not _ngrok_tunnel.public_url and timeout > 0:
                    await asyncio.sleep(0.5)
                    timeout -= 0.5

                if _ngrok_tunnel.public_url:
                    _ngrok_url = _ngrok_tunnel.public_url
                    print(f"Ngrok public URL: {_ngrok_url}")

                    # Update Gist with public URL
                    async with httpx.AsyncClient() as client:
                        gist_url = f"https://api.github.com/gists/{GIST_ID}"
                        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
                        gist_data = {
                            "description": "Ngrok public API gateway URL",
                            "files": {
                                "api_gateway_url.txt": {
                                    "content": _ngrok_url
                                }
                            }
                        }
                        response = await client.patch(gist_url, headers=headers, json=gist_data)
                        response.raise_for_status()
                        print("Updated GitHub Gist with ngrok URL")
                else:
                    raise RuntimeError("Ngrok tunnel failed to get public_url.")
            except Exception as e:
                _ngrok_tunnel = None
                _ngrok_url = None
                raise RuntimeError(f"Failed to start ngrok: {e}")
    return _ngrok_url
