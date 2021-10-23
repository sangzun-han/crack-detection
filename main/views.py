from django.shortcuts import render, redirect
from numpy.typing import _256Bit
from .models import Photo
import numpy as np
import cv2
import os

# Create your views here.
marker_length = 3.1


def index(request): 
    return render(request, 'index.html')

def upload(request):
    if request.method == 'POST':
        # model  photo post to save
        image = Photo()
        image.image = request.FILES['image']
        image.save()
        # opencv to flattening
        img = cv2.imread(image.image.url[1:])
        height, width = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
        parameters = cv2.aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(
        gray, aruco_dict, parameters=parameters
        )
        if ids is None:
            os.remove(image.image.url[1:])
            image.delete()
            print('c')
            return render(request, 'index.html', {
                'error': 'Marker does not detect please retry'
        }) 
        elif len(ids) != 4:
            os.remove(image.image.url[1:])
            image.delete()
            print('d')
            return render(request, 'index.html', {
                'error': 'Marker does not detect please retry'
        })
        
        # 각 마커의 바깥쪽 꼭지점을 뽑아내어 각 포인트에 저장
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
        
        
        # pts1 변환 전 사진의 네 좌표 좌상 좌하 우하 우상 순
        pts1 = np.float32([ap, cp, dp, bp])

        # 사진의 넓이, 높이 (픽셀)
        width = max(np.linalg.norm(pts1[0] - pts1[1]), np.linalg.norm(pts1[2] - pts1[3]))
        height = max(np.linalg.norm(pts1[0] - pts1[3]), np.linalg.norm(pts1[1] - pts1[2]))

        # 평탄화 될 사진의 비율 계산
        width_ratio = (width / height)
        height_ratio = 1

        # pts2 변환 후 사진의 네 좌표
        pts2 = np.array([
                [10, 10],
                [int(width_ratio * 500)-10, 10],
                [int(width_ratio * 500)-10, int(height_ratio * 500)-10],
                [10, int(height_ratio * 500)-10]
            ], 
            dtype=np.float32)
        # pts1의 좌표에 표시. perspective 변환 후 이동 점 확인.
        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(img, M=M, dsize=(int(width_ratio * 500), height_ratio * 500))
        

        # 변환된 사진을 이용하여 픽셀간 거리 구하기
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
        parameters = cv2.aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(
            gray, aruco_dict, parameters=parameters)

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
        ap = corners[3][0]
        bp = list(map(int,ap[0]))
        cp = list(map(int,ap[1]))
        dp = list(map(int,ap[2]))
        ap = list(map(int,ap[3]))
        cv2.circle(dst, ap, 3, (0, 0, 255), -1) # 빨강
        cv2.circle(dst, bp, 3, (0, 255, 0), -1) # 초록
        cv2.circle(dst, cp, 3, (255, 0, 0), -1) # 파랑
        cv2.circle(dst, dp, 3, (255, 255, 255), -1) # 하양
        
        cv2.line(dst,ap,dp,(0,0,255),1)
        std_length = ((ap[0]-dp[0])**2 + (ap[1]-dp[1])**2) ** (1/2)
        

        cv2.imwrite(image.image.url[1:],dst)
        return render(request, 'result.html', {
            'image': image,
            'std_length':std_length,
            'mkr_length' : marker_length,
            'width' : int(width_ratio * 500),
            'height' : int(height_ratio * 500),
        })
    else:
        return redirect('/')

def detection(request):
    if  request.method == 'GET':
        return render(request,'index.html',{"error":"It's a wrong approach."})
    else:
        # model  photo post to save
        image = Photo()
        image.image = request.FILES['image']
        image.save()
    
        print('a')
        
        img = cv2.imread(image.image.url[1:])
        print('b')
        height, width = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
        parameters = cv2.aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(
        gray, aruco_dict, parameters=parameters
        )

        if ids is None:
            os.remove(image.image.url[1:])
            image.delete()
            print('c')
            return render(request, 'index.html', {
                'error': 'Marker does not detect please retry'
        }) 
        elif len(ids) != 4:
            os.remove(image.image.url[1:])
            image.delete()
            print('d')
            return render(request, 'index.html', {
                'error': 'Marker does not detect please retry'
        })
        
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
        # 사진의 넓이, 높이 (픽셀)
        print(pts1[0], pts1[1])
        print(pts1[2], pts1[3])
        height = max(np.linalg.norm(pts1[0] - pts1[1]), np.linalg.norm(pts1[2] - pts1[3]))
        width = max(np.linalg.norm(pts1[0] - pts1[3]), np.linalg.norm(pts1[1] - pts1[2]))

        # 평탄화 될 사진의 비율 계산
        width_ratio = (height / width)
        height_ratio = 1

        # pts2 변환 후 사진의 네 좌표
        pts2 = np.array([
                [10, 10],
                [int(width_ratio * 500)-10, 10],
                [int(width_ratio * 500)-10, int(height_ratio * 500)-10],
                [10, int(height_ratio * 500)-10]
            ], dtype=np.float32)
        # pts1의 좌표에 표시. perspective 변환 후 이동 점 확인.
        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(img, M=M, dsize=(int(width_ratio * 500), height_ratio * 500))
            

        # 변환된 사진을 이용하여 픽셀간 거리 구하기
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
        parameters = cv2.aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(
            gray, aruco_dict, parameters=parameters)
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
        
        
        topLeft = corners[3][0]
        bp = list(map(int,topLeft[0]))
        cp = list(map(int,topLeft[1]))
        dp = list(map(int,topLeft[2]))
        ap = list(map(int,topLeft[3]))
        
        bottomRight = corners[0][0]
        z = list(map(int,bottomRight[0]))
        zx = list(map(int,bottomRight[1]))
        zc = list(map(int,bottomRight[2]))
        zv = list(map(int,bottomRight[3]))
        
        bottomLeft = corners[1][0]
        x = list(map(int,bottomLeft[0]))
        xx = list(map(int,bottomLeft[1]))
        xc = list(map(int,bottomLeft[2]))
        xv = list(map(int,bottomLeft[3]))

        topRight = corners[2][0]
        v = list(map(int,topRight[0]))
        vx = list(map(int,topRight[1]))
        vc = list(map(int,topRight[2]))
        vv = list(map(int,topRight[3]))

    

        cv2.circle(dst, ap, 3, (0, 0, 255), -1) # 빨강
        cv2.circle(dst, bp, 3, (0, 255, 0), -1) # 초록
        cv2.circle(dst, cp, 3, (255, 0, 0), -1) # 파랑
        cv2.circle(dst, dp, 3, (255, 255, 255), -1) # 하양
        
        cv2.circle(dst, z, 3, (0, 0, 255), -1) # 빨강
        cv2.circle(dst, zx, 3, (0, 255, 0), -1) # 초록
        cv2.circle(dst, zc, 3, (255, 0, 0), -1) # 파랑
        cv2.circle(dst, zv, 3, (255, 255, 255), -1) # 하양

        cv2.circle(dst, x, 3, (0, 0, 255), -1) # 빨강
        cv2.circle(dst, xx, 3, (0, 255, 0), -1) # 초록
        cv2.circle(dst, xc, 3, (255, 0, 0), -1) # 파랑
        cv2.circle(dst, xv, 3, (255, 255, 255), -1) # 하양

        cv2.circle(dst, v, 3, (0, 0, 255), -1) # 빨강
        cv2.circle(dst, vx, 3, (0, 255, 0), -1) # 초록
        cv2.circle(dst, vc, 3, (255, 0, 0), -1) # 파랑
        cv2.circle(dst, vv, 3, (255, 255, 255), -1) # 하양

        cv2.line(dst,ap,dp,(0,0,255),1)
        std_length = ((ap[0]-dp[0])**2 + (ap[1]-dp[1])**2) ** (1/2)
        
        # dst = dst[ cp[1]:cp[1]+xx[1], cp[0]: cp[0] + v[0] ]
        # dst = dst[ v[1]:cp[1]+xx[1], v[0]: cp[0] + v[0] ]

        cv2.imwrite(image.image.url[1:],dst) 
        return render(request, 'result.html', {
            'image': image,
            'std_length':std_length,
            'mkr_length' : marker_length,
            'width' : int(width_ratio * 500),
            'height' : int(height_ratio * 500),
            })
