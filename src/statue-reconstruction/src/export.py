"""
Export 3D Models to Various Formats
Supports OpenUSD, OBJ, STL, FBX, and more
"""

import logging
from pathlib import Path
import open3d as o3d
import trimesh
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MeshExporter:
    def __init__(self, output_dir):
        """
        Initialize mesh exporter
        
        Args:
            output_dir: Directory for exported files
        """
        self.output_dir = Path(output_dir)
        self.export_dir = self.output_dir / "exports"
        self.export_dir.mkdir(parents=True, exist_ok=True)
    
    def load_mesh(self, mesh_path):
        """Load mesh from file"""
        logger.info(f"Loading mesh from {mesh_path}")
        mesh = o3d.io.read_triangle_mesh(str(mesh_path))
        return mesh
    
    def export_obj(self, mesh, name="model"):
        """
        Export to OBJ format (Wavefront)
        Most widely supported format
        """
        output_path = self.export_dir / f"{name}.obj"
        
        # Open3D export
        o3d.io.write_triangle_mesh(str(output_path), mesh)
        
        logger.info(f"Exported OBJ: {output_path}")
        return output_path
    
    def export_stl(self, mesh, name="model", binary=True):
        """
        Export to STL format (3D printing)
        
        Args:
            mesh: Open3D mesh
            name: Output filename
            binary: Use binary format (True) or ASCII (False)
        """
        output_path = self.export_dir / f"{name}.stl"
        
        # Convert to trimesh for STL export
        vertices = np.asarray(mesh.vertices)
        triangles = np.asarray(mesh.triangles)
        tmesh = trimesh.Trimesh(vertices=vertices, faces=triangles)
        
        # Export
        tmesh.export(str(output_path), file_type='stl')
        
        logger.info(f"Exported STL: {output_path}")
        return output_path
    
    def export_ply(self, mesh, name="model"):
        """
        Export to PLY format
        Good for preserving vertex colors
        """
        output_path = self.export_dir / f"{name}.ply"
        
        o3d.io.write_triangle_mesh(str(output_path), mesh)
        
        logger.info(f"Exported PLY: {output_path}")
        return output_path
    
    def export_gltf(self, mesh, name="model"):
        """
        Export to glTF format (web-friendly)
        Used for Three.js, WebGL, etc.
        """
        output_path = self.export_dir / f"{name}.gltf"
        
        # Convert to trimesh
        vertices = np.asarray(mesh.vertices)
        triangles = np.asarray(mesh.triangles)
        tmesh = trimesh.Trimesh(vertices=vertices, faces=triangles)
        
        # Export
        tmesh.export(str(output_path), file_type='gltf')
        
        logger.info(f"Exported glTF: {output_path}")
        return output_path
    
    def export_usd(self, mesh, name="model"):
        """
        Export to OpenUSD format
        Requires pxr (USD Python bindings)
        """
        try:
            from pxr import Usd, UsdGeom, Vt, Gf
            
            output_path = self.export_dir / f"{name}.usd"
            
            # Create USD stage
            stage = Usd.Stage.CreateNew(str(output_path))
            
            # Create mesh
            mesh_path = f"/World/{name}"
            usd_mesh = UsdGeom.Mesh.Define(stage, mesh_path)
            
            # Set vertices
            vertices = np.asarray(mesh.vertices)
            vertex_list = [Gf.Vec3f(v[0], v[1], v[2]) for v in vertices]
            usd_mesh.CreatePointsAttr().Set(vertex_list)
            
            # Set face indices
            triangles = np.asarray(mesh.triangles).flatten()
            usd_mesh.CreateFaceVertexIndicesAttr().Set(triangles)
            
            # Set face vertex counts (all triangles)
            face_counts = [3] * len(mesh.triangles)
            usd_mesh.CreateFaceVertexCountsAttr().Set(face_counts)
            
            # Add vertex colors if available
            if mesh.has_vertex_colors():
                colors = np.asarray(mesh.vertex_colors)
                color_list = [Gf.Vec3f(c[0], c[1], c[2]) for c in colors]
                color_attr = usd_mesh.CreateDisplayColorPrimvar(UsdGeom.Tokens.vertex)
                color_attr.Set(color_list)
            
            # Save stage
            stage.Save()
            
            logger.info(f"Exported USD: {output_path}")
            return output_path
            
        except ImportError:
            logger.error("USD Python bindings not installed")
            logger.error("Install with: pip install usd-core")
            return None
    
    def export_usda(self, mesh, name="model"):
        """
        Export to USDA format (ASCII USD)
        Human-readable USD format
        """
        try:
            from pxr import Usd, UsdGeom, Vt, Gf
            
            output_path = self.export_dir / f"{name}.usda"
            
            # Create USD stage (ASCII format)
            stage = Usd.Stage.CreateNew(str(output_path))
            
            # Create mesh
            mesh_path = f"/World/{name}"
            usd_mesh = UsdGeom.Mesh.Define(stage, mesh_path)
            
            # Set geometry
            vertices = np.asarray(mesh.vertices)
            vertex_list = [Gf.Vec3f(v[0], v[1], v[2]) for v in vertices]
            usd_mesh.CreatePointsAttr().Set(vertex_list)
            
            triangles = np.asarray(mesh.triangles).flatten()
            usd_mesh.CreateFaceVertexIndicesAttr().Set(triangles)
            
            face_counts = [3] * len(mesh.triangles)
            usd_mesh.CreateFaceVertexCountsAttr().Set(face_counts)
            
            # Save
            stage.Save()
            
            logger.info(f"Exported USDA: {output_path}")
            return output_path
            
        except ImportError:
            logger.error("USD Python bindings not installed")
            return None
    
    def export_off(self, mesh, name="model"):
        """
        Export to OFF format (Object File Format)
        Simple format for geometry exchange
        """
        output_path = self.export_dir / f"{name}.off"
        
        vertices = np.asarray(mesh.vertices)
        triangles = np.asarray(mesh.triangles)
        
        with open(output_path, 'w') as f:
            f.write("OFF\n")
            f.write(f"{len(vertices)} {len(triangles)} 0\n")
            
            # Write vertices
            for v in vertices:
                f.write(f"{v[0]} {v[1]} {v[2]}\n")
            
            # Write faces
            for t in triangles:
                f.write(f"3 {t[0]} {t[1]} {t[2]}\n")
        
        logger.info(f"Exported OFF: {output_path}")
        return output_path
    
    def export_all_formats(self, mesh_path, name="model"):
        """
        Export to all supported formats
        
        Args:
            mesh_path: Input mesh file path
            name: Base name for exported files
        """
        logger.info("Exporting to all formats...")
        
        # Load mesh
        mesh = self.load_mesh(mesh_path)
        
        exported_files = {}
        
        # Export to each format
        exported_files['obj'] = self.export_obj(mesh, name)
        exported_files['stl'] = self.export_stl(mesh, name)
        exported_files['ply'] = self.export_ply(mesh, name)
        exported_files['gltf'] = self.export_gltf(mesh, name)
        exported_files['off'] = self.export_off(mesh, name)
        
        # Try USD formats
        usd_path = self.export_usd(mesh, name)
        if usd_path:
            exported_files['usd'] = usd_path
        
        usda_path = self.export_usda(mesh, name)
        if usda_path:
            exported_files['usda'] = usda_path
        
        logger.info(f"Exported {len(exported_files)} formats")
        return exported_files
    
    def create_web_viewer_html(self, gltf_path, name="model"):
        """
        Create HTML viewer for web visualization using Three.js
        """
        html_path = self.export_dir / f"{name}_viewer.html"
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Model Viewer - {name}</title>
    <style>
        body {{ margin: 0; overflow: hidden; }}
        canvas {{ display: block; }}
        #info {{
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-family: Arial;
            background: rgba(0,0,0,0.5);
            padding: 10px;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div id="info">
        <h3>{name}</h3>
        <p>Drag to rotate | Scroll to zoom</p>
    </div>
    <script type="module">
        import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.150.0/build/three.module.js';
        import {{ GLTFLoader }} from 'https://cdn.jsdelivr.net/npm/three@0.150.0/examples/jsm/loaders/GLTFLoader.js';
        import {{ OrbitControls }} from 'https://cdn.jsdelivr.net/npm/three@0.150.0/examples/jsm/controls/OrbitControls.js';

        // Scene setup
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x1a1a1a);

        // Camera
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 5;

        // Renderer
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Controls
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        // Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(5, 5, 5);
        scene.add(directionalLight);

        // Load model
        const loader = new GLTFLoader();
        loader.load('{gltf_path.name}', (gltf) => {{
            scene.add(gltf.scene);
            
            // Center model
            const box = new THREE.Box3().setFromObject(gltf.scene);
            const center = box.getCenter(new THREE.Vector3());
            gltf.scene.position.sub(center);
            
            // Adjust camera
            const size = box.getSize(new THREE.Vector3());
            const maxDim = Math.max(size.x, size.y, size.z);
            camera.position.z = maxDim * 2;
        }}, undefined, (error) => {{
            console.error('Error loading model:', error);
        }});

        // Animation loop
        function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }}
        animate();

        // Handle window resize
        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
    </script>
</body>
</html>"""
        
        with open(html_path, 'w') as f:
            f.write(html_content)
        
        logger.info(f"Created web viewer: {html_path}")
        return html_path


def main():
    """Example usage"""
    exporter = MeshExporter(output_dir="output")
    
    try:
        # Export all formats
        mesh_path = "output/mesh/final_mesh_poisson.ply"
        exported = exporter.export_all_formats(mesh_path, name="statue")
        
        logger.info("\nExported files:")
        for fmt, path in exported.items():
            logger.info(f"  {fmt.upper()}: {path}")
        
        # Create web viewer
        if 'gltf' in exported:
            viewer = exporter.create_web_viewer_html(exported['gltf'], name="statue")
            logger.info(f"\nOpen {viewer} in a web browser to view the model")
        
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    main()
