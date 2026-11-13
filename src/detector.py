
from ultralytics import YOLO


class ObjectDetector:

    CLASSES = [0, 2, 3, 5, 7]

    def __init__(
        self,
        #model_path="yolo11n.pt",
        model_path="yolo11s.pt",
        confidence=0.10,
        image_size=960
    ):

        self.model = YOLO(model_path)
        self.confidence = confidence
        self.image_size = image_size

    def detect(self, frame):

        results = self.model.predict(
            source=frame,
            classes=self.CLASSES,
            conf=self.confidence,
            imgsz=self.image_size,
            verbose=False
        )

        return results[0]
