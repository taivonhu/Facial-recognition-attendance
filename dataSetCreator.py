from PIL import Image,ImageTk
from tkinter import messagebox
from tkinter import *
import tkinter as tk
import pytesseract
import sqlite3
import PIL
import cv2
import os

# cam = cv2.VideoCapture(0)
detector=cv2.CascadeClassifier('C:\\Users\\VNTAI_PC\\Desktop\\doan5\\facenet\\haarcascade_frontalface_default.xml')

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 850)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)


id = "it001"
sampleNum=0
path = 'test/'+id
if not os.path.exists(path):
    os.makedirs(path)
while(True):
    #camera read
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        
        #incrementing sample number 
        sampleNum=sampleNum+1
        #saving the captured face in the dataset folder
        cv2.imwrite(path+"/"+id +'_'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
        cv2.imshow('frame',img)
    #wait for 100 miliseconds 
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    # break if the sample number is morethan 20
    elif sampleNum>20:
        # print("Thành công! ")
        lb5 = Label(window,text="Thành công!", height = 2,font=("Arial",18),width=30,background="#f7f700").grid(column=1, columnspan=2, row=9,padx=3,pady=5)
        break
# cam.release()
cv2.destroyAllWindows()

