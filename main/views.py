from django.shortcuts import render, redirect
from .models import Photo
import numpy as np
import cv2
from PIL import Image
# Create your views here.


def index(request):
    return render(request, 'index.html')

def flatting():
    img = cv2.imread('static/images/test.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    aruco_dict = cv2.arcuo.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(
        gray, aruco_dict, parameters=parameters
    )

    for i in range(len(ids)):
        c = corners[i][0]

        if ids[i][0] == 1:
            ap = [c[0, 0], c[0, 1]]
        if ids[i][0] == 2:
            cp = [c[1, 0], c[1, 1]]
        if ids[i][0] == 3:
            bp = [c[3, 0], c[3, 1]]
        if ids[i][0] == 4:
            dp = [c[2, 0], c[2, 1]]

    pts1 = np.float32([ap, bp, cp, dp])

    # 좌표의 이동점
    pts2 = np.float32([[60, 60], [60, 1050], [1050, 60], [1050, 1050]])
    # pts1의 좌표에 표시. perspective 변환 후 이동 점 확인.
    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(img, M, (1100, 1100))

def upload(request):
    flatting()
    # print(flatting())
    if request.method == 'POST':
        image = Photo()
        image.title = request.POST['title']
        image.image = request.FILES['image']       
        image.save()
        return render(request, 'result.html', {
            'image': image
        })
    else:
        return redirect('/')
