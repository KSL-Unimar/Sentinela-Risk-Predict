
import csv
import os
from collections import Counter, defaultdict

import matplotlib.pyplot as plt


REPORTS_DIR = "data/reports"

DETECTIONS_FILE = os.path.join(
    REPORTS_DIR, "detections.csv"
)

SUMMARY_FILE = os.path.join(
    REPORTS_DIR, "tracks_summary.csv"
)

OUTPUT_FILE = os.path.join(
    REPORTS_DIR, "sentinela_dashboard.png"
)


def read_csv(path):

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Arquivo não encontrado: {path}"
        )

    with open(
        path,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        return list(csv.DictReader(file))


def generate_dashboard():

    detections = read_csv(DETECTIONS_FILE)
    tracks = read_csv(SUMMARY_FILE)

    # Indicadores gerais
    total_detections = len(detections)
    total_tracks = len(tracks)

    confidences = [
        float(row["confidence"])
        for row in detections
        if row.get("confidence")
    ]

    average_confidence = (
        sum(confidences) / len(confidences)
        if confidences else 0
    )

    # Detecções por classe
    class_counts = Counter(
        row["object_class"]
        for row in detections
    )

    # Detecções por segundo
    timeline = defaultdict(int)

    for row in detections:

        second = int(float(row["time_seconds"]))
        timeline[second] += 1

    # Dez rastreamentos com maior intervalo observado
    longest_tracks = sorted(
        tracks,
        key=lambda row: float(
            row.get("observed_seconds") or 0
        ),
        reverse=True
    )[:10]

    # Criar painel
    fig, axes = plt.subplots(
        2, 2,
        figsize=(14, 9)
    )

    fig.suptitle(
        "SENTINELA - RISK PREDICT | PAINEL DE MONITORAMENTO",
        fontsize=15,
        fontweight="bold"
    )

    fig.text(
        0.08, 0.91,
        f"Detecções: {total_detections}",
        fontsize=12
    )

    fig.text(
        0.37, 0.91,
        f"Objetos acompanhados: {total_tracks}",
        fontsize=12
    )

    fig.text(
        0.72, 0.91,
        f"Confiança média: {average_confidence:.1%}",
        fontsize=12
    )

    # Gráfico 1: classes
    ax = axes[0, 0]

    if class_counts:

        classes = list(class_counts.keys())
        quantities = list(class_counts.values())

        ax.bar(classes, quantities)
        ax.set_title("Detecções por classe")
        ax.set_ylabel("Quantidade")
        ax.tick_params(axis="x", rotation=25)

    else:

        ax.set_title("Detecções por classe")
        ax.text(0.5, 0.5, "Sem dados",
                ha="center", va="center")

    # Gráfico 2: linha do tempo
    ax = axes[0, 1]

    if timeline:

        seconds = sorted(timeline.keys())
        quantities = [timeline[s] for s in seconds]

        ax.plot(seconds, quantities, marker="o")
        ax.set_title("Detecções ao longo do vídeo")
        ax.set_xlabel("Tempo (segundos)")
        ax.set_ylabel("Detecções por segundo")

    else:

        ax.set_title("Detecções ao longo do vídeo")
        ax.text(0.5, 0.5, "Sem dados",
                ha="center", va="center")

    # Gráfico 3: confiança
    ax = axes[1, 0]

    if confidences:

        ax.hist(confidences, bins=10)
        ax.set_title("Distribuição de confiança")
        ax.set_xlabel("Confiança")
        ax.set_ylabel("Quantidade")

    else:

        ax.set_title("Distribuição de confiança")
        ax.text(0.5, 0.5, "Sem dados",
                ha="center", va="center")

    # Gráfico 4: rastreamentos mais longos
    ax = axes[1, 1]

    if longest_tracks:

        labels = [
            f"ID {row['track_id']} ({row['object_class']})"
            for row in longest_tracks
        ]

        durations = [
            float(row["observed_seconds"])
            for row in longest_tracks
        ]

        ax.barh(labels, durations)
        ax.set_title("Maiores intervalos observados")
        ax.set_xlabel("Segundos entre primeira e última observação")
        ax.invert_yaxis()

    else:

        ax.set_title("Maiores intervalos observados")
        ax.text(0.5, 0.5, "Sem dados",
                ha="center", va="center")

    fig.text(
        0.5, 0.015,
        "Indicadores estatísticos. Não representam confirmação de comportamento suspeito.",
        ha="center",
        fontsize=9
    )

    plt.tight_layout(rect=[0, 0.04, 1, 0.88])

    # Salvar painel
    fig.savefig(
        OUTPUT_FILE,
        dpi=150,
        bbox_inches="tight"
    )

    print("\nPainel gerado com sucesso!")
    print(f"Arquivo: {OUTPUT_FILE}")

    plt.show()


if __name__ == "__main__":
    generate_dashboard()
