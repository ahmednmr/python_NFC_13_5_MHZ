import serial


	

def usb_init_port(usb_port,baud_rate,serial_timeout):	
	usb_init_port.ser = serial.Serial(usb_port, baud_rate,timeout=serial_timeout)

def usb_port_status():
	if usb_init_port.ser.is_open ==True:
		return True
	else :
		return False	
	
def usb_open_port():
	if usb_port_status() :
		print("is opened already")	
		return True
	else :
		usb_init_port.ser.open()
		if usb_port_status() :
			print("just opened")
			return True
		else :
			print("couldn't open the port")
			return False

def usb_close_port():
	if usb_port_status() :
		usb_init_port.ser.close()
		if usb_port_status() ==False:
			print("just closed")
			return True
		else :
			print("could't close the port")
			return False
	else :
		print("is closed already")
		return True
		
def usb_read_ch_serial():
	
	rec_char = usb_init_port.ser.read(1)
	return rec_char

def usb_read_hex_ch_serial():
	
	rec_char = usb_init_port.ser.read(1).hex()
	return rec_char
	
def usb_write_str_serial(_string):
	usb_flush_recieving()
	usb_init_port.ser.write(_string)

def usb_flush_recieving():
	usb_init_port.ser.flushInput()	

	
'''
usb_init_port("COM3","115200",0.0016)

usb_port_status()
usb_open_port()
usb_open_port()
usb_open_port()
usb_close_port()
usb_open_port()
usb_close_port()
usb_close_port()
usb_close_port()

usb_write_str_serial("hello")
usb_read_hex_ch_serial()
usb_close_port()
'''
	
