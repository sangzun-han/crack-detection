from django.shortcuts import render, redirect, get_object_or_404
from numpy import core, str_
from .models import Photo, Category
from .distance import Distance
import numpy as np
import cv2

from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
import json

# Create your views here.


def index(request):
    if request.method == 'POST':
        img = Photo()
        img.image = request.FILES.get('uploadImg')
        img.flatting_image = request.FILES.get('uploadImg')
        img.save()
        print(img.image.url)
        return redirect('info-upload/' + str(img.id))
    else:
        return render(request, 'index.html')


def infoUpload(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'infoUpload.html', {
        'img': photo,
    })


def infoProcess(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    photo.originWidth = request.POST['width']
    photo.originHeight = request.POST['height']
    photo.state = request.POST['state']
    photo.cause = request.POST['cause']
    photo.solution = request.POST['solution']
    photo.save()
    return redirect('db')


def canvas_page(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        image = get_object_or_404(Photo, pk=pk)
        img = cv2.imread(image.image.url[1:])

        width = int(request.POST['width'])
        height = int(request.POST['height'])

        # 좌상 우상 우하 좌하
        top_left = request.POST['w'].split(',')
        top_right = request.POST['x'].split(',')
        bottom_right = request.POST['y'].split(',')
        bottom_left = request.POST['z'].split(',')

        pts1 = np.float32([
            [int(int(top_left[0])-50), int(int(top_left[1])-50)],
            [int(int(top_right[0])+50), int(int(top_right[1])-50)],
            [int(int(bottom_right[0])+50), int(int(bottom_right[1])+50)],
            [int(int(bottom_left[0])-50), int(int(bottom_left[1]))+50]
        ])

        # 좌표 시작점을 (x+100,y+100)으로 -> 원하는곳의 좌표가 직선으로 X

        # pts1 = np.float32([
        #     [int((top_left[0])),int(int(top_left[1]))],
        #     [int((top_right[0])),int(int(top_right[1]))],
        #     [int((bottom_right[0])),int(int(bottom_right[1]))],
        #     [int((bottom_left[0])),int(int(bottom_left[1]))]
        # ])

        pixelWidth = max(np.linalg.norm(
            pts1[0] - pts1[1]), np.linalg.norm(pts1[2] - pts1[3]))
        pixelHeight = max(np.linalg.norm(
            pts1[0] - pts1[3]), np.linalg.norm(pts1[1] - pts1[2]))
        width_ratio = width/height
        height_ratio = 1

        pts2 = np.array([
            [0, 0],
            [int(width_ratio*pixelHeight), 0],
            [int(width_ratio*pixelHeight), int(height_ratio*pixelHeight)],
            [0, int(height_ratio*pixelHeight)]
        ], dtype=np.float32)
        print(int(width_ratio*pixelHeight))
        print(int(height_ratio*pixelHeight))
        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(img, M=M, dsize=(
            int(width_ratio*pixelHeight), int(height_ratio*pixelHeight)))
        cv2.imwrite(image.flatting_image.url[1:], dst)
        return render(request, 'test.html', {
            'image': image,
            'height': height,
            'imgWidth': int(width_ratio*pixelHeight),
            'imgHeight': int(height_ratio*pixelHeight),

        })


def db(request):
    dateList = Photo.objects.all().order_by('-id')
    page = request.GET.get('page', '1')
    paginator = Paginator(dateList, '5')  # Paginator(분할될 객체, 페이지 당 담길 객체수)
    page_obj = paginator.page(page)  # 페이지 번호를 받아 해당 페이지를 리턴 get_page 권장
    return render(request, 'db.html', {'page_obj': page_obj})


def dbDetail(request, pk):
    try:
        photo = Photo.objects.get(pk=pk)
    except:
        raise Http404("해당 게시물을 찾을 수 없습니다.")
    return render(request, 'dbDetail.html', {
        'img': photo
    })


def search(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Photo.objects.filter(category__name__icontains=search_str)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


def categories(request):
    return render(request, 'categories.html')
