from django.shortcuts import render, redirect
from .models import Photo
import numpy as np
import cv2

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
    if request.method == 'POST':
        # model  photo post to save
        image = Photo()
        image.image = request.FILES['image']
        image.save()

    img = cv2.imread(image.image.url[1:])
    # Convert into gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Image processing ( smoothing )
    # Averaging
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
    
    # Create feature detecting method
    # sift = cv2.xfeatures2d.SIFT_create()
    # surf = cv2.xfeatures2d.SURF_create()
    orb = cv2.ORB_create(nfeatures=1500)

    # Make featured Image
    keypoints, descriptors = orb.detectAndCompute(closing, None)
    featuredImg = cv2.drawKeypoints(closing, keypoints, None)
    contour, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    
    ctr_s = contour[0]
    if len(contour)>=2:
        for i in range(1,len(contour)):
            ctr_s=np.concatenate((ctr_s, contour[i]), axis=0)
            print(len(ctr_s))
    
    contours_min = np.argmin(ctr_s, axis = 0)
    contours_max = np.argmax(ctr_s, axis = 0)

    x_Min = (ctr_s[contours_min[0][0]][0][0],ctr_s[contours_min[0][0]][0][1])
    y_Min = (ctr_s[contours_min[0][1]][0][0],ctr_s[contours_min[0][1]][0][1])
    x_Max = (ctr_s[contours_max[0][0]][0][0],ctr_s[contours_max[0][0]][0][1])
    y_Max = (ctr_s[contours_max[0][1]][0][0],ctr_s[contours_max[0][1]][0][1])
    print(x_Min,y_Min,x_Max,y_Max)
    blue_color = (255, 0, 0)
    green_color = (0, 255, 0)
    red_color = (0, 0, 255)
    white_color = (255, 255, 255)

    
    a = img.copy()
    # 모두 0으로 되어 있는 빈 Canvas(검정색)

    cv2.drawContours(a, contour, -1, (255,255,255), 3)
    cv2.circle(a, x_Min, 5, blue_color, -1)
    cv2.circle(a, y_Min, 5, green_color, -1)
    cv2.circle(a, x_Max, 5, red_color, -1)
    cv2.circle(a, y_Max, 5, white_color, -1)
    cv2.line(a, x_Min, x_Max, blue_color, 2)
    cv2.line(a, y_Min, y_Max, green_color, 2)
    
    
    
    
   
    
    cv2.imwrite(image.image.url[1:], a)
    
    # Use plot to show original and output image
    return render(request, 'detection.html', {
        'image': image.image.url
    })

        # for contr in contour:
    #     rect = cv2.minAreaRect(contr)
    #     box = cv2.boxPoints(rect)   # 중심점과 각도를 4개의 꼭지점 좌표로 변환
    #     box = np.int0(box)          # 정수로 변환
    #     cv2.drawContours(closing, [box], -1, (255,255,255), -1)

     