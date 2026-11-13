
import csv
import os
from datetime import datetime


class EventAnalyzer:

    def __init__(
        self,
        reports_dir="data/reports",
        presence_threshold=30,
        minimum_frames=30
    ):
        self.reports_dir = reports_dir
        self.presence_threshold = presence_threshold
        self.minimum_frames = minimum_frames

        self.input_file = os.path.join(
            reports_dir, "tracks_summary.csv"
        )

        self.output_file = os.path.join(
            reports_dir, "analyzed_events.csv"
        )

    def analyze(self):

        if not os.path.exists(self.input_file):
            raise FileNotFoundError(
                "Arquivo tracks_summary.csv não encontrado. "
                "Processe um vídeo primeiro."
            )

        events = []

        with open(
            self.input_file,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            tracks = csv.DictReader(file)

            for track in tracks:

                duration = float(
                    track["observed_seconds"] or 0
                )

                frames = int(track["frames"] or 0)

                confidence = float(
                    track["average_confidence"] or 0
                )

                if (
                    duration >= self.presence_threshold
                    and frames >= self.minimum_frames
                ):

                    events.append({
                        "track_id": track["track_id"],
                        "object_class": track["object_class"],
                        "first_seen_seconds": track["first_seen_seconds"],
                        "last_seen_seconds": track["last_seen_seconds"],
                        "observed_interval_seconds": duration,
                        "frames": frames,
                        "average_confidence": confidence,
                        "event": "Prolonged observation interval",
                        "status": "Requires human review"
                    })

        with open(
            self.output_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            fields = [
                "track_id",
                "object_class",
                "first_seen_seconds",
                "last_seen_seconds",
                "observed_interval_seconds",
                "frames",
                "average_confidence",
                "event",
                "status"
            ]

            writer = csv.DictWriter(
                file,
                fieldnames=fields
            )

            writer.writeheader()
            writer.writerows(events)

        print("\nSENTINELA - ANALISE DE EVENTOS")
        print("=" * 40)
        print("Data:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("Rastreamentos analisados:", self._count_tracks())
        print("Ocorrências para revisão:", len(events))
        print("Arquivo gerado:", self.output_file)
        print("\nAnálise concluída.")


    def _count_tracks(self):

        with open(
            self.input_file,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            return sum(1 for _ in csv.DictReader(file))


if __name__ == "__main__":

    analyzer = EventAnalyzer()
    analyzer.analyze()
