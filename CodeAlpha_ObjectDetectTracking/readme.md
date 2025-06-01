# CodeAlpha AI Internship - Task 4: Object Detection and Tracking

## Description
A desktop application for real-time object detection and basic tracking in images and live webcam feeds using the YOLOv3 model.

## Features
-   Object detection with YOLOv3 (COCO dataset).
-   Supports static image uploads and live webcam input.
-   Bounding boxes, class labels, and confidence scores for detections.
-   Simple centroid-based object tracking with unique IDs.
-   Adjustable detection confidence and NMS thresholds via GUI.
-   FPS display for webcam performance.
-   Tkinter GUI.

## Technologies Used
-   Python 3.x
-   OpenCV (`opencv-python`) with DNN module
-   NumPy
-   Pillow (PIL)
-   SciPy (for centroid tracker's distance calculations)

## Setup and Installation
1.  **Prerequisites:** Python 3.6+.
2.  **Project Folder:** Create `CodeAlpha_ObjectDetectionTracking`.
3.  **`yolo_model` Subfolder:** Inside the project folder, create `yolo_model/`.
4.  **Download YOLOv3 Files:** Place these into `yolo_model/`:
    *   `yolov3.weights`: From [PJReddie's site](https://pjreddie.com/media/files/yolov3.weights) (~236MB)
    *   `yolov3.cfg`: From [Darknet GitHub](https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg)
    *   `coco.names`: From [Darknet GitHub](https://github.com/pjreddie/darknet/blob/master/data/coco.names)
5.  **Install Dependencies:**
    ```bash
    cd CodeAlpha_ObjectDetectionTracking
    pip install -r requirements.txt
    ```

## How to Run
Execute from the project directory:
```bash
python object_detection_gui.py

Wait for "Detector ready." status.
Use "Image" to upload or "Webcam" for live feed.
Notes
YOLOv3 is computationally intensive. CPU performance for webcam might be low. For GPU acceleration (NVIDIA), you'll need OpenCV built with CUDA support and uncomment relevant lines in object_detection_logic.py.
The centroid tracker is basic.
Screenshot

![Description of screenshot](C:\Users\ISHAIKH TECHNOLOGIES\Desktop\CODE ALPHA  TASKS\CodeAlpha_ObjectDetectTracking\Screenshot 2025-05-30 172000.png)

![GUI Screenshot](Screenshot 2025-05-30 172000.png)