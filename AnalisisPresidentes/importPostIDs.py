#cada vez que descargues los postIds de un presidente, hay que ir cambiando el user_id
import requests

graph_api_version = 'v2.9'

'''lo tuve que ir refreshing cada hora y no tuve problemas con facebook'''
access_token = 'EAACEdEose0cBAFtRKzdZCa2rLXNYlHdRRXd2mNAY4GtUWswPzVhL9WnDpnwRtArMcspjLSTRn3hC9aHciowVcHZCQ9IR2jJOZBh26p3E7fKv4hZBSu2u52v3ma5Bx67pgDX1EmnvYoG8KRA3lnZBZCu9HtWY5TyvBS7xSiQGPN7FzMug4ZBT34ba5lfvC2ERbQZD'

# presidentes' Facebook user id
user_id = '10152723078' #en este caso es de alejandro navarro

#FECHA DESDE PRIMARIAS HASTA DIA DE VOTACION
#since=2017-07-02&until=2017-11-19
# the graph API endpoint for ids on presidente's post
url = 'https://graph.facebook.com/{}/{}/posts?since=2017-11-15&until=2017-11-19'.format(graph_api_version, user_id)

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
with open('AlejandoNavarro_postIds_desdeLasPrimarias.txt', 'w', encoding='utf-8') as f:
    for id in postIds:
        f.write(id + '\n')