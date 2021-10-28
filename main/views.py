from django.shortcuts import render, redirect
from numpy import core
from .models import Photo
from .distance import Distance
from .marker import Marker
import numpy as np
import cv2
import os

# Create your views here.

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
        corners, ids = Marker.detect_marker(img)

        if ids is None:
            os.remove(image.image.url[1:])
            image.delete()
            return render(request, 'index.html', {
                'error': 'Marker does not detect please retry'
        }) 
        elif len(ids) != 4:
            os.remove(image.image.url[1:])
            image.delete()
            return render(request, 'index.html', {
                'error': 'Marker does not detect please retry'
        })
        
        # 변환 전 사진의 네 좌표 좌상 우상 우하 좌하 순
        pts1 = Marker.flatting(corners,ids)

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
        corners,ids = Marker.detect_marker(dst)

        # 마커 인식 못할경우 예외처리 
        if ids is None:
            os.remove(image.image.url[1:])
            image.delete()
            return render(request, 'index.html', {
                'error': 'Marker does not detect please retry'
        }) 
        elif len(ids) != 4:
            os.remove(image.image.url[1:])
            image.delete()
            return render(request, 'index.html', {
                'error': 'Marker does not detect please retry'
        })
        
        # 마커의 꼭지점 위치저장
        marker_vertex = corners[0][0]
        tl = list(map(int,marker_vertex[0]))
        tr = list(map(int,marker_vertex[1]))
        br = list(map(int,marker_vertex[2]))
        bl = list(map(int,marker_vertex[3]))

        cv2.circle(dst, bl, 3, (0, 0, 255), -1) # 빨강
        cv2.circle(dst, tl, 3, (0, 255, 0), -1) # 초록
        cv2.circle(dst, tr, 3, (255, 0, 0), -1) # 파랑
        cv2.circle(dst, br, 3, (255, 255, 255), -1) # 하양
        
        cv2.line(dst,bl,br,(0,0,255),1)
        std_length = Distance.distance(bl,br)
        
        cv2.imwrite(image.image.url[1:],dst)
        return render(request, 'result.html', {
            'image': image,
            'std_length':std_length,
            'mkr_length' : Distance.marker_length,
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
        img = cv2.imread(image.image.url[1:])
        height, width = img.shape[:2]
        corners,ids = Marker.detect_marker(img)
        
        if ids is None:
            os.remove(image.image.url[1:])
            image.delete()
            return render(request, 'index.html', {
                'error': 'Marker does not detect please retry'
        }) 
        elif len(ids) != 4:
            os.remove(image.image.url[1:])
            image.delete()
            return render(request, 'index.html', {
                'error': 'Marker does not detect please retry'
        })

        # 변환 전 사진의 네 좌표 좌상 우상 우하 좌하 순
        pts1 = Marker.flatting(corners, ids)

        # 사진의 넓이, 높이 (픽셀)
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
        corners, ids = Marker.detect_marker(dst)

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
        
        # Top left
        tltl = list(map(int,topLeft[0]))
        tltr = list(map(int,topLeft[1]))
        tlbr = list(map(int,topLeft[2]))
        tlbl = list(map(int,topLeft[3]))
        
        # Bottom Right
        brtl = list(map(int,bottomRight[0]))
        brtr = list(map(int,bottomRight[1]))
        brbr = list(map(int,bottomRight[2]))
        brbl = list(map(int,bottomRight[3]))
        
        # BottomLeft
        bltl = list(map(int,bottomLeft[0]))
        bltr = list(map(int,bottomLeft[1]))
        blbr = list(map(int,bottomLeft[2]))
        blbl = list(map(int,bottomLeft[3]))

        # TopRight
        trtl = list(map(int,topRight[0]))
        trtr = list(map(int,topRight[1]))
        trbr = list(map(int,topRight[2]))
        trbl = list(map(int,topRight[3]))


        cv2.line(dst,tlbl,tlbr,(0,0,255),1)
        std_length = Distance.distance(tlbl,tlbr)
        
        dst = dst[ tlbr[1]:bltr[1], tlbr[0]: trbl[0] ]
        gray = cv2.cvtColor(dst,cv2.COLOR_BGR2GRAY)
        blur = cv2.blur(gray,(3,3))
        # Apply logarithmic transform
        img_log = (np.log(blur+1)/(np.log(1+np.max(blur))))*255

        # Specify the data type
        img_log = np.array(img_log,dtype=np.uint8)

        # Image smoothing: bilateral filter
        bilateral = cv2.bilateralFilter(img_log, 5, 75, 75)

        # Canny Edge Detection
        edges = cv2.Canny(bilateral,100,200)
        # Morphological Closing Operator
        kernel = np.ones((5,5),np.uint8)
        closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)


        contour, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contour) == 0:
            return render(request, 'index.html', {
                'error': 'Cracks are not recognized.'})
        ctr_s = contour[0]
        if len(contour)>=2:
            for i in range(1,len(contour)):
                ctr_s=np.concatenate((ctr_s, contour[i]), axis=0)


        contours_min = np.argmin(ctr_s, axis = 0)
        contours_max = np.argmax(ctr_s, axis = 0)

        x_Min = (ctr_s[contours_min[0][0]][0][0],ctr_s[contours_min[0][0]][0][1])
        y_Min = (ctr_s[contours_min[0][1]][0][0],ctr_s[contours_min[0][1]][0][1])
        x_Max = (ctr_s[contours_max[0][0]][0][0],ctr_s[contours_max[0][0]][0][1])
        y_Max = (ctr_s[contours_max[0][1]][0][0],ctr_s[contours_max[0][1]][0][1])

        a = dst.copy()
        ellipse = cv2.fitEllipse(ctr_s)
        (x, y), (MA, ma), angle = cv2.fitEllipse(ctr_s)
        cv2.ellipse(a, ellipse, (255,0,0), 3)
        cv2.imwrite(image.image.url[1:],a)
        MA = Distance.real_distance(Distance.marker_length, std_length, MA)
        ma = Distance.real_distance(Distance.marker_length, std_length, ma)
        area = round(MA*ma*3.14,2)

        cv2.circle(a, x_Min, 3, Distance.black_color, -1)
        cv2.circle(a, y_Min, 3, Distance.black_color, -1)
        cv2.circle(a, x_Max, 3, Distance.black_color, -1)
        cv2.circle(a, y_Max, 3, Distance.black_color, -1)

        cv2.line(a, x_Min, y_Max, Distance.blue_color, 2)
        cv2.line(a, x_Max, y_Min, Distance.green_color, 2)
        cv2.line(a, x_Min, y_Min, Distance.red_color, 2)
        cv2.line(a, x_Max, y_Max, Distance.yellow_color, 2)

        green_length = Distance.distance(x_Max,y_Min)
        blue_length = Distance.distance(x_Min, y_Max)
        red_length = Distance.distance(x_Min, y_Min)
        yellow_length = Distance.distance(x_Max, y_Max)
        
        real_green = Distance.real_distance(Distance.marker_length, std_length, green_length)
        real_blue  = Distance.real_distance(Distance.marker_length, std_length, blue_length)
        real_red = Distance.real_distance(Distance.marker_length, std_length, red_length)
        real_yellow = Distance.real_distance(Distance.marker_length,std_length, yellow_length)

        cv2.imwrite(image.image.url[1:],a)
        return render(request, 'detection.html', {
            'image': image,
            'mkr_length' : Distance.marker_length,
            'width' : int(width_ratio * 500),
            'height' : int(height_ratio * 500),
            'green': real_green,
            'red': real_red,
            'yellow': real_yellow,
            'blue': real_blue,
            'area': area
            })
