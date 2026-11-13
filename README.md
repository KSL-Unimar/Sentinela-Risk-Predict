# SENTINELA – RISK PREDICT

**Sistema inteligente de monitoramento e análise preventiva de segurança**

## 1. Apresentação

O Sentinela – Risk Predict é um projeto de visão computacional desenvolvido em Python para auxiliar no monitoramento preventivo de ambientes, utilizando vídeos gravados como fonte de dados.

O sistema utiliza inteligência artificial para detectar objetos, acompanhar seus deslocamentos e registrar eventos que podem ser analisados posteriormente.

## 2. Tecnologias utilizadas

- Python 3
- YOLO (Ultralytics)
- OpenCV
- ByteTrack
- Pandas
- Matplotlib
- CSV

## 3. Funcionalidades

- Detecção de pessoas e veículos em vídeos.
- Rastreamento de objetos por identificadores.
- Registro de detecções e horários.
- Geração de estatísticas de rastreamento.
- Identificação de intervalos prolongados de observação.
- Geração de relatórios em CSV e TXT.
- Visualização de indicadores por meio de gráficos.

## 4. Estrutura do projeto

```text
Sentinela-Risk-Predict/
├── data/
│   ├── videos/
│   ├── processed/
│   └── reports/
├── models/
├── src/
│   ├── __init__.py
│   ├── detector.py
│   ├── tracker.py
│   ├── event_logger.py
│   ├── report_generator.py
│   └── event_analyzer.py
├── dashboard.py
├── main.py
├── requirements.txt
└── README.md
```

## 5. Instalação

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

No Arch Linux, o Python e o ambiente virtual podem ser preparados com:

```bash
sudo pacman -S python python-pip
python -m venv .venv
source .venv/bin/activate
```

## 6. Como executar

**Etapa 1 – Processamento do vídeo**

Coloque o vídeo na pasta `data/videos/` e execute:

```bash
python main.py
```

Utilize o caminho do vídeo conforme a configuração do programa.

**Etapa 2 – Gerar relatórios**

```bash
python -m src.report_generator
```

**Etapa 3 – Gerar análise de eventos**

```bash
python -m src.event_analyzer
```

**Etapa 4 – Gerar painel visual**

```bash
python dashboard.py
```

## 7. Arquivos gerados

Os resultados são armazenados em `data/reports/`:

| Arquivo | Descrição |
|---|---|
| detections.csv | Registro das detecções |
| tracks_summary.csv | Resumo dos rastreamentos |
| report_summary.txt | Relatório estatístico |
| attention_indicators.csv | Indicadores para revisão |
| analyzed_events.csv | Eventos analisados |
| sentinela_dashboard.png | Painel gráfico |

## 8. Critérios de análise

O sistema utiliza indicadores quantitativos, como intervalo entre primeira e última observação e quantidade de quadros registrados.

Esses indicadores servem para direcionar a atenção de um operador humano.

Uma permanência prolongada não significa, isoladamente, comportamento suspeito ou intenção criminosa.

## 9. Limitações conhecidas

- A precisão depende da qualidade e resolução do vídeo.
- Iluminação, obstáculos e movimentação podem afetar as detecções.
- O rastreamento pode apresentar perda ou troca de identificadores.
- O intervalo observado não comprova presença contínua.
- Os indicadores não representam previsão comprovada de crimes.
- Os resultados exigem interpretação humana.

## 10. Objetivo do projeto

Demonstrar a aplicação de inteligência artificial e visão computacional na análise preventiva de ambientes monitorados, oferecendo informações organizadas para auxiliar a tomada de decisão humana.

---

**SENTINELA – RISK PREDICT**

Projeto de análise preventiva de segurança baseado em inteligência artificial e visão computacional.