import airsim

import time
import os
import numpy as np
from PIL import Image
import argparse
import sys
import io
import cv2
import math
import copy
import base64
import skimage
import time
from datetime import datetime
import io

class airsim_data():
    def __init__(self):
        print("Establishing connection to airsim!")
        self.client= airsim.CarClient()
        self.client.confirmConnection()
        self.rover_state= self.client.getCarState()

        print("Establishing Car controls")
        self.client.enableApiControl(True)
        self.rover_controls= airsim.CarControls()

        print("Car Controls enabled")

        # Include example json of this will look?
        # rgb and depth will be in bytecode
        # IMU: 
        imu_dict={
                    "speed":None,
                    "px":None,
                    "py": None,
                    "pz":None,
                    "ow":None,
                    "ox": None,
                    "oy": None,
                    "oz": None
                }
        self.data_dict={
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "rgb": None,
                        "depth": None,
                        "imu": imu_dict
                        }
       
    def encode_img(self,image):
        # Convert the image into ubyte format!
        with io.BytesIO() as output_bytes:
            p_image=Image.fromarray(skimage.img_as_ubyte(image))
            p_image.convert('RGB')
            p_image.save(output_bytes,'JPEG')
            bytes_data= output_bytes.getvalue()

        # Encode it into base64 string since Json doesn't like his bytes
        base_str= str(base64.b64encode(bytes_data),'utf-8')

        return base_str

    def extract_images(self,mode=["RGB"]):
        """
            Get the images from airsim according to modality!
        """
        imgs=[]
        print("Gathering requests!")

        for modes in mode:
            if(modes=="RGB"):
                # Grab RGB data accordingly
                print("Getting the RGB data")
                imgs.append(airsim.ImageRequest("1",airsim.ImageType.Scene))
            
            if(modes=="Depth"):
                print("Getting the Depth Data")
                imgs.append(airsim.ImageRequest("0",airsim.ImageType.DepthVis))

        requests= self.client.simGetImages(imgs)

        print("Requests completed, processing data!")

        for req in requests:
            if(req.pixels_as_float):
                print("Processing the Depth Image")
                dimg_array = np.array(req.image_data_float)  
                dimg_encoded= self.encode_img(dimg_array)
                self.data_dict["depth"]= dimg_encoded
                print("Completed Processing Depth")

            elif(req.compress):
                print("Processing the RGB Image")
                img_array= Image.open(io.BytesIO(req.image_data_uint8))
                img_encoded= self.encode_img(np.array(img_array.convert('RGB')))
                self.data_dict["rgb"]= img_encoded


    def extract_imu(self):
        # Grab the car state kinematics
        position= self.rover_state.kinematics_estimated.position
        oriented= self.rover_state.kinematics_estimated.orientation
        self.data_dict["imu"]["speed"]=self.rover_state.speed
        self.data_dict["imu"]["px"]=position.x_val
        self.data_dict["imu"]["py"]=position.y_val
        self.data_dict["imu"]["pz"]=position.z_val

        # Sounds like that hurt!
        self.data_dict["imu"]["ow"]=oriented.w_val
        self.data_dict["imu"]["ox"]=oriented.x_val
        self.data_dict["imu"]["oy"]=oriented.y_val
        self.data_dict["imu"]["oz"]=oriented.z_val


    def run(self,steps=12,throttle=0.3):
        ## To run the simulation, let's have the car just move
        # forward until it falls off!
        for cnt in range(0,steps):

            if(steps% 2 ==0):
                self.rover_controls.brake=1
            else:
                self.rover_controls.brake=0

            self.rover_controls.throttle=float(throttle)
            
            # car goes forward
            self.rover_controls.steering= 0


            self.client.setCarControls(self.rover_controls)

            # Grab data while we are at it!
            # What's the time sir?
            print("Processing the data!")
            self.data_dict["time"]= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.extract_images(mode=["RGB","Depth"])
            self.extract_imu()
            print("Data currently recorded is:",self.data_dict)
            time.sleep(2)


def main():
    # Call Airsim. (Have him on speed dial)
    pkg=airsim_data()
    pkg.run()

main()