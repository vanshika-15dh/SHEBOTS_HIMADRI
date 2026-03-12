import cv2
import numpy as np
import sys


class RoboGambit_Perception:

    def __init__(self):

        self.camera_matrix = np.array([
            [1030.4890823364258, 0, 960],
            [0, 1030.489103794098, 540],
            [0, 0, 1]
        ], dtype=np.float32)

        self.dist_coeffs = np.zeros((1, 5))

        self.corner_world = {
            21: (350, 350),
            22: (350, -350),
            23: (-350, -350),
            24: (-350, 350)
        }

        self.corner_pixels = {}
        self.H_matrix = None

        self.board = np.zeros((6, 6), dtype=int)

        self.aruco_dict = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_4X4_50
        )

        self.aruco_params = cv2.aruco.DetectorParameters()

        self.detector = cv2.aruco.ArucoDetector(
            self.aruco_dict,
            self.aruco_params
        )

        print("Perception Initialized")


    def prepare_image(self, image):

        undistorted = cv2.undistort(
            image,
            self.camera_matrix,
            self.dist_coeffs,
            None,
            self.camera_matrix
        )

        gray = cv2.cvtColor(undistorted, cv2.COLOR_BGR2GRAY)

        return undistorted, gray


    def pixel_to_world(self, px, py):

        if self.H_matrix is None:
            return None, None

        pixel = np.array([[[px, py]]], dtype=np.float32)

        world = cv2.perspectiveTransform(pixel, self.H_matrix)

        return world[0][0][0], world[0][0][1]


    def process_image(self, image):

        self.board[:] = 0

        undistorted, gray = self.prepare_image(image)

        corners, ids, _ = self.detector.detectMarkers(gray)

        if ids is None:
            print("No markers detected")
            return

        ids = ids.flatten()

        cv2.aruco.drawDetectedMarkers(undistorted, corners, ids)

        self.corner_pixels = {}

        for i, marker_id in enumerate(ids):

            marker_corners = corners[i][0]

            cx = int((marker_corners[0][0] + marker_corners[2][0]) / 2)
            cy = int((marker_corners[0][1] + marker_corners[2][1]) / 2)

            if marker_id in self.corner_world:
                self.corner_pixels[marker_id] = (cx, cy)

        pixel_pts = []
        world_pts = []

        for marker_id in [21, 22, 23, 24]:

            if marker_id in self.corner_pixels:

                px, py = self.corner_pixels[marker_id]
                wx, wy = self.corner_world[marker_id]

                pixel_pts.append([px, py])
                world_pts.append([wx, wy])

        if len(pixel_pts) < 4:
            print("Not enough corner markers")
            return

        pixel_pts = np.array(pixel_pts, dtype=np.float32)
        world_pts = np.array(world_pts, dtype=np.float32)

        self.H_matrix, _ = cv2.findHomography(pixel_pts, world_pts)

        for i, marker_id in enumerate(ids):

            if 1 <= marker_id <= 10:

                marker_corners = corners[i][0]

                cx = int((marker_corners[0][0] + marker_corners[2][0]) / 2)
                cy = int((marker_corners[0][1] + marker_corners[2][1]) / 2)

                wx, wy = self.pixel_to_world(cx, cy)

                if wx is not None:
                    self.place_piece_on_board(marker_id, wx, wy)

        res = cv2.resize(undistorted, (1152, 648))
        cv2.imshow("Detected Markers", res)

        self.visualize_board()


    def place_piece_on_board(self, piece_id, x_coord, y_coord):

    # Board parameters
        board_min = -300
        square_size = 100

    # Convert world coordinate to board grid
        col = int((x_coord - board_min) / square_size)
        row = int((300 - y_coord) / square_size)

    # Clamp values inside board
        if col < 0: col = 0
        if col > 5: col = 5
        if row < 0: row = 0
        if row > 5: row = 5

        self.board[row][col] = piece_id


    def visualize_board(self):

        cell_size = 80

        board_img = np.ones((6 * cell_size, 6 * cell_size, 3),
                            dtype=np.uint8) * 255

        for r in range(6):

            for c in range(6):

                x1 = c * cell_size
                y1 = r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                cv2.rectangle(board_img, (x1, y1),
                              (x2, y2), (0, 0, 0), 2)

                piece = int(self.board[r][c])

                if piece != 0:

                    cv2.putText(board_img,
                                str(piece),
                                (x1 + 25, y1 + 50),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (0, 0, 255),
                                2)

        cv2.imshow("Game Board", board_img)


def main():

    if len(sys.argv) < 2:
        print("Usage: python perception.py image.png")
        return

    path = sys.argv[1]

    image = cv2.imread(path)

    if image is None:
        print("Failed to load image")
        return

    perception = RoboGambit_Perception()

    perception.process_image(image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
