from django.shortcuts import render
from django.http import HttpResponseRedirect
from analyzer.models import Contract, ContractText, ContractNatureParty, ContractCategory
from analyzer.forms import ContractForm
from watson_developer_cloud import NaturalLanguageUnderstandingV1, CompareComplyV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, CategoriesOptions, ConceptsOptions, RelationsOptions, SemanticRolesOptions, SentimentOptions, EntitiesOptions, KeywordsOptions
from django.urls import reverse
from datetime import date
import traceback
# from django.conf import settings
import PyPDF2, json, os
import pandas as pd
import csv
# Create your views here.

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version=str(date.today()),
    iam_apikey='0w1akurVaCODOeW8hwzb99RD5mLrIGCAEjCZLwilohOO',
    url='https://gateway.watsonplatform.net/natural-language-understanding/api'
)

compare_and_comply = CompareComplyV1(
    version=str(date.today()),
    iam_apikey='Gc_T-ndAWxlkvNNZDObnjGRyEW8aD3bp9Knydf6P9X1y',
    url='https://gateway.watsonplatform.net/compare-comply/api'
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
            userFile = request.FILES['document']
            fileName = userFile.name
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
                    categories=CategoriesOptions(),
                    concepts=ConceptsOptions(),
                    entities=EntitiesOptions(emotion=True, sentiment=True),
                    keywords=KeywordsOptions(emotion=True, sentiment=True),
                    relations=RelationsOptions(),
                    semantic_roles=SemanticRolesOptions(),
                    sentiment=SentimentOptions()
                )
            ).get_result()
            responseJson = json.dumps(response, indent=2)

            categoriesPath = "media/analyzer/results/categories/" + fileNoExt + ".csv"
            conceptsPath = "media/analyzer/results/concepts/" + fileNoExt + ".csv"
            entitiesPath = "media/analyzer/results/entities/" + fileNoExt + ".csv"
            keywordsPath = "media/analyzer/results/keywords/" + fileNoExt + ".csv"
            relationsPath = "media/analyzer/results/relations/" + fileNoExt + ".csv"  
            semanticRolesPath = "media/analyzer/results/semanticRoles/" + fileNoExt + ".csv"
            sentimentsPath = "media/analyzer/results/sentiments/" + fileNoExt + ".csv"
            contractElementsPath = "media/analyzer/results/contractElements/" + fileNoExt + ".csv"

            try:
                # do not store new record into db if record with this docu name exists
                # get contract from db given file path, create entry if null
                Contract.objects.get(document=filePath)
                print('\nContractElements for this file exists. API call halted.\n\n')
                
                
            except:
                traceback.print_exc()
                watsonRes = Contract()
                watsonRes.document.name = filePath
                watsonRes.resWatsonCategories.name = categoriesPath
                watsonRes.resWatsonConcepts.name = conceptsPath
                watsonRes.resWatsonEntities.name = entitiesPath
                watsonRes.resWatsonKeywords.name = keywordsPath
                watsonRes.resWatsonRelations.name = relationsPath
                watsonRes.resWatsonSemanticRoles.name = semanticRolesPath
                watsonRes.resWatsonSentiments.name = sentimentsPath
                watsonRes.resWatsonContractElements.name = contractElementsPath
                watsonRes.save()

                print('\nContractElements for this file does not exist. Begin extraction.\n\n')

                # if record does not exist, execute API call
                complyRes = compare_and_comply.classify_elements(file=userFile, model_id='contracts', filename=fileNoExt).get_result()
                # contractElements = exportElements(contractElementsPath, complyRes, watsonRes)
                extractElements(contractElementsPath, complyRes, watsonRes)
            
            # save to csv
            categories = exportCategories(categoriesPath, response)
            concepts = exportConcepts(conceptsPath, response)
            entities = exportEntities(entitiesPath, response)
            keywords = exportKeywords(keywordsPath, response)
            relations = exportRelations(relationsPath, response)
            semanticRoles = exportSemanticRoles(semanticRolesPath, response)
            sentiments = exportSentiments(sentimentsPath, response)
            
            # contractElements = exportElements(contractElementsPath, complyRes)
            
            # complyResJson = json.dumps(complyRes, indent=2)
            # print(complyResJson)
            # pdfToHTML =  complyRes['document']['html']

            # print(pdfToHTML)

            # with open(contractElementsPath, "r", encoding="utf-8-sig") as file:
            #     try:
            #         contents = []
            #         for line in file:
            #             contents.append(line)
            #         # for element in complyRes['elements']:
            #         #     element_text = element['text']
            #         #     elementList.append(element_text)
            #         #     writeCSV = element_text + "\n"
            #         #     file.write(writeCSV)
            #     except:
            #         traceback.print_exc()
            #         result = "An error occurred. Please try again."
            
            # element_text_list = []
            # element_nature = []
            # element_party = []
            # element_nature_party_list = []
            # element_category_list = []

            # contractElementsLine = []
            
            # with open(contractElementsPath, "r", encoding="utf-8-sig") as file:
            #     try:
            #         contractElementsLine = []

            #         reader = csv.reader(file, delimiter=",")
            #         for line in enumerate(reader):
            #             contractElementsLine.append(line)

            #         for i, line in contractElementsLine:
            #             # print(line)
            #             element_text.append(line[0])
            #             if(line[1] == '"None"'):
            #                 line[1] = 'None'
            #             if(line[2] == '"None"'):
            #                 line[2] = 'None'
            #             # if(line[3] == ''):
            #             #     line[3] = 'None'
            #             # element_nature.append(line[1])
            #             # element_party.append(line[2])
            #             element_nature_party.append(line[1])
            #             # element_category.append(line[3])
            #             element_category.append(line[2])

            #             # print(line[1] + ", " + line[2] + ", " + line[3])
            #             # print(line[1] + ", " + line[2])

            #     except:
            #         traceback.print_exc()
            #         result = "An error occurred. Please try again."
            element_text_list = []
            element_text = ContractText.objects.filter(contract__document=filePath)
            element_nature_party_list = []
            element_category_list = []

            for text in element_text:
                element_text_list.append(text.text)

                element_nature_party = ContractNatureParty.objects.filter(contractText=text)
                element_nature_party_sublist = []
                for nature_party in element_nature_party:
                    element_nature_party_sublist.append(nature_party.natureParty)
                    print(nature_party.natureParty)
                element_nature_party_list.append(element_nature_party_sublist)

                element_category = ContractCategory.objects.filter(contractText=text)
                element_category_sublist = []
                for category in element_category:
                    element_category_sublist.append(category.category)
                    print(category.category)
                element_category_list.append(element_category_sublist)
                
            # pdfFileObj.close()
            # contractElements = 
            exportElements(contractElementsPath, zip(element_text_list, element_nature_party_list, element_category_list))

            flat_element_category_list = sum(element_category_list, [])
            flat_element_nature_party_list = sum(element_nature_party_list, [])
            flat_element_nature_list = []
            flat_element_party_list = []
            categorySet = sorted(set(flat_element_category_list)) # get unique items by converting the list into a set
            naturePartySet = sorted(set(flat_element_nature_party_list))
            natureSet = []
            partySet = []
            categoryCount = []
            natureCount = []
            partyCount = []

            for category in categorySet:
                categoryCount.append(flat_element_category_list.count(category))
            
            for natureParty in flat_element_nature_party_list:
                print("natureParty: " + natureParty)
                if(natureParty != "None"):
                    nature, party = natureParty.split("-", 1)
                else:
                    nature, party = "None", "None"
                flat_element_nature_list.append(nature)
                flat_element_party_list.append(party)
            
            natureSet = sorted(set(flat_element_nature_list))            
            partySet = sorted(set(flat_element_party_list))

            for nature in natureSet:
                natureCount.append(flat_element_nature_list.count(nature))
            
            for party in partySet:
                partyCount.append(flat_element_party_list.count(party))
            
            return render(request, 
                        'analyzer/index.html', 
                        {
                            'form':form,
                            'categories':categories,
                            'concepts':concepts,
                            'entities':entities,
                            'keywords':keywords,
                            'relations':relations,
                            'semanticRoles':semanticRoles,
                            'sentiments':sentiments,
                            'contractElements' : zip(element_text_list, element_nature_party_list, element_category_list),
                            'fileName': fileName,
                            'categorySet' : zip(categorySet, categoryCount),
                            'natureSet' : zip(natureSet, natureCount),
                            'partySet' : zip(partySet, partyCount)
                            # 'contractElements' : zip(element_text, element_nature, element_party, element_category)
                            # 'contents':contents,
                            # 'pdfToHTML': pdfToHTML,
                            # 'contractElements' : contractElements
                        }
                    )
    else:
        form = ContractForm()
    # return HttpResponseRedirect(reverse('analyzer:index', args=(form)))
    return render(request, 'analyzer/index.html', {'form':form})

def exportCategories(categoriesPath, response = []):
    result = ''
    with open(categoriesPath, "w", encoding="utf-8-sig") as file:
        try:
            for category in response['categories']:
                category_score = str(category['score'])
                category_label = category['label']
                result = "score: " + category_score + \
                        "\nlabel: " + category_label + "\n\n\n"
                # print("result: " + result)
                writeCSV = category_score + "," + category_label + "\n"
                file.write(writeCSV)
                # print(category)
        except:
            traceback.print_exc()
            result = "An error occurred. Please try again."
        
    return result

def exportConcepts(conceptsPath, response = []):
    result = ''
    with open(conceptsPath, "w", encoding="utf-8-sig") as file:
        try:
            for concept in response['concepts']:
                concept_text = concept['text']
                concept_relevance = str(concept['relevance'])
                concept_dbPediaResource = concept['dbpedia_resource']
                result = "text: " + concept_text + \
                            "\nrelevance: " + concept_relevance + \
                            "\ndbpedia_resource" + concept_dbPediaResource + "\n\n\n"
                writeCSV = concept_text + ","+ concept_relevance + "," + concept_dbPediaResource + "\n"
                file.write(writeCSV)
                # print(concept)
        except:
            traceback.print_exc()
            result = "An error occurred. Please try again."
        
    return result

# def exportEmotions(emotionsPath, response = []):
#     result = ''
#     print(response)
#     with open(emotionsPath, "w") as file:
#         try:
#             for emotion in response['emotion']:
#                 # concept_text = concept['text']
#                 # concept_relevance = str(concept['relevance'])
#                 # concept_dbPediaResource = concept['dbpedia_resource']
#                 # result = "text: " + concept_text + \
#                 #             "\nrelevance: " + concept_relevance + \
#                 #             "\ndbpedia_resource" + concept_dbPediaResource + "\n\n\n"
#                 # writeCSV = concept_text + ","+ concept_relevance + "," + concept_dbPediaResource + "\n"
#                 # file.write(writeCSV)
#                 print(emotion)
#         except:
#             traceback.print_exc()
#             result = "An error occurred. Please try again."
#             watsonRes = Contract()
#             watsonRes.resWatsonEmotions.name = emotionsPath
#             watsonRes.save()
#     return result

def exportEntities(entitiesPath, response = []):
    result = ''
    with open(entitiesPath, "w", encoding="utf-8-sig") as file:
        try:
            for entity in response['entities']:
                entity_text= entity['text']
                entity_type = entity['type']
                # print(entity)
                result += "entity: " + entity_text + \
                            "\ntype: " + entity_type + "\n\n\n"
                writeCSV = entity_text +  "," + entity_type + "\n"
                file.write(writeCSV)
        except:
            traceback.print_exc()
            result = "An error occurred. Please try again."
        
    return result

def exportKeywords(keywordsPath, response = []):
    result = ''
    with open(keywordsPath, "w", encoding="utf-8-sig") as file:
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
            traceback.print_exc()
            result = "An error occurred. Please try again."
        
    return result

def exportRelations(relationsPath, response = []):
    result = ''
    with open(relationsPath, "w", encoding="utf-8-sig") as file:
        try:
            for relation in response['relations']:
                relation_type = relation['type']
                relation_sentence = relation['sentence']
                relation_arguments_text = ''
                relation_arguments_entities = ''
                relation_arguments_entities_type = ''
                relation_arguments_entities_text = ''
                
                for argument in relation['arguments']:
                    relation_arguments_text = argument['text']
                    for entity in argument['entities']: 
                        relation_arguments_entities_type = entity['type']
                        relation_arguments_entities_text = entity['text']
                        
                        result += "type: " + relation_type + \
                            "\nsentence: " + relation_sentence + \
                            "\narguments text: " + relation_arguments_text + \
                            "\narguments entities type: " + relation_arguments_entities_type + \
                            "\narguments entities text: " + relation_arguments_entities_text + "\n\n\n"

                        writeCSV = relation_type + "," + \
                            relation_sentence + "," + \
                            relation_arguments_text + "," + \
                            relation_arguments_entities_type + "," + \
                            relation_arguments_entities_text + "\n"
                        # print(relation)
                        file.write(writeCSV)
                # writeCSV = keyword_text + "," + keyword_count + "," + keyword_emotion + "," +  keyword_relevance + "," +  keyword_sentiment + "\n" 
                # file.write(writeCSV)
        except:
            traceback.print_exc()
            result = "An error occurred. Please try again."
        
    return result

def exportSemanticRoles(semanticRolesPath, response = []):
    result = ''
    with open(semanticRolesPath, "w", encoding="utf-8-sig") as file:
        try:
            # print(response)
            for sr in response['semantic_roles']:
                # for srSubject in sr['subject']:
                sr_subject_text = sr['subject']['text']
                sr_sentence = sr['sentence']
                # sr_object_text =  sr['object']['text']
                sr_action_text = sr['action']['text']
                sr_action_normalized = sr['action']['normalized']
                sr_verb_text = sr['action']['verb']['text']
                sr_verb_tense = sr['action']['verb']['tense']
                result += "sentence: " + sr_sentence + \
                        "\nsubject: " +  sr_subject_text + \
                        "\naction: " + sr_action_text + \
                        "\naction normalized: " + sr_action_normalized + \
                        "\nverb: " + sr_verb_text + \
                        "\nverb tense: " + sr_verb_tense + "\n\n\n"
                
                writeCSV = sr_sentence + "," + \
                            sr_subject_text + "," + \
                            sr_action_text + "," + \
                            sr_action_normalized + "," + \
                            sr_verb_text + "," + \
                            sr_verb_tense + "\n"
                file.write(writeCSV)
                # print(sr)
        except:
            traceback.print_exc()
            result = "An error occurred. Please try again."
        
    return result

def exportSentiments(sentimentsPath, response = []):
    result = ''
    with open(sentimentsPath, "w", encoding="utf-8-sig") as file:
        try:
            sentiment_document_label = response['sentiment']['document']['label']
            sentiment_document_score = str(response['sentiment']['document']['score'])

            # print(response['sentiment'])
            # for target in response['sentiment']['targets']:
            #     sentiment_target_text = target['text']
            #     sentiment_target_label = target['label']
            #     sentiment_target_score = str(target['score'])
            # result += "label: " + sentiment_document_label + \
            #             "\nscore: " +  sentiment_document_score + \
            #             "\ntarget text: " + sentiment_target_text + \
            #             "\ntarget label: " + sentiment_target_label + \
            #             "\ntarget score: " + sentiment_target_score + "\n\n\n"
            # writeCSV = sentiment_document_label + "," + \
            #             sentiment_document_score + "," + \
            #             sentiment_target_text + "," + \
            #             sentiment_target_label + "," + \
            #             sentiment_target_score + "\n"

            result += "label: " + sentiment_document_label + \
                        "\nscore: " +  sentiment_document_score + "\n\n\n"
            writeCSV = sentiment_document_label + "," + \
                        sentiment_document_score + "\n"
            file.write(writeCSV)
        except:
            traceback.print_exc()
            result = "An error occurred. Please try again."
        
    return result

def extractElements(contractElementsPath, complyRes, contract):
    try:
        for element in complyRes['elements']:
            
            element_text = element['text']
            contractText = ContractText()

            contractText.text = element_text
            contractText.contract = contract
            contractText.save()

            element_nature_party = 'None'
            element_category_label = 'None'
            
            if(element['types']):
                for element_type in element['types']:
                    if element_type['label']['nature'] != ' ' or element_type['label']['party'] != ' ':
                        element_nature_party = element_type['label']['nature'] + "-" + element_type['label']['party']
                        contractNatureParty = ContractNatureParty()
                        contractNatureParty.natureParty = element_nature_party
                        contractNatureParty.contractText = contractText
                        contractNatureParty.save()
            else:
                contractNatureParty = ContractNatureParty()
                contractNatureParty.natureParty = element_nature_party
                contractNatureParty.contractText = contractText
                contractNatureParty.save()
            
            if(element['categories']):
                for element_category in element['categories']:
                    if element_category['label'] != ' ':
                        element_category_label = element_category['label']
                        contractCategory = ContractCategory()
                        contractCategory.category = element_category_label
                        contractCategory.contractText = contractText
                        contractCategory.save()
            else:
                contractCategory = ContractCategory()
                contractCategory.category = element_category_label
                contractCategory.contractText = contractText
                contractCategory.save()
    except:
        traceback.print_exc()
        # result = "An error occurred. Please try again."
    return

def exportElements(contractElementsPath, contractElements):
    with open(contractElementsPath, "w", newline="\n", encoding="utf-8-sig") as file:
        try:

            # shortcut, does not break down nature_part and category_list individually
            # writer = csv.writer(file)
            # for row in contractElements:
            #     writer.writerow(row)

            for text, nature_party_list, category_list in contractElements:
                row = ""
                for nature_party in nature_party_list:
                    for category in category_list:
                        row = '"'+ text + '","' + nature_party + '","' + category + '"\n'
                        file.write(row)
        except:
            traceback.print_exc()
    return