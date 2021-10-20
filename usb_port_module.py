import serial


	

def usb_init_port(usb_port,baud_rate,serial_timeout):	
	usb_init_port.ser = serial.Serial(usb_port, baud_rate,timeout=serial_timeout)

def usb_port_status():
		if usb_init_port.ser.isOpen():
			return True
		else :
			return False

	
def usb_open_port():
	if usb_port_status() :
		print("opened")	
		return True
	else :
		print("hust opened")
		usb_init_port.ser.open()
		return False

def usb_close_port():
	usb_init_port.ser.close()
	
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
usb_open_port()

usb_write_str_serial("hello")
usb_read_hex_ch_serial()
usb_close_port()
'''
	
