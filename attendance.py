import cv2

camera_id = 0
delay = 1
window_name = 'QR Code Reader'

detector = cv2.QRCodeDetector()
capture = cv2.VideoCapture(camera_id)

while True:
    status, frame = capture.read()

    if status:
        qr, info, points, _ = detector.detectAndDecodeMulti(frame)
        if qr:
            for s, p in zip(info, points):
                if s:
                    print(s)
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)
                frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
        cv2.imshow(window_name, frame)

    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

cv2.destroyWindow(window_name)

from datetime import date
import json
today=str(date.today)
print(today)
d={"vu22csen0101443":0,"vu22csen0100351":0,"vu22csen0100381":0,"vu22csen0100399":0}
with open("{0}_attendance.json".format(today),"w") as f:
  json.dump(d,f)
  f.close()

def decoder(image):
  gray_img = cv2.cvtColor(image,0)
  qrCodeDetector + cv2.QRCodeDetector()
  data, bbox, _ =qrCodeDetector.detectAndDecode(image)
  data = str(data)

  if data:
    print("+++++:",data)
    if d[data] == 0:
      d[data] = 1
      print(d)
      with open("{0}_attendance.json".format(today_date)):
                json.dump(d,f)
                f.close()