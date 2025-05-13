from gpiozero import PWMOutputDevice, Servo, Device
from gpiozero.pins.rpigpio import RPiGPIOFactory

class DRCMotorController:
    def __init__(self, motorPin, servoPin):
        # GPIO13 & GPIO12 preferable
        # self.motor = PWMOutputDevice(pin=motorPin, frequency=100)
        Device.pin_factory = RPiGPIOFactory()
        self.servo = Servo(servoPin)  
        pass

    def setDrivingMotor(self, speed):
        # speed taken in between 0 and 1 - still to decide how to do this
        pass

    def setServoMotor(self, angle):
        # angle from 0 to 1 with gpiozero
        self.servo.value = angle
        pass

    def off (self):
        # self.motor.off()
        self.servo.off()
        pass
    
    def on (self):
        # self.motor.on()
        self.servo.on()
        pass


