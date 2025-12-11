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

> *"Spatial intelligence moves beyond both 1D sequences (text) and 2D images or videos by embedding AI’s understanding directly into a 3D framework. While a 2D image or video can show a visual representation of a scene, it lacks depth perception and real-world interactive capabilities. Conversely, spatial intelligence uses 3D and even 4D (adding time) contexts to build environments where AI can dynamically perceive, reason, and act. For example, current generative AI can produce realistic static images and short videos, but spatial intelligence can generate entire worlds — fully interactive, responsive environments where users can explore and manipulate objects as they would in reality. This makes it ideal for immersive gaming, education, simulation training, and virtual content creation."* by [Sanjeev Arora](https://medium.com/second-level-thinking/emerging-technology-spatial-intelligence-unlocking-3d-understanding-in-ai-d29e1c37d7c9)
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

## architecture

![Spatial Computing Stack](./references/SpatialComputingStack.png) by [Nokia](https://www.nokia.com/innovation/technology-vision/on-the-road-to-spatial-computing/)

At its foundation, the physical world (represented in green), encompasses humans, machines, robots, objects, and places, supported by existing enablers (light purple) such as networks, storage, compute resources, and AI/ML capabilities. The framework introduces five crucial new enabling technologies (dark purple): spatial user interfaces, mapping and localization systems, reality modeling and simulation tools, spatial data and contents, and content enablement services. These components work together to create a robust foundation for spatial computing applications.

This technology stack can be applied in consumer, enterprise and industrial applications using the enabling technologies differently to create unique solutions and experiences. How these new enablers function and interact impacts future network requirements and capabilities, as they introduce new demands and opportunities for network infrastructure and services.

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
* **Geo-Intel Lab:** [Geospatial Intelligence](https://geo.intel.iittnif.com/), Remote Sensing, GNSS, PNT, Digital Twins, and AI-powered decision systems.
* [With Spatial Intelligence, AI Will Understand the Real World | Fei-Fei Li | TED](https://www.youtube.com/watch?v=y8NtMZ7VGmU)
* [“The Future of AI is Here” — Fei-Fei Li Unveils the Next Frontier of AI](https://www.youtube.com/watch?v=vIXfYFB7aBI)
* [Fei-Fei Li: Spatial Intelligence is the Next Frontier in AI](https://www.youtube.com/watch?v=_PioN-CpOP0)
* [The Godmother of AI on jobs, robots & why world models are next | Dr. Fei-Fei Li](https://www.youtube.com/watch?v=Ctjiatnd6Xk)
* **Justin Johnson:** Researcher
* **Ben Mildenhall:** Researcher
* **Christoph Lassner:** Researcher in 3D and 4D perception
* **Matthew Tancik:** Head of Applied Research at Luma AI

