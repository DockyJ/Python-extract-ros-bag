'''
This script saves each topic in a bagfile as a csv or pictures.

Accepts a filename as an optional argument. Operates on all bagfiles in current directory if no argument provided

Usage1 (for one bag file):
	python extract_rosbag.py filename.bag
Usage 2 (for all bag files in current directory):
	python extract_rosbag.py

Written by Docky

'''

#coding:utf-8

import rosbag, roslib, rospy
import sys, csv, cv2
import os, time, string
import shutil
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from cv_bridge import CvBridgeError


#verify correct input arguments: 1 or 2
if (len(sys.argv) > 2):
	print("invalid number of arguments: " + str(len(sys.argv)))
	print("should be 2: 'extract_rosbag.py' and the name of the bag files")
	print("or just 1  : 'extract_rosbag.py'")
	sys.exit(1)
elif (len(sys.argv) == 2):
	listOfBagFiles = [sys.argv[1]]
	numberOfFiles = "1"
	print("reading only 1 bagfile: " + str(listOfBagFiles[0]))
elif (len(sys.argv) == 1):
	listOfBagFiles = [f for f in os.listdir(".") if f[-4:] == ".bag"]	#get list of only bag files in current dir.
	numberOfFiles = str(len(listOfBagFiles))
	print("reading all " + numberOfFiles + " bagfiles in current directory: \n")
	for f in listOfBagFiles:
		print(f)
	print("\n press ctrl+c in the next 10 seconds to cancel \n")
	time.sleep(10)
else:
	print("bad argument(s): " + str(sys.argv))
	sys.exit(1)


bridge = CvBridge()
count = 0
for bagFile in listOfBagFiles:
	count += 1
	print("\nreading file " + str(count) + " of " + numberOfFiles + ": " + bagFile)
	#access bag
	bag = rosbag.Bag(bagFile)
	bagContents = bag.read_messages()
	bagName = bag.filename		#/media/zhkj-robot/2021-01-09-14-46-26.bag


	#create a new directory string.rstrip(bagName, ".bag")
	folder_bag = string.rstrip(bag.filename, ".bag")
	try:	#else already exists
		os.makedirs(folder_bag)
	except:
		pass
	shutil.copyfile(bagName, folder_bag + '/' + bagName)
	print("\nCopied '" + bagName + "' to " + folder_bag)


	#get list of topics from the bag
	listOfTopics = []
	for topic, msg, t in bagContents:
		if topic not in listOfTopics:
			listOfTopics.append(topic)


	for topicName in listOfTopics:
		if topicName == "/camera_0/image/compressed":
			print("\nReading messages from " + topicName)
			for subtopic, msg, t in bag.read_messages(topicName):
				folder = string.rstrip(msg.header.frame_id)
				try:	#else already exists
					os.makedirs(folder_bag + '/' +folder)
				except:
					pass
				cv_image = bridge.compressed_imgmsg_to_cv2(msg, 'bgr8')
				timestr = "%.6f" %  msg.header.stamp.to_sec()
				image_name = timestr + '.jpg'	# an extension is necessary
				rgb_0_path = folder_bag + '/' + folder + '/'
				cv2.imwrite(rgb_0_path + image_name, cv_image)
				#print(rgb_0_path + image_name)
			print("Done extracting messages from " + topicName)

		elif topicName == "/camera_1/image/compressed":
			print("\nReading messages from " + topicName)
			for subtopic, msg, t in bag.read_messages(topicName):
				folder = string.rstrip(msg.header.frame_id)
				try:	#else already exists
					os.makedirs(folder_bag + '/' +folder)
				except:
					pass
				cv_image = bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
				timestr = "%.6f" %  msg.header.stamp.to_sec()
				image_name = timestr + '.jpg'	
				rgb_1_path = folder_bag + '/' + folder + '/'
				cv2.imwrite(rgb_1_path + image_name, cv_image)
				#print(rgb_1_path + image_name)
			print("Done extracting messages from " + topicName)

		if topicName == "/BMI088": 
			print("\nReading messages from " + topicName)
			#Create a new CSV file for each topic folder + '/' +string.replace(topicName, '/', '_slash_') + '.csv'
			filename = folder_bag + '/' + topicName.split('/')[-1] + '.csv'
			with open(filename, 'w+') as csvfile:
				filewriter = csv.writer(csvfile, delimiter = ',')
				firstIteration = True	#allows header row
				for subtopic, msg, t in bag.read_messages(topicName):	# for each instant in time that has data for topicName
					#parse data from this instant, which is of the form of multiple lines of "Name: value\n"
					# - put it in the form of a list of 2-element lists
					msgString = str(msg)
					msgList = msgString.split('\n')
					instantaneousListOfData = []
					for nameValuePair in msgList:
						splitPair = nameValuePair.split(':')
						for i in range(len(splitPair)):	#should be 0 to 1
							splitPair[i] = splitPair[i].strip()
						instantaneousListOfData.append(splitPair)
					#write the first row from the first element of each pair
					if firstIteration:	# header
						headers = ["rosbagTimestamp"]	#first column header
						for pair in instantaneousListOfData:
							headers.append(pair[0])
						filewriter.writerow(headers)
						firstIteration = False
					# write the value from each pair to the file
					values = [str(t)]	#first column will have rosbag timestamp
					for pair in instantaneousListOfData:
						if len(pair) > 1:
							values.append(pair[1])
					filewriter.writerow(values)
			print("Done extracting messages from " + topicName)


		elif topicName == "/GPS_fix": 
			print("\nReading messages from " + topicName)
			#Create a new CSV file for each topic folder + '/' +string.replace(topicName, '/', '_slash_') + '.csv'
			filename = folder_bag + '/' + topicName.split('/')[-1] + '.csv'
			with open(filename, 'w+') as csvfile:
				filewriter = csv.writer(csvfile, delimiter = ',')
				firstIteration = True	#allows header row
				for subtopic, msg, t in bag.read_messages(topicName):	# for each instant in time that has data for topicName
					#parse data from this instant, which is of the form of multiple lines of "Name: value\n"
					# - put it in the form of a list of 2-element lists
					msgString = str(msg)
					msgList = msgString.split('\n')
					instantaneousListOfData = []
					for nameValuePair in msgList:
						splitPair = nameValuePair.split(':')
						for i in range(len(splitPair)):	#should be 0 to 1
							splitPair[i] = splitPair[i].strip()
						instantaneousListOfData.append(splitPair)
					#write the first row from the first element of each pair
					if firstIteration:	# header
						headers = ["rosbagTimestamp"]	#first column header
						for pair in instantaneousListOfData:
							headers.append(pair[0])
						filewriter.writerow(headers)
						firstIteration = False
					# write the value from each pair to the file
					values = [str(t)]	#first column will have rosbag timestamp
					for pair in instantaneousListOfData:
						if len(pair) > 1:
							values.append(pair[1])
					filewriter.writerow(values)
			print("Done extracting messages from " + topicName)
	bag.close()
print "\n Done reading all " + numberOfFiles + " bag file."
