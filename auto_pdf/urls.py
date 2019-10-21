
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('', include('automate_pdf.urls')),
    path('automate_pdf/', include('automate_pdf.urls')),
    path('admin/', admin.site.urls),
]
