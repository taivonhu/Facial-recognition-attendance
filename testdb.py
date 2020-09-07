import sqlite3
import datetime

def insertOrUpdate(Id,MaMH,date_object):
    conn=sqlite3.connect("facestudents.db")

    cmd="SELECT MaSV,Datedd FROM diemdanh WHERE MaSV='"+format(str(Id))+"' and Datedd='"+format(str(date_object))+"'"
    print(cmd)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==0):
        cmd="INSERT INTO diemdanh (MaMH, MonHoc, MaSV, Name, Class, Datedd) VALUES ('"+str(MaMH)+"', 'Xu Ly Anh', '"+str(Id)+"', 'Van Quy','17it3','"+str(date_object)+"')"
    else :
    	print("ok")
    conn.execute(cmd)
    conn.commit()
    conn.close()


date_object = datetime.date.today()
MaSV=2
MaMH=1
insertOrUpdate(MaSV,MaMH,date_object)
