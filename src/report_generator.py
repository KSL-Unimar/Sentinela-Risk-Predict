
import csv
import os
from collections import Counter
from statistics import mean
from datetime import datetime


class ReportGenerator:

    def __init__(self, reports_dir="data/reports",
                 long_presence_seconds=30):

        self.reports_dir = reports_dir
        self.long_presence_seconds = long_presence_seconds

        os.makedirs(self.reports_dir, exist_ok=True)

        self.detections_path = os.path.join(
            self.reports_dir, "detections.csv"
        )

        self.summary_path = os.path.join(
            self.reports_dir, "tracks_summary.csv"
        )

        self.report_path = os.path.join(
            self.reports_dir, "report_summary.txt"
        )

        self.attention_path = os.path.join(
            self.reports_dir, "attention_indicators.csv"
        )

    def generate(self):

        if not os.path.exists(self.detections_path):
            raise FileNotFoundError(
                f"Arquivo não encontrado: {self.detections_path}"
            )

        if not os.path.exists(self.summary_path):
            raise FileNotFoundError(
                f"Arquivo não encontrado: {self.summary_path}"
            )

        with open(
            self.detections_path,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            detections = list(csv.DictReader(file))

        with open(
            self.summary_path,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            tracks = list(csv.DictReader(file))

        # Estatísticas gerais
        class_counts = Counter(
            row["object_class"] for row in detections
        )

        confidences = [
            float(row["confidence"])
            for row in detections
            if row.get("confidence")
        ]

        total_detections = len(detections)
        total_tracks = len(tracks)

        average_confidence = (
            mean(confidences) if confidences else 0
        )

        # Indicadores de permanência prolongada
        attention_items = []

        for track in tracks:

            duration = float(
                track.get("observed_seconds") or 0
            )

            if duration >= self.long_presence_seconds:

                attention_items.append({
                    "track_id": track["track_id"],
                    "object_class": track["object_class"],
                    "observed_seconds": duration,
                    "frames": track["frames"],
                    "indicator": "Longa permanência - revisar contexto"
                })

        # Exportar indicadores
        with open(
            self.attention_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            fields = [
                "track_id",
                "object_class",
                "observed_seconds",
                "frames",
                "indicator"
            ]

            writer = csv.DictWriter(
                file,
                fieldnames=fields
            )

            writer.writeheader()
            writer.writerows(attention_items)

        # Gerar relatório textual
        with open(
            self.report_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write("SENTINELA - RISK PREDICT\n")
            file.write("RELATORIO DE MONITORAMENTO\n")
            file.write("=" * 45 + "\n")

            file.write(
                f"Data de geração: "
                f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
            )

            file.write("INDICADORES GERAIS\n")
            file.write("-" * 45 + "\n")

            file.write(
                f"Total de detecções: {total_detections}\n"
            )

            file.write(
                f"Objetos acompanhados: {total_tracks}\n"
            )

            file.write(
                f"Confiança média: {average_confidence:.2%}\n"
            )

            file.write(
                f"Indicadores para revisão: "
                f"{len(attention_items)}\n\n"
            )

            file.write("DETECÇÕES POR CLASSE\n")
            file.write("-" * 45 + "\n")

            for object_class, quantity in class_counts.items():

                file.write(
                    f"{object_class}: {quantity}\n"
                )

            file.write("\nINDICADORES DE ATENÇÃO\n")
            file.write("-" * 45 + "\n")

            if attention_items:

                for item in attention_items:

                    file.write(
                        f"ID {item['track_id']} | "
                        f"{item['object_class']} | "
                        f"{item['observed_seconds']} segundos\n"
                    )

            else:

                file.write(
                    "Nenhum indicador de permanência prolongada.\n"
                )

            file.write("\n")
            file.write(
                "OBSERVACAO: permanência prolongada é um "
                "indicador para revisão humana, não uma "
                "evidência de comportamento suspeito.\n"
            )

            file.write(
                "O intervalo de observação não representa "
                "necessariamente visibilidade contínua.\n"
            )

        print("\nRelatórios gerados com sucesso!")
        print(self.report_path)
        print(self.attention_path)


if __name__ == "__main__":

    generator = ReportGenerator()
    generator.generate()
