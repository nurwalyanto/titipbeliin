from django.shortcuts import render
from .modul.naver import naver
import re
# Create your views here.
from django.http import HttpResponse,JsonResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
	
def api(request):
	url=None
	if 'url' in request.GET:
		url=request.GET['url']
	else:
		return JsonResponse({
			'status':'error',
			'message':'Parameter URL not set'
		})
	
	try:
		url=re.findall('(https?:\/\/)?([^\/\r\n]+)(\/[^\r\n]*)?',url)[0]
		if 'shopping.naver.com' == url[1]:
			url="https://"+"".join(url[1:])
		else:
			return JsonResponse({
				'status':'error',
				'message':'No supported hosts'
			}) 
		temp=naver(url)
		data={
			'name':temp.getName(),
			'price':temp.getPrice(),
			'option':temp.getOption(),
		}
		return JsonResponse(data)
	except Exception as e:
		return JsonResponse({
			'status':'error',
			'message':'url may invalid'
		})