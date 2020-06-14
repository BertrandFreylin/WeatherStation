#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import detector
import weather
import therm
import ADC0834

wait_blink = 0.1
period_btw_save = 60 * 5
time_sleep = period_btw_save - wait_blink
time_to_display = 60 * 60 * 24 * 3
number_of_lines = time_to_display / period_btw_save
pins = {'Red': 24, 'Green': 18, 'Blue': 27}
COLOR = {'Red': 0xFF0000, 'Green': 0x00FF00, 'Blue': 0x0000FF}


def cleanup():
    GPIO.cleanup()


def config():
    GPIO.setmode(GPIO.BCM)
    ADC0834.setup()

    # setup_light()

    therm.setup_files(number_of_lines)
    weather.setup_files(number_of_lines)


def color_start():
    p_R.start(0)
    p_G.start(0)
    p_B.start(0)


def color_stop():
    p_R.stop()
    p_G.stop()
    p_B.stop()


def start():
    while True:
        date = time.strftime("%Y-%m-%dT%H:%M:%S-04:00")
        # color_start()

        # set_color(COLOR['Red'])
        detector.main()

        # set_color(COLOR['Green'])
        therm.main(number_of_lines, date)

        # set_color(COLOR['Blue'])
        weather.main(number_of_lines, date)

        # color_stop()
        time.sleep(period_btw_save)


def destroy():
    # color_stop()
    detector.destroy()
    therm.destroy()
    weather.destroy()
    GPIO.cleanup()


def map_light(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def set_color(color):
    red_value = (color & 0xFF0000) >> 16
    green_value = (color & 0x00FF00) >> 8
    blue_value = (color & 0x0000FF) >> 0
    red_value = map_light(red_value, 0, 255, 0, 100)
    green_value = map_light(green_value, 0, 255, 0, 100)
    blue_value = map_light(blue_value, 0, 255, 0, 100)
    p_R.ChangeDutyCycle(red_value)
    p_G.ChangeDutyCycle(green_value)
    p_B.ChangeDutyCycle(blue_value)


def setup_light():
    global p_R, p_G, p_B
    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT, initial=GPIO.HIGH)

    p_R = GPIO.PWM(pins['Red'], 2000)
    p_G = GPIO.PWM(pins['Green'], 2000)
    p_B = GPIO.PWM(pins['Blue'], 2000)

    color_start()


if __name__ == '__main__':
    try:
        cleanup()
        config()
        start()
    except KeyboardInterrupt:
        destroy()
