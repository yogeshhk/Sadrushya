"""
Structure from Motion (SfM) using COLMAP
Estimates camera poses and creates sparse 3D point cloud
"""

import subprocess
import logging
from pathlib import Path
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SfMPipeline:
    def __init__(self, image_dir, output_dir, colmap_path="colmap"):
        """
        Initialize SfM pipeline with COLMAP
        
        Args:
            image_dir: Directory containing input images
            output_dir: Directory for COLMAP output
            colmap_path: Path to COLMAP executable
        """
        self.image_dir = Path(image_dir)
        self.output_dir = Path(output_dir)
        self.database_path = self.output_dir / "database.db"
        self.sparse_dir = self.output_dir / "sparse"
        self.colmap_path = colmap_path
        
        # Create directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.sparse_dir.mkdir(exist_ok=True)
    
    def feature_extraction(self, camera_model="SIMPLE_RADIAL"):
        """
        Extract features from images
        
        Args:
            camera_model: Camera model (SIMPLE_RADIAL, PINHOLE, etc.)
        """
        logger.info("Extracting features...")
        
        cmd = [
            self.colmap_path, "feature_extractor",
            "--database_path", str(self.database_path),
            "--image_path", str(self.image_dir),
            "--ImageReader.camera_model", camera_model,
            "--SiftExtraction.max_num_features", "8192"
        ]
        
        subprocess.run(cmd, check=True)
        logger.info("Feature extraction complete")
    
    def feature_matching(self, matching_type="exhaustive"):
        """
        Match features between image pairs
        
        Args:
            matching_type: 'exhaustive', 'sequential', or 'spatial'
        """
        logger.info(f"Matching features ({matching_type})...")
        
        if matching_type == "exhaustive":
            cmd = [
                self.colmap_path, "exhaustive_matcher",
                "--database_path", str(self.database_path),
                "--SiftMatching.guided_matching", "1"
            ]
        elif matching_type == "sequential":
            cmd = [
                self.colmap_path, "sequential_matcher",
                "--database_path", str(self.database_path),
                "--SequentialMatching.overlap", "10"
            ]
        else:
            raise ValueError(f"Unknown matching type: {matching_type}")
        
        subprocess.run(cmd, check=True)
        logger.info("Feature matching complete")
    
    def sparse_reconstruction(self):
        """Perform sparse 3D reconstruction"""
        logger.info("Running sparse reconstruction...")
        
        cmd = [
            self.colmap_path, "mapper",
            "--database_path", str(self.database_path),
            "--image_path", str(self.image_dir),
            "--output_path", str(self.sparse_dir)
        ]
        
        subprocess.run(cmd, check=True)
        logger.info("Sparse reconstruction complete")
    
    def bundle_adjustment(self):
        """Refine camera poses and 3D points"""
        logger.info("Running bundle adjustment...")
        
        # Find the reconstruction directory (usually '0')
        recon_dir = self.sparse_dir / "0"
        if not recon_dir.exists():
            logger.warning("No reconstruction found in sparse/0")
            return
        
        cmd = [
            self.colmap_path, "bundle_adjuster",
            "--input_path", str(recon_dir),
            "--output_path", str(recon_dir),
            "--BundleAdjustment.refine_focal_length", "1",
            "--BundleAdjustment.refine_extra_params", "1"
        ]
        
        subprocess.run(cmd, check=True)
        logger.info("Bundle adjustment complete")
    
    def export_to_text(self):
        """Export COLMAP binary format to text for inspection"""
        logger.info("Exporting to text format...")
        
        recon_dir = self.sparse_dir / "0"
        output_text_dir = self.output_dir / "sparse_text"
        output_text_dir.mkdir(exist_ok=True)
        
        cmd = [
            self.colmap_path, "model_converter",
            "--input_path", str(recon_dir),
            "--output_path", str(output_text_dir),
            "--output_type", "TXT"
        ]
        
        subprocess.run(cmd, check=True)
        logger.info(f"Text export complete: {output_text_dir}")
    
    def get_reconstruction_stats(self):
        """Get statistics about the reconstruction"""
        stats_file = self.sparse_dir / "0" / "project.ini"
        
        if not stats_file.exists():
            logger.warning("No reconstruction statistics found")
            return None
        
        # Parse cameras.txt and points3D.txt for stats
        text_dir = self.output_dir / "sparse_text"
        
        stats = {
            "num_cameras": 0,
            "num_images": 0,
            "num_points": 0
        }
        
        cameras_file = text_dir / "cameras.txt"
        if cameras_file.exists():
            with open(cameras_file) as f:
                stats["num_cameras"] = sum(1 for line in f if not line.startswith("#"))
        
        images_file = text_dir / "images.txt"
        if images_file.exists():
            with open(images_file) as f:
                stats["num_images"] = sum(1 for line in f if not line.startswith("#") and line.strip()) // 2
        
        points_file = text_dir / "points3D.txt"
        if points_file.exists():
            with open(points_file) as f:
                stats["num_points"] = sum(1 for line in f if not line.startswith("#"))
        
        logger.info(f"Reconstruction stats: {stats}")
        return stats
    
    def run_full_pipeline(self):
        """Run the complete SfM pipeline"""
        logger.info("Starting full SfM pipeline...")
        
        # Step 1: Feature extraction
        self.feature_extraction()
        
        # Step 2: Feature matching
        self.feature_matching(matching_type="exhaustive")
        
        # Step 3: Sparse reconstruction
        self.sparse_reconstruction()
        
        # Step 4: Bundle adjustment
        self.bundle_adjustment()
        
        # Step 5: Export to text
        self.export_to_text()
        
        # Step 6: Get stats
        stats = self.get_reconstruction_stats()
        
        logger.info("SfM pipeline complete!")
        return stats


def main():
    """Example usage"""
    sfm = SfMPipeline(
        image_dir="data/input_images",
        output_dir="output/sparse"
    )
    
    try:
        stats = sfm.run_full_pipeline()
        logger.info(f"Final reconstruction: {stats}")
    except subprocess.CalledProcessError as e:
        logger.error(f"COLMAP error: {e}")
        logger.error("Make sure COLMAP is installed and in your PATH")
        logger.error("Install: https://colmap.github.io/install.html")


if __name__ == "__main__":
    main()
