import face_recognition
import cv2
import numpy as np
import serial
from time import sleep

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
IR = 0xF3
FAN_N_UV = 0x74
SERVO = 0x63
BUTTON = 0xF6
OFF =  0x66
ON = 0x65
SEND_DETECT_FLAG = True
uart_header = [0x55,0x61]

# FAN,UV 정지
def OFF_FAN_N_UV():
    send_data = uart_header
    send_data.append(FAN_N_UV)
    send_data.append(OFF)
    ser.write(send_data)
    print(send_data)
    
# FAN,UV 실행
def ON_FAN_N_UV():
    send_data = uart_header
    send_data.append(FAN_N_UV)
    send_data.append(ON)
    ser.write(send_data)
    print(send_data)


#서보 제어(문 열림)
def ON_SERVO():
    uart_header = [0x61,0x62] #0x55,0x66
    send_data = uart_header
    send_data.append(SERVO) #servo
    send_data.append(ON) #on
    ser.write(send_data)
    print(send_data)

#서보 제어(문 닫힘)
def OFF_SERVO():
    send_data = uart_header
    send_data.append(SERVO)
    send_data.append(OFF)
    ser.write(send_data)
    print(send_data)
    send_data=[]

ser = serial.Serial ("/dev/ttyS0", 115200)    #Open port with baud rate

video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH,320)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Load a second sample picture and learn how to recognize it.
yulim_image = face_recognition.load_image_file("yulim2.jpg")
yulim_face_encoding = face_recognition.face_encodings(yulim_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    yulim_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden",
    "Hwang Yulim"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        if not face_encodings:
            SEND_DETECT_FLAG = True
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        if name == "Barack Obama": #만약 오바마가 맞다면
            ON_SERVO()
        elif name == "Hwang Yulim": #만약 오바마가 맞다면
            if SEND_DETECT_FLAG:
                ON_SERVO()
                SEND_DETECT_FLAG = not SEND_DETECT_FLAG

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()