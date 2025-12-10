# Sadrushya

**Sadrushya** (सादृश्य, meaning *similar to the scene*) is an open-source initiative in the domain of **Spatial Intelligence**. Our goal is to build tools, libraries, and applications that empower developers, researchers, and creators to generate, manipulate, and interact with 3D scenes using cutting-edge AI, ML, and generative technologies.

**Two high-impact, future-proof themes**: **Macro-Spatial Intelligence** (Aerial) and **Micro-Spatial Intelligence** (Physical AI/3D).

This approach bridges the gap between today's 2D computer vision and tomorrow's 3D generative world, focusing on "Spatial Intelligence" — a concept championed by visionaries like Fei-Fei Li—while respecting your constraint for manageable compute requirements.

## Personally
- This repository outlines a transition strategy for a Gen AI consultant moving into **Spatial Intelligence**. Unlike the saturated LLM market, this domain applies AI to **geometry, 3D space, and physical understanding**.


**Transitioning from NLP to the Physical World**

*> "Build for the world that is coming (3D/Spatial), not the world that is already here (2D Text)."*

> *"The next frontier of AI isn't just generating text or images; it's understanding and generating the 3D physical world."* — Adapted from Fei-Fei Li's "Spatial Intelligence".

**Why this domain?**
* **Unsaturated Market:** High demand in "Real World AI" (Robotics, Digital Twins, Agriculture, Defense) vs. generic Chatbots.
* **Compute Efficient:** Relies on **Geometric Deep Learning** and **Edge Inference** (OpenVINO, TinyML) rather than massive GPU clusters required for training LLMs.
* **Global & Local Potential:** Massive scope in India (AgriTech, Infrastructure) and globally (Metaverse, Architecture/AEC).

---

## 🏗 Core Themes

I have consolidated your thoughts into two primary pillars. Focus deeply on these 2; discard scattered interests.

### Theme 1: Macro-Spatial Intelligence (Project *Shyenakshi*)
**Focus:** Aerial, Drone, and Satellite Imagery.
* **The "Why":** Analyzing the world from above. Critical for Agriculture (India's backbone), Defense, and Urban Planning.
* **Key Application:** Converting raw aerial data into actionable insights (Crop health, vehicle detection, land usage).
* **Modality:** 2D High-Res Images $\rightarrow$ Geo-tagged Insights.

### Theme 2: Micro-Spatial & Physical AI (Project *Sadrushya*)
**Focus:** Indoor environments, 3D Geometry, and OpenUSD.
* **The "Why":** Understanding human spaces. Bridging the gap between 2D floor plans and 3D Digital Twins.
* **Key Application:** Generative design for architecture, automated 3D model retrieval (RAG for 3D), and "Text-to-Scene" agents.
* **Modality:** 2D Vectors/Sketches $\rightarrow$ 3D Geometry/USD.

---

## 🛠 Open Source Tech Stack (Low-Compute/Edge Focus)

To operate as an individual consultant without an A100 cluster, rely on inference optimization and geometric libraries.

| Layer | Tools & Libraries | Usage |
| :--- | :--- | :--- |
| **3D & Geometry** | **PyTorch3D**, **Kaolin** (Nvidia), **Open3D** | Geometric Deep Learning, Mesh processing. |
| **Scene Description** | **OpenUSD** (Universal Scene Description) | The HTML of 3D; essential for interoperability. |
| **Inference/Edge** | **Intel OpenVINO**, **ONNX Runtime** | Deploy models on standard CPUs/Laptops. |
| **Vision (2D)** | **OpenCV**, **YOLOv8** (Nano/Small) | Efficient object detection and image processing. |
| **Generative/Agents** | **LangGraph**, **Agno** | Building workflow agents for CAD/USD automation. |

---

## 🚀 Concrete Projects to Build

Build these three portfolio projects to demonstrate expertise.

### Project A: The "Hawk-Eye" Ag-Bot (Aerial)
*From `Notes_Shyenakshi.md`*
* **Goal:** A lightweight tool to detect crop diseases or count assets in drone imagery.
* **Technique:** Fine-tune a lightweight **YOLOv8** or **SegFormer** on aerial datasets.
* **Edge Twist:** Optimize the model using **OpenVINO** to run on a standard laptop or Drone onboard computer (e.g., Raspberry Pi/Jetson).
* **Monetization:** API for local ag-consultancies or solar farm inspectors.

### Project B: "FloorPlan-to-Twin" Generator (Indoor)
*From `Notes_FloorPlan.md`*
* **Goal:** Convert a 2D image of a floor plan into a basic 3D USD (Universal Scene Description) model.
* **Technique:** 1.  **Vectorization:** Use OpenCV/DeepFloorplan to extract walls/windows as vectors.
    2.  **Extrusion:** algorithmically lift 2D vectors to 3D meshes.
    3.  **GenAI:** Use Stable Diffusion to apply textures to the 3D surfaces.
* **Monetization:** Micro-SaaS for Real Estate agents (Virtual Staging).

### Project C: Geometric RAG Agent (Generative 3D)
*From `Notes_PhysicalAI.md` & `Notes_GeometryAsNewModality.md`*
* **Goal:** A "Copilot" for 3D designers. User asks: *"Give me a modern chair with wooden legs"*.
* **Technique:** 1.  **Database:** Index a free 3D dataset (like Objaverse) using **PointNet** embeddings (geometry) + CLIP embeddings (text).
    2.  **Retrieval:** Retrieve the best matching 3D asset.
    3.  **Format:** Return the result as an OpenUSD file.
* **Monetization:** Plugin for Blender or NVIDIA Omniverse.

---

## 📚 Learning Plan & Resources

### 1. Fundamentals (Weeks 1-4)
* **Course:** [Deep Learning on Point Clouds (PointNet)](http://stanford.edu/~rqi/pointnet/)
* **Read:** *Geometric Deep Learning* (Bronstein et al.) - [Link](https://geometricdeeplearning.com/)
* **Skill:** Master **Numpy** and **Linear Algebra** (Quaternions, Matrices) – this is more important here than in NLP.

### 2. Domain Specialization (Weeks 5-8)
* **Aerial:** [Satellite Imagery Deep Learning](https://www.youtube.com/playlist?list=PLvz5lCwTgdXDNcXEVwwHsb9DwjNXZGsoy) (DigitalSreeni/DeepWorks).
* **OpenUSD:** [NVIDIA USD Resources](https://developer.nvidia.com/usd) – Learn to manipulate 3D scenes via Python code.

### 3. Emerging Tech (Weeks 9+)
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

## 🔮 Future Consultant Monetization Strategy

1.  **Specific Knowledge:** Position yourself not as a "GenAI Expert" (too broad), but as a **"Spatial Data Strategist"**.
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


