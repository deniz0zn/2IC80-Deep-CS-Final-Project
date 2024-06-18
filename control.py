from onvif import ONVIFCamera
from time import sleep
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO)

class CameraControl:
    def __init__(self, ip, port, username, password, wsdl_path):
        logging.info(f"Initializing camera at IP: {ip}, Port: {port}")
        self.camera = ONVIFCamera(ip, port, username, password, wsdl_path)
        self.media_service = self.camera.create_media_service()
        self.ptz_service = self.camera.create_ptz_service()
        self.profile = self.media_service.GetProfiles()[0]  # Using the first profile
        self.token = self.profile.token
        self.ptz_token = self.profile.PTZConfiguration.token
        logging.info("Camera initialized successfully")

    def perform_move(self, ptz_service, request):
        """ Helper function to perform move operation """
        logging.info(f"Performing move with parameters: {request.Velocity}")
        ptz_service.ContinuousMove(request)
        # Assuming we want the command to take effect for 1 second
        sleep(1)
        ptz_service.Stop({'ProfileToken': request.ProfileToken})
        logging.info("Move completed and stopped")

    def move_tilt(self, velocity):
        """ Move the camera in tilt direction """
        logging.info(f"Moving tilt with velocity: {velocity}")
        request = self.ptz_service.create_type('ContinuousMove')
        request.ProfileToken = self.token
        request.Velocity = {'PanTilt': {'x': 0, 'y': velocity}}
        self.perform_move(self.ptz_service, request)

    def move_pan(self, velocity):
        """ Move the camera in pan direction """
        logging.info(f"Moving pan with velocity: {velocity}")
        request = self.ptz_service.create_type('ContinuousMove')
        request.ProfileToken = self.token
        request.Velocity = {'PanTilt': {'x': velocity, 'y': 0}}
        self.perform_move(self.ptz_service, request)

    def zoom(self, velocity):
        """ Zoom in or out """
        logging.info(f"Zooming with velocity: {velocity}")
        request = self.ptz_service.create_type('ContinuousMove')
        request.ProfileToken = self.token
        request.Velocity = {'Zoom': {'x': velocity}}
        self.perform_move(self.ptz_service, request)

# Example of usage
if __name__ == '__main__':
    cam_control = CameraControl('192.168.88.123', 8080, 'admin', '123456', r"C:\Users\ozndn\Downloads\specs-development\specs-development\wsdl\ver10\device\wsdl")
    cam_control.move_pan(0.5)  # Move camera to the right
    cam_control.move_tilt(0.2)  # Move camera upward
    cam_control.zoom(1)  # Zoom in
