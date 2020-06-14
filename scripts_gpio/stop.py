#!/usr/bin/env python3
import RPi.GPIO as GPIO
import detector
import weather
import therm


def destroy():
    detector.destroy()
    therm.destroy()
    weather.destroy()
    GPIO.cleanup()


if __name__ == '__main__':
    try:
        destroy()
    except KeyboardInterrupt:
        destroy()
