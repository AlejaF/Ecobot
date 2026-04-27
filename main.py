import cv2
import numpy as np
import time
from datetime import datetime
import sqlite3
import os

# =========================
# CONFIGURACIÓN
# =========================
video_path = 'data/Tetrapak.mp4'

# ROI (ajústalo a tu caso)
roi_x, roi_y = 455, 9
roi_w, roi_h = 1010, 1066

# Movimiento
threshold_area = 5000   # área válida (ajustar)
cooldown_time = 3       # segundos entre eventos

# Batch
max_event_frames = 20

# Guardar dataset (activar/desactivar)
SAVE_DATASET = True
dataset_path = "dataset/Tetrapak"
os.makedirs(dataset_path, exist_ok=True)

# =========================
# BASE DE DATOS
# =========================
conn = sqlite3.connect("events.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS eventos (
    timestamp TEXT,
    objeto TEXT
)
""")
conn.commit()

# =========================
# MODELO (placeholder)
# =========================
def predict(frame):
    return "Tetrapak"  # reemplazar luego

def classify_batch(frames):
    preds = [predict(f) for f in frames]
    return max(set(preds), key=preds.count)

# =========================
# VIDEO
# =========================
cap = cv2.VideoCapture(video_path)

def preprocess_frame(frame):
    return frame  # sin resize por ahora

fgbg = cv2.createBackgroundSubtractorMOG2(
    history=300,
    varThreshold=40,
    detectShadows=True
)

kernel = np.ones((5, 5), np.uint8)

last_event_time = 0
frame_id = 0

print("🚀 Sistema iniciado...")

# =========================
# LOOP PRINCIPAL
# =========================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = preprocess_frame(frame)

    # ROI (recortamos un poco la derecha para evitar flare)
    roi = frame[roi_y:roi_y+roi_h, roi_x:roi_x+int(roi_w*0.8)]

    # Preprocesamiento
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Background subtraction
    fgmask = fgbg.apply(blur)

    _, thresh = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # =========================
    # FILTRO POR CONTORNOS
    # =========================
    contours, _ = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    valid_area = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 500 < area < 50000:  # ajustar según pruebas
            valid_area += area

    # =========================
    # FILTRO POR CAMBIO GLOBAL (LUZ)
    # =========================
    total_pixels = clean.shape[0] * clean.shape[1]
    movement_ratio = np.count_nonzero(clean) / total_pixels

    current_time = time.time()

    # =========================
    # DETECCIÓN DE EVENTO
    # =========================
    if (
        valid_area > threshold_area and
        movement_ratio < 0.3 and  # evita flare
        (current_time - last_event_time > cooldown_time)
    ):
        print("📦 Evento detectado")

        last_event_time = current_time

        frames_batch = []
        frame_count = 0

        # =========================
        # CAPTURA DINÁMICA
        # =========================
        while frame_count < max_event_frames:
            ret, batch_frame = cap.read()
            if not ret:
                break

            batch_frame = preprocess_frame(batch_frame)

            roi_batch = batch_frame[roi_y:roi_y+roi_h, roi_x:roi_x+int(roi_w*0.8)]

            gray_b = cv2.cvtColor(roi_batch, cv2.COLOR_BGR2GRAY)
            blur_b = cv2.GaussianBlur(gray_b, (5, 5), 0)

            fgmask_b = fgbg.apply(blur_b)
            _, thresh_b = cv2.threshold(fgmask_b, 200, 255, cv2.THRESH_BINARY)
            clean_b = cv2.morphologyEx(thresh_b, cv2.MORPH_OPEN, kernel)

            movement_b = np.count_nonzero(clean_b)

            if movement_b < threshold_area * 0.3:
                break

            frames_batch.append(roi_batch)
            print("Frames captured:", len(frames_batch))
            # Guardar para dataset
            if SAVE_DATASET and frame_count % 2 == 0:
                cv2.imwrite(f"{dataset_path}/frame_{frame_id}.jpg", roi_batch)
                frame_id += 1

            frame_count += 1

        # =========================
        # CLASIFICACIÓN
        # =========================
        if len(frames_batch) > 0:
            objeto = classify_batch(frames_batch)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"✅ Detectado: {objeto} | Frames: {len(frames_batch)}")

            cursor.execute(
                "INSERT INTO eventos VALUES (?, ?)",
                (timestamp, objeto)
            )
            conn.commit()

    # =========================
    # VISUALIZACIÓN
    # =========================
    cv2.imshow("ROI", roi)
    cv2.imshow("Mask", clean)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# =========================
# CIERRE
# =========================
cap.release()
cv2.destroyAllWindows()
conn.close()

print("🛑 Sistema detenido")