import os
import time
import json
import requests
from PIL import Image, ImageDraw, ImageFont

PASSWORD = os.environ["PASSWORD"]
URL = "https://sc-live-images.deta.dev/upload?password=" + PASSWORD


def update_image(date):
  try:
    original = Image.open('original_banner.png')
    draw = ImageDraw.Draw(original)
    font = ImageFont.truetype('Comfortaa-Bold.ttf', 100)
    font_small = ImageFont.truetype('Comfortaa-Bold.ttf', 50)

    all_versions = requests.get(
      "https://pypi.org/pypi/scratchconnect/json").json()["releases"]
    latest_version = list(all_versions.keys())[-1]

    recent_downloads = requests.get(
      "https://pypistats.org/api/packages/scratchconnect/recent").json(
      )["data"]["last_month"]

    total_size = requests.get(
      "https://api.github.com/repos/Sid72020123/scratchconnect").json()["size"]

    draw.text((1810, 170), latest_version, font=font, fill=(255, 255, 255))
    draw.text((750, 767),
              f"{recent_downloads:,} (last month)",
              font=font,
              fill=(255, 255, 255))
    draw.text((2750, 767),
              f"{total_size}KB (Github)",
              font=font,
              fill=(255, 255, 255))
    draw.text((2850, 1250),
              f"Last Updated on {date}",
              font=font_small,
              fill=(255, 255, 255))
    original.thumbnail((1000, 1000))
    original.save("banner.png")

    file = {'file': open('banner.png', 'rb')}
    r = requests.put(URL, files=file)
    if r.status_code == 200:
      return True
    else:
      return False
  except:
    return False


def start():
  last_update = ""
  with open("last_update.json", "r") as file:
    try:
      last_update = json.loads(file.read())["Date"]
    except:
      last_update = ""
  while True:
    current_date = time.strftime("%d/%m/%Y")
    if last_update != current_date:
      u = update_image(current_date)
      if u:
        print(f"Updated data for: {current_date}")
        with open("last_update.json", "w") as file:
          file.write(json.dumps({"Date": current_date}))
        last_update = current_date
    time.sleep(3600)
