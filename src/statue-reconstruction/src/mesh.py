"""
Mesh Generation and Texturing
Converts dense point cloud to textured mesh
"""

import subprocess
import logging
from pathlib import Path
import open3d as o3d
import numpy as np
import trimesh

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MeshGenerator:
    def __init__(self, dense_dir, output_dir):
        """
        Initialize mesh generator
        
        Args:
            dense_dir: Directory with dense point cloud
            output_dir: Directory for mesh output
        """
        self.dense_dir = Path(dense_dir)
        self.output_dir = Path(output_dir)
        self.mesh_dir = self.output_dir / "mesh"
        self.mesh_dir.mkdir(parents=True, exist_ok=True)
    
    def poisson_reconstruction(self, input_ply, depth=9, scale=1.1):
        """
        Poisson surface reconstruction
        
        Args:
            input_ply: Input point cloud file
            depth: Octree depth (higher = more detail, 8-12 typical)
            scale: Scale factor for reconstruction
        """
        logger.info("Running Poisson surface reconstruction...")
        
        # Load point cloud
        pcd = o3d.io.read_point_cloud(str(input_ply))
        
        # Estimate normals if not present
        if not pcd.has_normals():
            logger.info("Computing normals...")
            pcd.estimate_normals(
                search_param=o3d.geometry.KDTreeSearchParamHybrid(
                    radius=0.1, max_nn=30
                )
            )
            pcd.orient_normals_consistent_tangent_plane(k=15)
        
        # Poisson reconstruction
        logger.info(f"Reconstructing mesh (depth={depth})...")
        mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
            pcd, depth=depth, scale=scale
        )
        
        # Remove low-density vertices
        vertices_to_remove = densities < np.quantile(densities, 0.01)
        mesh.remove_vertices_by_mask(vertices_to_remove)
        
        logger.info(f"Mesh created: {len(mesh.vertices)} vertices, {len(mesh.triangles)} triangles")
        
        # Save mesh
        output_mesh = self.mesh_dir / "poisson_mesh.ply"
        o3d.io.write_triangle_mesh(str(output_mesh), mesh)
        logger.info(f"Mesh saved: {output_mesh}")
        
        return output_mesh, mesh
    
    def ball_pivoting_reconstruction(self, input_ply, radii=[0.005, 0.01, 0.02, 0.04]):
        """
        Ball-pivoting algorithm for mesh reconstruction
        
        Args:
            input_ply: Input point cloud file
            radii: List of ball radii for reconstruction
        """
        logger.info("Running Ball-Pivoting reconstruction...")
        
        # Load point cloud
        pcd = o3d.io.read_point_cloud(str(input_ply))
        
        # Estimate normals if not present
        if not pcd.has_normals():
            pcd.estimate_normals(
                search_param=o3d.geometry.KDTreeSearchParamHybrid(
                    radius=0.1, max_nn=30
                )
            )
        
        # Ball pivoting
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
            pcd,
            o3d.utility.DoubleVector(radii)
        )
        
        logger.info(f"Mesh created: {len(mesh.vertices)} vertices, {len(mesh.triangles)} triangles")
        
        # Save mesh
        output_mesh = self.mesh_dir / "ball_pivot_mesh.ply"
        o3d.io.write_triangle_mesh(str(output_mesh), mesh)
        logger.info(f"Mesh saved: {output_mesh}")
        
        return output_mesh, mesh
    
    def clean_mesh(self, mesh, remove_duplicates=True, remove_degenerate=True,
                   remove_unreferenced=True, cluster_connected=True):
        """
        Clean and optimize mesh
        
        Args:
            mesh: Open3D TriangleMesh object
            remove_duplicates: Remove duplicate vertices and triangles
            remove_degenerate: Remove degenerate triangles
            remove_unreferenced: Remove unreferenced vertices
            cluster_connected: Keep only largest connected component
        """
        logger.info("Cleaning mesh...")
        
        if remove_duplicates:
            mesh.remove_duplicated_vertices()
            mesh.remove_duplicated_triangles()
        
        if remove_degenerate:
            mesh.remove_degenerate_triangles()
        
        if remove_unreferenced:
            mesh.remove_unreferenced_vertices()
        
        if cluster_connected:
            triangle_clusters, cluster_n_triangles, cluster_area = (
                mesh.cluster_connected_triangles()
            )
            triangle_clusters = np.asarray(triangle_clusters)
            cluster_n_triangles = np.asarray(cluster_n_triangles)
            
            # Keep largest cluster
            largest_cluster_idx = cluster_n_triangles.argmax()
            triangles_to_remove = triangle_clusters != largest_cluster_idx
            mesh.remove_triangles_by_mask(triangles_to_remove)
        
        logger.info(f"Cleaned mesh: {len(mesh.vertices)} vertices, {len(mesh.triangles)} triangles")
        return mesh
    
    def simplify_mesh(self, mesh, target_triangles=50000):
        """
        Simplify mesh by reducing triangle count
        
        Args:
            mesh: Open3D TriangleMesh object
            target_triangles: Target number of triangles
        """
        logger.info(f"Simplifying mesh to ~{target_triangles} triangles...")
        
        simplified_mesh = mesh.simplify_quadric_decimation(
            target_number_of_triangles=target_triangles
        )
        
        logger.info(f"Simplified: {len(simplified_mesh.triangles)} triangles")
        return simplified_mesh
    
    def smooth_mesh(self, mesh, iterations=5):
        """
        Smooth mesh using Laplacian smoothing
        
        Args:
            mesh: Open3D TriangleMesh object
            iterations: Number of smoothing iterations
        """
        logger.info(f"Smoothing mesh ({iterations} iterations)...")
        
        smoothed_mesh = mesh.filter_smooth_laplacian(
            number_of_iterations=iterations
        )
        
        return smoothed_mesh
    
    def texture_mesh_from_colmap(self, mesh_path, colmap_path="colmap"):
        """
        Apply texture to mesh using COLMAP's delaunay mesher
        
        Args:
            mesh_path: Path to input mesh
            colmap_path: Path to COLMAP executable
        """
        logger.info("Texturing mesh with COLMAP...")
        
        # This requires running COLMAP's delaunay_mesher
        # For now, we'll use a simplified approach
        logger.warning("Full COLMAP texturing requires additional setup")
        logger.info("Using vertex colors from point cloud instead")
        
        return mesh_path
    
    def visualize_mesh(self, mesh, show_wireframe=False):
        """Visualize mesh using Open3D"""
        logger.info("Visualizing mesh...")
        
        # Compute vertex normals for better lighting
        mesh.compute_vertex_normals()
        
        if show_wireframe:
            o3d.visualization.draw_geometries(
                [mesh],
                mesh_show_wireframe=True,
                window_name="Mesh"
            )
        else:
            o3d.visualization.draw_geometries(
                [mesh],
                window_name="Mesh"
            )
    
    def convert_to_trimesh(self, o3d_mesh):
        """Convert Open3D mesh to Trimesh for advanced operations"""
        vertices = np.asarray(o3d_mesh.vertices)
        triangles = np.asarray(o3d_mesh.triangles)
        
        mesh = trimesh.Trimesh(vertices=vertices, faces=triangles)
        return mesh
    
    def run_full_pipeline(self, input_ply, method="poisson", 
                         simplify=True, visualize=False):
        """
        Run complete mesh generation pipeline
        
        Args:
            input_ply: Input point cloud file
            method: 'poisson' or 'ball_pivoting'
            simplify: Whether to simplify mesh
            visualize: Whether to visualize result
        """
        logger.info("Starting mesh generation pipeline...")
        
        # Step 1: Generate mesh
        if method == "poisson":
            mesh_path, mesh = self.poisson_reconstruction(input_ply)
        elif method == "ball_pivoting":
            mesh_path, mesh = self.ball_pivoting_reconstruction(input_ply)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Step 2: Clean mesh
        mesh = self.clean_mesh(mesh)
        
        # Step 3: Simplify (optional)
        if simplify:
            mesh = self.simplify_mesh(mesh, target_triangles=100000)
        
        # Step 4: Smooth
        mesh = self.smooth_mesh(mesh, iterations=3)
        
        # Step 5: Save final mesh
        final_mesh = self.mesh_dir / f"final_mesh_{method}.ply"
        o3d.io.write_triangle_mesh(str(final_mesh), mesh)
        logger.info(f"Final mesh saved: {final_mesh}")
        
        # Step 6: Visualize (optional)
        if visualize:
            self.visualize_mesh(mesh)
        
        logger.info("Mesh generation complete!")
        return final_mesh, mesh


def main():
    """Example usage"""
    mesh_gen = MeshGenerator(
        dense_dir="output/dense",
        output_dir="output"
    )
    
    try:
        # Generate mesh using Poisson reconstruction
        final_mesh, mesh = mesh_gen.run_full_pipeline(
            input_ply="output/dense/fused_filtered.ply",
            method="poisson",
            simplify=True,
            visualize=True
        )
        
        logger.info(f"Final mesh: {final_mesh}")
        
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    main()
