"""
URL configuration for mypjt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('finlife/', include('finlife.urls')),
    path('accounts/', include('accounts.urls')),
    path('exchange/', include('exchange.urls')),
    path('comments/', include('comments.urls')),
    # 11-20 윤희준 퀘스트, 훈련장 쓸 장고 작성
    path('quest/', include('quest.urls')),
    path('bucket/', include('bucket.urls')),
    # 11-25 신희원 뉴스 기능 생성
    path('news/', include('news.urls'))
]
