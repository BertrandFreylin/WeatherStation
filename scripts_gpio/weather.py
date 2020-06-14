#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

dhtPin = 17
MAX_UNCHANGE_COUNT = 100

STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5


def read_dht():
    GPIO.setup(dhtPin, GPIO.OUT)
    GPIO.output(dhtPin, GPIO.HIGH)
    time.sleep(0.05)
    GPIO.output(dhtPin, GPIO.LOW)
    time.sleep(0.02)
    GPIO.setup(dhtPin, GPIO.IN, GPIO.PUD_UP)

    unchanged_count = 0
    last = -1
    data = []
    while True:
        current = GPIO.input(dhtPin)
        data.append(current)
        if last != current:
            unchanged_count = 0
            last = current
        else:
            unchanged_count += 1
            if unchanged_count > MAX_UNCHANGE_COUNT:
                break

    state = STATE_INIT_PULL_DOWN

    lengths = []
    current_length = 0

    for current in data:
        current_length += 1

        if state == STATE_INIT_PULL_DOWN:
            if current == GPIO.LOW:
                state = STATE_INIT_PULL_UP
            else:
                continue
        if state == STATE_INIT_PULL_UP:
            if current == GPIO.HIGH:
                state = STATE_DATA_FIRST_PULL_DOWN
            else:
                continue
        if state == STATE_DATA_FIRST_PULL_DOWN:
            if current == GPIO.LOW:
                state = STATE_DATA_PULL_UP
            else:
                continue
        if state == STATE_DATA_PULL_UP:
            if current == GPIO.HIGH:
                current_length = 0
                state = STATE_DATA_PULL_DOWN
            else:
                continue
        if state == STATE_DATA_PULL_DOWN:
            if current == GPIO.LOW:
                lengths.append(current_length)
                state = STATE_DATA_PULL_UP
            else:
                continue
    if len(lengths) != 40:
        return False

    shortest_pull_up = min(lengths)
    longest_pull_up = max(lengths)
    halfway = (longest_pull_up + shortest_pull_up) / 2
    bits = []
    the_bytes = []
    byte = 0

    for length in lengths:
        bit = 0
        if length > halfway:
            bit = 1
        bits.append(bit)
    for i in range(0, len(bits)):
        byte = byte << 1
        if bits[i]:
            byte = byte | 1
        else:
            byte = byte | 0
        if (i + 1) % 8 == 0:
            the_bytes.append(byte)
            byte = 0
    checksum = (the_bytes[0] + the_bytes[1] +
                the_bytes[2] + the_bytes[3]) & 0xFF
    if the_bytes[4] != checksum:
        return False

    return the_bytes[0], the_bytes[2]


def setup_files(number_of_lines):
    num_lines_temp = sum(1 for line in open('/home/bertrand/workspace/rasp/static/data/weather_temp.csv'))
    if num_lines_temp > number_of_lines:
        to_delete = int(num_lines_temp - number_of_lines)
        with open('/home/bertrand/workspace/rasp/static/data/weather_temp.csv', 'r') as fin:
            data = fin.read().splitlines(True)
        with open('/home/bertrand/workspace/rasp/static/data/weather_temp.csv', 'w') as fout:
            fout.writelines(data[to_delete:])
        fin.close()
        fout.close()

    num_lines_humidity = sum(1 for line in open('/home/bertrand/workspace/rasp/static/data/weather_humidity.csv'))
    if num_lines_humidity > number_of_lines:
        to_delete = int(num_lines_humidity - number_of_lines)
        with open('/home/bertrand/workspace/rasp/static/data/weather_humidity.csv', 'r') as fin:
            data = fin.read().splitlines(True)
        with open('/home/bertrand/workspace/rasp/static/data/weather_humidity.csv', 'w') as fout:
            fout.writelines(data[to_delete:])
        fin.close()
        fout.close()
    return


def main(number_of_lines, date):
    result = None
    while not result:
        result = read_dht()
    if result:
        humidity, temperature = result

        weather_temp = open("/home/bertrand/workspace/rasp/static/data/weather_temp.csv", "a+")
        weather_temp.write("%s,%s\n" % (date, temperature))
        num_lines_temp = sum(1 for line in open('/home/bertrand/workspace/rasp/static/data/weather_temp.csv'))
        if num_lines_temp > number_of_lines:
            with open('/home/bertrand/workspace/rasp/static/data/weather_temp.csv', 'r') as fin:
                data = fin.read().splitlines(True)
            with open('/home/bertrand/workspace/rasp/static/data/weather_temp.csv', 'w') as fout:
                fout.writelines(data[1:])
        weather_temp.close()
        weather_temp_total = open("/home/bertrand/workspace/rasp/static/data/weather_temp_total.csv", "a+")
        weather_temp_total.write("%s,%s\n" % (date, temperature))
        weather_temp_total.close()

        weather_humidity = open("/home/bertrand/workspace/rasp/static/data/weather_humidity.csv", "a+")
        weather_humidity.write("%s,%s\n" % (date, humidity))
        num_lines_humidity = sum(1 for line in open('/home/bertrand/workspace/rasp/static/data/weather_humidity.csv'))
        if num_lines_humidity > number_of_lines:
            with open('/home/bertrand/workspace/rasp/static/data/weather_humidity.csv', 'r') as fin:
                data = fin.read().splitlines(True)
            with open('/home/bertrand/workspace/rasp/static/data/weather_humidity.csv', 'w') as fout:
                fout.writelines(data[1:])
        weather_humidity.close()
        weather_humidity_total = open("/home/bertrand/workspace/rasp/static/data/weather_humidity_total.csv", "a+")
        weather_humidity_total.write("%s,%s\n" % (date, humidity))
        weather_humidity_total.close()
        return

def destroy():
    weather_temp = open("/home/bertrand/workspace/rasp/static/data/weather_temp.csv", "a+")
    weather_temp.close()
    weather_humidity = open("/home/bertrand/workspace/rasp/static/data/weather_humidity.csv", "a+")
    weather_humidity.close()
    weather_humidity_total = open("/home/bertrand/workspace/rasp/static/data/weather_humidity_total.csv", "a+")
    weather_humidity_total.close()
    weather_temp_total = open("/home/bertrand/workspace/rasp/static/data/weather_temp_total.csv", "a+")
    weather_temp_total.close()
    return
