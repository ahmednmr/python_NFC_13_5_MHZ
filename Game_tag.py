import tkinter as tk
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

		
		self.label_text= tk.StringVar()
		self.label_text.set( "NFC is Not Connected" )
		self.label_port_status = tk.Label(self, textvariable = self.label_text)
		self.label_port_status.place(x = 120,y = 35) 
		
		
		Open_serial_button = tk.Button(self, text="Connect NFC",command=self.Open_PORT,height=1,width=10).place(x = 400,y = 10)  
		
		read_tag_button = tk.Button(self, text="read tag",command=self.read_tag,height=1,width=10).place(x = 400,y = 50)
		
		hello_button = tk.Button(self, text="Start program",command=self.Start_programming,height=1,width=10).place(x = 400,y = 90)
		
		close_serial_button = tk.Button(self, text="Disconnect NFC",command=self.Close_PORT,height=1,width=10).place(x = 400,y = 130) 
		
		Exit_button = tk.Button(self, text="Exit",command=self.Exit,height=1,width=10).place(x = 400,y = 170) 
		
	
	
	def Start_programming(self):
		print("Start_programming")
		
	def Close_PORT(self):
		print("Close_PORT")
		NFC.nfc_deinit()
		self.label_text.set("NFC is Not Connected")

	def Open_PORT(self):
		print("Open_PORT")
		nfc_init=NFC.nfc_init(self.clicked_ports.get())
		if nfc_init==True:
			self.label_text.set("NFC is Connected")
	
	def read_tag(self):
		
		print("read_tag")
		for x in range (1,10):
			tag_exist_status=NFC.nfc_check_tag_exist()
			if tag_exist_status==True:
				print("Tag exist ="+str(tag_exist_status))
				read_status=NFC.nfc_read_tag_data()
				if read_status==True :
					print(NFC.company_id)
					print(NFC.tag_id)
					print(NFC.tag_points)
					break
			time.sleep(0.2)
	
	
	
	def Exit(self):
		self.after(0, self.destroy)
		
	def task(self):
		
		window.after(1, self.task)  # reschedule event in 2 seconds


if __name__ == "__main__":
	window = Window()
	window.geometry("490x210")
	window.after(1, window.task)
	window.mainloop()
    
 
