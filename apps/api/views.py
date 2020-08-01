from django.http import JsonResponse, HttpResponse, HttpRequest


# Create your views here.
def get_continued_strong_list(request: HttpRequest):
    return JsonResponse({"code": 0, "msg": "成功"})
