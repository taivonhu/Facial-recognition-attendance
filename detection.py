import sys
import time
import cv2
from facenet.face_contrib import *
import datetime
import sqlite3

# id    INTEGER
# MaMH   INTEGER,
# MonHoc VARCHAR (100),
# MaSV   INTEGER,
# Name   VARCHAR (40),
# Class  CHAR (10),
# Date   DATE
#trangthai int

#insert/update data to sqlite
date_object = datetime.date.today()
MaMH=1
dem=0
def insertOrUpdate(frame,Id,MaMH,date_object):
    conn=sqlite3.connect("facestudents.db")
    Status=""
    cmd="SELECT MaSV,Datedd FROM diemdanh WHERE MaSV='"+format(str(Id))+"' and Datedd='"+format(str(date_object))+"'"
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==0):
        cmd="INSERT INTO diemdanh (MaMH, MonHoc, MaSV, Name, Class, Datedd) VALUES ('"+str(MaMH)+"', 'Xu Ly Anh', '"+str(Id)+"', '','17it3','"+str(date_object)+"')"
        #print("INSERT")
        Status="OK-"+format(str(Id))
        cv2.putText(frame,"Status: "+ Status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)
    else :
        #print("No INSERT")
        Status=" Detect"
        cv2.putText(frame,"Status: "+Status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)
    conn.execute(cmd)
    conn.commit()
    conn.close()

def add_overlays(frame, faces, frame_rate, colors, confidence=0.4):
    if faces is not None:
        for idx, face in enumerate(faces):
            face_bb = face.bounding_box.astype(int)
            cv2.rectangle(frame, (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]), colors[idx], 2)
            if face.name and face.prob:
                if face.prob > confidence:
                    class_id = face.name
                    insertOrUpdate(frame,class_id,MaMH,date_object)  
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


if __name__ == '__main__':
    run('models', 'models/your_model.pkl', video_file=None, output_file=None) #'demo2.avi'


    
# https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/