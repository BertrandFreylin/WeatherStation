#!/usr/bin/env python3
import time
from picamera import PiCamera, Color
import shutil
from PIL import Image


def main():
    date = time.strftime("%Y_%m_%d_%H_%M_%S")
    date_photo = time.strftime("%d-%m-%Y %H:%M")
    name_file = '/home/bertrand/images/someone_%s.png' % date

    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (2592, 1458)
    camera.annotate_text_size = 50
    camera.annotate_text = date_photo
    camera.annotate_background = Color('white')
    camera.annotate_foreground = Color('black')
    camera.brightness = 60
    camera.contrast = 55
    time.sleep(5)
    camera.capture(name_file)
    camera.close()

    shutil.move(name_file, '/home/bertrand/workspace/rasp/static/image_last/last.png')
    foo = Image.open('/home/bertrand/workspace/rasp/static/image_last/last.png').convert('RGB')
    foo = foo.resize((1024, 576), Image.ANTIALIAS)
    foo.save("/home/bertrand/workspace/rasp/static/image_last/last.jpg", optimize=True, quality=95)

    return


def destroy():
    camera = PiCamera()
    camera.close()
    return
