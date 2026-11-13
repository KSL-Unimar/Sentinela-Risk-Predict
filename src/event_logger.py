
import csv
import os
from collections import defaultdict


class EventLogger:

    def __init__(self, reports_dir):

        os.makedirs(reports_dir, exist_ok=True)

        self.detections_path = os.path.join(
            reports_dir, "detections.csv"
        )

        self.summary_path = os.path.join(
            reports_dir, "tracks_summary.csv"
        )

        self.tracks = defaultdict(lambda: {
            "class": "",
            "first_frame": 0,
            "last_frame": 0,
            "frames": 0,
            "confidence_sum": 0.0
        })

        self.file = open(
            self.detections_path,
            "w",
            newline="",
            encoding="utf-8"
        )

        self.writer = csv.DictWriter(
            self.file,
            fieldnames=[
                "frame",
                "time_seconds",
                "track_id",
                "object_class",
                "confidence",
                "center_x",
                "center_y"
            ]
        )

        self.writer.writeheader()

    def register(self, frame_number, fps, boxes, names):

        if fps <= 0:
            fps = 30.0

        if boxes.id is None:
            return

        ids = boxes.id.cpu().numpy().astype(int)
        coordinates = boxes.xyxy.cpu().numpy()
        classes = boxes.cls.cpu().numpy().astype(int)
        confidences = boxes.conf.cpu().numpy()

        for track_id, xyxy, cls, confidence in zip(
            ids, coordinates, classes, confidences
        ):

            x1, y1, x2, y2 = xyxy

            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            object_class = names[int(cls)]

            self.writer.writerow({
                "frame": frame_number,
                "time_seconds": round(frame_number / fps, 2),
                "track_id": int(track_id),
                "object_class": object_class,
                "confidence": round(float(confidence), 4),
                "center_x": round(float(center_x), 2),
                "center_y": round(float(center_y), 2)
            })

            track = self.tracks[int(track_id)]

            if track["frames"] == 0:
                track["class"] = object_class
                track["first_frame"] = frame_number

            track["last_frame"] = frame_number
            track["frames"] += 1
            track["confidence_sum"] += float(confidence)

    def close(self, fps):

        self.file.close()

        if fps <= 0:
            fps = 30.0

        with open(
            self.summary_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "track_id",
                    "object_class",
                    "first_seen_seconds",
                    "last_seen_seconds",
                    "observed_seconds",
                    "frames",
                    "average_confidence"
                ]
            )

            writer.writeheader()

            for track_id, track in self.tracks.items():

                first = track["first_frame"]
                last = track["last_frame"]

                writer.writerow({
                    "track_id": track_id,
                    "object_class": track["class"],
                    "first_seen_seconds": round(first / fps, 2),
                    "last_seen_seconds": round(last / fps, 2),
                    "observed_seconds": round(
                        (last - first) / fps, 2
                    ),
                    "frames": track["frames"],
                    "average_confidence": round(
                        track["confidence_sum"] /
                        track["frames"], 4
                    )
                })