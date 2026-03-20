import urllib.request
import os
import time

logos = {
    "real_madrid.png": "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Real_Madrid_CF.svg/105px-Real_Madrid_CF.svg.png",
    "barcelona.png": "https://upload.wikimedia.org/wikipedia/en/thumb/4/47/FC_Barcelona_%28crest%29.svg/105px-FC_Barcelona_%28crest%29.svg.png",
    "bayern.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg/105px-FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg.png",
    "psg.png": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a7/Paris_Saint-Germain_F.C..svg/105px-Paris_Saint-Germain_F.C..svg.png",
    "arsenal.png": "https://upload.wikimedia.org/wikipedia/en/thumb/5/53/Arsenal_FC.svg/105px-Arsenal_FC.svg.png",
    "liverpool.png": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Liverpool_FC.svg/105px-Liverpool_FC.svg.png",
    "man_city.png": "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Manchester_City_FC_badge.svg/105px-Manchester_City_FC_badge.svg.png",
    "man_utd.png": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/Manchester_United_FC_crest.svg/105px-Manchester_United_FC_crest.svg.png"
}

logo_dir = os.path.join("assets", "logos")
if not os.path.exists(logo_dir):
    os.makedirs(logo_dir)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

for name, url in logos.items():
    print(f"Attempting download: {name}")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(os.path.join(logo_dir, name), 'wb') as f:
                f.write(response.read())
            print(f"Successfully downloaded {name}")
    except Exception as e:
        print(f"Failed to download {name}: {e}")
    time.sleep(1) # Be gentle to Wikimedia
