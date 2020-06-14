#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

ADC_CS = 5
ADC_CLK = 19
ADC_DIO = 6


def setup(cs=5,clk=19,dio=6):
	global ADC_CS, ADC_CLK, ADC_DIO
	ADC_CS=cs
	ADC_CLK=clk
	ADC_DIO=dio
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)			# Number GPIOs by BCM mode
	GPIO.setup(ADC_CS, GPIO.OUT)		# Set pins' mode is output
	GPIO.setup(ADC_CLK, GPIO.OUT)		# Set pins' mode is output


def getResult(channel=0):	 				# Get ADC result, input channel

	sel = int(channel > 1 & 1)
	odd = channel & 1
	# print("sel: {}, odd: {}".format(sel, odd))

	GPIO.setup(ADC_DIO, GPIO.OUT)
	GPIO.output(ADC_CS, 0)
	
	# Start bit
	GPIO.output(ADC_CLK, 0)
	GPIO.output(ADC_DIO, 1)
	time.sleep(0.000002)
	GPIO.output(ADC_CLK, 1)
	time.sleep(0.000002)

	# Single End mode
	GPIO.output(ADC_CLK, 0)
	GPIO.output(ADC_DIO, 1)
	time.sleep(0.000002)
	GPIO.output(ADC_CLK, 1)
	time.sleep(0.000002)

	# ODD
	GPIO.output(ADC_CLK, 0)
	GPIO.output(ADC_DIO, odd)
	time.sleep(0.000002)
	GPIO.output(ADC_CLK, 1)
	time.sleep(0.000002)

	# Select
	GPIO.output(ADC_CLK, 0)
	GPIO.output(ADC_DIO, sel)
	time.sleep(0.000002)
	GPIO.output(ADC_CLK, 1)

	GPIO.output(ADC_DIO, 1)
	time.sleep(0.000002)
	GPIO.output(ADC_CLK, 0)
	GPIO.output(ADC_DIO, 1)
	time.sleep(0.000002)

	dat1 = 0
	for i in range(0, 8):
		GPIO.output(ADC_CLK, 1);  time.sleep(0.000002)
		GPIO.output(ADC_CLK, 0);  time.sleep(0.000002)
		GPIO.setup(ADC_DIO, GPIO.IN)
		dat1 = dat1 << 1 | GPIO.input(ADC_DIO)  
	
	dat2 = 0
	for i in range(0, 8):
		dat2 = dat2 | GPIO.input(ADC_DIO) << i
		GPIO.output(ADC_CLK, 1);  time.sleep(0.000002)
		GPIO.output(ADC_CLK, 0);  time.sleep(0.000002)
	
	GPIO.output(ADC_CS, 1)
	GPIO.setup(ADC_DIO, GPIO.OUT)

	if dat1 == dat2:
		return dat1
	else:
		return 0
