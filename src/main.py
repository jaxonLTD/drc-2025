import motor_controller
import color_detection
import cv2

class SlayMax:
    def __init__ (self):
        self.motorController = motor_controller.DRCMotorController(motorPin=13, servoPin=12)
        self.started = False

    def endLoop (self):
        self.motorController.setServoMotor(angle=0.5)
        self.started = False
        pass

    def startLoop (self):
        self.motorController.setServoMotor(angle=0.5)
        self.started = True
        pass

    def mainLoop (self):
        cap = cv2.VideoCapture("/dev/video0")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to grab frame.")
                continue
            
            steering, processed_frame, finish = color_detection.process_frame(frame)
            
            # cv2.imshow('RC Car Line Follower', processed_frame)
            print(f"Steering: {steering:.2f} {'(FINISH DETECTED)' if finish else ''}")

            cv2.imwrite("img.jpg", processed_frame)

            if (finish):
                self.motorController.setServoMotor(angle=0.5)
                self.motorController.setDrivingMotor(speed=0)
                self.motorController.off()
                self.started = False

            if (self.started == True):
                #change drive motor later
                self.motorController.setServoMotor(angle=steering)
                self.motorController.setDrivingMotor(speed=0.1)
            

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
            
        

# def main():
#     cap = cv2.VideoCapture(0)
#     # motorController = motor_controller.DRCMotorController(motorPin=13, servoPin=12)
    
#     if not cap.isOpened():
#         print("Error: Could not open camera.")
#         return
    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Error: Failed to grab frame.")
#             break
        
#         steering, processed_frame, finish = color_detection.process_frame(frame)

#         # cv2.imshow('RC Car Line Follower', processed_frame)
#         print(f"Steering: {steering:.2f} {'(FINISH DETECTED)' if finish else ''}")

#         cv2.imwrite("img.jpg", processed_frame)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     main()