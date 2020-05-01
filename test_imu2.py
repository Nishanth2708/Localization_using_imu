import RPi.GPIO as gpio
import time
import numpy as np		
import math
import serial

def init():
	gpio.setmode(gpio.BOARD)
	gpio.setup(31, gpio.OUT)
	gpio.setup(33, gpio.OUT)
	gpio.setup(35, gpio.OUT)
	gpio.setup(37, gpio.OUT)

	gpio.setup(7, gpio.IN, pull_up_down= gpio.PUD_UP)
	gpio.setup(12, gpio.IN, pull_up_down= gpio.PUD_UP)

def gameover():
	gpio.output(31, False)
	gpio.output(33, False)
	gpio.output(35, False)
	gpio.output(37, False)
	
	gpio.cleanup()




file1 = open("imu_drive.txt","a")



#file1 = open("Encoder_data_3.txt","a")

def forward(ticks):
	init()


	counterBR = np.uint64(0)
	counterFL = np.uint64(0)

	buttonBR = int(0)
	buttonFL = int(0)

	# Initialize pwm signal to control motor
	pwm1 = gpio.PWM(31,50)
	pwm2 = gpio.PWM(37,50)
	val = 60
	pwm1.start(val)
	pwm2.start(val)
	time.sleep(0.1)

	for i in range (0,10000000):
		print("counterBR = ",counterBR,"counterFL = ",counterFL,"BR state: ", gpio.input(12),"FL state: ", gpio.input(7))
		#file1.write(str(gpio.input(12))+str(gpio.input(7))+"\n"k)
		if int(gpio.input(12) != int(buttonBR)):
			buttonBR = int(gpio.input(12))
			counterBR += 1

		if int(gpio.input(7) != int(buttonFL)):
			buttonFL = int(gpio.input(7))
			counterFL = counterFL+1
	
		error = counterFL-counterBR
		counterBR += error
		if counterFL >= ticks:
			pwm1.stop()
			
		if counterBR >= ticks:
			pwm2.stop()


		if counterBR >=ticks and counterFL >= ticks :	
			gameover()
			print("Thanks for Playing")
			avg = float(counterBR+counterFL)/2

			dist = 100*avg/97
			dist = int(dist)
			file1.write(str(dist)+"\n")
			break

def reverse(ticks):
	init()


	counterBR = np.uint64(0)
	counterFL = np.uint64(0)

	buttonBR = int(0)
	buttonFL = int(0)

	# Initialize pwm signal to control motor
	pwm1 = gpio.PWM(33,50)
	pwm2 = gpio.PWM(35,50)
	val = 60
	pwm1.start(val)
	pwm2.start(val)
	time.sleep(0.1)

	for i in range (0,10000000):
		print("counterBR = ",counterBR,"counterFL = ",counterFL,"BR state: ", gpio.input(12),"FL state: ", gpio.input(7))
		#file1.write(str(gpio.input(12))+str(gpio.input(7))+"\n")

		if int(gpio.input(12) != int(buttonBR)):
			buttonBR = int(gpio.input(12))
			counterBR += 1

		if int(gpio.input(7) != int(buttonFL)):
			buttonFL = int(gpio.input(7))
			counterFL = counterFL+1
		
		error = counterFL-counterBR
		counterBR += error
		if counterFL >= ticks:
			pwm1.stop()
			
		if counterBR >= ticks:
			pwm2.stop()


		if counterBR >=ticks and counterFL >= ticks :	
			gameover()
			print("Thanks for Playing")
			#file1.close()
			break

def left(rot):
	init()
	ticks= rot*5.85
	

	counterBR = np.uint64(0)
	counterFL = np.uint64(0)

	buttonBR = int(0)
	buttonFL = int(0)

	# Initialize pwm signal to control motor
	pwm1 = gpio.PWM(33,50)
	pwm2 = gpio.PWM(37,50)
	val = 95
#	time.sleep(0.1)
	count =0
	flag = 0
	ser = serial.Serial('/dev/ttyUSB0', 9600)
	while True:
		if (ser.in_waiting >0):
			count +=1

			line = ser.readline()
			if count > 10:
				if flag ==0:
					pwm2.start(val)
					#time.sleep(0.01)
					pwm1.start(val)
					flag =1			
				line = line.rstrip().lstrip()
				line = str(line)
				line = line.strip("'")
				line = line.strip("b'")

				line = line[2:9]
				angle = float(line)
				diff = 360 - angle
				print("Angle = ",angle,"counterBR = ",counterBR,"counterFL = ",counterFL,"BR state: ", gpio.input(12),"FL state: ", gpio.input(7))
				#file1.write(str(gpio.input(12))+str(gpio.input(7))+"\n")
				#angle = getimu()
				#diff = int(360-angle)
				if int(gpio.input(12) != int(buttonBR)):
					buttonBR = int(gpio.input(12))
					counterBR += 1

				if int(gpio.input(7) != int(buttonFL)):
					buttonFL = int(gpio.input(7))
					counterFL = counterFL+1
						
				error = counterFL-counterBR
				counterBR += error
				if  counterFL >= ticks or (diff>=rot-3 and diff<=rot+3) :
					pwm1.stop()
					
				if  counterBR >= ticks or (diff>=rot-3 and diff<=rot+3):
					pwm2.stop()


				if (counterBR >=ticks and counterFL >= ticks) or (diff>=rot-3 and diff<=rot+3):
					gameover()
					avg = float(counterBR+counterFL)/2
					a = int(avg/0.25)
					file1.write(str(diff)+"\n")					
					print("Thanks for Playing")
					#file1.close()
					break

def right(rot):
	init()
	ticks= rot*5.85


	counterBR = np.uint64(0)
	counterFL = np.uint64(0)

	buttonBR = int(0)
	buttonFL = int(0)

	# Initialize pwm signal to control motor
	pwm1 = gpio.PWM(31,50)
	pwm2 = gpio.PWM(35,50)
	val = 95
#	pwm1.start(val)
#	pwm2.start(val)
	time.sleep(0.1)
	count =0
	flag =0
	ser = serial.Serial('/dev/ttyUSB0', 9600)
	while True:
		if (ser.in_waiting >0):
			count +=1

			line = ser.readline()
			if count > 10:


				if flag ==0:
					pwm1.start(val)
					pwm2.start(val)
					flag =1
				line = line.rstrip().lstrip()
				line = str(line)
				line = line.strip("'")
				line = line.strip("b'")
				line= line[2:9]
				diff = float(line)



				print("Angle = ",diff,"counterBR = ",counterBR,"counterFL = ",counterFL,"BR state: ", gpio.input(12),"FL state: ", gpio.input(7))
				#print("counterBR = ",counterBR,"counterFL = ",counterFL,"BR state: ", gpio.input(12),"FL state: ", gpio.input(7))
				#file1.write(str(gpio.input(12))+str(gpio.input(7))+"\n"))
				#diff = getimu()	
			#	diff = 360-angle 
				if int(gpio.input(12) != int(buttonBR)):
					buttonBR = int(gpio.input(12))
					counterBR += 1

				if int(gpio.input(7) != int(buttonFL)):
					buttonFL = int(gpio.input(7))
					counterFL = counterFL+1
						
				error = counterFL-counterBR
				counterBR += error
				if counterFL >= ticks or diff >= rot:
					pwm1.stop()
					pwm2.stop()
				#if counterBR >= ticks or diff >= rot:
					#pwm2.stop()


				#if (counterBR >=ticks and counterFL >= ticks) or diff >= rot :	
					#gameover()
					#print("Thanks for Playing")
					#file1.close()
					break

def key_input(event):
	init()
	print("Key: " ,event)
	key_press = event
#	tf=1
	if key_press.lower() == 'w':
		x = input('Enter distance in Meters:')
		x = float(x)
		ticks= (1/(3.14*2*0.0325))*x*960
		forward(ticks)
	elif key_press.lower() == 's':
		x = input('Enter distance in Meters:')
		x = float(x)
		ticks= (1/(3.14*2*0.0325))*x*960
		reverse(ticks)
	elif key_press.lower() == 'a':
		x = input('Enter Angle in degrees:')
		x = int(x)
	#	ticks = int(ticks)
		left(x)
	elif key_press.lower() == 'd':
		x = input('Enter Angle in degrees:')
		x = float(x)
		#ticks= x*0.25
		right(x)
	else:
		print("Invalid")
		#gameover()
		#gpio.cleanup()

def getimu():
	ser = serial.Serial('/dev/ttyUSB0',9600)

	count = 0

	while True:

		if(ser.in_waiting>0):
			count+=1

			# Read Serial Stream

			line = ser.readline()
		#	print(line)

			# Avoid first n-lines
			if count >10:

				# Strip serial stream of extra characters
				line = line.rstrip().lstrip()
			#	print(line)

				line = str(line)
				line = line.strip("'")
				line = line.strip("b'")
			#	print(line)

				# Return float

				line = float(line)
				return line
while True:
#	forward(rev)
	key_press = input("Select driving mode:")
	if key_press =='p':
#		file1.close()
		break
	key_input(key_press)
