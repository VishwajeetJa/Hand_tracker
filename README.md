# 🛡️ Proximity Guard Pro

A<img width="1286" height="1004" alt="Screenshot 2025-12-03 145700" src="https://github.com/user-attachments/assets/8d50b32e-1950-4a7c-a801-4040a32a5883" />
 real-time Computer Vision prototype that tracks hand movements and triggers a "DANGER" alert when approaching a virtual object.

## 🎥 Demo
> *Tracks the hand centroid using HSV color segmentation and calculates dynamic distance to a central target.*

## ✨ Features
* **No AI/ML APIs:** Built entirely with classical Computer Vision (OpenCV).
* **Real-time Tracking:** Uses HSV color thresholding and Centroid calculation.
* **Dynamic States:** Automatically switches between **SAFE** (Green), **WARNING** (Orange), and **DANGER** (Red).
* **Pro HUD:** Custom-built overlay with distance bars and transparent zones.

## 🛠️ Tech Stack
* Python 3.x
* OpenCV (`cv2`)
* NumPy

## 🚀 How to Run
1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Proximity-Guard.git](https://github.com/YOUR_USERNAME/Proximity-Guard.git)
    cd Proximity-Guard
    ```

2.  **Install dependencies**
    ```bash
    pip install opencv-python numpy
    ```

3.  **Run the script**
    ```bash
    python hand_tracker.py
    ```

## ⚙️ How to Calibrate
1.  When you run the script, a **Calibration Window** will open.
2.  Adjust the `H Min/Max` sliders until your hand is **white** and the background is **black** in the "Mask View".
3.  Move your hand towards the center to test the detection!
