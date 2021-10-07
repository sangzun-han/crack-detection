import numpy as np
import cv2
from matplotlib import pyplot as plt

# 마우스 콜백 함수: 연속적인 원을 그리기 위한 콜백 함수


def DrawConnectedCircle(event, x, y, flags, param):
    global drawing
    # 마우스 왼쪽 버튼이 눌리면 드로윙을 시작함
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        cv2.circle(dst, (x, y), 6, (0, 0, 255), -1)
        points.append((x, y))
        print(x, y)
        if len(points) > 1:
            for i in range(len(points)-1):
                cv2.line(dst, points[i], points[i+1], (255, 0, 255), 2)
            length_set.append(((points[len(points)-1][0]-points[len(points)-2][0])**2 + (
                points[len(points)-1][1]-points[len(points)-2][1])**2)**(1/2))
            total_length = round((marker_length*sum(length_set))/std_length, 4)
            cv2.rectangle(dst, (547, 8), (686, 34), (255, 255, 255), -1)
            cv2.putText(dst, str(total_length)+"CM", (550, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        drawing = False

    # 마우스 왼쪽 버튼을 떼면 드로윙을 종료함
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False


input_path = "input_img/flattening/"
output_path = "output_img/flattening/"
img_name = "test2"
extension = ".png"
marker_length = 3.1
img = cv2.imread(input_path + img_name + extension)
# [x,y] 좌표점을 4x2의 행렬로 작성


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()
corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(
    gray, aruco_dict, parameters=parameters)
frame_markers = cv2.aruco.drawDetectedMarkers(img.copy(), corners, ids)


for i in range(len(ids)):
    c = corners[i][0]
    plt.plot([c[:, 0].mean()], [c[:, 1].mean()],
             "o", label="id={0}".format(ids[i]))
    if ids[i][0] == 1:
        ap = [c[0, 0], c[0, 1]]
    if ids[i][0] == 2:
        cp = [c[1, 0], c[1, 1]]
    if ids[i][0] == 3:
        bp = [c[3, 0], c[3, 1]]
    if ids[i][0] == 4:
        dp = [c[2, 0], c[2, 1]]


# 좌표점은 좌상->좌하->우상->우하
pts1 = np.float32([ap, bp, cp, dp])

# 좌표의 이동점
pts2 = np.float32([[60, 60], [60, 1050], [1050, 60], [1050, 1050]])

# pts1의 좌표에 표시. perspective 변환 후 이동 점 확인.

M = cv2.getPerspectiveTransform(pts1, pts2)

dst = cv2.warpPerspective(img, M, (1100, 1100))

gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()
corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(
    gray, aruco_dict, parameters=parameters)
frame_markers = cv2.aruco.drawDetectedMarkers(dst.copy(), corners, ids)

ids_1 = corners[2][0]
standard = [(ids_1[2][0], ids_1[2][1]), (ids_1[3][0], ids_1[3][1])]
std_length = ((ids_1[2][0]-ids_1[3][0])**2 +
              (ids_1[2][1] - ids_1[3][1])**2)**(1/2)
cv2.line(dst, (int(standard[0][0]), int(standard[0][1])), (int(
    standard[1][0]), int(standard[1][1])), (0, 0, 255), 2)

cv2.putText(dst, "3.1CM", (int(standard[0][0]), int(standard[0][1])),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
points = []
length_set = []


drawing = False  # 마우스 왼쪽 버튼이 눌러지면 그리기 시작

cv2.namedWindow('image')
cv2.setMouseCallback('image', DrawConnectedCircle)

while(1):
    cv2.imshow('image', dst)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cv2.imwrite(output_path + img_name + extension, dst)
