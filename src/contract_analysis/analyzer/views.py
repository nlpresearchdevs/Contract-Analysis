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
            fileName = request.FILES['document'].name
            filePath = os.path.join('media/analyzer/contracts/', fileName)
            fileNoExt, fileExt = os.path.splitext('media/analyzer/contracts/' + fileName)
            
            # save file if does not exist
            if not os.path.exists(filePath):
                form.save()
            
            # return HttpResponseRedirect('analyzer/success.html')
            # file name without extension
            fileNoExt = fileNoExt.replace('media/analyzer/contracts/','')
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
                    keywords=KeywordsOptions(emotion=True, sentiment=True),
                    # categories=CategoriesOptions();
                )
            ).get_result()
            keywords = json.dumps(response, indent=2)

            # df = pd.read_json(keywords)
            # df = df.loc[['keyword', 'relevance', 'tcount']].T
            # df.to_csv('media/analyzer/keywords/' + fileName)

            # return HttpResponseRedirect(reverse('analyzer:index', args=(form, keywords)))
            pdfFileObj.close()
            print(keywords)

            keywordsPath = "media/analyzer/keywords/" + fileNoExt + ".csv"
            result = ''
            
            with open(keywordsPath, "w") as file:
                try:
                    for keyword in response['keywords']:
                        keyword_text = keyword['text']
                        keyword_count =  str(keyword['count'])
                        keyword_emotion = max(keyword['emotion'], key=lambda k: keyword['emotion'][k])
                        keyword_relevance = str(keyword['relevance'])
                        keyword_sentiment = keyword['sentiment']['label']
                        result += "keyword: " +  keyword_text + \
                                    "\ncount: " + keyword_count + \
                                    "\nemotion: " + keyword_emotion + \
                                    "\nrelevance: " + keyword_relevance + \
                                    "\nsentiment: " + keyword_sentiment + "\n\n\n"
                        # print(keyword)
                        writeCSV = keyword_text + "," + keyword_count + "," + keyword_emotion + "," +  keyword_relevance + "," +  keyword_sentiment + "\n" 
                        file.write(writeCSV)
                except:
                    result = "Invalid PDF file. Please upload another PDF file."
            # return HttpResponseRedirect(reverse('analyzer:index', args=(form, keywords)))

            # save csv to db reswatsonkeywords column
            watsonRes = Contract()
            watsonRes.resWatsonKeywords.name = keywordsPath
            watsonRes.save()

            return render(request, 'analyzer/index.html', {'form':form, 'keywords':result})
    else:
        form = ContractForm()
    # return HttpResponseRedirect(reverse('analyzer:index', args=(form)))
    return render(request, 'analyzer/index.html', {'form':form})