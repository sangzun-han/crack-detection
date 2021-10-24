import cv2
import numpy as np

class Marker:
  def detect_marker(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(
        gray, aruco_dict, parameters=parameters
    )
    return corners, ids
  
  def flatting(corners, ids):
    for i in range(len(ids)):
      if ids[i] == 1:
        #좌상
        topLeft = corners[i][0]
      if ids[i] == 2:
        #우상
        topRight = corners[i][0]
      if ids[i] == 3:
        #좌하
        bottomLeft = corners[i][0]
      if ids[i] == 4:
        #우하
        bottomRight = corners[i][0]

    # 각 마커의 바깥쪽 꼭지점을 뽑아내어 각 포인트에 저장
    tltl = (int(topLeft[0][0]), int(topLeft[0][1]))
    trtr = (int(topRight[1][0]), int(topRight[1][1]))
    blbl = (int(bottomLeft[3][0]), int(bottomLeft[3][1]))
    brbr = (int(bottomRight[2][0]), int(bottomRight[2][1]))
        
    # pts1 변환 전 사진의 네 좌표 좌상 우상 우하 좌하 순
    pts1 = np.float32([tltl, trtr, brbr, blbl])
    return pts1