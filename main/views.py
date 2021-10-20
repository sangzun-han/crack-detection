from django.shortcuts import render, redirect
from .models import Photo
import numpy as np
import cv2

# Create your views here.


def index(request):
    return render(request, 'index.html')

def upload(request):
    if request.method == 'POST':
        image = Photo()
        image.title = request.POST['title']
        image.image = request.FILES['image']
        image.save()

        # open cv img - imread
        img = cv2.imread(image.image.url[1:])
        height, width = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
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
        
        ids_1 = corners[2][0] # 2
        standard = [(ids_1[2][0],ids_1[2][1]),(ids_1[3][0],ids_1[3][1])]
        cv2.line(img,(int(standard[0][0]),int(standard[0][1])),(int(standard[1][0]),int(standard[1][1])),(0,0,255),5)
        cv2.putText(img,"3.1CM",(int(standard[0][0]),int(standard[0][1])),cv2.FONT_HERSHEY_SIMPLEX,5.5,(0,0,255),5)
        
        pts1 = np.float32([ap, cp, dp, bp])
        width = max(np.linalg.norm(pts1[0] - pts1[1]), np.linalg.norm(pts1[2] - pts1[3]))
        height = max(np.linalg.norm(pts1[0] - pts1[3]), np.linalg.norm(pts1[1] - pts1[2]))
        
        width_ratio = (width / height)
        height_ratio = 1
        pts2 = np.array([
                [10, 10],
                [int(width_ratio * 500)-10, 10],
                [int(width_ratio * 500)-10, int(height_ratio * 500)-10],
                [10, int(height_ratio * 500)-10]
            ], 
        dtype=np.float32)
       
        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(img, M=M, dsize=(int(width_ratio * 500), height_ratio * 500))
        cv2.imwrite(image.image.url[1:],dst)
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
        parameters = cv2.aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers (
            gray, aruco_dict, parameters=parameters
        )

        return render(request, 'result.html', {
            'image': image,
            'standard': standard,
            'corners': corners[3],
        })
    else:
        return redirect('/')