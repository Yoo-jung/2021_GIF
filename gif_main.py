import requests
import json
import cv2
import serial
import time


#protocol
FACE = 0xF4
SEASON = 0xF5
TEMP = 0xF6
uart_header = [0x55,0x66]

#     get face frame

# 카메라 영상을 받아올 객체 선언 및 설정(영상 소스, 해상도 설정)
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)

# haar cascade 검출기 객체 선언
face_cascade = cv2.CascadeClassifier('GIF2021_1/haarcascade/haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')
# 무한루프
face_check = 'N'
while True:    
    ret, frame = capture.read()     # 카메라로부터 현재 영상을 받아 frame에 저장, 잘 받았다면 ret가 참
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 영상을 흑백으로 바꿔줌

    # scaleFactor를 1에 가깝게 해주면 정확도가 상승하나 시간이 오래걸림
    # minNeighbors를 높여주면 검출률이 상승하나 오탐지율도 상승
    faces = face_cascade.detectMultiScale(gray, scaleFactor= 1.5, minNeighbors=3, minSize=(20,20))
    # eyes = eye_cascade.detectMultiScale(gray, scaleFactor= 1.5, minNeighbors=3, minSize=(10,10))
    # print(faces)
    
    # 찾은 얼굴이 있으면
    # 얼굴 영역을 영상에 사각형으로 표시
    if len(faces) :
        for  x, y, w, h in faces :
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255,255,255), 2, cv2.LINE_4)
            face_check = 'Y'
    '''if len(eyes) :
        for  x, y, w, h in eyes :
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,255), 2, cv2.LINE_4)'''
    cv2.imshow("original", frame)   # frame(카메라 영상)을 original 이라는 창에 띄워줌 
    
    #     if get faceframe -> break!!!!!!!
    if face_check == 'Y':  # 키보드의 q 를 누르면 무한루프가 멈춤
            send_data = uart_header
            send_data.append(FACE)
            send_data.append(0x00)
            serial.write(send_data)
            send_data =[]
            time.sleep(1)
            break

capture.release()                   # 캡처 객체를 없애줌
cv2.destroyAllWindows()             # 모든 영상 창을 닫아줌


#     sort weather
# get API data
response = requests.get('http://api.weatherapi.com/v1/current.json?key=56e480e2ae5c44f381d65742211111&q=seoul&aqi=yes')
jsonObj = json.loads(response.text)

# print weather data-> temp & condition
print(jsonObj['current']['temp_c'], jsonObj['current']['condition']['text'])

# print date data & time
print(jsonObj['location']['localtime'])
send_data = uart_header

# sort Season data
seoson = jsonObj['location']['localtime'][5:7]
send_data.append(SEASON)
if  seoson == '12' or seoson <= '2':
    print('Winter')
    send_data.append(0x04)
    serial.write(send_data)
    send_data=[]
elif seoson >= '9' and seoson <= '11':
    print('Fall')
    send_data.append(0x02)
    serial.write(send_data)
    send_data=[]
elif seoson >= '5' and seoson <= '8':
    print('Summer')
    send_data.append(0x03)
    serial.write(send_data)
    send_data=[]
else:
    print('Spring')
    send_data.append(0x02)
    serial.write(send_data)
    send_data=[]
    
#sort Temp data
temp = int(jsonObj['current']['temp_c'])
send_data = uart_header
send_data.append(TEMP)
if temp >= 28:
    print('0x05')
    send_data.append(0x05)
elif temp >= 20 and temp < 28:
    print('0x06')
    send_data.append(0x06)
elif temp >= 10 and temp < 20:
    print('0x07')
    send_data.append(0x07)
elif temp >= 0 and temp < 10:
    print('0x08')
    send_data.append(0x08)
elif temp < 0:
    print('0x09')
    send_data.append(0x09)
    
serial.write(send_data)
send_data=[]