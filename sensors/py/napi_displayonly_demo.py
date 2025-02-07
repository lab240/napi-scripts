# main.py

import time
from PIL import Image, ImageDraw, ImageFont
import spidev
import SSD1306
import napi_sci_hw as hw  # Импортируем наш модуль с новым названием
import napi_sci_sht30 as sht30  # Импортируем наш модуль с новым названием
import subprocess

# Инициализация OLED дисплея
SPI_PORT = 2
SPI_DEVICE = 0

#rstpin = 7  # GPIO2_A7
#rstchip = "/dev/gpiochip2"
#dcpin = 9  # GPIO2_B1
#dcchip = "/dev/gpiochip2"

dcpin = 7  # GPIO2_A7
dcchip = "/dev/gpiochip2"
rstpin = 9  # GPIO2_B1
rstchip = "/dev/gpiochip2"

spi = spidev.SpiDev()
spi.open(SPI_PORT, SPI_DEVICE)
spi.max_speed_hz = 8000000
disp = SSD1306.SSD1306_128_64(rstpin=rstpin, rstchip=rstchip, dcpin=dcpin, dcchip=dcchip, spi=spi)

disp.begin()
disp.clear()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

while True:
    draw.rectangle((0, 0, width, height), fill=255)

    # Системная информация
    cmd = "ip -4 addr show dev end0 | awk '/inet/ {print $2}' | cut -d'/' -f1"
    IP = "IP:" + subprocess.check_output(cmd, shell=True).decode('utf-8')

    # Отображение данных на экране
    draw.text((0, 0), IP, font=font, fill=0)
    disp.ShowImage(disp.getbuffer(image))
    time.sleep(0.5)
