from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info_upload/<pk>' ,views.info_upload, name="info_upload"),
    path('canvas_page/', views.canvas_page, name="canvas_page"),
    path('result_page/' ,views.result_page, name="result_page_"),
    # path('detection/', views.detection, name='detection')
]
