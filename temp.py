import os 
import glob 
import time
 
os.system('modprobe w1-gpio') 
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/' 
device_folder = glob.glob(base_dir + '28*')[0] 
device_file = device_folder + '/w1_slave'

timeStamp = time.strftime("%Y%m%d_%H%M%S") 
outFileName = "".join(["temp_sensor_data_", timeStamp, ".dat"]) 
outFile = open(outFileName, 'w') 
outFile.write('    time [s]    temp [*C]    temp [*F]\n') 

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

# Intial time and screen print information
tInit = time.time()	
tInterval = 5.0 
print("\n    time [s]    temp [*C]    temp [*F]")

# Main Loop
try:
	while True:
		t1 = time.time()
		[temp_c, temp_f] = read_temp()
		t2 = time.time()
		dt = t2 - tInit
		outFile.write(" %12.2e %12.2f %12.2f\n" % (dt, temp_c, temp_f))

		print("%12.2e %12.2f %12.2f" % (dt, temp_c, temp_f))
		tDiff = tInterval - (t2 - t1)
		time.sleep(tDiff)
	
except KeyboardInterrupt:
	print("Keyboard Interrupt, ending main loop...")
	pass

outFile.close()
