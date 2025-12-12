"""
Image Preprocessing and Object Segmentation
Prepares input images and isolates the statue using YOLO or SAM
"""

import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImagePreprocessor:
    def __init__(self, input_dir, output_dir, model_path="yolov8n.pt"):
        """
        Initialize preprocessor
        
        Args:
            input_dir: Directory containing input images
            output_dir: Directory for processed images
            model_path: Path to YOLO model weights
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load YOLO model
        self.model = YOLO(model_path)
        
    def resize_images(self, max_size=1920):
        """Resize images to manageable size while preserving aspect ratio"""
        resized_dir = self.output_dir / "resized"
        resized_dir.mkdir(exist_ok=True)
        
        for img_path in self.input_dir.glob("*.jpg"):
            img = cv2.imread(str(img_path))
            h, w = img.shape[:2]
            
            if max(h, w) > max_size:
                scale = max_size / max(h, w)
                new_w, new_h = int(w * scale), int(h * scale)
                img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
            
            output_path = resized_dir / img_path.name
            cv2.imwrite(str(output_path), img)
            logger.info(f"Resized: {img_path.name}")
        
        return resized_dir
    
    def segment_object(self, confidence_threshold=0.25):
        """
        Detect and segment the main object (statue) in images
        
        Args:
            confidence_threshold: Minimum confidence for detection
        """
        segmented_dir = self.output_dir / "segmented"
        masks_dir = self.output_dir / "masks"
        segmented_dir.mkdir(exist_ok=True)
        masks_dir.mkdir(exist_ok=True)
        
        for img_path in self.input_dir.glob("*.jpg"):
            img = cv2.imread(str(img_path))
            
            # Run YOLO detection
            results = self.model(img, conf=confidence_threshold)
            
            if len(results[0].boxes) > 0:
                # Get the largest detected object
                boxes = results[0].boxes.xyxy.cpu().numpy()
                confidences = results[0].boxes.conf.cpu().numpy()
                
                # Find box with highest confidence
                best_idx = np.argmax(confidences)
                x1, y1, x2, y2 = map(int, boxes[best_idx])
                
                # Create mask
                mask = np.zeros(img.shape[:2], dtype=np.uint8)
                mask[y1:y2, x1:x2] = 255
                
                # Apply mask to image
                segmented = cv2.bitwise_and(img, img, mask=mask)
                
                # Save results
                cv2.imwrite(str(segmented_dir / img_path.name), segmented)
                cv2.imwrite(str(masks_dir / img_path.name), mask)
                
                logger.info(f"Segmented: {img_path.name}")
            else:
                logger.warning(f"No object detected in {img_path.name}")
    
    def undistort_images(self, camera_matrix=None, dist_coeffs=None):
        """Undistort images if camera calibration is available"""
        if camera_matrix is None or dist_coeffs is None:
            logger.info("No calibration data provided, skipping undistortion")
            return
        
        undistorted_dir = self.output_dir / "undistorted"
        undistorted_dir.mkdir(exist_ok=True)
        
        for img_path in self.input_dir.glob("*.jpg"):
            img = cv2.imread(str(img_path))
            h, w = img.shape[:2]
            
            # Get optimal new camera matrix
            new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
                camera_matrix, dist_coeffs, (w, h), 1, (w, h)
            )
            
            # Undistort
            undistorted = cv2.undistort(img, camera_matrix, dist_coeffs, 
                                       None, new_camera_matrix)
            
            # Crop based on ROI
            x, y, w, h = roi
            undistorted = undistorted[y:y+h, x:x+w]
            
            cv2.imwrite(str(undistorted_dir / img_path.name), undistorted)
            logger.info(f"Undistorted: {img_path.name}")
    
    def extract_features(self, method='SIFT'):
        """Extract and visualize features for verification"""
        features_dir = self.output_dir / "features"
        features_dir.mkdir(exist_ok=True)
        
        if method == 'SIFT':
            detector = cv2.SIFT_create()
        elif method == 'ORB':
            detector = cv2.ORB_create()
        else:
            raise ValueError(f"Unknown method: {method}")
        
        for img_path in self.input_dir.glob("*.jpg"):
            img = cv2.imread(str(img_path))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detect keypoints
            keypoints, descriptors = detector.detectAndCompute(gray, None)
            
            # Draw keypoints
            img_keypoints = cv2.drawKeypoints(
                img, keypoints, None, 
                flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
            )
            
            cv2.imwrite(str(features_dir / img_path.name), img_keypoints)
            logger.info(f"Extracted {len(keypoints)} features from {img_path.name}")


def main():
    """Example usage"""
    preprocessor = ImagePreprocessor(
        input_dir="data/input_images",
        output_dir="data/preprocessed"
    )
    
    # Step 1: Resize images
    logger.info("Step 1: Resizing images...")
    resized_dir = preprocessor.resize_images(max_size=1920)
    
    # Step 2: Segment objects
    logger.info("Step 2: Segmenting objects...")
    preprocessor.segment_object(confidence_threshold=0.3)
    
    # Step 3: Extract features for visualization
    logger.info("Step 3: Extracting features...")
    preprocessor.extract_features(method='SIFT')
    
    logger.info("Preprocessing complete!")


if __name__ == "__main__":
    main()
