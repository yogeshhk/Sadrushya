# Sadrushya(सादृश्य)

**Sadrushya** is an open-source initiative focused on **Spatial AI for real-world intelligence**, designed for independent consultants and researchers who want to work in **high-value, low-compute AI domains**.

This repository documents a **domain transition roadmap** for moving from generic GenAI/LLMs into **geometry-centric, spatial intelligence consulting**.

**Two high-impact, future-proof themes**: **Macro-Spatial Intelligence** (Aerial) and **Micro-Spatial Intelligence** (Physical AI/3D).

This approach bridges the gap between today's 2D computer vision and tomorrow's 3D generative world, focusing on "Spatial Intelligence", a concept championed by visionaries like Fei-Fei Li.

> *"The next frontier of AI isn't just generating text or images; it's understanding and generating the 3D physical world."* — Adapted from Fei-Fei Li's "Spatial Intelligence".

---

## Vision

Most AI work today focuses on text and 2D images.  
The next valuable frontier is **AI that understands space, geometry, and the physical world**.

Sadrushya focuses only on **consulting-grade, monetizable Spatial AI domains**:

- Aerial Intelligence (agriculture, infrastructure, surveillance)
- Built Environment Intelligence (floorplans → 3D → digital twins)
- Geometry as a Searchable Modality (3D retrieval/RAG)

This direction is practical, future-proof, and suitable for **solo consultants without heavy GPU dependency**.

---

## Positioning

This project positions the author as:

**“Spatial AI Consultant for Aerial Intelligence and Digital Twin Automation using Lightweight Geometry AI.”**

This niche is:
- Rare
- High-demand
- Compute-efficient
- Strongly relevant for **India + global markets**

---

## Personally
This repository outlines a transition strategy for a Gen AI consultant moving into **Spatial Intelligence**. Unlike the saturated LLM market, this domain applies AI to **geometry, 3D space, and physical understanding**.


**Why this domain?**
* **Unsaturated Market:** High demand in "Real World AI" (Robotics, Digital Twins, Agriculture, Defense) vs. generic Chatbots.
* **Compute Efficient:** Relies on **Geometric Deep Learning** and **Edge Inference** (OpenVINO, TinyML) rather than massive GPU clusters required for training LLMs.
* **Global & Local Potential:** Massive scope in India (AgriTech, Infrastructure) and globally (Metaverse, Architecture/AEC).

---

## 🏗 Core Themes

### Theme 1: Macro-Spatial Intelligence 
**Focus:** Aerial, Drone, and Satellite Imagery.
* **The "Why":** Analyzing the world from above. Critical for Agriculture (India's backbone), Defense, and Urban Planning.
* **Key Application:** Converting raw aerial data into actionable insights (Crop health, vehicle detection, land usage).
* **Modality:** 2D High-Res Images $\rightarrow$ Geo-tagged Insights.

### Theme 2: Micro-Spatial & Physical AI 
**Focus:** Indoor environments, 3D Geometry, and OpenUSD.
* **The "Why":** Understanding human spaces. Bridging the gap between 2D floor plans and 3D Digital Twins.
* **Key Application:** Generative design for architecture, automated 3D model retrieval (RAG for 3D), and "Text-to-Scene" agents.
* **Modality:** 2D Vectors/Sketches $\rightarrow$ 3D Geometry/USD.

---

## Core Consulting Themes (Focused & Prioritized)

### 1. Aerial Spatial Intelligence

**Problem Solved**
- Extract insights from satellite and drone data.

**Real-World Clients**
- Agriculture firms
- Solar plant inspectors
- Smart city planners
- Defense & surveillance contractors

**Typical Outcomes**
- Crop stress maps
- Object detection (vehicles, encroachments)
- Land-use classification

**Modalities**
- 2D high-resolution aerial imagery → geo-tagged insights

---

### 2. Floorplan → 3D Digital Twin Automation

**Problem Solved**
- Manual creation of 3D models from 2D architectural plans is slow and expensive.

**Real-World Clients**
- Real-estate platforms
- Architecture studios
- Property surveyors

**Typical Outcomes**
- Auto-generated 3D models from floorplans
- Virtual staging pipelines

**Modalities**
- 2D vector drawings → 3D meshes → OpenUSD scenes

---

### 3. Geometry RAG (3D Retrieval Systems)

**Problem Solved**
- Designers and engineers struggle to reuse 3D assets efficiently.

**Real-World Clients**
- Product designers
- CAD/BIM firms
- Game asset studios

**Typical Outcomes**
- “Search by shape” engines
- Text → 3D asset retrieval

**Modalities**
- Point clouds + mesh embeddings + text embeddings

---

## Consulting-Oriented Use Cases

| Client Type | Consulting Deliverables |
|-------------|--------------------------|
| AgriTech firms | Crop health APIs |
| Smart city teams | Aerial analytics dashboards |
| Real estate portals | Floorplan-to-3D automations |
| AEC firms | Lightweight digital twins |
| Manufacturing | 3D asset retrieval assistants |

---

## 🛠 Open Source Tech Stack (Low-Compute/Edge Focus)

| Layer | Tools & Libraries | Usage |
| :--- | :--- | :--- |
| **3D & Geometry** | **PyTorch3D**, **Kaolin** (Nvidia), **Open3D** | Geometric Deep Learning, Mesh processing. |
| **Scene Description** | **OpenUSD** (Universal Scene Description) | The HTML of 3D; essential for interoperability. |
| **Inference/Edge** | **Intel OpenVINO**, **ONNX Runtime** | Deploy models on standard CPUs/Laptops. |
| **Vision (2D)** | **OpenCV**, **YOLOv8** (Nano/Small) | Efficient object detection and image processing. |
| **Generative/Agents** | **LangGraph**, **Agno** | Building workflow agents for CAD/USD automation. |

---

## 🚀 Concrete Projects to Build

Build these portfolio projects to demonstrate expertise.
### Project 1: Drone → Crop Health Analyzer

**Goal**
Detect crop stress, count objects, and generate health heatmaps.

**Stack**
- YOLOv8-nano
- OpenCV
- OpenVINO

**Datasets**
- DOTA
- xView
- PlantVillage

**Deliverable**
- REST API + dashboard

---

### Project 2: Floorplan → 3D Digital Twin Generator

**Goal**
Convert 2D plans into 3D OpenUSD scenes.

**Pipeline**
1. OpenCV vector extraction
2. Mesh generation using Open3D/PyTorch3D
3. Export to OpenUSD

**Datasets**
- CubiCasa5k
- RPLAN

**Deliverable**
- CLI + Web viewer demo

---

### Project 3: Geometry RAG System

**Goal**
Build a search engine for 3D shapes.

**Stack**
- PointNet / PointNet++
- FAISS
- CLIP

**Datasets**
- Objaverse
- ShapeNet

**Deliverable**
- Query API + embedding visualizer

---

## Benchmarking & Metrics

Each project must track:

- Inference time (CPU)
- Model size (MB)
- Accuracy (mAP / IoU)
- Latency after OpenVINO optimization

This makes the work **consulting-grade** instead of academic-only.

---

## 📚 Learning Plan & Resources

### 1. Fundamentals 
* **Course:** [Deep Learning on Point Clouds (PointNet)](http://stanford.edu/~rqi/pointnet/)
* **Read:** *Geometric Deep Learning* (Bronstein et al.) - [Link](https://geometricdeeplearning.com/)
* **Skill:** Master **Numpy** and **Linear Algebra** (Quaternions, Matrices) – this is more important here than in NLP.

### 2. Domain Specialization 
* **Aerial:** [Satellite Imagery Deep Learning](https://www.youtube.com/playlist?list=PLvz5lCwTgdXDNcXEVwwHsb9DwjNXZGsoy) (DigitalSreeni/DeepWorks).
* **OpenUSD:** [NVIDIA USD Resources](https://developer.nvidia.com/usd) – Learn to manipulate 3D scenes via Python code.

### 3. Emerging Tech 
* **Read:** *Spatial Intelligence* (Fei-Fei Li's recent talks).
* **Tool:** Explore **NVIDIA Omniverse** (Digital Twin platform).

---

## 📂 Recommended Datasets

| Domain | Dataset Name | Description |
| :--- | :--- | :--- |
| **Indoor/3D** | **CubiCasa5k** | Large-scale floorplan image dataset. |
| **Indoor/3D** | **Objaverse** | Massive dataset of 3D objects (great for RAG). |
| **Aerial** | **DOTA / xView** | Large-scale datasets for object detection in aerial images. |
| **Agriculture** | **Plant Village** | Crop disease classification. |

---
## Who This Repository Is For

- Independent consultants
- Applied researchers
- Engineers shifting from generic LLM work
- Practitioners who want **real-world, monetizable AI skills**

---

## Philosophy

This project deliberately avoids:
- Generic LLM wrappers
- GPU-heavy pipelines
- Research-only prototypes

The focus is:
**Real geometry, real deployment, real consulting value.**

---

## 🔮 Future ...

1.  **Specific Knowledge** **"Spatial Data Strategist"**.
2.  **Services:**
    * **Custom RAG for Engineering:** "Chat with your CAD files/Blueprints".
    * **Automated Inspection Pipelines:** Drone footage analysis pipelines for infrastructure.
3.  **Passive Income:** API for "Image to Floorplan" conversion or "Crop Health Heatmap" generation.

---

## 🔗 References & Influencers
* **Fei-Fei Li:** For the vision of Spatial Intelligence.
* **NVIDIA Omniverse Team:** For OpenUSD and Industrial Digital Twins.
* **Florent Poux:** Excellent tutorials on 3D Point Cloud processing.
* **Repos to Study:** `DeepFloorplan`, `PointNet++`, `Kaolin`.


