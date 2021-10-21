import usb_port_module as usb
import helper_module as helper
from array import *
import time

'''
//U8 NFC_Fixed_Company_ID_array[4]           ={0xE9,0xE8,0xE7,0xE6};
unsigned char config_arr[]                 ={0x14,0x01,0x14,0x01};
unsigned char response_config_arr[]        ={0X00,0X00,0XFF,0X00,0XFF,0X00,0X00,0X00,0XFF,0X02,0XFE,0XD5,0X15,0X16,0X00};

unsigned char read_tag_arr[]               ={0x4A,0x01,0x00};
unsigned char response_read_tag_arr[]      ={0x00,0x00,0xFF,0x00,0xFF,0x00,0x00,0x00,0xFF,0X0F,0XF1,0XD5,0X4B,0X01};
unsigned char NFC_Recieved_Data[13]        ={0};

unsigned char read_tag_data[]              ={0x40,0x01,0x30,0x04};
unsigned char response_read_tag_data[]     ={0x00,0x00,0xFF,0x00,0xFF,0x00,0x00,0x00,0xFF,0X13,0XED,0XD5,0X41,0X00};


unsigned char write_page_frame[8]          ={0x40,0x01,0xA2};
unsigned char response_write_page[]        ={0x00,0x00,0xFF,0x00,0xFF,0x00,0x00,0x00,0xFF,0X03,0XFD,0XD5,0X41,0X00,0xEA,0x00};

'''
DATA_TO_NFC_BYTE=0xD4
END_FRAME_BYTE=0x00
DATA_RECIEVING_CIZE=12
COMPANY_ID_PAGE_NUMBER            =4
TAG_ID_PAGE_NUMBER                =5
TAG_POINTS_PAGE_NUMBER            =6

company_id,tag_id,tag_points=0,0,0

fixed_frame_arr        =array('B',[0x55,0x55,0x00,0x00,0x00,0x00,0x00,0xFF])
config_arr             =array('B',[0x14,0x01,0x14,0x01])
response_config_arr    =array('B',[0X00,0X00,0XFF,0X00,0XFF,0X00,0X00,0X00,0XFF,0X02,0XFE,0XD5,0X15,0X16,0X00])

read_tag_arr           =array('B',[0x4A,0x01,0x00])
response_read_tag_arr  =array('B',[0x00,0x00,0xFF,0x00,0xFF,0x00,0x00,0x00,0x00,0xFF,0X0F,0XF1,0XD5,0X4B,0X01])
NFC_Recieved_Data      =array('B')

read_tag_data          =array('B',[0x40,0x01,0x30,0x04])
response_read_tag_data =array('B',[0x00,0x00,0xFF,0x00,0xFF,0x00,0x00,0x00,0xFF,0X13,0XED,0XD5,0X41,0X00])


write_page_frame       =array('B',[0x40,0x01,0xA2,0x00,0x00,0x00,0x00,0x00])
response_write_page    =array('B',[0x00,0x00,0xFF,0x00,0xFF,0x00,0x00,0x00,0xFF,0X03,0XFD,0XD5,0X41,0X00,0xEA,0x00])


def nfc_init(usb_port):
	rec_arr =array('B')
	usb.usb_init_port(usb_port,"115200",0.01)
	
	
	nfc_send_data_frame(config_arr)
	for i in range(0,len(response_config_arr)):
		y=usb.usb_read_ch_serial()
		rec_arr.append(int.from_bytes(y, "big"))
	
	for i in range(0,len(response_config_arr)):
		print(hex(rec_arr[i])+" ",end='')	

	comparison = rec_arr == response_config_arr
	if comparison :
		return True
	else :
		return False

def nfc_send_fixed_frame():
	usb.usb_write_str_serial(fixed_frame_arr)

def nfc_send_data_frame(data_array):
	sum=DATA_TO_NFC_BYTE
	send_arr =array('B')
	Data_length=len(data_array)+1
	
	nfc_send_fixed_frame()
	send_arr.append(Data_length)
	send_arr.append(helper.helper_2s_complement(Data_length))  #check_sum
	send_arr.append(DATA_TO_NFC_BYTE)
	for x in range(0,Data_length-1) :
		send_arr.append(data_array[x])
		sum+=data_array[x]
	send_arr.append(helper.helper_2s_complement(sum))
	send_arr.append(END_FRAME_BYTE)	
	
	usb.usb_write_str_serial(send_arr)

def nfc_check_tag_exist():
	rec_arr =array('B')
	
	
	nfc_send_data_frame(read_tag_arr)
	
	for i in range(0,len(response_read_tag_arr)):
		y=usb.usb_read_ch_serial()
		rec_arr.append(int.from_bytes(y, "big"))
	
	#for i in range(0,len(response_read_tag_arr)):
	#	print(hex(rec_arr[i])+" ",end='')	
	
	comparison = rec_arr == response_read_tag_arr
	if comparison :
		return True
	else :
		return False
		
def nfc_read_tag_data():
	rec_arr =array('B')
	data_arr=array('B')
	global company_id
	global tag_id
	global tag_points
	
	nfc_send_data_frame(read_tag_data)
	
	for i in range(0,len(response_read_tag_data)):
		y=usb.usb_read_ch_serial()
		rec_arr.append(int.from_bytes(y, "big"))
	
	for i in range(0,DATA_RECIEVING_CIZE):
		y=usb.usb_read_ch_serial()
		data_arr.append(int.from_bytes(y, "big"))
	
	#for i in range(0,len(response_read_tag_data)):
	#	print(hex(rec_arr[i])+" ")	
	
	#for i in range(0,DATA_RECIEVING_CIZE):
	#	print(hex(data_arr[i])+" ")	
	
	company_id=(data_arr[0]<<24)|(data_arr[1]<<16)|(data_arr[2]<<8)|(data_arr[3])
	#print(company_id)
	tag_id=(data_arr[4]<<24)|(data_arr[5]<<16)|(data_arr[6]<<8)|(data_arr[7])
	#print(tag_id)
	tag_points=(data_arr[8]<<24)|(data_arr[9]<<16)|(data_arr[10]<<8)|(data_arr[11])
	#print(tag_points)
	
	comparison = rec_arr == response_read_tag_data
	if comparison :
		return True
	else :
		return False		

def nfc_write_page(page_number,data):
	data_byte_array=array('B')
	rec_arr  =array('B')

	data_byte_array.append(data&0x000000FF)
	data_byte_array.append((data&0x0000FF00)>>8)
	data_byte_array.append((data&0x00FF0000)>>16)
	data_byte_array.append((data&0xFF000000)>>24)
	
	
	write_page_frame[3]=page_number
	write_page_frame[4]=data_byte_array[3]
	write_page_frame[5]=(data_byte_array[2])
	write_page_frame[6]=(data_byte_array[1])
	write_page_frame[7]=(data_byte_array[0])
	
	nfc_send_data_frame(write_page_frame)
	
	for i in range(0,len(response_write_page)):
		y=usb.usb_read_ch_serial()
		rec_arr.append(int.from_bytes(y, "big"))
	
	for i in range(0,len(response_write_page)):
		print(hex(rec_arr[i])+" ",end="")	
	
	comparison = rec_arr == response_write_page
	if comparison :
		return True
	else :
		return False		


def  nfc_write_company_id(Company_id):

	status=nfc_write_page(COMPANY_ID_PAGE_NUMBER,Company_id);
	return status

def nfc_write_tag_ID(tag_number):
	
	status=nfc_write_page(TAG_ID_PAGE_NUMBER,tag_number);
	return status;



def nfc_write_Tag_Points(points):	
	status=nfc_write_page(TAG_POINTS_PAGE_NUMBER,points);
	return status;
	
def nfc_deinit():
	usb.usb_close_port()

def nfc_port_status():
	status=usb.usb_port_status()
	return status

'''	
init_status=nfc_init("COM3")	
print("\n init nfc ="+str(init_status))
nfc_deinit()
print(nfc_port_status())


val =int(input("""Enter your value: 
1- read the Tag_id
2- write tag_data
             """))
print(val)

if val==2:
	company_id = int(input("Enter your company id: "))
	print(company_id)
	tag_id = int(input("Enter your tag id: "))
	print(tag_id)
	tag_points = int(input("Enter your tag points : "))
	print(tag_points)


for x in range (1,10):

	tag_exist_status=nfc_check_tag_exist()
	print("Tag exist ="+str(tag_exist_status))
		
	if tag_exist_status==True :

		if val==1 :
			valid_data_status=nfc_read_tag_data()
			print("valid data reding ="+str(valid_data_status))
			print("company id ="+str(company_id))
			print("tag id ="+str(tag_id))
			print("tag points ="+str(tag_points))
		elif val==2 :
			
			tag_write_page_status=nfc_write_company_id(company_id)
			print("write page status  ="+str(tag_write_page_status))
			tag_write_page_status=nfc_write_tag_ID(tag_id)
			print("write page status  ="+str(tag_write_page_status))
			tag_write_page_status=nfc_write_Tag_Points(tag_points)
			print("write page status  ="+str(tag_write_page_status))
		
		else :
			print("wrong sclect")
		break
	
	time.sleep(0.2)	
		
'''	