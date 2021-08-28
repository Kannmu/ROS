import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np
import json
from cv_bridge import CvBridge, CvBridgeError
import sys
import os
import time
# Read Image Filename And Sort
file_list = []
for filename in os.listdir(r'./Images'):
    filename = filename.split('.')[0]
    file_list.append(filename)
# print(file_list)
file_list = list(map(int, file_list))
file_list.sort()
file_list = list(map(str, file_list))
# print(file_list)
# sys.exit()
PubEnable = True
def ImagePub():
    global PubEnable
    rospy.init_node('img_publisher', anonymous=True)
    # rospy.init_node('pub_enable_subscriber', anonymous=True)
    img_pub = rospy.Publisher('image', Image, queue_size=2)
    # rospy.Subscriber('pub_enable',bool,PubEnable_Callback)
    rate = rospy.Rate(30) #Chane Frequence
    bridge = CvBridge()
    count = 0
    while ((not rospy.is_shutdown()) and (PubEnable)):
        Content = read_config()
        # print(Content)
        PubEnable = ((Content['Enable'] == str(True)) or (Content['Enable'] == "true"))
        ImgSize = list(map(int,Content['Image Size'].split()))
        # print(ImgSize)
        # print(type(Content['Enable']))
        # print(PubEnable)


        for i in file_list:
            img = read_images(i,ImgSize)
            msg = bridge.cv2_to_imgmsg(img, encoding="bgr8")
            img_pub.publish(msg)
            rate.sleep()

def read_images(i,ImgSize):
    img = cv2.imread("./Images/"+i+'.jpg') #Change Format
    img = cv2.resize(img,(ImgSize[0],ImgSize[1])) #Img Size
    # print(i)
    # cv2.imshow('image',img)
    return img

def read_config():
    with open('./Config/Config.json') as json_file:
        config = json.load(json_file)['Publisher']
    return config
    
if __name__ == '__main__':
    try:
        ImagePub()
    except rospy.ROSInterruptException:
        pass
