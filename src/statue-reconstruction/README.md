# Statue 3D Reconstruction Pipeline

Convert 30-40 images of a statue (or any object) into a complete 3D mesh model with texture, exportable to multiple formats including OpenUSD, OBJ, STL, and glTF.

## 🎯 Overview

This project implements a complete photogrammetry pipeline:
1. **Preprocessing**: Image resizing, object segmentation (YOLO)
2. **Structure from Motion (SfM)**: Camera pose estimation using COLMAP
3. **Multi-View Stereo (MVS)**: Dense 3D reconstruction
4. **Mesh Generation**: Poisson surface reconstruction
5. **Export**: Multiple formats (USD, OBJ, STL, glTF, PLY)

## 📋 Prerequisites

### System Requirements
- Python 3.8+
- 8GB+ RAM (16GB recommended)
- GPU recommended for faster processing (optional)

### External Dependencies

**COLMAP** (Required for SfM/MVS):
```bash
# Ubuntu/Debian
sudo apt-get install colmap

# macOS
brew install colmap

# Windows
# Download from: https://github.com/colmap/colmap/releases
```

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/statue-reconstruction.git
cd statue-reconstruction
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Install USD for OpenUSD export:
```bash
pip install usd-core
```

## 📁 Project Structure

```
statue-reconstruction/
├── data/
│   ├── input_images/          # Place your 30-40 images here
│   └── preprocessed/           # Processed images
├── src/
│   ├── preprocess.py          # Image preprocessing & segmentation
│   ├── sfm.py                 # Structure from Motion
│   ├── mvs.py                 # Multi-View Stereo
│   ├── mesh.py                # Mesh generation
│   └── export.py              # Export to various formats
├── output/
│   ├── sparse/                # Sparse reconstruction
│   ├── dense/                 # Dense point cloud
│   ├── mesh/                  # Generated meshes
│   └── exports/               # Final exported models
├── requirements.txt
└── README.md
```

## 🎬 Quick Start

### Step 1: Prepare Your Images

Place 30-40 images of your statue in `data/input_images/`:
- Capture from multiple angles (360° coverage)
- Maintain consistent lighting
- Avoid motion blur
- Include overlapping views (70%+ overlap)

**Tips for good captures:**
- Use a turntable or walk around the object
- Keep the camera at the same distance
- Take photos every 10-15 degrees
- Include top and bottom angles if possible

### Step 2: Run Preprocessing

```bash
python src/preprocess.py
```

This will:
- Resize images to manageable resolution
- Detect and segment the statue using YOLO
- Extract features for matching

### Step 3: Structure from Motion

```bash
python src/sfm.py
```

Creates sparse 3D point cloud and estimates camera poses.

### Step 4: Dense Reconstruction

```bash
python src/mvs.py
```

Generates dense point cloud from sparse reconstruction.

### Step 5: Mesh Generation

```bash
python src/mesh.py
```

Creates triangulated mesh from dense point cloud.

### Step 6: Export to Formats

```bash
python src/export.py
```

Exports the mesh to:
- **OBJ** - Universal format
- **STL** - 3D printing
- **PLY** - Point cloud with colors
- **glTF** - Web/AR/VR
- **USD/USDA** - OpenUSD (if installed)

## 🎨 Complete Pipeline Example

Run the entire pipeline:

```python
from pathlib import Path
from src.preprocess import ImagePreprocessor
from src.sfm import SfMPipeline
from src.mvs import MVSPipeline
from src.mesh import MeshGenerator
from src.export import MeshExporter

# 1. Preprocess
preprocessor = ImagePreprocessor("data/input_images", "data/preprocessed")
preprocessor.resize_images()
preprocessor.segment_object()

# 2. Structure from Motion
sfm = SfMPipeline("data/input_images", "output/sparse")
sfm.run_full_pipeline()

# 3. Dense Reconstruction
mvs = MVSPipeline("output/sparse", "output")
mvs.run_full_pipeline("data/input_images")

# 4. Generate Mesh
mesh_gen = MeshGenerator("output/dense", "output")
mesh_path, mesh = mesh_gen.run_full_pipeline(
    "output/dense/fused_filtered.ply",
    method="poisson"
)

# 5. Export All Formats
exporter = MeshExporter("output")
exported = exporter.export_all_formats(mesh_path, name="my_statue")
```

## 🔧 Advanced Configuration

### Customize YOLO Detection

In `src/preprocess.py`:
```python
preprocessor = ImagePreprocessor(
    input_dir="data/input_images",
    output_dir="data/preprocessed",
    model_path="yolov8n.pt"  # Options: yolov8n, yolov8s, yolov8m
)
```

### Adjust Mesh Quality

In `src/mesh.py`:
```python
mesh_gen.poisson_reconstruction(
    input_ply="...",
    depth=10,  # Higher = more detail (8-12 typical)
    scale=1.1
)
```

### Simplify Mesh for Web

```python
mesh = mesh_gen.simplify_mesh(mesh, target_triangles=50000)
```

## 📊 Expected Results

| Stage | Output | Size |
|-------|--------|------|
| Sparse Point Cloud | ~10K-50K points | <10 MB |
| Dense Point Cloud | 500K-2M points | 50-200 MB |
| Mesh (High Quality) | 500K-2M triangles | 100-500 MB |
| Mesh (Simplified) | 50K-100K triangles | 10-50 MB |

## 🐛 Troubleshooting

### COLMAP not found
```bash
# Add COLMAP to PATH
export PATH="/path/to/colmap:$PATH"
```

### Out of memory during MVS
Reduce image resolution in preprocessing:
```python
preprocessor.resize_images(max_size=1280)  # Default: 1920
```

### Mesh has holes
Try different reconstruction methods:
```python
# Instead of Poisson
mesh_gen.ball_pivoting_reconstruction(input_ply)
```

### USD export fails
Install USD Python bindings:
```bash
pip install usd-core
```

## 🎓 Learn More

- [COLMAP Documentation](https://colmap.github.io/)
- [Open3D Tutorials](http://www.open3d.org/docs/release/)
- [Photogrammetry Guide](https://en.wikipedia.org/wiki/Photogrammetry)
- [OpenUSD Documentation](https://openusd.org/)

## 📝 Citation

If you use this code in your research, please cite:

```bibtex
@software{statue_reconstruction,
  title={Statue 3D Reconstruction Pipeline},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/statue-reconstruction}
}
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- COLMAP team for photogrammetry tools
- Open3D for 3D processing
- Ultralytics for YOLO
- Pixar for OpenUSD

## 📞 Support

- Issues: [GitHub Issues](https://github.com/yourusername/statue-reconstruction/issues)
- Email: your.email@example.com

---

**Happy Reconstructing! 🗿✨**
