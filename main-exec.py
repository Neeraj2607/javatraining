from PIL.Image import ImageTransformHandler
import cv2
import numpy as np
import pytesseract
import tkinter as tk
import smtplib
from email.message import EmailMessage
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

pytesseract.pytesseract.tesseract_cmd="C:/Program Files/Tesseract-OCR/tesseract.exe"

cascade= cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
states={"AN":"Andaman and Nicobar",
    "AP":"Andhra Pradesh","AR":"Arunachal Pradesh",
    "AS":"Assam","BR":"Bihar","CH":"Chandigarh",
    "DN":"Dadra and Nagar Haveli","DD":"Daman and Diu",
    "DL":"Delhi","GA":"Goa","GJ":"Gujarat",
    "HR":"Haryana","HP":"Himachal Pradesh",
    "JK":"Jammu and Kashmir","KA":"Karnataka","KL":"Kerala",
    "LD":"Lakshadweep","MP":"Madhya Pradesh","MH":"Maharashtra","MN":"Manipur",
    "ML":"Meghalaya","MZ":"Mizoram","NL":"Nagaland","OD":"Odissa",
    "PY":"Pondicherry","PN":"Punjab","RJ":"Rajasthan","SK":"Sikkim","TN":"TamilNadu",
    "TR":"Tripura","UP":"Uttar Pradesh", "WB":"West Bengal","CG":"Chhattisgarh",
    "TS":"Telangana","JH":"Jharkhand","UK":"Uttarakhand"}

#initialise GUI
top=tk.Tk()
top.geometry('800x600')
top.title('Number Plate Detection')
top.configure(background='#CDCDCD')

label=Label(top,background='#CDCDCD', font=('arial',15,'bold'))
sign_image = Label(top)


def extract_num(img_filename):
    global label_packed
    img=cv2.imread(img_filename)
    img=cv2.resize(img,None,fx=0.8,fy=0.8)
    #Img To Gray
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    nplate=cascade.detectMultiScale(gray,1.1,4)
    #crop portion
    for (x,y,w,h) in nplate:
        wT,hT,cT=img.shape
        a,b=(int(0.02*wT),int(0.02*hT))
        plate=img[y+a:y+h-a,x+b:x+w-b,:]
        #make the img more darker to identify LPR
        kernel=np.ones((1,1),np.uint8)
        plate=cv2.dilate(plate,kernel,iterations=1)
        plate=cv2.erode(plate,kernel,iterations=1)
        plate_gray=cv2.cvtColor(plate,cv2.COLOR_BGR2GRAY)
        (thresh,plate)=cv2.threshold(plate_gray,127,255,cv2.THRESH_BINARY)
        #read the text on the plate
        
        read=pytesseract.image_to_string(plate)
        read=''.join(e for e in read if e.isalnum())
        stat=read[0:2]
        #sending mail
        msg=EmailMessage()
        msg['Subject']='Vehicle Number Detected!!!!'
        msg['From']='Message from Connected Device'
        msg['To']='projectmsg15@gmail.com'
        msg.set_content(str(read))
    
        server=smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.login("alietprojectbatch15@gmail.com","Project15batch")
        server.send_message(msg)
        server.quit()
        cv2.rectangle(img,(x,y),(x+w,y+h),(51,51,255),2)
        cv2.rectangle(img,(x-1,y-40),(x+w+1,y),(51,51,255),-1)
        cv2.putText(img,read,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2)

        cv2.imshow("plate",plate)
        
    cv2.imwrite("Result.png",img)
    cv2.imshow("Result",img)
    if cv2.waitKey(0)==113:
        exit()
    cv2.destroyAllWindows()
def show_classify_button(file_path):
    classify_b=Button(top,text="Detect Image",command=lambda: extract_num(file_path),padx=10,pady=5)
    classify_b.configure(background='#364156', foreground='white',font=('arial',10,'bold'))
    classify_b.place(relx=0.79,rely=0.46)

def upload_image():
    try:
        file_path=filedialog.askopenfilename()
        uploaded=Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25),(top.winfo_height()/2.25)))
        im=ImageTk.PhotoImage(uploaded)
        
        sign_image.configure(image=im)
        sign_image.image=im
        label.configure(text='')
        show_classify_button(file_path)
    except:
        pass

upload=Button(top,text="Upload an image",command=upload_image,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('arial',10,'bold'))

upload.pack(side=BOTTOM,pady=50)
sign_image.pack(side=BOTTOM,expand=True)
label.pack(side=BOTTOM,expand=True)
heading = Label(top, text="Detect Number Plate",pady=20, font=('arial',20,'bold'))
heading.configure(background='#CDCDCD',foreground='#364156')
heading.pack()
top.mainloop()






