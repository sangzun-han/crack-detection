from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='index'),
    path('info-upload/<pk>', views.infoUpload, name="infoUpload"),
    path('canvas_page/', views.canvas_page, name="canvas_page"),
    # path('result_page/' ,views.result_page, name="result_page_"),
    path('db/', views.db, name="db"),
    path('categories/', views.categories, name="categories"),
    path('info-process/<pk>', views.infoProcess, name="infoProcess"),
    path('search', csrf_exempt(views.search), name="search"),
    path('db/<pk>', views.dbDetail, name="dbDetail")
    # path('detection/', views.detection, name='detection')
]
