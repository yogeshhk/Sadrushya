"""
Complete 3D Reconstruction Pipeline Runner
Orchestrates the entire process from images to 3D model
"""

import argparse
import logging
from pathlib import Path
import time
from src.preprocess import ImagePreprocessor
from src.sfm import SfMPipeline
from src.mvs import MVSPipeline
from src.mesh import MeshGenerator
from src.export import MeshExporter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ReconstructionPipeline:
    def __init__(self, input_dir, output_dir="output", name="model"):
        """
        Initialize complete reconstruction pipeline
        
        Args:
            input_dir: Directory containing input images (30-40 images)
            output_dir: Directory for all outputs
            name: Name for the output model
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.name = name
        
        # Create directory structure
        self.preprocessed_dir = self.output_dir / "preprocessed"
        self.sparse_dir = self.output_dir / "sparse"
        self.dense_dir = self.output_dir / "dense"
        self.mesh_dir = self.output_dir / "mesh"
        self.export_dir = self.output_dir / "exports"
        
        # Timing
        self.timings = {}
    
    def validate_images(self):
        """Validate input images"""
        images = list(self.input_dir.glob("*.jpg")) + \
                 list(self.input_dir.glob("*.jpeg")) + \
                 list(self.input_dir.glob("*.png"))
        
        if len(images) < 15:
            logger.warning(f"Only {len(images)} images found. Recommended: 30-40 images")
            return False
        
        logger.info(f"Found {len(images)} images")
        return True
    
    def step_preprocess(self, max_size=1920, segment=True):
        """
        Step 1: Preprocess images
        
        Args:
            max_size: Maximum image dimension
            segment: Whether to run object segmentation
        """
        logger.info("="*60)
        logger.info("STEP 1: PREPROCESSING")
        logger.info("="*60)
        
        start_time = time.time()
        
        preprocessor = ImagePreprocessor(
            input_dir=str(self.input_dir),
            output_dir=str(self.preprocessed_dir)
        )
        
        # Resize images
        resized_dir = preprocessor.resize_images(max_size=max_size)
        
        # Optional segmentation
        if segment:
            try:
                preprocessor.segment_object(confidence_threshold=0.25)
            except Exception as e:
                logger.warning(f"Segmentation failed: {e}")
                logger.warning("Continuing without segmentation")
        
        # Extract features for verification
        preprocessor.extract_features(method='SIFT')
        
        self.timings['preprocess'] = time.time() - start_time
        logger.info(f"Preprocessing completed in {self.timings['preprocess']:.2f}s")
    
    def step_sfm(self):
        """Step 2: Structure from Motion"""
        logger.info("="*60)
        logger.info("STEP 2: STRUCTURE FROM MOTION")
        logger.info("="*60)
        
        start_time = time.time()
        
        sfm = SfMPipeline(
            image_dir=str(self.input_dir),
            output_dir=str(self.sparse_dir)
        )
        
        try:
            stats = sfm.run_full_pipeline()
            
            if stats and stats['num_images'] > 0:
                logger.info(f"Reconstructed {stats['num_images']} cameras")
                logger.info(f"Created {stats['num_points']} 3D points")
            else:
                logger.error("SfM failed to reconstruct scene")
                return False
                
        except Exception as e:
            logger.error(f"SfM failed: {e}")
            return False
        
        self.timings['sfm'] = time.time() - start_time
        logger.info(f"SfM completed in {self.timings['sfm']:.2f}s")
        return True
    
    def step_mvs(self):
        """Step 3: Multi-View Stereo (Dense Reconstruction)"""
        logger.info("="*60)
        logger.info("STEP 3: DENSE RECONSTRUCTION (MVS)")
        logger.info("="*60)
        
        start_time = time.time()
        
        mvs = MVSPipeline(
            sparse_dir=str(self.sparse_dir),
            output_dir=str(self.output_dir)
        )
        
        try:
            dense_ply = mvs.run_full_pipeline(
                image_dir=str(self.input_dir),
                visualize=False
            )
            
            logger.info(f"Dense point cloud created: {dense_ply}")
            
        except Exception as e:
            logger.error(f"MVS failed: {e}")
            return False, None
        
        self.timings['mvs'] = time.time() - start_time
        logger.info(f"MVS completed in {self.timings['mvs']:.2f}s")
        return True, dense_ply
    
    def step_mesh(self, dense_ply, method="poisson", simplify=True):
        """
        Step 4: Generate Mesh
        
        Args:
            dense_ply: Path to dense point cloud
            method: 'poisson' or 'ball_pivoting'
            simplify: Whether to simplify mesh
        """
        logger.info("="*60)
        logger.info("STEP 4: MESH GENERATION")
        logger.info("="*60)
        
        start_time = time.time()
        
        mesh_gen = MeshGenerator(
            dense_dir=str(self.dense_dir),
            output_dir=str(self.output_dir)
        )
        
        try:
            mesh_path, mesh = mesh_gen.run_full_pipeline(
                input_ply=str(dense_ply),
                method=method,
                simplify=simplify,
                visualize=False
            )
            
            logger.info(f"Mesh generated: {mesh_path}")
            
        except Exception as e:
            logger.error(f"Mesh generation failed: {e}")
            return False, None
        
        self.timings['mesh'] = time.time() - start_time
        logger.info(f"Mesh generation completed in {self.timings['mesh']:.2f}s")
        return True, mesh_path
    
    def step_export(self, mesh_path):
        """Step 5: Export to Multiple Formats"""
        logger.info("="*60)
        logger.info("STEP 5: EXPORT TO FORMATS")
        logger.info("="*60)
        
        start_time = time.time()
        
        exporter = MeshExporter(output_dir=str(self.output_dir))
        
        try:
            exported = exporter.export_all_formats(
                mesh_path=str(mesh_path),
                name=self.name
            )
            
            logger.info(f"Exported {len(exported)} formats:")
            for fmt, path in exported.items():
                logger.info(f"  - {fmt.upper()}: {path}")
            
            # Create web viewer
            if 'gltf' in exported:
                viewer_path = exporter.create_web_viewer_html(
                    exported['gltf'],
                    name=self.name
                )
                logger.info(f"\nWeb viewer created: {viewer_path}")
                logger.info("Open in browser to view the 3D model")
            
        except Exception as e:
            logger.error(f"Export failed: {e}")
            return False
        
        self.timings['export'] = time.time() - start_time
        logger.info(f"Export completed in {self.timings['export']:.2f}s")
        return True
    
    def run_full_pipeline(self, max_size=1920, segment=True, 
                         mesh_method="poisson", simplify=True):
        """
        Run complete reconstruction pipeline
        
        Args:
            max_size: Maximum image dimension for preprocessing
            segment: Whether to segment objects
            mesh_method: 'poisson' or 'ball_pivoting'
            simplify: Whether to simplify final mesh
        """
        logger.info("\n" + "="*60)
        logger.info("STARTING COMPLETE 3D RECONSTRUCTION PIPELINE")
        logger.info("="*60 + "\n")
        
        total_start = time.time()
        
        # Validate
        if not self.validate_images():
            logger.warning("Image validation warning - continuing anyway")
        
        # Step 1: Preprocess
        self.step_preprocess(max_size=max_size, segment=segment)
        
        # Step 2: SfM
        if not self.step_sfm():
            logger.error("Pipeline failed at SfM stage")
            return False
        
        # Step 3: MVS
        success, dense_ply = self.step_mvs()
        if not success:
            logger.error("Pipeline failed at MVS stage")
            return False
        
        # Step 4: Mesh
        success, mesh_path = self.step_mesh(
            dense_ply,
            method=mesh_method,
            simplify=simplify
        )
        if not success:
            logger.error("Pipeline failed at mesh generation stage")
            return False
        
        # Step 5: Export
        if not self.step_export(mesh_path):
            logger.error("Pipeline failed at export stage")
            return False
        
        # Final summary
        total_time = time.time() - total_start
        
        logger.info("\n" + "="*60)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY!")
        logger.info("="*60)
        logger.info(f"\nTotal time: {total_time:.2f}s ({total_time/60:.2f} minutes)")
        logger.info("\nStage timings:")
        for stage, duration in self.timings.items():
            logger.info(f"  {stage}: {duration:.2f}s")
        
        logger.info(f"\nFinal outputs in: {self.export_dir}")
        logger.info("\nNext steps:")
        logger.info("  1. Check exports/ folder for your 3D models")
        logger.info("  2. Open the HTML viewer to see the result")
        logger.info("  3. Use OBJ/STL files for 3D printing")
        logger.info("  4. Use USD files for Blender/USD workflows")
        
        return True


def main():
    parser = argparse.ArgumentParser(
        description="3D Reconstruction Pipeline - Convert images to 3D models"
    )
    parser.add_argument(
        "input_dir",
        help="Directory containing input images (30-40 recommended)"
    )
    parser.add_argument(
        "-o", "--output",
        default="output",
        help="Output directory (default: output)"
    )
    parser.add_argument(
        "-n", "--name",
        default="model",
        help="Model name (default: model)"
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=1920,
        help="Maximum image dimension (default: 1920)"
    )
    parser.add_argument(
        "--no-segment",
        action="store_true",
        help="Skip object segmentation"
    )
    parser.add_argument(
        "--mesh-method",
        choices=["poisson", "ball_pivoting"],
        default="poisson",
        help="Mesh reconstruction method (default: poisson)"
    )
    parser.add_argument(
        "--no-simplify",
        action="store_true",
        help="Skip mesh simplification"
    )
    
    args = parser.parse_args()
    
    # Create and run pipeline
    pipeline = ReconstructionPipeline(
        input_dir=args.input_dir,
        output_dir=args.output,
        name=args.name
    )
    
    success = pipeline.run_full_pipeline(
        max_size=args.max_size,
        segment=not args.no_segment,
        mesh_method=args.mesh_method,
        simplify=not args.no_simplify
    )
    
    if success:
        logger.info("\n✅ Reconstruction completed successfully!")
    else:
        logger.error("\n❌ Reconstruction failed!")
        exit(1)


if __name__ == "__main__":
    main()
