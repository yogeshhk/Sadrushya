# Sadrushya(सादृश्य)

**Sadrushya** is an open-source initiative focused on **Spatial Intelligence**: Macro-Spatial Intelligence (Aerial) and Micro-Spatial Intelligence (Physical AI/3D).

> *"The next frontier of AI isn't just generating text or images; it's understanding and generating the 3D physical world."* — Adapted from Fei-Fei Li's "Spatial Intelligence".

---

## Vision

Most AI work today focuses on text and 2D images.  The next valuable frontier is **AI that understands space, geometry, and the physical world**.

Sadrushya focuses only on **consulting-grade, monetizable Spatial AI domains**:

- Aerial Intelligence (Agriculture surveillance)
- 3D Scenes Intelligence (Digital Twins)
- Geometry as a Searchable Modality (2D/3D for RAG)

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

### Theme 2: Micro-Spatial Intelligence (aka Physical AI)
**Focus:** Indoor environments, 3D Geometry, and OpenUSD.
* **The "Why":** Understanding human spaces. Bridging the gap between 2D floor plans and 3D Digital Twins.
* **Key Application:** Generative design for architecture, automated 3D model retrieval (RAG for 3D), and "Text-to-Scene" agents.
* **Modality:** 2D Vectors/Sketches $\rightarrow$ 3D Geometry/USD.


## 🛠 Open Source Tech Stack (Low-Compute/Edge Focus)

| Layer | Tools & Libraries | Usage |
| :--- | :--- | :--- |
| **3D & Geometry** | **PyTorch3D**, **Kaolin** (Nvidia), **Blender**, **Open3D** | Geometric Deep Learning, Mesh processing. |
| **Scene Description** | **OpenUSD** (Universal Scene Description) | The HTML of 3D; essential for interoperability. |
| **Inference/Edge** | **Intel OpenVINO**, **ONNX Runtime** | Deploy models on standard CPUs/Laptops. |
| **Vision (2D)** | **OpenCV**, **YOLOv8** (Nano/Small) | Efficient object detection and image processing. |
| **Generative/Agents** | **LangGraph**, **Agno** | Building workflow agents for CAD/USD automation. |


## 🔗 References & Influencers
* **Fei-Fei Li:** For the vision of Spatial Intelligence.
* **NVIDIA Omniverse Team:** For OpenUSD and Industrial Digital Twins.
* **Florent Poux:** Excellent tutorials on 3D Point Cloud processing.
* **Repos to Study:** `DeepFloorplan`, `PointNet++`, `Kaolin`.


