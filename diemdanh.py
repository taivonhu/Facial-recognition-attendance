import sys
import time
import cv2
from facenet.face_contrib import *
import datetime
import sqlite3
from tkinter import messagebox
from tkinter import *
import tkinter as tk
from PIL import Image,ImageTk
from tkinter import ttk


window = Tk()
window.title("Điểm Danh")
window_height = 718
window_width = 1388
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
window.config(background="white")

date_object = datetime.date.today()

image = Image.open('logo.png')
image = image.resize((window_width, 96), Image.ANTIALIAS)
pic = ImageTk.PhotoImage(image)
lab1=Label (image=pic)
lab1.grid(columnspan=15, row=0)

lb0 = Label(window,text="", height = 3,bg="white",width=8).grid(sticky = W,column=4, row=2)
# lbl1 = Label(window, text="Danh sách sinh viên đã điểm danh: "+format(str(date_object)), fg='black', font=("Helvetica", 16, "bold"))
# lbl1.grid(columnspan=2,column=7, row=2)

listNodes = Listbox(window, width=70, height=25, font=("Helvetica", 12))
listNodes.grid(columnspan=4,column=7, row=4,rowspan=10)
scrollbar = Scrollbar(window, orient="vertical")
scrollbar.config(command=listNodes.yview)
scrollbar.grid(column=11,row=4, rowspan=10, sticky='NS')
listNodes.config(yscrollcommand=scrollbar.set)
# for x in range(100):
#     listNodes.insert(END, "  "+str(x+1)+"  quy")
n4 = tk.StringVar() 
ngayh2 = ttk.Combobox(window, state="readonly", textvariable = n4, width=10,font='Times 18 bold') 
ngayh2['values'] = (format(str(date_object))) 
ngayh2.grid(column = 9, row = 3) 
ngayh2.current(0)

n5 = tk.StringVar() 
TietH1 = ttk.Combobox(window, state="readonly", textvariable = n5, width=8,font='Times 18 bold') 
TietH1['values'] = ('Tiết 1-2')
TietH1.grid(column = 10, row = 3) 
TietH1.current(0)

def combo_input(conn,MonH):
    rowsQuery ="SELECT DISTINCT NgayHoc FROM diemdanh WHERE MonHoc='"+str(MonH)+"'"
    cursor= conn.execute(rowsQuery)
    data = []
    for row in cursor.fetchall():
        data.append(row[0])
    ngayh2['values'] =data
    rowsQuery1 ="SELECT DISTINCT TietHoc FROM diemdanh WHERE MonHoc='"+str(MonH)+"'"
    cursor= conn.execute(rowsQuery1)
    data1 = []
    for row in cursor.fetchall():
        data1.append(row[0])
    TietH1['values'] =data1

def Xemdsdd():
    conn  = sqlite3.connect("facestudents.db")
    MonH  = n1.get()
    TietH = n5.get()
    NgayD = n4.get()
    NhomH = MonH.find('(')+1;
    dem   = 0
    listNodes.delete(0,'end')
    cmd="SELECT * FROM diemdanh WHERE NgayHoc='"+str(NgayD)+"' and MonHoc='"+str(MonH)+"' and TietHoc='"+str(TietH)+"'"
    cursor=conn.execute(cmd)
    for row in cursor:
        dem+=1
        listNodes.insert(END,str(dem)+"      " +row[2]+"      "+row[4]+"      "+row[3])
    rowsQuery ="SELECT count(MaSV) FROM students WHERE Nhom='"+str("Nhóm "+MonH[NhomH])+"'"
    cursor= conn.execute(rowsQuery)
    numberOfRows = cursor.fetchone()[0]
    Vang = numberOfRows-dem
    rowsQuery1 ="SELECT count(MonHoc) FROM hocphan WHERE MonHoc='"+str(MonH)+"'"
    cursor= conn.execute(rowsQuery1)
    Sobuoi = cursor.fetchone()[0]
    lb5 = Label(window,text="Có Mặt: "+str(dem), height = 1,bg="white",width=10,font=("Arial",16,"bold"
        )).grid(column=7, row=17)
    lb6 = Label(window,text="Vắng: "+str(Vang), height = 1,bg="white",width=10,font=("Arial",16,"bold"
        )).grid(column=8, row=17)
    lb7 = Label(window,text="Số lần điểm danh: "+str(Sobuoi), height = 1,bg="white",width=15,font=("Arial",16,"bold"
        )).grid(columnspan=2,column=9, row=17)
    combo_input(conn,MonH)
    conn.close()

def DanhSach():
    conn  = sqlite3.connect("facestudents.db")
    MonH  = n1.get()
    NhomH = MonH.find('(')+1;
    dem   = 0
    listNodes.delete(0,'end')

    rowsQuery1 ="SELECT count(MonHoc) FROM hocphan WHERE MonHoc='"+str(MonH)+"'"
    cursor1= conn.execute(rowsQuery1)
    Sobuoi = cursor1.fetchone()[0]

    cmd="SELECT *FROM students WHERE Nhom='"+str("Nhóm "+MonH[NhomH])+"'"
    cursor=conn.execute(cmd)
    for row in cursor:
        dem+=1
        MaSVDD=row[0] 
        rowsQuery2 ="SELECT count(MaSV) FROM diemdanh WHERE MaSV ='"+str(MaSVDD)+"'and MonHoc='"+str(MonH)+"'"
        cursor2= conn.execute(rowsQuery2)
        numberOfRows = cursor2.fetchone()[0]
        Vang = Sobuoi - numberOfRows
        listNodes.insert(END,str(dem)+"     " +MaSVDD+"     "+row[2]+"     Vắng: " + str(Vang)+"      "+row[1])
    conn.close()
  
# ///////////////////////////////////////////////////////////////
lb2 = Label(window,text="Học Phần:",justify=LEFT,anchor="w", height = 1,font=("Arial",20,"bold"), fg="blue",bg="white",width=8).grid(sticky = W,column=4, row=3)
n1 = tk.StringVar() 
monhoc = ttk.Combobox(window, state="readonly", textvariable = n1, width=25,font='Times 18 bold') 
monhoc['values'] =('Kiểm Thử Phầm Mềm(1)',
                    'Kiểm Thử Phầm Mềm(2)',  
                   'Chuyên Đề(1)', 
                   'Chuyên Đề(2)', 
                   'Xử Lý Ảnh(1)', 
                   'Xử Lý Ảnh(2)',
                   'Xử Lý Tín Hiệu Số(1)',
                   'Xử Lý Tín Hiệu Số(2)') 
monhoc.grid(column = 5, row = 3) 
monhoc.current(0)  
#///////////////////////////////////////////////////////////////
lb3 = Label(window,text="Ngày :",justify=LEFT,anchor="w", height = 1,font=("Arial",20,"bold"), fg="blue",bg="white",width=8).grid(sticky = W,column=4, row=4)
n2 = tk.StringVar() 
ngayh1 = ttk.Combobox(window, state="readonly", textvariable = n2, width=25,font='Times 18 bold') 
# Adding combobox drop down list 
ngayh1['values'] = (format(str(date_object))) 
ngayh1.grid(column = 5, row = 4) 
ngayh1.current(0)

lb4 = Label(window,text="Tiết :",justify=LEFT,anchor="w", height = 1,font=("Arial",20,"bold"), fg="blue",bg="white",width=8).grid(sticky = W,column=4, row=5)
n3 = tk.StringVar() 
buoi = ttk.Combobox(window, state="readonly", textvariable = n3, width=25,font='Times 18 bold') 
buoi['values'] = ('Tiết 1-4', 
                  'Tiết 6-9', 
                  'Tiết 1-2', 
                  'Tiết 3-4', 
                  'Tiết 6-7', 
                  'Tiết 8-9') 
buoi.grid(column = 5, row = 5) 
buoi.current(0)  


btnDS= Button(window, text="Xem Danh Sách",width=12,heigh=1,font=("Times",15,"bold"), fg="white", background="blue", command=DanhSach)
btnDS.grid(column=7, row=3)
btnDDD= Button(window, text="Đã Điểm Danh",width=12,heigh=1,font=("Times",15,"bold"), fg="white", background="blue", command=Xemdsdd)
btnDDD.grid(column=8, row=3)
# ///////////////////////////////////////////////////////////////////


# /////////////////////////////////////////////////////////////////// diem danh
#insert/update data to sqlite
def insertOrUpdate(frame,Id):
    conn=sqlite3.connect("facestudents.db")
    HoTen = ""
    Lop=""
    MonH  = n1.get()
    TietH = n3.get()
    NhomH = MonH.find('(')+1;
    cmdht="SELECT Name,Class,Nhom FROM students WHERE MaSV='{}'".format(str(Id))
    cursor=conn.execute(cmdht)
    for row in cursor:
        HoTen = row[0]
        Lop   = row[1]
        Nhom1 = row[2]
        Nhom2 = Nhom1.find(' ')+1;
        Nhom3 = Nhom1[Nhom2]
    MonH  = MonH[0:NhomH] + Nhom3 + ")"
    cmd   ="SELECT * FROM diemdanh WHERE MaSV='"+format(str(Id))+"' and NgayHoc='"+format(str(date_object))+"' and MonHoc='"+str(MonH)+"' and TietHoc='"+str(TietH)+"'"
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==0):
        cmd="INSERT INTO diemdanh (MonHoc, MaSV, HoTen, Lop, TietHoc,NgayHoc) VALUES ('"+str(MonH)+"', '"+str(Id)+"', '"+str(HoTen)+"', '"+str(Lop)+"','"+str(TietH)+"','"+str(date_object)+"')"
    else :
        cv2.putText(frame,"OK", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)
    conn.execute(cmd)
    conn.commit()
    conn.close()
# ///////////////////////////////////////////////////////////////////

def add_overlays(frame, faces, frame_rate, colors, confidence=0.6):
    if faces is not None:
        for idx, face in enumerate(faces):
            face_bb = face.bounding_box.astype(int)
            cv2.rectangle(frame, (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]), colors[idx], 2)
            if face.name and face.prob:
                if face.prob > confidence:
                    class_id = face.name
                    insertOrUpdate(frame,class_id) 
                else:
                    class_id = 'Unknow'
                    # class_name = face.name
                cv2.putText(frame, class_id, (face_bb[0], face_bb[3] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            colors[idx], thickness=2, lineType=2)
                cv2.putText(frame, '{:.02f}'.format(face.prob * 100), (face_bb[0], face_bb[3] + 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[idx], thickness=1, lineType=2)
    # cv2.putText(frame, str(frame_rate) + " fps", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
    #             thickness=2, lineType=2)


def run(model_checkpoint, classifier, video_file=None, output_file=None):
    conn=sqlite3.connect("facestudents.db")
    MonH  = n1.get()
    TietH = n3.get()
    NhomH = MonH.find('(')+1;
    cmd   ="SELECT * FROM hocphan WHERE MonHoc='"+str(MonH)+"' and TietHoc='"+str(TietH)+"' and NgayHoc='"+format(str(date_object))+"'"
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==0):
        cmd="INSERT INTO hocphan (MonHoc, TietHoc, NgayHoc) VALUES ('"+str(MonH)+"','"+str(TietH)+"','"+str(date_object)+"')"
    print(cmd)
    conn.execute(cmd)
    conn.commit()
    conn.close()

    frame_interval = 3  # Number of frames after which to run face detection
    fps_display_interval = 5  # seconds
    frame_rate = 0
    frame_count = 0
    if video_file is not None:
        video_capture = cv2.VideoCapture(video_file)
    else:
        # Use internal camera
        video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    width = frame.shape[1]
    height = frame.shape[0]
    if output_file is not None:
        video_format = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_file, video_format, 20, (width, height))
    face_recognition = Recognition(model_checkpoint, classifier)
    start_time = time.time()
    colors = np.random.uniform(0, 255, size=(1, 3))
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        if (frame_count % frame_interval) == 0:
            faces = face_recognition.identify(frame)
            for i in range(len(colors), len(faces)):
                colors = np.append(colors, np.random.uniform(150, 255, size=(1, 3)), axis=0)
            # Check our current fps
            end_time = time.time()
            if (end_time - start_time) > fps_display_interval:
                frame_rate = int(frame_count / (end_time - start_time))
                start_time = time.time()
                frame_count = 0

        add_overlays(frame, faces, frame_rate, colors)

        frame_count += 1
        cv2.imshow('Video', frame)
        if output_file is not None:
            out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    if output_file is not None:
        out.release()
    video_capture.release()
    cv2.destroyAllWindows()

def play():
    if __name__ == '__main__':
        run('models', 'models/your_model.pkl', video_file=None, output_file=None) #'demo2.avi'
btnDD= Button(window, text="Điểm Danh",width=22,heigh=1,font=("Times",20,"bold"), fg="white", background="blue", command=play)
btnDD.grid(column=5, row=6)

window.mainloop()

    
# https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/