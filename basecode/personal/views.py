from django.shortcuts import render
from django.shortcuts import render
from django.conf import settings

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from personal.models import Document
from personal.forms import DocumentForm

import json
from watson_developer_cloud import VisualRecognitionV3
from json import dumps

from django.conf import settings

from zipfile import *

import zipfile
import sys
import os ,shutil
from django.core.files import File




visual_recognition = VisualRecognitionV3('2018-03-19',iam_apikey='sP7JZ1IK2WInVJA8HuRxTWPxvdYCxJOOS46IGRn2LkFX')

def index(request):
    vPos=Document.objects.order_by('uploaded_at')
    form=DocumentForm()
    return render(request, 'personal/home.html', { 'Pos':vPos ,'form':form })


def dataset(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, )
        if form.is_valid():
            form.save()
            return redirect ('index')
    else:
        form = DocumentForm
        return render (request, 'personal/success.html',{
            'form' : form
        })










  







    
    
    

    





















