import sys
import io
from language_detector import LanguageDetector
from corpus import CorpusHelper, CorpusModel
import json
import facebook

ch = CorpusHelper(language='spanish')
ch.load()
cm = CorpusModel(corpus=ch)
params = cm.fit()
print('Our model has an AUC of {}'.format(cm.x_validation(params)))
# el data_json hay que rellenarlo con un ciclo para que vaya cambiando los candidatos y el post
# ocupando lo que había hecho la popi, les cambié los nombres a esto para que sea más fácil jeje

fileRead = open('AlejandoNavarro_postIds_desdeLasPrimarias.txt')
presidente_txtList = fileRead.readlines()
# saca el \n de todos los item de la lista
presidenteSacarSlashNList = [i.replace('\n', '') for i in presidente_txtList]
# saca el user_id_ de todos los item de la lista porque queremos una lista de solo los postIds
presidenteSoloPostId_List = [i.replace('10152723078_', '') for i in presidenteSacarSlashNList]
# sacar el ultimo termino de la lista porque por alguna razon es un item empty
presidenteSoloPostId_List = presidenteSoloPostId_List[:-1]

datas_json = []
for x in range(0,len(presidenteSoloPostId_List)):
    datas_json.append('AlejandroNavarroCommentsOfpost' + presidenteSoloPostId_List[x] + '.json')
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'backslashreplace')
totalPositivos=0
totalComentarios=0
for data_json in datas_json:
    comentarios = []
    with open(data_json, mode='r', encoding='utf-8', ) as file:
        lector = json.load(file)
        for x in range(0, len(lector)):
            if len(lector[x])!=0:
                comentarios.append(lector[x]['message'])
    Id = LanguageDetector()
    # comentarios = [text for text in comentarios if Id.detect(text) == 'es']
    # for text in comentarios:
    #	print('{}: {}'.format(Id.detect(text), text))

    lista = cm.predict(comentarios, params)
    print(lista)
    comentariosPositivos = 0
    total = len(lista)
    totalComentarios+=total
    print(total)
    for index in range(0, len(lista)):
        comentariosPositivos += lista[index]
        totalPositivos+=comentariosPositivos
    porcentajePositivo = ((comentariosPositivos / total) * 100)
    print(porcentajePositivo)
    print("% aprobación")
    #comentariosNegativos = total - comentariosPositivos
    #porcentajeNegativo = ((comentariosNegativos / total) * 100)
    #print(porcentajeNegativo)
    #print("% de reprobación")
totalPorcentajePositivo = ((totalPositivos / totalComentarios) * 100)
print('El candidato Navarro tiene un porcentaje de aprobación de : {}%'.format(totalPorcentajePositivo))