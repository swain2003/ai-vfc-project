# 🚗 AI-Integrated Vehicular Fog Computing Framework (AI-VFC)

> An AI-driven Vehicular Fog Computing framework for Intelligent Transportation Systems (ITS), integrating Deep Reinforcement Learning (DRL), LSTM-based mobility prediction, and Federated Learning for intelligent task offloading, low-latency edge computing, and secure VANET communication.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/AI-Driven-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/DRL-Reinforcement%20Learning-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/LSTM-Mobility%20Prediction-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Federated-Learning-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/VANET-Security-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Simulation-NS3%20%7C%20SUMO%20%7C%20MATLAB-yellow?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-gold?style=for-the-badge" />
</p>

---

## Overview

AI-Integrated Vehicular Fog Computing (AI-VFC) is a research-oriented project focused on building an intelligent, low-latency Vehicular Fog Computing framework for Intelligent Transportation Systems (ITS). The framework integrates Artificial Intelligence techniques such as Deep Reinforcement Learning (DRL), Long Short-Term Memory (LSTM) networks, and Federated Learning (FL) to improve task offloading, mobility prediction, resource allocation, and VANET security.

The proposed architecture combines three computational layers:

* Vehicle Layer
* Fog Layer
* Cloud Layer

The framework is designed to support real-time vehicular communication, edge computing, proactive handover management, and privacy-preserving distributed learning.

---

## Objectives

* Design a conceptual architecture for Vehicular Fog Computing
* Implement an intelligent decision engine for efficient task allocation
* Optimize execution decisions using latency, energy, and workload metrics
* Analyze system performance using simulation-based evaluation metrics

---

## Features

* AI-driven Vehicular Fog Computing architecture
* Deep Reinforcement Learning (DRL)-based task offloading
* LSTM-based mobility and RSU handover prediction
* Federated Learning (FL) for privacy-preserving distributed training
* Federated anomaly detection for VANET security
* Multi-objective optimization model for adaptive execution
* Edge computing support using Fog Nodes and RSUs
* Offline resilience and distributed decision-making
* Simulation-based evaluation using NS-3, SUMO, and MATLAB

---

## System Architecture

The AI-VFC framework follows a three-layer hierarchical architecture:

### 1. Vehicle Layer

* Collects data from sensors, GPS, LiDAR, and onboard units
* Performs local preprocessing and inference
* Supports V2V, V2I, and V2F communication

### 2. Fog Layer

* Handles task offloading and resource allocation
* Executes AI-based workload management
* Performs anomaly detection and mobility prediction
* Enables low-latency edge processing through RSUs and edge servers

### 3. Cloud Layer

* Performs global model training and analytics
* Aggregates federated learning updates
* Maintains policy and system-wide optimization

---

## Tech Stack

### Programming Languages

* Python

### AI & Machine Learning

* Deep Reinforcement Learning (DRL)
* Federated Learning (FL)
* LSTM Networks

### Simulation & Research Tools

* NS-3
* SUMO
* MATLAB

### Web Technologies

* HTML
* CSS

### Core Domains

* VANET
* Edge Computing
* Intelligent Transportation Systems (ITS)

---

## Methodology

1. Designed the conceptual AI-VFC framework for Vehicular Fog Computing.
2. Implemented the architecture into a working simulation-oriented system using Python.
3. Developed a DRL-based intelligent decision engine for optimized task execution.
4. Built LSTM-based mobility prediction and proactive RSU handover mechanisms.
5. Integrated Federated Learning for privacy-preserving distributed model training.
6. Evaluated system performance using simulation datasets and analytical metrics.

---

## Optimization Model

The framework uses a multi-objective optimization model for adaptive task execution:

```text
C = αL + βE + γW
```

Where:

* L = Latency
* E = Energy Consumption
* W = Workload
* α, β, γ = Adaptive priority weights

---

## Workflow

1. Data Generation from vehicular sensors
2. Data Transmission through V2X communication
3. Edge Pre-processing at Fog Nodes
4. AI-based Decision Making
5. Task Execution across Vehicle/Fog/Cloud layers
6. Feedback Learning and Continuous Optimization

---

## Results

The AI-VFC framework demonstrates improved task allocation efficiency by dynamically selecting execution environments across Vehicle, Fog, and Cloud layers based on latency, energy consumption, and workload constraints.

Key projected improvements include:

* ~35–40% reduction in latency
* ~32–38% energy savings
* ~98% anomaly detection accuracy
* Reduced handover delay
* Better fog resource utilization
* Offline operational resilience during cloud disconnection

---

## Applications

* Intelligent Transportation Systems (ITS)
* Autonomous Vehicles
* Smart Traffic Management
* Edge AI Systems
* VANET Security
* Real-Time Vehicular Analytics

---

## Future Scope

* Integration with real-time vehicular datasets
* Enhancement using advanced AI/ML optimization models
* Real-world deployment in distributed vehicular environments
* Integration with blockchain-based trust mechanisms
* 6G-enabled Vehicular Fog Computing support
* Digital Twin integration for predictive simulations

---

## Project Status

Research paper based on this framework is currently in preparation.

---

## How to Run the Project

Follow the steps below to set up and run the AI-VFC project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/swain2003/ai-vfc-project.git
cd ai-vfc-project
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

### 4. Install Required Dependencies

```bash
pip install pandas matplotlib flask
```

### 5. Run the Simulation (CLI)

```bash
python main.py
```

Simulation outputs are written to `results/` (auto-created), including:

- `metrics.txt`
- `metrics.json`
- `simulation_output.csv`
- plot images (`plot_*.png`)

### 6. Run the Dashboard (Optional)

```bash
python dashboard/app.py
```

Then open:

```text
http://localhost:5000
```

---

## Project Structure

```text
ai-vfc-project/
│
├── main.py
├── config/
├── core/
├── dashboard/
│   ├── app.py
│   └── templates/
├── data/
├── evaluation/
├── utils/
├── README.md
└── LICENSE
```

---

## Author

* Anubhaba Swain

---

## License

This project is intended for academic and research purposes.
