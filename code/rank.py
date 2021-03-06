# importing the needed bindings
from descriptor import DescribeTexture
from descriptor import DescribeColor
from descriptor import ColorTree
from ranker import Ranker
import shutil
import argparse
import copy
import cv2
import os

# instantiating the classes for color, texture and tree description
cdes = DescribeColor((16, 32, 1))
txdes = DescribeTexture()
tdes = ColorTree([6])

# building the argument parser and parse the command line arguments
argprse = argparse.ArgumentParser()
argprse.add_argument("-d", "--dataset", required = True,
	help = "FilePath to the folder that has target images to be indexed")
argprse.add_argument("-c", "--hsv", required = True,
	help = "File Path where the computed hsv index is saved")
argprse.add_argument("-t", "--texture", required = True,
	help = "File Path where the computed texture index is saved")
argprse.add_argument("-b", "--btree", required = True,
	help = "File Path where the computed tree index is saved")
argprse.add_argument("-q", "--query", required = True,
	help = "File Path to the query image")
argmnts = vars(argprse.parse_args())

# loading the query image and describing its color, texture and tree features
query_img = cv2.imread(argmnts["query"])
cfeats = cdes.describe_color(copy.copy(query_img))
texture = txdes.describe_texture(copy.copy(query_img))
tree = tdes.color_tree(copy.copy(query_img))
 
# ranking the images in our dataset based on the query image
ranker = Ranker(argmnts["hsv"], argmnts["texture"], argmnts["btree"])
final_results = ranker.rank(cfeats, texture, tree)

current_path = os.path.dirname(os.path.abspath(__file__))

# iterating over the final results
for (score, resID) in final_results:
	# printing the image names in the order of increasing score
	print resID + "    "+ str(score)
	source_path = argmnts["dataset"]+"/"+ resID
	dest_path = current_path+"/result/"+resID
	shutil.copy2(source_path,dest_path)

