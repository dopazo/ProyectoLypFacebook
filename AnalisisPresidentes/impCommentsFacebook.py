import requests
import json

# LO SIGUIENTE CREA UNA LISTA DEL CONTENIDO QUE TIENE UN ARCHIVO TXT
fileRead = open('AlejandoNavarro_postIds_desdeLasPrimarias.txt')
# crear una lista de todos los post ids, pero todos los items tienen \n al final
presidente_txtList = fileRead.readlines()
# saca el \n de todos los item de la lista
presidenteSacarSlashNList = [i.replace('\n', '') for i in presidente_txtList]
# saca el user_id_ de todos los item de la lista porque queremos una lista de solo los postIds
presidenteSoloPostId_List = [i.replace('10152723078_', '') for i in presidenteSacarSlashNList]
# sacar el ultimo termino de la lista porque por alguna razon es un item empty
presidenteSoloPostId_List = presidenteSoloPostId_List[:-1]
# se puede ver esto al imprimir cada lista
#print(presidente_txtList)
#print(presidenteSacarSlashNList)
print(presidenteSoloPostId_List)

fileRead.close()
#####################################

graph_api_version = 'v2.9'
access_token = 'EAACEdEose0cBAICBsLGmZBmmBEFot6eqXEgwJj60TdaIQXcWSZBZCqJS5rhQcocHCbY5I7PirT2oUqGkDptiiHbvYz2IF31PMVSvpOZBmZAn2jJyef1v5hhWSe30u7V67XqSOPfBDoWtNDRR119t0SlkLNaZAVScpKV5zrpEZBoLENHgNDe9LrZAiGTYkvKwFBcfmgKAOKXZCSQZDZD'

# user id (id del presidente; CAMBIAR POR CADA PRESIDENTE)
user_id = '10152723078'

for id in presidenteSoloPostId_List:

    # the graph API
    url = 'https://graph.facebook.com/{}/{}_{}/comments'.format(graph_api_version, user_id, id)

    comments = []

    r = requests.get(url, params={'access_token': access_token})
    while True:
        data = r.json()

        # catch errors returned by the Graph API
        if 'error' in data:
            raise Exception(data['error']['message'])

        # append the text of each comment into the comments list
        for comment in data['data']:
            comments.append(comment)

        # check if there are more comments
        if 'paging' in data and 'next' in data['paging']:
            r = requests.get(data['paging']['next'])
            print('Encontrados {} comments'.format(len(data['data'])))
        else:
            break
    with open('AlejandroNavarroCommentsOfPost' + id + '.json', 'w', encoding='utf-8') as outfile:
        json.dump(comments, outfile, indent=4, ensure_ascii=False)