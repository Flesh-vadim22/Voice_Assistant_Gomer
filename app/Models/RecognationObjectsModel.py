import numpy as np
import cv2
from app.Models.WorkWithMessagesModel import WorkWithMessageModel
import app.Models.BrowserModel

class RecognationObjectsModel:

    def __init__(self, object=None):
        self.object = object
        self.message = WorkWithMessageModel()
        self.browser = app.Models.BrowserModel.BrowserModel()

    def findObjects(self, outputs, img):
        hT, wT, cT = img.shape
        bbox = []
        classIds = []
        confs = []
        confThreshold = 0.5
        nmsThreshold = 0.2
        classNames = []
        classFile = r'app\Models\config\coco.names'

        with open(classFile, 'r') as f:
            classNames = f.read().rstrip('\n').split('\n')

        for output in outputs:
            for det in output:
                scores = det[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > confThreshold:
                    w, h = int(det[2] * wT), int(det[3] * hT)
                    x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)
                    bbox.append([x, y, w, h])
                    classIds.append(classId)
                    confs.append(float(confidence))

        # Работа с рамкой объекта изображения
        indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)
        for i in indices:
            i = i[0]
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(img, f'{classNames[classIds[i]].upper()}{int(confs[i] * 100)}%', (x, y - 10),
                        cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 2)
            self.object = classNames[classIds[i]].upper()
            self.message.speak_object(self.browser.translate_phrase(self.object))



    def recogn_objects(self):

        whT = 320
        modelConfiguration = r'app\Models\config\yolov3-tiny.cfg'   # наименование конфига
        modelWeights = r'app\Models\config\yolov3-tiny.weights'  # наименование файла весов

        net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights) # чтение нейронной сети с помощью её конфига и весов
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV) # задание BACKENDA нейронной сети
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU) # установка целевого значения  исп. ресурсов для NN

        cap = cv2.VideoCapture(0)
        wCap, hCap = 640, 480
        cap.set(3, wCap)
        cap.set(4, hCap)
        webcam = True

        while True:
            if webcam:
                success, frame = cap.read()
            else:
                frame = cv2.imread(r'app\Models\config\cat.jpg')
            blob = cv2.dnn.blobFromImage(frame, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False) # конвертирование изображения в формат данных NN
            net.setInput(blob)          # установка формата данных сети
            layersNames = net.getLayerNames()   # получение имен слоёв сети

            outputNames = [(layersNames[i[0] - 1]) for i in net.getUnconnectedOutLayers()] # получение имен сети только выходных слоёв
            outputs = net.forward(outputNames) # получение результатов от 3-х выходных слоёв сети
            self.findObjects(outputs, frame)  # нахождение объекта изобраэения и получение его вероятности
            cv2.imshow('Cap', frame)
            k = cv2.waitKey(1)
            if k == 27 or cv2.getWindowProperty('Cap', cv2.WND_PROP_VISIBLE) < 1:
                break

        cv2.destroyAllWindows()