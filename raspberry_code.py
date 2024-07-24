from picamera2 import Picamera2
from cryptography.fernet import Fernet
import cv2
import tkinter as tk
import requests
import os 
import signal
import atexit
def on_exit():
	if os.path.exists("output.jpg"):
		os.remove("output.jpg")
	if os.path.exists("encoded.jpg"):
		os.remove("encoded.jpg")
atexit.register(on_exit)
signal.signal(signal.SIGTERM,on_exit)
signal.signal(signal.SIGINT,on_exit)

url = "http://your_device_ip_where_django_server_runs:8000/"
s = requests.Session()

if os.path.exists("output.jpg"):
	os.remove("output.jpg")
if os.path.exists("encoded.jpg"):
	os.remove("encoded.jpg")

#key = Fernet.generate_key()     #--This will generate a unique key for both encryption and decryption. Below is a generated key which will be constant for all transactions.
key = b'bY7JXmRqIyzj4kdkc_YBwJwzTOlc2WEfflGx8RauxaQ='         # It is NOT AT ALL SAFE to use here. But I have used it directly for the time being.


fnet = Fernet(key)

window=tk.Tk()
window.geometry('800x800+600+200')
def on_close(event=None):
	if os.path.exists("output.jpg"):
		os.remove("output.jpg")
	if os.path.exists("encoded.jpg"):
		os.remove("encoded.jpg")
	window.destroy()
	
window.protocol("WM_DELETE_WINDOW",on_close)


def req_new():
	win=tk.Toplevel()
	win.geometry('250x150+700+300')

	def inserts(event=None):
		text = e.get()
		try:
			with open('output.jpg','rb') as file:
				Org_data = file.read()
				Enc_data = fnet.encrypt(Org_data)
				with open('encoded.jpg','wb') as encfile:
					encfile.write(Enc_data)
			with open('encoded.jpg','rb') as file:
				data1 = s.get(url+"new/")
				#print(*data1.cookies)
				csrf_token = data1.cookies['csrftoken']
				#print(csrf_token)
				data2 = s.post(url+"new/",files = {'imgfile':file}, data={'csrfmiddlewaretoken':csrf_token, "name":text})
				ResLabel.configure(text=data2.text,image=None)
			if os.path.exists("encoded.jpg"):
				os.remove("encoded.jpg")
			if os.path.exists("output.jpg"):
				os.remove("output.jpg")
			print("Data sent successfully")
		except:
			print("Failed to transfer image")
		win.destroy()
	win.bind( "<Return>" , inserts )
	l=tk.Label( win , height=2, text="Please Enter Your Name:", borderwidth=1, font=("Tahoma", 12), background="white", foreground="black", relief="flat")
	l.place( relheight=0.3, relwidth=1, rely=0, relx=0)
	e=tk.Entry( win , font=("Tahoma",16,'bold'))
	e.place( relheight=0.3, relwidth=0.9, rely=0.3, relx=0.07)
	b1=tk.Button( win , text='Submit', command=inserts , font=("Trebuchet MS", 13, 'bold'), background="#0066ff", foreground="white", activeforeground="white", activebackground="#3311ff", relief="flat")
	b1.place( relheight=0.3, relwidth=0.9, rely=0.6, relx=0.07)
    
def req(event=None):
	try:
		
		with open('output.jpg','rb') as file:
			Org_data = file.read()
			Enc_data = fnet.encrypt(Org_data)
			with open('encoded.jpg','wb') as encfile:
				encfile.write(Enc_data)
		with open('encoded.jpg','rb') as file:
			data1 = s.get(url+"match/")
			#print(*data1.cookies)
			csrf_token = data1.cookies['csrftoken']
			#print(csrf_token)
			data2 = s.post(url+"match/",files = {'imgfile':file},data={'csrfmiddlewaretoken':csrf_token})
			ResLabel.configure(text=data2.text,image=None)
		if os.path.exists("encoded.jpg"):
			os.remove("encoded.jpg")
		print("Data sent successfully")
		
	except Exception as e:
		print("Failed to transfer image")
		print(e)
		

def capture(event=None):
	cam = Picamera2()
	cam.start_preview(None)
	capture_config = cam.create_still_configuration(main={"format":"XRGB8888"})
	cam.configure(capture_config)
	cam.controls.ExposureTime=100000
	cam.controls.Contrast=31.0
	cam.start_and_capture_file("output.jpg")
	cam.close()
	img = cv2.imread("output.jpg")
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imwrite("output.jpg",img)
	img_temp = cv2.resize(img,(800,600))
	cv2.imshow("Preview Window",img_temp)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	ResLabel.configure(text="Image Captured")
	
   
pane = tk.Frame(window)
if os.path.exists("encoded.jpg"):
	os.remove("encoded.jpg")

l=tk.Label( window , height=5, text="ATM Interface Example", borderwidth=1, font=("Tahoma", 18), foreground="black", relief="flat")
l.pack(fill='both')
pane.pack(fill = "both")
b1=tk.Button( pane , height = 4, text='NEW USER', command=req_new , font=("Trebuchet MS", 18), background="#0066ff", foreground="white", activeforeground="white", activebackground="#3311ff", relief="flat")
b1.pack( fill = "both", expand = True)
b2=tk.Button( pane , height = 4, text='CAPTURE', command=capture , font=("Trebuchet MS", 18), background="#0066ff", foreground="white", activeforeground="white", activebackground="#3311ff", relief="flat")
b2.pack( fill = "both", expand = True)
b3=tk.Button( pane , height = 4, text='MATCH', command=req , font=("Trebuchet MS", 18), background="#0066ff", foreground="white", activeforeground="white", activebackground="#3311ff", relief="flat")
b3.pack( fill = "both", expand = True)

ResLabel = tk.Label(window, font=("Tahoma", 18))
ResLabel.pack(fill='both',expand = True)

window.bind( "<Return>" , capture )
window.mainloop()
