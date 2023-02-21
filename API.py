import os
import time
import json
import requests
from PIL import Image, ImageDraw, ImageFont

PASSWORD = os.environ["PASSWORD"]
URL = "https://sc-live-images.deta.dev/upload?password=" + PASSWORD


def update_image_sui(h, d):
  try:
    original = Image.open('original_sui_banner.png')
    draw = ImageDraw.Draw(original)
    font = ImageFont.truetype('Comfortaa-Bold.ttf', 25)
    small_font = ImageFont.truetype('Comfortaa-Bold.ttf', 15)
    version = requests.get("https://sui.sid72020123.repl.co").json()["Version"]
    total_users_indexed = requests.get("https://sui.sid72020123.repl.co/status").json()["TotalUsers"]
    random_data = requests.get("https://sui.sid72020123.repl.co/random").json()["RandomData"][0]
    id = random_data["_id"]
    u = random_data["Username"]
    with open("user_pfp.png", "wb") as file:
      file.write(requests.get(f"https://xnw7rh.deta.dev/get/https://uploads.scratch.mit.edu/get_image/user/{id}_90x90.png?v=").content)
    pfp = Image.open("user_pfp.png").convert("RGBA")
    draw.text((268, 135), version, font=font, fill=(255, 255, 255))
    draw.text((342, 194), f"{total_users_indexed:,}", font=font, fill=(255, 255, 255))
    draw.text((281, 332), id, font=font, fill=(255, 255, 255))
    draw.text((402,391), u, font=font, fill=(255, 255, 255))
    original.paste(pfp, (150, 330), mask=pfp)
    draw.text((595, 470), f"Last updated on {d} at {h}", font=small_font, fill=(255, 255, 255))
    original.thumbnail((1000, 1000))
    original.save("sui_banner.png")

    file = {'file': open('sui_banner.png', 'rb')}
    r = requests.put(URL, files=file)
    if r.status_code == 200:
      return True
    else:
      return False
  except Exception as E:
    print(E)
    return False


def update_image_sc(date):
  try:
    original = Image.open('original_sc_banner.png')
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
    original.save("sc_banner.png")

    file = {'file': open('sc_banner.png', 'rb')}
    r = requests.put(URL, files=file)
    if r.status_code == 200:
      return True
    else:
      return False
  except:
    return False


def get_schedules():
  with open("last_update.json", "r") as file:
    try:
      return json.loads(file.read())
    except:
      return {"scLive": "", "SUILive": ""}


def update_schedules(type, t):
  data = get_schedules()
  with open("last_update.json", "w") as file:
    data[type] = t
    file.write(json.dumps(data))


def start_sc():
  last_update = get_schedules()["scLive"]
  while True:
    current_date = time.strftime("%d/%m/%Y")
    if last_update != current_date:
      u = update_image_sc(current_date)
      if u:
        print(f"SC: Updated data for: {current_date}")
        update_schedules("scLive", current_date)
        last_update = current_date
    time.sleep(3600)


def start_sui():
  schedule_time = get_schedules()["SUILive"]
  while True:
    current_time = time.strftime("%H:%M:%S")
    if schedule_time == current_time:
      d = time.strftime("%d/%m/%Y")
      u = update_image_sui(current_time, d)
      if u:
        print(f"SUI: Updated data for: {d} {current_time}")
      t = schedule_time.split(":")
      if t[0] == "23":
        t[0] = "00"
      else:
        if int(t[0]) + 1 < 10:
          t[0] = "0" + str(int(t[0]) + 1)
        else:
          t[0] = str(int(t[0]) + 1)
      st = ":".join(t)
      update_schedules("SUILive", st)
      schedule_time = get_schedules()["SUILive"]
    time.sleep(1)
