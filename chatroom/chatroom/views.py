import json

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from room.models import Room_list

def test(request):
    # return HttpResponse(json.dumps('msg'))
    # r=Room_list.objects.all()
    # r=list(r)
    # return  JsonResponse(r,safe=False)
    import json
    data = json.dumps(list(Room_list.objects.all().values('roomname','introduce','user')))
    return HttpResponse(data)
