
import argparse
import os
import cv2

from src.detector import ObjectDetector
from src.tracker import ObjectTracker
from src.event_logger import EventLogger


def process_video(video_path, output_dir):

    if not os.path.isfile(video_path):
        raise FileNotFoundError(
            f"Vídeo não encontrado: {video_path}"
        )

    os.makedirs(output_dir, exist_ok=True)

    reports_dir = "data/reports"

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise RuntimeError("Não foi possível abrir o vídeo.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if fps <= 0:
        fps = 30.0

    output_path = os.path.join(
        output_dir, "sentinela_resultado.mp4"
    )

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    if not writer.isOpened():
        cap.release()
        raise RuntimeError("Não foi possível criar o vídeo.")

    detector = ObjectDetector()
    tracker = ObjectTracker(detector)
    logger = EventLogger(reports_dir)

    frame_number = 0

    print("Sentinela iniciado!")
    print("Processando vídeo...")

    try:
        while True:

            ret, frame = cap.read()

            if not ret:
                break

            frame_number += 1

            result = tracker.track(frame)

            if result.boxes is not None:

                logger.register(
                    frame_number,
                    fps,
                    result.boxes,
                    result.names
                )

                if result.boxes.id is not None:

                    boxes = result.boxes.xyxy.cpu().numpy()
                    ids = result.boxes.id.cpu().numpy().astype(int)
                    classes = result.boxes.cls.cpu().numpy().astype(int)
                    confidences = result.boxes.conf.cpu().numpy()

                    for box, track_id, cls, confidence in zip(
                        boxes, ids, classes, confidences
                    ):

                        x1, y1, x2, y2 = map(int, box)

                        label = (
                            f"{result.names[int(cls)]} "
                            f"ID:{track_id} "
                            f"{confidence:.2f}"
                        )

                        cv2.rectangle(
                            frame,
                            (x1, y1),
                            (x2, y2),
                            (0, 255, 0),
                            2
                        )

                        cv2.putText(
                            frame,
                            label,
                            (x1, max(y1 - 10, 20)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 255, 0),
                            2
                        )

            cv2.putText(
                frame,
                "SENTINELA - RISK PREDICT",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            writer.write(frame)

            if frame_number % 100 == 0:
                print(
                    f"Quadros processados: {frame_number}"
                )

    finally:
        cap.release()
        writer.release()
        logger.close(fps)

    print("\nProcessamento concluído!")
    print(f"Vídeo: {output_path}")
    print(f"Relatórios: {reports_dir}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Sentinela - Risk Predict"
    )

    parser.add_argument(
        "--video",
        default="data/videos/condominio.mp4"
    )

    parser.add_argument(
        "--output",
        default="data/processed"
    )

    args = parser.parse_args()

    process_video(args.video, args.output)