import cv2
import numpy as np
import math

def nothing(x):
    pass

def draw_hud(frame, state, distance, max_dist):
    
    height, width, _ = frame.shape
    
    
    COLOR_BG = (30, 30, 30)      
    COLOR_TEXT = (255, 255, 255) 
    
    if state == "SAFE":
        status_color = (0, 255, 128) 
    elif state == "WARNING":
        status_color = (0, 165, 255) 
    else: 
        status_color = (0, 0, 255)   

   
    panel_w = 280
    panel_h = 130
    x1, y1 = width - panel_w - 20, 20
    x2, y2 = width - 20, 20 + panel_h
    
   
    overlay = frame.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), COLOR_BG, -1)
    
    cv2.rectangle(overlay, (x1, y1), (x2, y2), status_color, 2)
    
    alpha = 0.7
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    cv2.putText(frame, "PROXIMITY GUARD", (x1 + 15, y1 + 30), 
                cv2.FONT_HERSHEY_DUPLEX, 0.6, COLOR_TEXT, 1, cv2.LINE_AA)
    
    cv2.putText(frame, state, (x1 + 15, y1 + 70), 
                cv2.FONT_HERSHEY_TRIPLEX, 1.0, status_color, 2, cv2.LINE_AA)

    bar_x = x1 + 15
    bar_y = y1 + 90
    bar_w = 240
    bar_h = 15
    
   
    fill_ratio = 1.0 - min(1.0, distance / 350) 
    if fill_ratio < 0: fill_ratio = 0
    
    fill_width = int(bar_w * fill_ratio)
    
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (50, 50, 50), -1)
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_h), status_color, -1)
    
    cv2.putText(frame, f"DIST: {int(distance)}px", (bar_x, bar_y + 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1, cv2.LINE_AA)

def main():
    cap = cv2.VideoCapture(0)
    
    cv2.namedWindow("Calibration")
    cv2.createTrackbar("H Min", "Calibration", 0, 179, nothing)
    cv2.createTrackbar("S Min", "Calibration", 40, 255, nothing)
    cv2.createTrackbar("V Min", "Calibration", 60, 255, nothing)
    cv2.createTrackbar("H Max", "Calibration", 25, 179, nothing)
    cv2.createTrackbar("S Max", "Calibration", 255, 255, nothing)
    cv2.createTrackbar("V Max", "Calibration", 255, 255, nothing)

    radius_danger = 80
    radius_warning = 200

    print("Running Pro Version. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        center_x, center_y = w // 2, h // 2

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        h_min = cv2.getTrackbarPos("H Min", "Calibration")
        s_min = cv2.getTrackbarPos("S Min", "Calibration")
        v_min = cv2.getTrackbarPos("V Min", "Calibration")
        h_max = cv2.getTrackbarPos("H Max", "Calibration")
        s_max = cv2.getTrackbarPos("S Max", "Calibration")
        v_max = cv2.getTrackbarPos("V Max", "Calibration")

        mask = cv2.inRange(hsv, (h_min, s_min, v_min), (h_max, s_max, v_max))
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=2)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        current_state = "SAFE"
        distance = 400 
        
       
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) > 1000:
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    
                    distance = math.sqrt((cx - center_x)**2 + (cy - center_y)**2)
                    
                    
                    if distance < radius_danger:
                        current_state = "DANGER"
                    elif distance < radius_warning:
                        current_state = "WARNING"
                    
                    
                    line_color = (0, 255, 128)
                    if current_state == "WARNING": line_color = (0, 165, 255)
                    if current_state == "DANGER": line_color = (0, 0, 255)
                    
                    cv2.line(frame, (cx, cy), (center_x, center_y), line_color, 2)
                    cv2.circle(frame, (cx, cy), 8, line_color, -1)
                    cv2.drawContours(frame, [c], -1, line_color, 2)

       
        overlay = frame.copy()
        
       
        cv2.circle(overlay, (center_x, center_y), radius_warning, (0, 165, 255), -1)
        
        cv2.circle(overlay, (center_x, center_y), radius_danger, (0, 0, 255), -1)
        
        
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        
       
        cv2.circle(frame, (center_x, center_y), radius_warning, (0, 165, 255), 1, cv2.LINE_AA)
        cv2.circle(frame, (center_x, center_y), radius_danger, (0, 0, 255), 1, cv2.LINE_AA)
        
        cv2.line(frame, (center_x - 10, center_y), (center_x + 10, center_y), (255,255,255), 1)
        cv2.line(frame, (center_x, center_y - 10), (center_x, center_y + 10), (255,255,255), 1)

        draw_hud(frame, current_state, distance, 350)
        
        if current_state == "DANGER":
            red_layer = np.zeros_like(frame)
            red_layer[:] = (0, 0, 255)
            cv2.addWeighted(red_layer, 0.1, frame, 1.0, 0, frame)

        mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        mask_small = cv2.resize(mask_bgr, (160, 120))
        frame[h-130:h-10, 10:170] = mask_small
        cv2.rectangle(frame, (10, h-130), (170, h-10), (255, 255, 255), 1)
        cv2.putText(frame, "CALIBRATION", (15, h-115), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)

        cv2.imshow("Proximity Guard Pro", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()