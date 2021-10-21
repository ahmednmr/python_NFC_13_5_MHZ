'''
remove usb bug
'''

import tkinter  as tk
import tkinter.messagebox as msgbox
import NFC_module as NFC
import serial.tools.list_ports
from tkinter import filedialog as fd
import time
 


 
class Window(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Game tag Scan ")
		
# check and print all available ports 
		
		ports = serial.tools.list_ports.comports()
		available_ports = ["None"]
		for x in ports:
			available_ports.append(x.device)
			
		print(available_ports)
		
############
		
		self.clicked_ports = tk.StringVar()
		self.clicked_ports.set( "COM3" )
		self.label_port_text = tk.Label(self, text = "Select The USB PORT").place(x = 10,y = 10) 
		self.drop_ports = tk.OptionMenu( self , self.clicked_ports , *available_ports ).place(x=15,y=30)

		
		self.nfc_status_text= tk.StringVar()
		self.nfc_status_text.set( "NFC is Not Connected" )
		self.label_port_status = tk.Label(self, textvariable = self.nfc_status_text)
		self.label_port_status.place(x = 120,y = 35) 
		
		self.company_id_text                = tk.StringVar()
		self.company_id_text.set("")
		self.company_id_label         = tk.Label(self, text = "Company ID :").place(x = 10,y = 70)  
		self.company_id_name_entry    = tk.Entry(self, textvar=self.company_id_text,width=20).place(x=120,y=70)
		
		self.tag_id_text                = tk.StringVar()
		self.tag_id_text.set("")
		self.tag_id_label         = tk.Label(self, text = "Tag Number :").place(x = 10,y = 105)  
		self.tag_id_name_entry    = tk.Entry(self, textvar=self.tag_id_text,width=20).place(x=120,y=105)
		
		self.tag_points_text                = tk.StringVar()
		self.tag_points_text.set("")
		self.tag_points_label         = tk.Label(self, text = "Tag    Points  :").place(x = 10,y = 140)  
		self.tag_points_name_entry    = tk.Entry(self, textvar=self.tag_points_text,width=20).place(x=120,y=140)
		
		Open_serial_button = tk.Button(self, text="Connect NFC",command=self.Open_PORT,height=1,width=10).place(x = 400,y = 10)  
		
		read_tag_button = tk.Button(self, text="read tag",command=self.read_tag,height=1,width=10).place(x = 400,y = 50)
		
		hello_button = tk.Button(self, text="Start program",command=self.Start_programming,height=1,width=10).place(x = 400,y = 90)
		
		close_serial_button = tk.Button(self, text="Disconnect NFC",command=self.Close_PORT,height=1,width=10).place(x = 400,y = 130) 
		
		Exit_button = tk.Button(self, text="Exit",command=self.Exit,height=1,width=10).place(x = 400,y = 170) 
		
	
	
	def Start_programming(self):
		NFC.company_id=int(self.company_id_text.get())
		NFC.tag_id=int(self.tag_id_text.get())
		NFC.tag_points=int(self.tag_points_text.get())
		
		if(NFC.tag_id<=1000000) :
			print("Start_programming")
			print("read_tag")
			for x in range (1,10):
				tag_exist_status=NFC.nfc_check_tag_exist()
				if tag_exist_status==True:
					print("Tag exist ="+str(tag_exist_status))
					status_company_id=NFC.nfc_write_company_id(NFC.company_id)
					status_tag_id=NFC.nfc_write_tag_ID(NFC.tag_id)
					status_tag_points=NFC.nfc_write_Tag_Points(NFC.tag_points)
					break
				time.sleep(0.2)	
		else :
			print("tag number should be less than 1000000")
		
		if status_company_id==True :
			print("done writing")
		
	def Close_PORT(self):
		print("Close_PORT")
		self.company_id_text.set("")
		self.tag_id_text.set("")
		self.tag_points_text.set("")
		NFC.nfc_deinit()
		self.nfc_status_text.set("NFC is Not Connected")

	def Open_PORT(self):
		print("Open_PORT")
		nfc_init=NFC.nfc_init(self.clicked_ports.get())
		if nfc_init==True:
			self.nfc_status_text.set("NFC is Connected")
	
	def read_tag(self):
		
		print("read_tag")
		for x in range (1,10):
			tag_exist_status=NFC.nfc_check_tag_exist()
			if tag_exist_status==True:
				print("Tag exist ="+str(tag_exist_status))
				read_status=NFC.nfc_read_tag_data()
				if read_status==True :
					self.company_id_text.set(NFC.company_id)
					self.tag_id_text.set(NFC.tag_id)
					self.tag_points_text.set(NFC.tag_points)
					print(NFC.company_id)
					print(NFC.tag_id)
					print(NFC.tag_points)
					break
			time.sleep(0.2)
	
	
	
	def Exit(self):
		self.after(0, self.destroy)
		
	def task(self):
	
		
		window.after(100, self.task)  # reschedule event in 2 seconds


if __name__ == "__main__":
	window = Window()
	window.geometry("490x210")
	window.after(100, window.task)
	window.mainloop()
    
'''
 	def task2(self):
		is_port_open=NFC.nfc_port_status()
		if is_port_open==True :
			print("port is open")
'''			
