import serial

#Identify serial Connection
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
			

			line = line[2:10]
			#line = float(line)
			print (line)
