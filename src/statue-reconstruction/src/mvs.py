"""
Multi-View Stereo (MVS) - Dense 3D Reconstruction
Converts sparse point cloud to dense point cloud
"""

import subprocess
import logging
from pathlib import Path
import open3d as o3d
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MVSPipeline:
    def __init__(self, sparse_dir, output_dir, colmap_path="colmap"):
        """
        Initialize MVS pipeline
        
        Args:
            sparse_dir: Directory with sparse reconstruction
            output_dir: Directory for dense output
            colmap_path: Path to COLMAP executable
        """
        self.sparse_dir = Path(sparse_dir)
        self.output_dir = Path(output_dir)
        self.dense_dir = self.output_dir / "dense"
        self.colmap_path = colmap_path
        
        self.dense_dir.mkdir(parents=True, exist_ok=True)
    
    def image_undistortion(self, image_dir):
        """
        Undistort images based on camera parameters
        
        Args:
            image_dir: Directory with original images
        """
        logger.info("Undistorting images...")
        
        cmd = [
            self.colmap_path, "image_undistorter",
            "--image_path", str(image_dir),
            "--input_path", str(self.sparse_dir / "0"),
            "--output_path", str(self.dense_dir),
            "--output_type", "COLMAP"
        ]
        
        subprocess.run(cmd, check=True)
        logger.info("Image undistortion complete")
    
    def patch_match_stereo(self, max_image_size=3200):
        """
        Run PatchMatch stereo for dense reconstruction
        
        Args:
            max_image_size: Maximum image dimension for processing
        """
        logger.info("Running PatchMatch stereo...")
        
        cmd = [
            self.colmap_path, "patch_match_stereo",
            "--workspace_path", str(self.dense_dir),
            "--workspace_format", "COLMAP",
            "--PatchMatchStereo.max_image_size", str(max_image_size),
            "--PatchMatchStereo.geom_consistency", "true"
        ]
        
        subprocess.run(cmd, check=True)
        logger.info("PatchMatch stereo complete")
    
    def stereo_fusion(self, min_num_pixels=5):
        """
        Fuse depth maps into dense point cloud
        
        Args:
            min_num_pixels: Minimum number of consistent views
        """
        logger.info("Fusing stereo depth maps...")
        
        output_ply = self.dense_dir / "fused.ply"
        
        cmd = [
            self.colmap_path, "stereo_fusion",
            "--workspace_path", str(self.dense_dir),
            "--workspace_format", "COLMAP",
            "--input_type", "geometric",
            "--output_path", str(output_ply),
            "--StereoFusion.min_num_pixels", str(min_num_pixels)
        ]
        
        subprocess.run(cmd, check=True)
        logger.info(f"Stereo fusion complete: {output_ply}")
        return output_ply
    
    def filter_point_cloud(self, input_ply, output_ply=None, 
                          voxel_size=0.01, nb_neighbors=20, std_ratio=2.0):
        """
        Filter and clean the dense point cloud
        
        Args:
            input_ply: Input point cloud file
            output_ply: Output file path
            voxel_size: Voxel size for downsampling
            nb_neighbors: Number of neighbors for statistical outlier removal
            std_ratio: Standard deviation ratio threshold
        """
        logger.info("Filtering point cloud...")
        
        # Load point cloud
        pcd = o3d.io.read_point_cloud(str(input_ply))
        logger.info(f"Original points: {len(pcd.points)}")
        
        # Downsample
        pcd_down = pcd.voxel_down_sample(voxel_size=voxel_size)
        logger.info(f"After downsampling: {len(pcd_down.points)}")
        
        # Remove statistical outliers
        pcd_filtered, ind = pcd_down.remove_statistical_outlier(
            nb_neighbors=nb_neighbors,
            std_ratio=std_ratio
        )
        logger.info(f"After filtering: {len(pcd_filtered.points)}")
        
        # Save filtered point cloud
        if output_ply is None:
            output_ply = self.dense_dir / "fused_filtered.ply"
        
        o3d.io.write_point_cloud(str(output_ply), pcd_filtered)
        logger.info(f"Filtered point cloud saved: {output_ply}")
        
        return output_ply
    
    def visualize_point_cloud(self, ply_path):
        """Visualize the point cloud using Open3D"""
        logger.info(f"Visualizing {ply_path}...")
        
        pcd = o3d.io.read_point_cloud(str(ply_path))
        
        # Compute normals for better visualization
        pcd.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(
                radius=0.1, max_nn=30
            )
        )
        
        o3d.visualization.draw_geometries(
            [pcd],
            window_name="Dense Point Cloud",
            point_show_normal=False
        )
    
    def export_to_formats(self, input_ply):
        """Export point cloud to various formats"""
        pcd = o3d.io.read_point_cloud(str(input_ply))
        
        # Export to PLY (already done)
        # Export to PCD
        pcd_path = self.dense_dir / "fused.pcd"
        o3d.io.write_point_cloud(str(pcd_path), pcd)
        logger.info(f"Exported to PCD: {pcd_path}")
        
        # Export to XYZ
        xyz_path = self.dense_dir / "fused.xyz"
        points = np.asarray(pcd.points)
        colors = np.asarray(pcd.colors)
        with open(xyz_path, 'w') as f:
            for i in range(len(points)):
                f.write(f"{points[i, 0]} {points[i, 1]} {points[i, 2]} "
                       f"{int(colors[i, 0]*255)} {int(colors[i, 1]*255)} {int(colors[i, 2]*255)}\n")
        logger.info(f"Exported to XYZ: {xyz_path}")
    
    def run_full_pipeline(self, image_dir, visualize=False):
        """Run the complete MVS pipeline"""
        logger.info("Starting full MVS pipeline...")
        
        # Step 1: Undistort images
        self.image_undistortion(image_dir)
        
        # Step 2: PatchMatch stereo
        self.patch_match_stereo()
        
        # Step 3: Stereo fusion
        fused_ply = self.stereo_fusion()
        
        # Step 4: Filter point cloud
        filtered_ply = self.filter_point_cloud(fused_ply)
        
        # Step 5: Export to multiple formats
        self.export_to_formats(filtered_ply)
        
        # Step 6: Visualize (optional)
        if visualize:
            self.visualize_point_cloud(filtered_ply)
        
        logger.info("MVS pipeline complete!")
        return filtered_ply


def main():
    """Example usage"""
    mvs = MVSPipeline(
        sparse_dir="output/sparse",
        output_dir="output"
    )
    
    try:
        result = mvs.run_full_pipeline(
            image_dir="data/input_images",
            visualize=True
        )
        logger.info(f"Dense reconstruction saved: {result}")
    except subprocess.CalledProcessError as e:
        logger.error(f"COLMAP error: {e}")
        logger.error("Make sure COLMAP is installed with CUDA support for PatchMatch")
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    main()
