import setup_path 
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


class Airsim_console():

    def __init__(self):
        print("Connecting to Airsim Client: ")
        self.client = airsim.CarClient()
        self.client.confirmConnection()
        print("Connection confirmed, Enabling Car controls ")
        self.client.enableApiControl(True)
        self.car_controls= airsim.CarControls()

        print("Car Controls enabled, Please enter Command parameters ")
        self.car_state=self.client.getCarState()
        self.mode = bool(input("Input car Mode: True (distance commands) " or "False"))
        if(self.mode):
            print("Going to Distance mode! ")
            pass
        else:
            self.repeat= int(input("How many repeats? " or "3"))
        self.record= bool(input("Record Images? " or "False"))
        self.fold= os.getcwd()+'/pictures3/'

        self.projectionMatrix = np.array([[1, 0.000000000, 0.000000000, -127.5000000000],
                              [0.000000000, 1, 0.000000000, -71.5000000000],
                              [0.000000000, 0.000000000, 1.00000000, 127.5 ],
                            [0.000000000, 0.000000000, -1/20.0000000, 0.000000000]])
    
        color = (0,255,0)
        self.rgb = "%d %d %d" % color

    def savePointCloud(self,image, fileName):
       f = open(fileName, "w")
       for x in range(image.shape[0]):
         for y in range(image.shape[1]):
            pt = image[x,y]
            if (math.isinf(pt[0]) or math.isnan(pt[0])):
              # skip it
              None
            else: 
              f.write("%f %f %f %s\n" % (pt[0], pt[1], pt[2]-1, self.rgb))
       f.close()

    def grab_images(self,idx2):
        responses = self.client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.DepthVis),  #depth visualization image
            airsim.ImageRequest("1", airsim.ImageType.DisparityNormalized, True), #depth in perspective projection
            #airsim.ImageRequest("1", airsim.ImageType.DepthPerspective, True), #depth in perspective projection
            airsim.ImageRequest("1", airsim.ImageType.Scene), #scene vision image in png format
            airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)])  #scene vision image in uncompressed RGBA array
        
        print('Retrieved images: %d', len(responses))

        for response in responses:
            filename = self.fold+'py' + str(idx2)
            if not os.path.exists(self.fold):
                os.makedirs(self.fold)

            if response.pixels_as_float:
                print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
                depth_img=response
                dimg_array=np.array(response.image_data_float).reshape(144,256)
                dimg2=copy.deepcopy(((dimg_array/(dimg_array.max()))*255).astype(np.uint8))
                dimg= Image.fromarray(dimg2)
                if dimg.mode != 'RGB':
                    dimg = dimg.convert('RGB')
                
                print("Saving Depth Image!")
                dimg.save(os.path.normpath(filename+'_depth.png'))
                dimg = dimg.convert('I')

                rawImage = self.client.simGetImage(0, airsim.ImageType.DepthPerspective,"")
                #png= np.array(rawImage[0].image_data_float,dtype=np.uint8).reshape(144,256)
                png = cv2.imdecode(np.frombuffer(rawImage, np.uint8) , cv2.IMREAD_UNCHANGED)
                gray = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)
                Image3D = cv2.reprojectImageTo3D(np.array(gray), self.projectionMatrix)
                print("Saving Point Cloud!")
                self.savePointCloud(np.array(Image3D), filename+'_cloudpoint.asc')

                #airsim.write_file(os.path.normpath(file_name+'_depth.png'),)
            elif response.compress: #png format
                print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
                #print(type(response.image_data_uint8))
                print("Saving RGB Image!")
                airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)
                img_data=Image.open(io.BytesIO(response.image_data_uint8))
                if img_data.mode != 'RGB':
                    img_data = img_data.convert('RGB')
                #img_data.show()

            else: #uncompressed array
                pass
                # print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
                # img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) #get numpy array
                # img_rgba = img1d.reshape(response.height, response.width, 4) #reshape array to 4 channel image array H X W X 4
                # img_rgba = np.flipud(img_rgba) #original image is flipped vertically
                # img_rgba[:,:,1:2] = 100 #just for fun add little bit of green in all pixels
                # airsim.write_png(os.path.normpath(filename + '.greener.png'), img_rgba) #write to png 

        self.img_data=img_data
        self.dimg=dimg

    def run_cmds(self):
        print("Starting systems! Please initialize :")
        cnt=0

        if(self.mode == False):
            while cnt<self.repeat:
                self.car_controls.throttle=float(input("Car Throttle (0-1): ") or "0")
                steer=input("Car Steering left or right : " or "forward")

                # check first if the brakes are on
                if(self.car_controls.brake ==1):
                    self.car_controls.brake = 0
                else:
                    pass

                if(steer == "left"):
                    self.car_controls.steering=-0.5
                elif(steer == "right"):
                    self.car_controls.steering=0.5
                elif(steer == "" or steer == "forward"):
                    self.car_controls.steering=0
                elif(steer=="brake"):
                    self.car_controls.brake= 1
                elif (steer == "reverse"):
                    self.car_controls.is_manual_gear = True;
                    self.car_controls.manual_gear = -1
                    self.car_controls.steering = 0
                
                self.client.setCarControls(self.car_controls)
                print("Go Forward")
                time.sleep(2)
                if(self.car_controls.is_manual_gear == True):
                    self.car_controls.is_manual_gear = False; # change back gear to auto
                    self.car_controls.manual_gear = 0  

                if(self.record==True):
                    self.grab_images(cnt)
                else:
                    pass


                cnt=cnt+1
        else:
            cmds= input("Please input commands (split by space): Throttle direction ")
              # check first if the brakes are on
            
            cmds_list= cmds.split(" ") 
            iterations= len(cmds_list)

            for cnt in range(0,iterations,2):
                print("Commands listed:", cmds_list[cnt:cnt+2])
                self.car_controls.throttle=float(cmds_list[cnt])
                #steer=input("Car Steering left or right : " or "forward")
                steer=cmds_list[cnt+1]
                # check first if the brakes are on
                if(self.car_controls.brake ==1):
                    self.car_controls.brake = 0
                else:
                    pass

                if(steer == "left"):
                    print("Go Left")
                    self.car_controls.steering=-0.5
                elif(steer == "right"):
                    print("Go Right")
                    self.car_controls.steering=0.5
                elif(steer == "" or steer == "forward"):
                    print("Go Forward")
                    self.car_controls.steering=0
                elif(steer=="brake"):
                    print("Braking!")
                    self.car_controls.brake= 1
                elif (steer == "reverse"):
                    print("reversing!")
                    self.car_controls.is_manual_gear = True;
                    self.car_controls.manual_gear = -1
                    self.car_controls.steering = 0
                
                elif (steer == "reverse_left"):
                    print("Reverse Left")
                    self.car_controls.steering=-0.5
                    self.car_controls.is_manual_gear = True;
                    self.car_controls.manual_gear = -1

                elif (steer == "reverse_right"):
                    print("Reverse Left")
                    self.car_controls.steering=0.5
                    self.car_controls.is_manual_gear = True;
                    self.car_controls.manual_gear = -1

                self.client.setCarControls(self.car_controls)
               
                time.sleep(2)
                if(self.car_controls.is_manual_gear == True):
                    self.car_controls.is_manual_gear = False; # change back gear to auto
                    self.car_controls.manual_gear = 0  

                if(self.record==True):
                    self.grab_images(cnt)
                else:
                    pass

            
def main():
    airsim_cons=Airsim_console()
    airsim_cons.run_cmds()


if __name__ == '__main__':
    main()