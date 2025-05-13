import cv2
import numpy as np

def process_frame(frame):
    """
        steering_value: float between 0.05 and 0.1 duty cycle (0.075 is straight)
        processed_frame: visualized frame with detected lines highlighted
        finish_detected: boolean indicating if finish line (green) is detected
    """
    processed_frame = frame.copy()
    height, width = frame.shape[:2]
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # right side of track range
    blue_lower = np.array([100, 50, 50])
    blue_upper = np.array([130, 255, 255])
    
    # left side of track range
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([35, 255, 255])
    
    # end of track range
    green_lower = np.array([40, 50, 50])
    green_upper = np.array([80, 255, 255])

    # mask image for ranges    
    blue_mask = cv2.inRange(hsv_frame, blue_lower, blue_upper)
    yellow_mask = cv2.inRange(hsv_frame, yellow_lower, yellow_upper)
    green_mask = cv2.inRange(hsv_frame, green_lower, green_upper)
    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)  # bgr for displaying image
    
    combined_mask = cv2.bitwise_or(blue_mask, cv2.bitwise_or(yellow_mask, green_mask))
    processed_frame = np.where(combined_mask[:, :, np.newaxis] > 0, frame, gray_frame)
    
    # look for green
    green_pixels = cv2.countNonZero(green_mask)
    finish_detected = green_pixels > (width * height * 0.05)  # 5% of frame, increase if motors stop to early
    
    # steering calc for mid of screen in bottom third
    roi_height = height // 3
    bottom_region = hsv_frame[height - roi_height:height, :]
    
    bottom_blue_mask = cv2.inRange(bottom_region, blue_lower, blue_upper)
    bottom_yellow_mask = cv2.inRange(bottom_region, yellow_lower, yellow_upper)
    
    # find blue and yellow
    blue_moments = cv2.moments(bottom_blue_mask)
    yellow_moments = cv2.moments(bottom_yellow_mask)
    
    # Default to center position (0.075 duty cycle)
    steering_value = 0.075
    
    # Find both lines
    if blue_moments["m00"] > 0 and yellow_moments["m00"] > 0:
        blue_x = int(blue_moments["m10"] / blue_moments["m00"])
        yellow_x = int(yellow_moments["m10"] / yellow_moments["m00"])
        
        # find center of lines
        center_x = (blue_x + yellow_x) // 2
        
        # Map center_x from 0-width to 0.05-0.1 duty cycle
        # 0 = left edge (0.05), width = right edge (0.1)
        steering_value = 0.05 + (center_x / width) * 0.05
        
        # draw line for visuals
        print("both colors detected")
        cv2.line(processed_frame, (width//2, height), (center_x, height - roi_height), (0, 255, 255), 2)
    
    # if only blue steer left (away)
    elif blue_moments["m00"] > 0: 
        blue_x = int(blue_moments["m10"] / blue_moments["m00"])
        # Map from 0-1 scale to 0.05-0.1 (with offset to steer away)
        raw_steering = 0.3 - (0.2 * (1 - (blue_x / width)))
        # Convert to 0.05-0.1 range
        steering_value = 0.05 + raw_steering * 0.05
        
    # if only yellow steer right (away)
    elif yellow_moments["m00"] > 0:
        yellow_x = int(yellow_moments["m10"] / yellow_moments["m00"])
        # Map from 0-1 scale to 0.05-0.1 (with offset to steer away)
        raw_steering = 0.7 + (0.2 * (yellow_x / width))
        # Convert to 0.05-0.1 range
        steering_value = 0.05 + raw_steering * 0.05
        
    # Ensure steering value is between 0.05 and 0.1
    steering_value = max(0.05, min(0.1, steering_value))
    
    # Add directional indicator to the frame
    cv2.putText(processed_frame, f"Steering: {steering_value:.4f}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    if finish_detected:
        cv2.putText(processed_frame, "FINISH LINE DETECTED", (width//2 - 150, height//2), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    
    return steering_value, processed_frame, finish_detected