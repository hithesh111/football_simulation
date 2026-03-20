import urllib.request
import os

logo_dir = "assets/logos"
os.makedirs(logo_dir, exist_ok=True)

url = "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Real_Madrid_CF.svg/105px-Real_Madrid_CF.svg.png"
print(f"Downloading Real Madrid to {logo_dir}...")
try:
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        with open(os.path.join(logo_dir, "real_madrid.png"), "wb") as f:
            f.write(response.read())
    print("Success!")
    print("Files in logos:", os.listdir(logo_dir))
except Exception as e:
    print(f"Error: {e}")
