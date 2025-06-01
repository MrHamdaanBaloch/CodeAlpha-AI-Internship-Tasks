# object_detection_logic.py
import cv2
import numpy as np
import os
# Removed time import as it wasn't used in this simplified version

class ObjectDetector:
    def __init__(self, conf_thresh=0.5, nms_thresh=0.4):
        model_dir = "yolo_model"
        weights_path = os.path.join(model_dir, "yolov3.weights")
        config_path = os.path.join(model_dir, "yolov3.cfg")
        names_path = os.path.join(model_dir, "coco.names")

        self.net = None
        self.classes = []
        self.output_layers_names = [] 
        self.colors = []
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        if not all(os.path.exists(p) for p in [weights_path, config_path, names_path]):
            print("ERROR: YOLO model files not found in 'yolo_model/'. Download them first.")
            return

        try:
            self.net = cv2.dnn.readNet(weights_path, config_path)
            
            with open(names_path, "r") as f:
                self.classes = [line.strip() for line in f.readlines()]
            
            layer_names = self.net.getLayerNames()
            unconnected_out_layers_indices = self.net.getUnconnectedOutLayers()

            # --- START: ROBUST HANDLING FOR getUnconnectedOutLayers ---
            if isinstance(unconnected_out_layers_indices, np.ndarray):
                if unconnected_out_layers_indices.ndim > 1: # e.g., [[200], [231], [252]]
                    self.output_layers_names = [layer_names[i[0] - 1] for i in unconnected_out_layers_indices]
                else: # e.g., [200, 231, 252] (1D array)
                    self.output_layers_names = [layer_names[i - 1] for i in unconnected_out_layers_indices]
            elif isinstance(unconnected_out_layers_indices, (list, tuple)): # Handle list/tuple of scalars
                 self.output_layers_names = [layer_names[i - 1] for i in unconnected_out_layers_indices]
            elif isinstance(unconnected_out_layers_indices, int): # Handle single scalar int
                self.output_layers_names = [layer_names[unconnected_out_layers_indices - 1]]
            else:
                # Fallback or raise error if format is unexpected
                print(f"Warning: Unexpected format for getUnconnectedOutLayers(): {type(unconnected_out_layers_indices)}")
                # Attempt a common fallback if it's a list-like structure of single-element lists
                try:
                    self.output_layers_names = [layer_names[i[0] - 1] for i in unconnected_out_layers_indices]
                except:
                    raise TypeError(f"Could not parse output layers from getUnconnectedOutLayers() output: {unconnected_out_layers_indices}")
            # --- END: ROBUST HANDLING ---

            self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
            print("YOLOv3 model loaded successfully.")
        except cv2.error as e:
            print(f"Error loading YOLO model: {e}")
            self.net = None
        except Exception as e_gen: # Catch other general exceptions during init
            print(f"An unexpected error occurred during ObjectDetector init: {e_gen}")
            self.net = None


        self.confidence_threshold = conf_thresh
        self.nms_threshold = nms_thresh

    def detect(self, frame):
        if self.net is None: # Check if network loaded
            cv2.putText(frame, "YOLO Model Load Error", (10,30), self.font, 1, (0,0,255),2)
            return frame, []

        height, width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers_names) # Use the processed names

        class_ids, confidences, boxes = [], [], []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > self.confidence_threshold:
                    center_x, center_y = int(detection[0] * width), int(detection[1] * height)
                    w, h = int(detection[2] * width), int(detection[3] * height)
                    x, y = int(center_x - w / 2), int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, self.nms_threshold)
        
        final_indices = []
        if hasattr(indices, 'flatten'): # Check if it's a NumPy array that can be flattened
            final_indices = indices.flatten()
        elif isinstance(indices, (list, tuple)) and len(indices) > 0 : # If it's a non-empty list/tuple
            # If it's a list of lists like [[0], [2]], flatten it
            if all(isinstance(sub, (list, tuple, np.ndarray)) and len(sub) == 1 for sub in indices):
                final_indices = [item[0] for item in indices]
            else: # Assume it's already a flat list of indices
                final_indices = list(indices)
        # If indices is empty or None, final_indices remains empty


        detected_objects_summary = []
        for i in final_indices:
            x, y, w, h = boxes[i]
            label = str(self.classes[class_ids[i]])
            color = self.colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{label} {confidences[i]*100:.0f}%", (x, y - 8), self.font, 0.6, color, 2)
            detected_objects_summary.append({"label": label, "confidence": confidences[i], "box": (x,y,w,h)})
        return frame, detected_objects_summary

    # Added for compatibility with GUI if settings are updated
    def set_confidence_threshold(self, threshold):
        self.confidence_threshold = float(threshold)

    def set_nms_threshold(self, threshold):
        self.nms_threshold = float(threshold)