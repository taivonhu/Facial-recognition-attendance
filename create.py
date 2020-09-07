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


def show_frame():
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)




window = Tk()
window.title("Cập nhật thông tin và khuôn mặt")
window_height = 518
window_width = 1288
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
window.config(background="white")



cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 850)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

lb1 = Label(window,text="CẬP NHẬT THÔNG TIN VÀ HÌNH ẢNH KHUÔN MẶT", height = 1,font=("Arial",18,"bold"), fg="blue",bg="white")
lb1.grid(column=0, row=0)
window.bind('<Escape>', lambda e: window.quit())
lmain = Label(window)
lmain.grid(column=0, rowspan=18)
show_frame()



#insert/update data to sqlite
def insertOrUpdate(Id,Name,Classlb,Khoalb,Nhomlb):
    conn=sqlite3.connect("facestudents.db")
    cmd="SELECT * FROM students WHERE MaSV='{}'".format(str(Id))

    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE students SET Name='{}'".format(str(Name))+",Class='{}'".format(str(Classlb))+",Nhom='{}'".format(str(Nhomlb))+",Khoa='{}'".format(str(Khoalb))+" WHERE MaSV='{}'".format(str(Id))
        # print("Đang cập nhật lại thông tin và hình ảnh khuôn mặt!",Id,Name)
        print(cmd)
        lb4 = Label(window,text="Đã cập nhật lại thông tin và hình ảnh khuôn mặt", height = 2,font=("Arial",10),width=35).grid(
            column=1, columnspan=2, row=10,padx=3,pady=5)
    else:
        cmd="INSERT INTO students (MaSV, Name, Class, Nhom, Khoa) VALUES ('"+str(Id)+"', '"+str(Name)+"', '"+str(Classlb)+"','"+str(Nhomlb)+"' ,'"+str(Khoalb)+"')"
        # cmd="INSERT INTO students(MaSV,Name,Class,XuLyAnh,KiemThuPhanMem,DoAnCoSo) Values("+str(Id)+","+str(Name)+","",0,0,0)"
        lb4 = Label(window,text="Đã thêm thông tin sinh viên", height = 2,font=("Arial",10),width=30).grid(
            column=1, columnspan=2, row=10,padx=3,pady=5)
        # print("Đang thêm thông tin sinh viên: ",Id,Name)
    conn.execute(cmd)
    conn.commit()
    conn.close()
    id1 = str(Id)
    quet(id1)
    cam.release()


# userINP = Entry(root, width=25, bg ="White")
# userINP.place(x=120,y=100)
# userINP.get(...)

def Laytt():
    Id      = LbId.get().upper()
    name    = LbName.get().upper()
    classlb = LbClass.get().upper()
    Khoalb  = LbKhoa.get().upper()
    Nhomlb  = LbNhom.get()
    if Id =="":
        messagebox.showinfo("Thông Báo!","Vui Lòng Nhập Mã Sinh Viên!")
    elif classlb =="" or name =="":
        messagebox.showinfo("Thông báo!","Vui Lòng Nhập Họ Tên, Lớp Của Sinh Viên!")
    else:
        lb3 = Label(window,text="Mã SV: "+ Id +"  Lớp: "+classlb+"\n"+"Họ tên: "+ name + Khoalb + Nhomlb, height = 3,font=("Arial",18),width=30).grid(column=1, columnspan=2, row=9,padx=3,pady=5)
        insertOrUpdate(Id,name,classlb,Khoalb,Nhomlb)
    # print(id,name,classlb)
        
lb1 = Label(window,text="Mã SV:", height = 1,font=("Arial",20), fg="blue",bg="#EAE4E2",width=6).grid(column=1, row=3)
LbId = Entry(window,width=15,font='Times 25 bold')
LbId.grid(column=2, row=3)

lb2 = Label(window,text="Họ Tên :", height = 1,font=("Arial",20), fg="blue",bg="#EAE4E2",width=6).grid(column=1, row=4)
LbName = Entry(window,width=15,font='Times 25 bold')
LbName.grid(column=2, row=4)

lb3 = Label(window,text="Lớp :", height = 1,font=("Arial",20), fg="blue",bg="#EAE4E2",width=6).grid(column=1, row=5)
LbClass = Entry(window,width=15,font='Times 25 bold')
LbClass.grid(column=2, row=5)

lb4 = Label(window,text="Nhóm :", height = 1,font=("Arial",20), fg="blue",bg="#EAE4E2",width=6).grid(column=1, row=6)
LbNhom = Entry(window,width=15,font='Times 25 bold')
LbNhom.grid(column=2, row=6)

lb4 = Label(window,text="Khóa :", height = 1,font=("Arial",20), fg="blue",bg="#EAE4E2",width=6).grid(column=1, row=7)
LbKhoa = Entry(window,width=15,font='Times 25 bold')
LbKhoa.grid(column=2, row=7)

btnOk= Button(window, text="OK",width=10,heigh=1,font=("Times",18,"bold"), fg="black", background="blue",command=Laytt)
btnOk.grid(column=2, row=8)


def quet(Id):
    sampleNum=0
    path = 'your_face/'+Id
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
            cv2.imwrite(path+"/"+Id +'_'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
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


window.mainloop()