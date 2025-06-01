
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import cv2
import threading
import numpy as np
from objdetectlogic import ObjectDetector 

class ObjectDetectionApp:
    def __init__(self, master_window):
        self.master = master_window
        master_window.title("Object Detection - YOLOv3 (CodeAlpha)")
        master_window.geometry("800x650")
        master_window.configure(bg="#e0e0e0")

        self.detector = ObjectDetector()
        
        self.webcam_active = False
        self.video_capture = None
        self.current_static_pil_image = None

        controls_frame = tk.Frame(master_window, bg="#d0d0d0", pady=5)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)

        self.upload_button = tk.Button(controls_frame, text="Upload Image", command=self.upload_image, font=("Arial",9))
        self.upload_button.pack(side=tk.LEFT, padx=5)
        self.webcam_btn = tk.Button(controls_frame, text="Start Webcam", command=self.toggle_webcam, font=("Arial",9))
        self.webcam_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Label(controls_frame, text="Conf:", font=("Arial",9), bg="#d0d0d0").pack(side=tk.LEFT, padx=(10,0))
        self.conf_slider = ttk.Scale(controls_frame, from_=0.1, to=0.9, orient=tk.HORIZONTAL, length=100, command=self.update_conf)
        self.conf_slider.set(0.5) 
        self.conf_slider.pack(side=tk.LEFT)

        self.image_label = tk.Label(master_window, bg="#333")
        self.image_label.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        
        
        self.status_bar = tk.Label(master_window, text="Initializing...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        
        if self.detector.net is None: 
            self.status_bar.config(text="ERROR: YOLO Model not loaded. Check 'yolo_model' folder.")
            self.upload_button.config(state=tk.DISABLED)
            self.webcam_btn.config(state=tk.DISABLED)
            messagebox.showerror("Model Error", "YOLO Model not loaded. Check 'yolo_model' folder and console.")
            return 
        else:
            self.status_bar.config(text="Detector Ready.")
       
            self.update_conf(self.conf_slider.get()) 


    def update_conf(self, val_str): 
        val = float(val_str)
        if self.detector and self.detector.net:
            self.detector.set_confidence_threshold(val)
            
            self.detector.set_nms_threshold(0.4) 
            self.status_bar.config(text=f"Confidence: {val:.2f}")
            if self.current_static_pil_image and not self.webcam_active:
                 self.process_static_image_async(self.current_static_pil_image.copy())


    def upload_image(self):
        if self.webcam_active: self.toggle_webcam() 
        if not self.detector or not self.detector.net: 
            messagebox.showerror("Error", "Detector not loaded!")
            return
        filepath = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if not filepath: return
        try:
            pil_image = Image.open(filepath)
            self.current_static_pil_image = pil_image
            self.process_static_image_async(pil_image.copy())
        except Exception as e:
            self.status_bar.config(text=f"Error processing image: {e}")
            messagebox.showerror("Image Error", f"Could not load/process image: {e}")

    def process_static_image_async(self, pil_image):
        self.status_bar.config(text="Processing image...")
        self.upload_button.config(state=tk.DISABLED)
        self.webcam_btn.config(state=tk.DISABLED)
        threading.Thread(target=self._process_static_image_task, args=(pil_image,), daemon=True).start()

    def _process_static_image_task(self, pil_image):
        cv_image = cv2.cvtColor(np.array(pil_image.convert('RGB')), cv2.COLOR_RGB2BGR)
        processed_frame, detected_info = self.detector.detect(cv_image)
        self.display_image(processed_frame)
        self.status_bar.config(text=f"Image processed. Found {len(detected_info)} objects.")
        self.upload_button.config(state=tk.NORMAL)
        self.webcam_btn.config(state=tk.NORMAL)

    def toggle_webcam(self):
        if self.webcam_active:
            self.webcam_active = False
            self.webcam_btn.config(text="Start Webcam")
            if self.video_capture: self.video_capture.release()
            self.status_bar.config(text="Webcam stopped.")
        else:
            if not self.detector or not self.detector.net:
                messagebox.showerror("Error", "Detector not loaded!")
                return
            try:
                self.video_capture = cv2.VideoCapture(0) 
                if not self.video_capture.isOpened(): 
                    self.video_capture.release()
                    self.video_capture = cv2.VideoCapture(1)
                    if not self.video_capture.isOpened(): raise IOError("Cannot open webcam")
                self.webcam_active = True
                self.current_static_pil_image = None 
                self.image_label.image = None 
                self.webcam_btn.config(text="Stop Webcam")
                self.status_bar.config(text="Webcam active...")
                self._update_webcam_feed()
            except Exception as e:
                self.status_bar.config(text=f"Webcam error: {e}")
                messagebox.showerror("Webcam Error", f"Could not start webcam: {e}")
                self.webcam_active = False

    def _update_webcam_feed(self):
        if not self.webcam_active or not self.video_capture or not self.video_capture.isOpened(): return
        ret, frame = self.video_capture.read()
        if ret:
            frame_flipped = cv2.flip(frame, 1)
            processed_frame, _ = self.detector.detect(frame_flipped) 
            self.display_image(processed_frame)
        if self.webcam_active: 
            self.master.after(20, self._update_webcam_feed)

    def display_image(self, cv_image_bgr):
        cv_image_rgb = cv2.cvtColor(cv_image_bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(cv_image_rgb)
        
        w, h = self.image_label.winfo_width(), self.image_label.winfo_height()
        if w < 2 or h < 2: w, h = 780, 580 
        pil_img.thumbnail((w - 10, h - 10), Image.Resampling.LANCZOS)
        
        imgtk = ImageTk.PhotoImage(image=pil_img)
        self.image_label.imgtk = imgtk 
        self.image_label.config(image=imgtk)

    def on_close(self):
        if self.webcam_active and self.video_capture: 
            self.video_capture.release()
        self.master.destroy()

if __name__ == "__main__":
    import os 
    yolo_dir = "yolo_model"
    required = ["yolov3.weights", "yolov3.cfg", "coco.names"]
    gui_launch_ok = True
    if not os.path.exists(yolo_dir) or not all(os.path.exists(os.path.join(yolo_dir, f)) for f in required):
        print(f"ERROR: Missing YOLO model files in '{yolo_dir}/'.")
        print(f"Required: {', '.join(required)}")
      
        gui_launch_ok = False 
    
    if gui_launch_ok:
        root = tk.Tk()
        app = ObjectDetectionApp(root)
        root.mainloop()
    else:
        print("Application will not start due to missing model files.")