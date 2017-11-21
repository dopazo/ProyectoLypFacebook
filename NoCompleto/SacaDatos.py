import requests
import facebook
import json
import datetime

# Su Token, por alguna razon no me deja usar uno de una cuenta temporal de prueba :c
access_token = 'EAACEdEose0cBALotohafHTnp3qVjjLGpsnsG2Q5tGez0QZApdQkzZCecOPZBoUlC2LZBGwHjvxBRcFT3ScWVkS22Biz8eKZCENZBNzRMLpOkHX9daBPSH6iMbv68BnR3Ena0gRoXGNZAZAZBcZCxB10wuZCHM6mruwSXQ9CgtAYKjmgdEqtGBhShiZAPSwhaiJClKqcZD'

# Facebook user id de la pagina de Guiller
user_id = "1481491872064849"
#553775568008058

# post id de una publicacion de la pagina de piñera
post_id = "1698259343559669"

# conectar con la api graph de facebook
graph = facebook.GraphAPI(access_token=access_token, version="2.10")

# obtener el usuario, esto retorna un diccionario con un id y nombre
usuario = graph.get_object(id=user_id, fields='name')
# del diccionario usuario, guardo el campo de nombre nomas
nombre = usuario['name']

# empece a probar con varios que encontré
#about = graph.get_object(id=user_id, fields='about')
#categoria = graph.get_object(id=user_id, fields='category')
#hablando = graph.get_object(id=user_id, fields='talking_about_count')
#likes = graph.get_object(id=user_id, fields='fan_count')  # likes en la página
# Esta la encontré util por si hacemos automatico la busqueda de los candidatos(asegurarnos que sea la oficial)
#es_verificada = graph.get_object(id=user_id, fields='is_verified')
#####################
# Busca las publicaciones del usuario y entrega en un diccionario
# el id de la publicación, y los comentarios, que a su vez tienen mas "ramificaciones"

#FECHA DESDE LAS PRIMARIAS HASTA EL DIA DE LAS VOTACIONES
# since=2017-07-02,until=2017-11-19
# datetime.datetime(aa,mm,dd,hh,mm,ss).timestamp()
sinceDate=int(datetime.datetime(2017,11,21,15,00,00).timestamp())
untilDate=int(datetime.datetime(2017,11,21,16,00,00).timestamp())

prueba = graph.get_object(id=user_id, fields='posts{id,comments, message,since=sinceDate,until=untilDate}')
#print('Encontrados {} posts'.format(len(prueba['posts']['data'])))

#print(prueba['posts']['data'][0]['comments']['data'])
#print(prueba['posts']['data'][0])

allData = []
vWhile=0
vFor=0
posts = prueba['posts']
while True:
    try:
        print("vuelta del while")
        vWhile=vWhile+1
        for dato in posts:
            allData.append(posts)
            print("vuelta del for")
            #Sacar mas comments de cada post
            if 'paging' in posts['data']['comments'] and 'next' in posts['data']['comments']['paging']:
                posts = requests.get(posts['data']['comments']['paging']['next']).json()
                print('Encontrados {} comments'.format(len(posts['data']['comments'])))
            vFor=vFor+1
        #Sacar mas posts
        if 'paging' in posts and 'next' in posts['paging']:
            posts = requests.get(posts['paging']['next']).json()
            print('Encontrados {} posts'.format(len(posts['data'])))
        else:
            break
    except KeyError as e:
        print("ERROR {}".format(str(e)))
        break

print("...vueltas del While: ")
print(vWhile)
print("...vueltas del For: ")
print(vFor)
#print(allData)

with open('data.json', 'w') as outfile:
    json.dump(allData, outfile, indent=4)

#with open('data.json', 'w') as outfile:
#    json.dump(prueba, outfile, indent=4)

#####################

# Mostrar algo corto, funciona
# print("Imprimiento la informacion de " +nombre+ ":")
# print("Likes en la página: ")
# print(likes['fan_count'])
# print(about['about'])
