from django.contrib import admin
from django.urls import include, path
from . import views




urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.download_file, name='download'),
    # path('convert/', views.convert_pdf_to_image, name='convert'),
    path('get_position/', views.get_position, name='get_position'),
    path('automate/', views.automate_and_create_zip, name='automate'),
]