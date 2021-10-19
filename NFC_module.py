import usb_port_module as usb
import helper_module as helper
from array import *

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
fixed_frame_arr        =array('B',[0x55,0x55,0x00,0x00,0x00,0x00,0x00,0xFF])
config_arr             =array('B',[0x14,0x01,0x14,0x01])
response_config_arr    =array('B',[0X00,0X00,0XFF,0X00,0XFF,0X00,0X00,0X00,0XFF,0X02,0XFE,0XD5,0X15,0X16,0X00])

read_tag_arr           =array('B',[0x4A,0x01,0x00])
response_read_tag_arr  =array('B',[0x00,0x00,0xFF,0x00,0xFF,0x00,0x00,0x00,0xFF,0X0F,0XF1,0XD5,0X4B,0X01])
NFC_Recieved_Data      =array('B')

read_tag_data          =array('B',[0x40,0x01,0x30,0x04])
response_read_tag_data =array('B',[0x00,0x00,0xFF,0x00,0xFF,0x00,0x00,0x00,0xFF,0X13,0XED,0XD5,0X41,0X00])


write_page_frame       =array('B',[0x40,0x01,0xA2])
response_write_page    =array('B',[0x00,0x00,0xFF,0x00,0xFF,0x00,0x00,0x00,0xFF,0X03,0XFD,0XD5,0X41,0X00,0xEA,0x00])


def nfc_init(usb_port):
	rec_arr =array('B')
	usb.usb_init_port(usb_port,"115200",0.0016)
	
	
	nfc_send_data_frame(config_arr)
	for i in range(0,len(response_config_arr)):
		y=usb.usb_read_ch_serial()
		rec_arr.append(int.from_bytes(y, "big"))
	
	#for i in range(0,len(response_config_arr)):
	#	print(hex(rec_arr[i]))	

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


	
init_status=nfc_init("COM3")	
print(init_status)