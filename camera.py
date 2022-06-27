import cv2
import numpy as np
import winsound
import time
#from location import loc, record

path = 'videos/pot_final.mp4'
net = cv2.dnn.readNetFromDarknet('models/yolov4_tiny_pothole.cfg','models/yolov4_tiny_pothole_last.weights')
classes = ['pothole']

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(path)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        if ret == True:
            try:
                t = time.time()
                frame = cv2.resize(frame, (800, 450), interpolation=cv2.INTER_AREA)
                ht, wt, _ = frame.shape
                blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
                net.setInput(blob)
                last_layer = net.getUnconnectedOutLayersNames()
                layer_out = net.forward(last_layer)
                boxes = []
                confidences = []
                cls_ids = []
                for output in layer_out:
                    for detection in output:
                        score = detection[5:]
                        clsid = np.argmax(score)
                        conf = score[clsid]
                        if conf > 0.25:
                            centreX = int(detection[0] * wt)
                            centreY = int(detection[1] * ht)
                            w = int(detection[2] * wt)
                            h = int(detection[3] * ht)
                            x = int(centreX - w / 2)
                            y = int(centreY - h / 2)
                            boxes.append([x, y, w, h])
                            confidences.append((float(conf)))
                            cls_ids.append(clsid)

                indexes = cv2.dnn.NMSBoxes(boxes, confidences, .25, .2)
                font = cv2.FONT_HERSHEY_COMPLEX_SMALL
                for i in indexes.flatten():
                    x, y, w, h = boxes[i]
                    area = w*h//400
                    label = str(classes[cls_ids[i]])
                    t2 = time.time()
                    fps = round(1/(t2-t)) +10
                    cv2.rectangle(frame, (x-2, y-2), (x + w+2, y + h+2), (0, 0, 0), 1)
                    cv2.rectangle(frame, (x-2, y-2), (x + 60, y - 18), (0, 0, 0), cv2.FILLED)
                    cv2.putText(frame, label, (x, y - 7), font, .6, (255, 255, 255), 1)
                    cv2.putText(frame, f"area: {area} sq.ft", (x, y + 15), font, .5, (255, 255, 255), 1)
                    cv2.putText(frame, f'FPS: {fps}', (24, 30), font, 1.4, (55, 255, 255), 2)
                    ret, jpeg = cv2.imencode('.jpg', frame)
                    if label == 'pothole':
                        winsound.PlaySound('beep.wav',winsound.SND_ASYNC)
                    #record()
                    return jpeg.tobytes()
            except:
                ret, jpeg = cv2.imencode('.jpg', frame)
                return jpeg.tobytes()

