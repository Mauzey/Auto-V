# import modules
import pyvjoy

class Vehicle():
    max_axis_value = 32767
    
    def __init__(self):
        # pyvjoy controller emulator
        self.controller = pyvjoy.VJoyDevice(1)
        
        # vehicle axis values
        self.axis = {
            'steering_angle': 0.5,
            'throttle_value': 0,
            'brake_value': 0
        }
        
        self.update()
        
        print('[INFO] Vehicle object initialised...')
    
    def set_axis(self, axis, value):
        self.axis[axis] = value
        self.update()
    
    def update(self):
        self.controller.data.wAxisX = int(self.axis['steering_angle'] * Vehicle.max_axis_value)
        self.controller.data.wAxisY = int(self.axis['throttle_value'] * Vehicle.max_axis_value)
        self.controller.data.wAxisZ = int(self.axis['brake_value'] * Vehicle.max_axis_value)
        
        self.controller.update()