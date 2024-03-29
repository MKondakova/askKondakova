"""askKondakova URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.new_questions, name='new_questions'),
                  path('hot/', views.hot_questions, name='hot'),
                  path('tag/<tag_type>', views.tag_news, name='tag_questions'),
                  path('question/<int:question_id>', views.question_page, name='question'),
                  path('login/', views.login_page, name='login'),
                  path('logout/', views.logout_page, name='logout'),
                  path('sign_up/', views.sign_up_page, name='signup'),
                  path('ask/', views.new_question, name='ask'),
                  path('profile/edit/', views.settings_page, name='settings'),
                  path('vote/', views.vote, name='vote'),
                  path('make_correct/', views.make_correct, name='make_correct'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
