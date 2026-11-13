
class ObjectTracker:

    def __init__(self, detector):

        self.detector = detector

        self.tracker_config = (
            "models/sentinela_bytetrack.yaml"
        )

    def track(self, frame):

        results = self.detector.model.track(

            source=frame,

            persist=True,

            tracker=self.tracker_config,

            classes=self.detector.CLASSES,

            conf=self.detector.confidence,

            imgsz=self.detector.image_size,

            verbose=False
        )

        return results[0]