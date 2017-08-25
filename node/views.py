#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import json

def home(request):
    List = ['geml', '渲染Json到模板']
    Dict = {'site': 'cherry', 'author': 'geml'}
    return render(request, 'home.html', {
            'List': json.dumps(List),
            'Dict': json.dumps(Dict)
        })

def shanxing(request):
    List = ['geml', '渲染Json到模板']
    Dict = {'site': 'cherry', 'author': 'geml'}
    return render(request, 'shanxing.html', {
            'List': json.dumps(List),
            'Dict': json.dumps(Dict)
        })
