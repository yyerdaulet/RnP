import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Загрузи свою обученную модель
model = load_model("my_model.h5")  # замени на имя твоей модели

# Запусти камеру
cap = cv2.VideoCapture(0)  # 0 — встроенная камера

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))

    for y in range(0, 480 - 200 + 1, 50):
        for x in range(0, 640 - 200 + 1, 50):
            crop = frame[y:y+200, x:x+200]
            img = crop.astype('float32') / 255.0
            img = np.expand_dims(img, axis=0)

            prediction = model.predict(img, verbose=0)
            class_id = np.argmax(prediction)
            confidence = np.max(prediction)

            if confidence > 0.9:
                cv2.rectangle(frame, (x, y), (x+200, y+200), (0,255,0), 2)
                label = f"Class {class_id}, {confidence:.2f}"
                cv2.putText(frame, label, (x+5, y+25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 1)

    cv2.imshow("CNN Detector", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Esc для выхода
        break

cap.release()
cv2.destroyAllWindows()