import io
import json
import sys
from corpus import CorpusHelper, CorpusModel
from language_detector import LanguageDetector

ch = CorpusHelper(language='spanish')
ch.load()
cm = CorpusModel(corpus=ch)
params = cm.fit()
print('Our model has an AUC of {}'.format(cm.x_validation(params)))

candidatos=['AlejandroGuillier','AlejandroNavarro','BeatrizSanchez','CarolinaGoic','EduardoArtes','JoseAntonioKast','MarcoEnriquez-Ominami','SebastianPiñera']
#consecuente con el orden de "candidatos"
idsCandidatos=['1481491872064849','10152723078','137510593443379','377671865775887','321406001578434','881095048648989','386634201382499','553775568008058']

# todo: al final meter todo dentro del for de candidatos para que analice todo al ejecutarlo solo una vez
posID=0
aprobaciones= []
candidatosPubliNoVacias= []
candidatosPubliVacias= []
for candidato in candidatos:
    publiVacias=0
    publiNoVacias=0
    idCandidato=idsCandidatos[posID]
    fileRead = open('PostIdsDeTodosLosPresidentes/' + candidato + '_postIds_desdeLasPrimarias.txt')
    presidente_txtList = fileRead.readlines()
    # saca el \n de todos los item de la lista
    presidenteSacarSlashNList = [i.replace('\n', '') for i in presidente_txtList]
    # saca el user_id_ de todos los item de la lista porque queremos una lista de solo los postIds
    presidenteSoloPostId_List = [i.replace(idCandidato + '_', '') for i in presidenteSacarSlashNList]
    # sacar el ultimo termino de la lista porque por alguna razon es un item empty
    presidenteSoloPostId_List = presidenteSoloPostId_List[:-1]

    datas_json = []
    for x in range(0, len(presidenteSoloPostId_List)):
        datas_json.append('JsonCommentsDeLosPresidentes/' + candidato + 'JSONcomments/' + candidato + 'CommentsOfpost' +
                          presidenteSoloPostId_List[x] + '.json')
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'backslashreplace')
    totalPositivos = 0
    totalComentarios = 0
    for data_json in datas_json:
        comentarios = []
        with open(data_json, mode='r', encoding='utf-8', ) as file:
            lector = json.load(file)
            for x in range(0, len(lector)):
                comentarios.append(lector[x]['message'])
        Id = LanguageDetector()
        # comentarios = [text for text in comentarios if Id.detect(text) == 'es']
        # for text in comentarios:
        #	print('{}: {}'.format(Id.detect(text), text))
        if len(comentarios) > 0:
            lista = cm.predict(comentarios, params)
            publiNoVacias+=1
        else:
            publiVacias+=1
            #todo with open(postIdsVacios )
        print(lista)
        comentariosPositivos = 0
        total = len(lista)
        totalComentarios += total
        print(total)
        for index in range(0, len(lista)):
            comentariosPositivos += lista[index]
        totalPositivos += comentariosPositivos
        porcentajePositivo = ((comentariosPositivos / total) * 100)
        print("{0:0.2f}% aprobación".format(porcentajePositivo))

    totalPorcentajePositivo = ((totalPositivos / totalComentarios) * 100)
    print('Las publicaciones del candidato ' +candidato+ ' tiene un porcentaje de aprobación de: {0:0.2f}%'.format(totalPorcentajePositivo))
    #cambia al sgte idCandidato
    aprobaciones.append(totalPorcentajePositivo)
    candidatosPubliNoVacias.append(publiNoVacias)
    candidatosPubliVacias.append(publiVacias)
    posID+=1
print()
print("PORCENTAJE DE POSITIVIDAD DE LOS COMENTARIOS DE FACEBOOK DE LAS PUBLICACIONES DE LOS CANDIDATOS:\n")
for i in range(len(candidatos)):
    print(candidatos[i]+ ': {0:0.2f}%'.format(aprobaciones[i]))
    print('  Publicaciones con comentarios: {}'.format(candidatosPubliNoVacias[i]))
    print('  Publicaciones vacias: {}'.format(candidatosPubliVacias[i]))
    print()

