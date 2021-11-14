from django.shortcuts import render, redirect, get_object_or_404
from numpy import core, str_
from .models import Photo
from .distance import Distance
import numpy as np
import cv2

# Create your views here.
def index(request):
    if request.method == 'POST':
        image = Photo()
        image.image = request.FILES['image']
        image.flatting_image = request.FILES['image']
        image.save()
        img = cv2.imread(image.image.url[1:])
        height, width = img.shape[:2]
        image.origin_width = width
        image.origin_height = height
        image.save()
        return redirect('info_upload/' + str(image.id))
    else:
        return render(request, 'index.html')

def info_upload(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'info_upload.html', {
        'image' : photo,
    })

def canvas_page(request):
    if request.method == 'POST':
        print(request.POST)
        pk = request.POST['pk']
        image = get_object_or_404(Photo,pk=pk)
        img = cv2.imread(image.image.url[1:])

        width = int(request.POST['width'])
        height = int(request.POST['height'])

        # 좌상 우상 우하 좌하
        top_left = request.POST['w'].split(',')
        top_right = request.POST['x'].split(',')
        bottom_right = request.POST['y'].split(',')
        bottom_left = request.POST['z'].split(',')
        pts1 = np.float32([
            [int(top_left[0]),int(top_left[1])],
            [int(top_right[0]),int(top_right[1])],
            [int(bottom_right[0]),int(bottom_right[1])],
            [int(bottom_left[0]),int(bottom_left[1])]
        ])

        pixelWidth = max(np.linalg.norm(pts1[0] - pts1[1]), np.linalg.norm(pts1[2] - pts1[3]))
        pixelHeight = max(np.linalg.norm(pts1[0] - pts1[3]), np.linalg.norm(pts1[1] - pts1[2]))

        width_ratio = width/height
        height_ratio = 1

        pts2 = np.array([
                [0, 0],
                [int(width_ratio*pixelHeight),0],
                [int(width_ratio*pixelHeight), int(height_ratio*pixelHeight)],
                [0, int(height_ratio*pixelHeight)]
        ], dtype=np.float32)

        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(img, M=M, dsize=(int(width_ratio*pixelHeight), int(height_ratio*pixelHeight)))
        cv2.imwrite(image.flatting_image.url[1:], dst)
        return render(request, 'test.html', {
            'image': image,
        })

def result_page(request):
    return 0
