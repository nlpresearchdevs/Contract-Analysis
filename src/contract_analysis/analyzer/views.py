from django.shortcuts import render
from django.http import HttpResponseRedirect
from analyzer.models import Contract
from analyzer.forms import ContractForm
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from django.urls import reverse
# from django.conf import settings
import PyPDF2, json, os
import pandas as pd
# Create your views here.

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-01-02',
    iam_apikey='_6QTxuEr5B2xuwU8-KOIu1TIc64u0a34-wLRB0jco_Zs',
    url='https://gateway-tok.watsonplatform.net/natural-language-understanding/api'
)

def index(request):
    # vPos=Contract.objects.order_by('uploaded_at')
    form=ContractForm()
    # return render(request, 'analyzer/index.html', { 'Pos':vPos ,'form':form })
    return render(request, 'analyzer/index.html', {'form':form})

def upload_file(request):
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            fileName = request.FILES['document'].name
            filePath = os.path.join('media/analyzer/contracts/', fileName)
            fileNameOnly, fileExt = os.path.splitext('media/analyzer/contracts/' + fileName)
            if not os.path.exists(filePath):
                form.save()
            
            # return HttpResponseRedirect('analyzer/success.html')
            fileNameOnly = fileNameOnly.replace('media/analyzer/contracts/','')
            pdfFileObj  = open('media/analyzer/contracts/' + fileName, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

            text = ''
            for page in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(page)
                text += pageObj.extractText()
            
            response = natural_language_understanding.analyze(
                text=text,
                features=Features(
                    entities=EntitiesOptions(emotion=True, sentiment=True),
                    keywords=KeywordsOptions(emotion=True, sentiment=True)
                    # keywords=KeywordsOptions()
                )
            ).get_result()
            keywords = json.dumps(response, indent=2)

            # df = pd.read_json(keywords)
            # df = df.loc[['keyword', 'relevance', 'tcount']].T
            # df.to_csv('media/analyzer/keywords/' + fileName)

            # return HttpResponseRedirect(reverse('analyzer:index', args=(form, keywords)))
            pdfFileObj.close()
            print(keywords)

            keywordsPath = "media/analyzer/keywords/" + fileNameOnly + ".csv"
            result = ''
            
            with open(keywordsPath, "w") as file:
                for keyword in response['keywords']: 
                    result += "keyword: " + keyword['text'] + \
                                "\n\trelevance: " + str(keyword['relevance']) + \
                                "\n\tcount: " + str(keyword['count']) + "\n\n\n"
                    print(keyword)
                    writeCSV = keyword['text'] + ", " +  str(keyword['count']) + ", " + str(keyword['relevance']) + "\n"
                    file.write(writeCSV)
            # return HttpResponseRedirect(reverse('analyzer:index', args=(form, keywords)))
            return render(request, 'analyzer/index.html', {'form':form, 'keywords':result})
    else:
        form = ContractForm()
    # return HttpResponseRedirect(reverse('analyzer:index', args=(form)))
    return render(request, 'analyzer/index.html', {'form':form})