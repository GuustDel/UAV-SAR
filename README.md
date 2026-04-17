# UAV-SAR: Multi-Agent Search & Rescue System

## Overview

This project explores a **decentralized multi-agent approach** to UAV-based **Search and Rescue (SAR)**.

The focus is on combining:

* **Swarm intelligence (ACO-inspired coordination)**
* **Agent-based decision-making (BDI principles)**

The goal is to study how multiple agents can coordinate efficiently without central control.

---

## Core Idea

Agents interact through a **shared environment** using:

* attraction to potential targets
* repulsion to avoid overlapping search

This enables emergent coordination and distributed exploration.

---

## Agent Behaviour

Each agent follows a general lifecycle:

* **Explore**: search the environment
* **Exploit**: investigate potential targets
* **Return**: manage resources (e.g. battery)
* **Adapt**: adjust behaviour under changing conditions

This reflects an exploration–exploitation trade-off in a dynamic environment. 
