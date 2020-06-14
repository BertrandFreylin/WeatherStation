#!/usr/bin/env python3
import ADC0834
import time
import math


def setup_files(number_of_lines):
    num_lines_temp = sum(1 for line in open('/home/bertrand/workspace/rasp/static/data/therm_inside.csv'))
    if num_lines_temp > number_of_lines:
        to_delete = int(num_lines_temp - number_of_lines)
        with open('/home/bertrand/workspace/rasp/static/data/therm_inside.csv', 'r') as fin:
            data = fin.read().splitlines(True)
        with open('/home/bertrand/workspace/rasp/static/data/therm_inside.csv', 'w') as fout:
            fout.writelines(data[to_delete:])
        fin.close()
        fout.close()

    num_lines_photo = sum(1 for line in open('/home/bertrand/workspace/rasp/static/data/photo.csv'))
    if num_lines_photo > number_of_lines:
        to_delete = int(num_lines_photo - number_of_lines)
        with open('/home/bertrand/workspace/rasp/static/data/photo.csv', 'r') as fin:
            data = fin.read().splitlines(True)
        with open('/home/bertrand/workspace/rasp/static/data/photo.csv', 'w') as fout:
            fout.writelines(data[to_delete:])
        fin.close()
        fout.close()
        return


def main(number_of_lines, date):
    temp_val_raw = ADC0834.getResult(0)
    Vr = 5 * float(temp_val_raw) / 255
    Rt = 10000 * Vr / (5 - Vr)
    temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))
    temp_val = round(temp - 273.15)
    time.sleep(1)
    lum_val = round((ADC0834.getResult(2) * -1) + 255)

    weather_temp = open("/home/bertrand/workspace/rasp/static/data/therm_inside.csv", "a+")
    weather_temp.write("%s,%s\n" % (date, temp_val))
    num_lines_temp = sum(1 for line in open('/home/bertrand/workspace/rasp/static/data/therm_inside.csv'))
    if num_lines_temp > number_of_lines:
        with open('/home/bertrand/workspace/rasp/static/data/therm_inside.csv', 'r') as fin:
            data = fin.read().splitlines(True)
        with open('/home/bertrand/workspace/rasp/static/data/therm_inside.csv', 'w') as fout:
            fout.writelines(data[1:])
    weather_temp.close()
    weather_temp_total = open("/home/bertrand/workspace/rasp/static/data/therm_inside_total.csv", "a+")
    weather_temp_total.write("%s,%s\n" % (date, temp_val))
    weather_temp_total.close()

    photo = open("/home/bertrand/workspace/rasp/static/data/photo.csv", "a+")
    photo.write("%s,%s\n" % (date, lum_val))
    num_lines_photo = sum(1 for line in open('/home/bertrand/workspace/rasp/static/data/photo.csv'))
    if num_lines_photo > number_of_lines:
        with open('/home/bertrand/workspace/rasp/static/data/photo.csv', 'r') as fin:
            data = fin.read().splitlines(True)
        with open('/home/bertrand/workspace/rasp/static/data/photo.csv', 'w') as fout:
            fout.writelines(data[1:])
    photo.close()
    photo_total = open("/home/bertrand/workspace/rasp/static/data/photo_total.csv", "a+")
    photo_total.write("%s,%s\n" % (date, lum_val))
    photo_total.close()
    return


def destroy():
    weather_temp = open("/home/bertrand/workspace/rasp/static/data/therm_inside.csv", "a+")
    weather_temp.close()
    weather_temp_total = open("/home/bertrand/workspace/rasp/static/data/therm_inside_total.csv", "a+")
    weather_temp_total.close()

    photo = open("/home/bertrand/workspace/rasp/static/data/photo.csv", "a+")
    photo.close()
    photo_total = open("/home/bertrand/workspace/rasp/static/data/photo_total.csv", "a+")
    photo_total.close()
    return
