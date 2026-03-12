# Task 2 – Perception System for RoboGambit

---

## Introduction

In this task, we implemented the **perception module** for the RoboGambit system.  
The goal of this module is to analyze an image of the physical chess board and determine the **current board configuration automatically**.

The system detects **ArUco markers placed on the pieces and board corners**, converts their pixel locations into real-world coordinates, and finally maps each piece to the correct square of the **6×6 chess board**.

This allows the robot system to understand the board state from a camera image and pass the detected board configuration to the game engine.

---

## Libraries Used

The perception system is implemented in **Python** using the following libraries:

- **OpenCV** – for image processing and ArUco marker detection  
- **NumPy** – for matrix operations and board representation  
- **sys** – for command line input

Example import section from the code:

```python
import cv2
import numpy as np
import sys

## Camera Calibration

To correctly interpret the image, the camera parameters are defined using a camera matrix.

This matrix contains the focal length and optical center of the camera.

Example from the implementation:

self.camera_matrix = np.array([
    [1030.4890823364258, 0, 960],
    [0, 1030.489103794098, 540],
    [0, 0, 1]
], dtype=np.float32)

self.dist_coeffs = np.zeros((1, 5))

The image is first undistorted before further processing.

Example:
undistorted = cv2.undistort(
    image,
    self.camera_matrix,
    self.dist_coeffs,
    None,
    self.camera_matrix
)
## ArUco Marker Detection

ArUco markers are used to identify both board corners and game pieces.

The OpenCV ArUco dictionary used is:

self.aruco_dict = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_4X4_50
)
The detector then scans the grayscale image for markers:
corners, ids, _ = self.detector.detectMarkers(gray)

Detected markers are also drawn on the image for visualization:
cv2.aruco.drawDetectedMarkers(undistorted, corners, ids)

## Board Corner Detection

Four markers are placed at the corners of the board to establish the board coordinate system.

Marker ID	Board Corner
21	Top Left
22	Bottom Left
23	Bottom Right
24	Top Right

These markers help compute a transformation between image coordinates and real-world board coordinates.

Example mapping in the code:

self.corner_world = {
    21: (350, 350),
    22: (350, -350),
    23: (-350, -350),
    24: (-350, 350)
}

## Pixel to World Coordinate Transformation

Once the corner markers are detected, the program computes a transformation that converts pixel positions into board coordinates.

Example:

self.H_matrix, _ = cv2.findHomography(pixel_pts, world_pts)


Then each marker center can be converted into world coordinates:

world = cv2.perspectiveTransform(pixel, self.H_matrix)


This step allows us to determine where each piece lies on the board.

## Board Representation

The detected board state is stored as a 6 × 6 NumPy array.

self.board = np.zeros((6, 6), dtype=int)


Each number represents a piece detected on that square.

For example:

[[0 0 0 0 0 0]
 [0 1 0 0 0 0]
 [0 0 0 7 0 0]
 [0 0 0 0 0 0]
 [0 0 3 0 0 0]
 [0 0 0 0 0 0]]

## Mapping Pieces to Board Squares

Once the world coordinates of a marker are known, they are converted into row and column positions on the board.

Example from the code:

col = int((x_coord - board_min) / square_size)
row = int((300 - y_coord) / square_size)


Values are then clamped to stay within the board limits:

if col < 0: col = 0
if col > 5: col = 5
if row < 0: row = 0
if row > 5: row = 5


Finally, the piece ID is placed in the board array:

self.board[row][col] = piece_id

## Visualizing the Board

To make the detected board easier to understand, a visual board representation is generated.

Each square is drawn using OpenCV and piece IDs are displayed inside the squares.

Example:

cv2.rectangle(board_img, (x1, y1),
              (x2, y2), (0, 0, 0), 2)

cv2.putText(board_img,
            str(piece),
            (x1 + 25, y1 + 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2)


This produces a visual grid showing the detected pieces.

## Running the Program

The perception program is executed from the command line by providing an image.

Example:

python perception.py image.png


The program then:

Loads the image

Detects all markers

Converts marker positions to board coordinates

Generates the board configuration

Displays the detected board

Example code from main():

path = sys.argv[1]

image = cv2.imread(path)

perception = RoboGambit_Perception()

perception.process_image(image)

## Output

Two windows are displayed:

Detected Markers – shows the camera image with detected markers.

Game Board – shows the reconstructed board state.

This allows us to visually verify whether pieces are placed correctly.

## Conclusion

In this task, we built a perception module capable of detecting a physical chess board configuration using ArUco markers. The system processes camera images, detects marker positions, converts them into board coordinates, and reconstructs the current game state.

This perception system acts as the bridge between the physical board and the RoboGambit chess engine, enabling the robot to understand the real-world board and make intelligent decisions based on the detected positions.


---


