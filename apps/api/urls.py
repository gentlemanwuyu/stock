from django.conf.urls import url
from .views import get_continued_strong_list

urlpatterns = [
    url(r'^stock/get-continued-strong-list$', get_continued_strong_list),
]