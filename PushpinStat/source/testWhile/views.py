# from django.shortcuts import render
from django.http import HttpResponse
from .getstats import read_stats_block


def updatestate(request):
    print('querying socket stat...')
    read_stats_block()
    return HttpResponse('update done')
