import cv2
import numpy as np
import os
import face_recognition
from datetime import datetime
import csv
import requests
import threading

path = 'known_pics'
unknown_path = 'static/unknown_pics'
if not os.path.exists(unknown_path):
    os.makedirs(unknown_path)

names = []
images = []
pics_list = os.listdir(path)
saved_unknown_encodings = []

for l in pics_list:
    curPic = cv2.imread(f'{path}/{l}')
    images.append(curPic)
    names.append(os.path.splitext(l)[0])

def encodeingImg(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list

encode_list_known = encodeingImg(images)

def save_full_image(image, unknown_path, cam_id):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    img_name = f"{unknown_path}/cam{cam_id}_unknown_{timestamp}.jpg"
    cv2.imwrite(img_name, image)
    url = "http://192.168.1.106:5000/upload"
    files = {'file': open(img_name, 'rb')}
    try:
        requests.post(url, files=files)
    except requests.exceptions.RequestException as e:
        print(f"Error uploading image: {e}")


logfile = 'DB.csv'

if not os.path.isfile(logfile):
    with open(logfile, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Date", "Time"])

def process_camera(cam_id):
    cam = cv2.VideoCapture(cam_id)
    while True:
        ret, img = cam.read()
        if not ret:
            print(f"Failed to capture image from camera {cam_id}")
            continue

        if img is None:
            print(f"Empty frame from camera {cam_id}")
            continue

        img_s = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        img_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2RGB)

        faceCurentFrame = face_recognition.face_locations(img_s)
        encoderCurentFrame = face_recognition.face_encodings(img_s, faceCurentFrame)

        for encode_face, face_loc in zip(encoderCurentFrame, faceCurentFrame):
            matches = face_recognition.compare_faces(encode_list_known, encode_face)
            face_Distance = face_recognition.face_distance(encode_list_known, encode_face)

            match_index = np.argmin(face_Distance)

            if matches[match_index]:
                name = names[match_index].upper()
                color = (0, 255, 0)
            else:
                name = "UNKNOWN"
                color = (0, 0, 255)

                if not any(face_recognition.compare_faces(saved_unknown_encodings, encode_face)):
                    save_full_image(img, unknown_path, cam_id)
                    saved_unknown_encodings.append(encode_face)

            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            current_time = now.strftime("%H:%M:%S")

            with open(logfile, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, current_date, current_time])

            y1, x2, y2, x1 = face_loc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), color, cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow(f'face recognition {cam_id}', img)
        cv2.waitKey(1)


if __name__ == '__main__':
    camera_ids = [0]  
    threads = []
    for cam_id in camera_ids:
        t = threading.Thread(target=process_camera, args=(cam_id,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()







"""
import cv2
import numpy as np
import os
import face_recognition
from datetime import datetime
import csv
import requests
import threading

path = 'known_pics'
unknown_path = 'static/unknown_pics'
if not os.path.exists(unknown_path):
    os.makedirs(unknown_path)

names = []
images = []
pics_list = os.listdir(path)
saved_unknown_encodings = []

for l in pics_list:
    curPic = cv2.imread(f'{path}/{l}')
    images.append(curPic)
    names.append(os.path.splitext(l)[0])

def encodeingImg(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list

encode_list_known = encodeingImg(images)

def save_full_image(image, unknown_path, cam_id):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    img_name = f"{unknown_path}/cam{cam_id}_unknown_{timestamp}.jpg"
    cv2.imwrite(img_name, image)
    url = "http://10.32.101.151:5000/upload"  
    files = {'file': open(img_name, 'rb')}
    try:
        requests.post(url, files=files)
    except requests.exceptions.RequestException as e:
        print(f"Error uploading image: {e}")

logfile = 'DB.csv'

if not os.path.isfile(logfile):
    with open(logfile, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Date", "Time"])

def process_camera(cam_id):
    cam = cv2.VideoCapture(cam_id)
    while True:
        ret, img = cam.read()
        if not ret:
            print(f"Failed to capture image from camera {cam_id}")
            continue

        if img is None:
            print(f"Empty frame from camera {cam_id}")
            continue

        img_s = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        img_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2RGB)

        faceCurentFrame = face_recognition.face_locations(img_s)
        encoderCurentFrame = face_recognition.face_encodings(img_s, faceCurentFrame)

        for encode_face, face_loc in zip(encoderCurentFrame, faceCurentFrame):
            matches = face_recognition.compare_faces(encode_list_known, encode_face)
            face_Distance = face_recognition.face_distance(encode_list_known, encode_face)

            match_index = np.argmin(face_Distance)

            if matches[match_index]:
                name = names[match_index].upper()
                color = (0, 255, 0)
            else:
                name = "UNKNOWN"
                color = (0, 0, 255)

                if not any(face_recognition.compare_faces(saved_unknown_encodings, encode_face)):
                    save_full_image(img, unknown_path, cam_id)
                    saved_unknown_encodings.append(encode_face)

            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            current_time = now.strftime("%H:%M:%S")

            with open(logfile, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, current_date, current_time])

            y1, x2, y2, x1 = face_loc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), color, cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow(f'face recognition {cam_id}', img)
        cv2.waitKey(1)


if __name__ == '__main__':
    camera_ids = [0]  
    threads = []
    for cam_id in camera_ids:
        t = threading.Thread(target=process_camera, args=(cam_id,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

"""





           
    






