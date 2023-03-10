# -*- coding: utf-8 -*-
"""Computer_vision.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13-_svwDlyf9wipV0VnRIEcjxo5lmpCwD

# Trial Code

Using SLAM technique to convert 2d video into point cloud
"""

pip install torch opencv-python open3d

"""Converting vid from drive to point cloud

"""

from google.colab import drive
drive.mount('/content/drive')

import torch
import cv2
import open3d as o3d
import numpy as np
from google.colab.patches import cv2_imshow

fx = 3717.26220
cx = 398.55759
fy = 3717.26220
cy = 2246.47705
# Define camera intrinsic matrix (perform camera calibration for DC MTP8450 LRF SPI)
K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])

# Define feature extractor and matcher
# Create an orb (feature finder)
orb = cv2.ORB_create(nfeatures=5000)
# BFMatcher (returns closest match)
bf_matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True) #hamming distance between strings


# # Initializing Open3D visualization window for showing point cloud 
# vis = o3d.visualization.Visualizer()
# vis.create_window()

# Initialize SLAM state variables
map_points = o3d.geometry.PointCloud()
keyframes = []
# Open video file
cap = cv2.VideoCapture('/content/drive/MyDrive/make-a-thon/IMG_1606.MOV')

frame_num = 0
while cap.isOpened():
    # Read frame from video
    ret, frame = cap.read()
    #ret is bollean that checks if the frame was read successfully
    if not ret:
        break

    print(frame_num, " is being dealt with \n")
    frame_num += 1
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #detecting key points
    kp = orb.detect(gray)
    #cv2_imshow( gray)

    if len(kp) < 100:
        # Not enough keypoints, skip frame
        continue

    # Compute descriptors for the key frames
    kp, des = orb.compute(gray, kp)

    #Checking if this is the first frame
    if not keyframes:
        # create point cloud file and append if first frame
        map_points.points = o3d.utility.Vector3dVector(np.zeros((0, 3)))
        keyframes.append((kp, des))
        continue

    #get the previous frame and descriptions
    prev_kp, prev_des = keyframes[-1]
    #match current frame with previous frame and get matches
    matches = bf_matcher.match(prev_des, des)

    if len(matches) < 10:
        # Not enough matches, skip frame
        continue

    # Estimate essential matrix and recover pose
    prev_pts = np.float32([prev_kp[m.queryIdx].pt for m in matches])
    cur_pts = np.float32([kp[m.trainIdx].pt for m in matches])
    # essential matrix correlates two camera frames using the intrinsic matrix
    E, mask = cv2.findEssentialMat(cur_pts, prev_pts, K)
    #get relative position between the two frames using a RANSAC algorithm
    _, R, t, mask = cv2.recoverPose(E, cur_pts, prev_pts, K)

    # triangulate the 3D points 
    cur_pts_3d = cv2.triangulatePoints(np.eye(3, 4), np.hstack((R, t)), prev_pts.T, cur_pts.T).T
    cur_pts_3d /= cur_pts_3d[:, 3][:, None]

    # making the point cloud 
    map_points.points = o3d.utility.Vector3dVector(np.vstack((map_points.points, cur_pts_3d[:, :3])))

    #update our key frames matrix
    keyframes.append((kp, des))

    # # Visualize map and camera pose
    # vis.clear_geometries()
    # vis.add_geometry(map_points)
    # cam = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.2)
    # cam.transform(np.hstack((R, t)))
    # vis.add_geometry(cam)
    # vis.poll_events()
    # vis.update_renderer()

# Free memory
cap.release()
#vis.close()
# saving the point cloud file
# Create point cloud
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(map_points.points)

# Save point cloud as .ply file
o3d.io.write_point_cloud("point_cloud.ply", pcd)

"""# File Convert"""

!pip install trimesh

!pip install pygltflib

!pip install open3d==0.13.0

!pip install pygltf

import open3d as o3d
import trimesh
import pygltflib

# Load point cloud from file
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(map_points.points)

# Convert to Trimesh
mesh = o3d.geometry.TriangleMesh.from_legacy_pointcloud(pcd)

# Save as GLB
mesh.export("point_cloud.glb")

import numpy as np
import pygltflib
import open3d as o3d

# Load point cloud from PLY file
pcd = o3d.io.read_point_cloud("point_cloud.ply")

# Convert point cloud to a Numpy array
points = np.asarray(pcd.points)

# Create mesh object using the numpy array
mesh = pygltflib.Mesh.from_vertices(points)

# Save mesh object as GLB file
pygltflib.write_glb("point_cloud.glb", [mesh])

import open3d as o3d
import pygltf
import numpy as np

# Load the PLY file as a point cloud
pcd = o3d.io.read_point_cloud("locker.ply")

# Convert the point cloud to a mesh
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd)

# Get the vertices and faces from the mesh
vertices = np.asarray(mesh.vertices)
faces = np.asarray(mesh.triangles)

# Create a GLTF mesh from the vertices and faces
gl_mesh = pygltf.Mesh.from_primitives([pygltf.Primitive(
    attributes={
        'POSITION': pygltf.Accessor(
            component_type=pygltf.Accessor.FLOAT,
            count=len(vertices),
            data=vertices.ravel().tolist(),
            type=pygltf.TYPE_VEC3,
        )
    },
    indices=pygltf.Accessor(
        component_type=pygltf.Accessor.UNSIGNED_INT,
        count=len(faces) * 3,
        data=faces.ravel().tolist(),
    ),
    mode=pygltf.Primitive.TRIANGLES,
)])

# Create a GLTF scene with the mesh
gl_scene = pygltf.Scene(name='Scene', nodes=[
    pygltf.Node(mesh=gl_mesh),
])

# Create a GLTF file with the scene
glb = pygltf.GLTF(
    scene=0,
    scenes=[gl_scene],
    asset=pygltf.Asset(version='2.0'),
)

# Write the GLB file
pygltf2.write_glb('locker.glb', glb)

"""# Learning"""

map_points = o3d.geometry.PointCloud()
keyframes = []
# Open video file
cap = cv2.VideoCapture('/content/drive/MyDrive/make-a-thon/IMG_1606.MOV')

assert cap.isOpened()
orb = cv2.ORB_create(nfeatures=100)
# read in 10 frames into an array
F = [cap.read()[1] for i in range(10)]
# conver them to gray
G= [cv2.cvtColor(g, cv2.COLOR_BGR2GRAY) for g in F]
# compute keyfranes
keyframes = [orb.detect(k) for k in G]
des = [orb.compute(g, kp)[1] for g,kp in zip(G, keyframes)]

for i in range(1,10):
  B = bf_matcher.match(des[i], des[i-1])
  print(len(B))


 
    
    # Estimate essential matrix and recover pose
    #prev_pts = np.float32([prev_kp[m.queryIdx].pt for m in matches])
    #cur_pts = np.float32([kp[m.trainIdx].pt for m in matches])
    # essential matrix correlates two camera frames using the intrinsic matrix

!apt-get install -y xvfb x11-utils
!pip install pyvirtualdisplay

from pyvirtualdisplay import Display
from IPython import display as ipythondisplay

display = Display(visible=0, size=(1024, 768))
display.start()

"""Displaying random point cloud"""

import open3d as o3d

# create a point cloud
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(np.random.rand(100, 3))

# create an offscreen renderer
renderer = o3d.visualization.O3DOffscreenRenderer(800, 600)

# create a visualizer and set the geometry
vis = o3d.visualization.Visualizer(renderer)
vis.create_window()
vis.add_geometry(pcd)

# render the scene and save the image
vis.poll_events()
vis.update_renderer()
image = renderer.capture_screen_float_buffer(do_render=True)
o3d.io.write_image("pointcloud.png", image)

B[0]

list(a)

list(b)

|

[x*x for x in range(10)]

X=[1,2,3]
A=['foo', 'bar', 'c']

for i in range(3):
  print(str(X[i]) + A[i])

list(zip(X, A))

[str(x)+a for x,a in zip(X,A)]

[str(Q[0])+Q[1] for Q in zip(X,A)]

Q=(1,2)

a,b=Q

a

b



"""# **Room Tone**

Installation
"""

pip install torch opencv-python open3d

"""Cloud server that contains the file"""

from google.colab import drive
drive.mount('/content/drive')

"""Importing all files"""

import torch
import cv2
import open3d as o3d
import numpy as np
from google.colab.patches import cv2_imshow

"""Setting the intrinsic matrix of the camera (obtained by caliberation)"""

fx = 3717.26220
cx = 398.55759
fy = 3717.26220
cy = 2246.47705
# Define camera intrinsic matrix (perform camera calibration for DC MTP8450 LRF SPI)
K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])

"""Setting up variables for using SLAM technique """

# Define feature extractor and matcher
# Create an orb (feature finder)
orb = cv2.ORB_create(nfeatures=1000)
# BFMatcher (returns closest match)
bf_matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True) #hamming distance between strings

# Initialize SLAM state variables
map_points = o3d.geometry.PointCloud()
keyframes = []
# Open video file
cap = cv2.VideoCapture('/content/drive/MyDrive/make-a-thon/IMG_1608.MOV')

"""Looping through the frames of the video. 
Steps:


1.   Find features of the frame
2.   Correlate the frame to the previous frame if possible
3.   Define the homogeneous rotation and translation matrix of movement
4.   Triangulation of 3D points


"""

num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print("Number of frames: ", num_frames)
print("\nEstimated time is ", num_frames/240," minutes to ", num_frames/180," minutes")
while cap.isOpened():
    # Read frame from video
    ret, frame = cap.read()
    #ret is bollean that checks if the frame was read successfully
    if not ret:
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #detecting key points
    kp = orb.detect(gray)
    #cv2_imshow( gray)

    if len(kp) < 100:
        # Not enough keypoints, skip frame
        continue

    # Compute descriptors for the key frames
    kp, des = orb.compute(gray, kp)

    #Checking if this is the first frame
    if not keyframes:
        # create point cloud file and append if first frame
        map_points.points = o3d.utility.Vector3dVector(np.zeros((0, 3)))
        keyframes.append((kp, des))
        continue

    #get the previous frame and descriptions
    prev_kp, prev_des = keyframes[-1]
    #match current frame with previous frame and get matches
    matches = bf_matcher.match(prev_des, des)

    if len(matches) < 10:
        # Not enough matches, skip frame
        continue

    # Estimate essential matrix and recover pose
    prev_pts = np.float32([prev_kp[m.queryIdx].pt for m in matches])
    cur_pts = np.float32([kp[m.trainIdx].pt for m in matches])
    # essential matrix correlates two camera frames using the intrinsic matrix
    E, mask = cv2.findEssentialMat(cur_pts, prev_pts, K)
    #get relative position between the two frames using a RANSAC algorithm
    _, R, t, mask = cv2.recoverPose(E, cur_pts, prev_pts, K)

    # triangulate the 3D points 
    cur_pts_3d = cv2.triangulatePoints(np.eye(3, 4), np.hstack((R, t)), prev_pts.T, cur_pts.T).T
    cur_pts_3d /= cur_pts_3d[:, 3][:, None]

    # making the point cloud 
    map_points.points = o3d.utility.Vector3dVector(np.vstack((map_points.points, cur_pts_3d[:, :3])))

    #update our key frames matrix
    keyframes.append((kp, des))

"""Saving the file as plot cloud"""

# Free memory
cap.release()

# Save point cloud as .ply file
o3d.io.write_point_cloud("gb_room.ply", map_points)

np.version.version

