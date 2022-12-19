# Python-extract-ros-bag
用python编写的提取ros bag包内的图片和相对应名称topic的信息

This script saves each topic in a bagfile as a csv or pictures.

Accepts a filename as an optional argument. Operates on all bagfiles in current directory if no argument provided

Usage1 (for one bag file):
	python extract_rosbag.py filename.bag
  
Usage 2 (for all bag files in current directory):
	python extract_rosbag.py
  
Written by Docky
