from django.http import JsonResponse, HttpRequest
from .services.stock import GetContinuedStrongList


# Create your views here.
def get_continued_strong_list(request: HttpRequest):
    service = GetContinuedStrongList(request.GET)
    result = service.handle()
    return JsonResponse({"code": 0, "msg": "成功", "data": result})
