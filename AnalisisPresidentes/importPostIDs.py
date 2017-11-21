#cada vez que descargues los postIds de un presidente, hay que ir cambiando el user_id
import requests

graph_api_version = 'v2.9'

'''lo tuve que ir refreshing cada hora y no tuve problemas con facebook'''
access_token = 'EAACEdEose0cBABPoFCuODRz05tkrmzXecOSZCx994oKSZAmziUVVDFE4xm02OCTyBkdgZCEOhBmGIteEkRZBBDbkSZCJ8hKfs7sIBt4ur9nVAWejNHk9iGhsdojDNNocmY0CuTIMEtUVHhzjuu1tw8TUMy7QlVdZAZCpzuwXLnymbJbtMJAggMCMZAARM9G5ZAEwZD'

# presidentes' Facebook user id
user_id = '1481491872064849' #en este caso es de alejandro guillier

#FECHA DESDE PRIMARIAS HASTA DIA DE VOTACION
#since=2017-07-02&until=2017-11-19
# the graph API endpoint for ids on presidente's post
url = 'https://graph.facebook.com/{}/{}/posts?since=2017-11-16&until=2017-11-19'.format(graph_api_version, user_id)

#hacer una lista de los post_ids
postIds = []
r = requests.get(url, params={'access_token': access_token})
while True:
    data = r.json()

    # catch errors returned by the Graph API
    if 'error' in data:
        raise Exception(data['error']['id'])

    # append the text of each id into the postIds list
    for id in data['data']:
        # remove line breaks in each id
        text = id['id'].replace('\n', ' ')
        postIds.append(text)

    print('got {} postIds'.format(len(data['data'])))

    # check if there are more postIds
    if 'paging' in data and 'next' in data['paging']:
        r = requests.get(data['paging']['next'])
    else:
        break

# guardar los postIds a un archivo llamado NombreDePresidentePostIds.txt
with open('PresiPostIds.txt', 'w', encoding='utf-8') as f:
    for id in postIds:
        f.write(id + '\n')