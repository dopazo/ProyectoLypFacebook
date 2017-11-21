import requests
import facebook
import json

# Su Token, por alguna razon no me deja usar uno de una cuenta temporal de prueba :c
access_token = 'EAACEdEose0cBABPoFCuODRz05tkrmzXecOSZCx994oKSZAmziUVVDFE4xm02OCTyBkdgZCEOhBmGIteEkRZBBDbkSZCJ8hKfs7sIBt4ur9nVAWejNHk9iGhsdojDNNocmY0CuTIMEtUVHhzjuu1tw8TUMy7QlVdZAZCpzuwXLnymbJbtMJAggMCMZAARM9G5ZAEwZD'

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
# ESTAS SON LAS IMPORTANTES
# saca los comentarios de una publicacion de piñera(id=idPiñera_idPost), pero solo de un post dado
#comentarios = graph.get_object(id="553775568008058_1698259343559669", fields='comments')
#print(comentarios['comments'])

# Busca las publicaciones del usuario y entrega en un diccionario
# el id de la publicación, y los comentarios, que a su vez tienen mas "ramificaciones"

#FECHA DESDE LAS PRIMARIAS HASTA EL DIA DE LAS VOTACIONES
# since=2017-07-02,until=2017-11-19

prueba = graph.get_object(id=user_id, fields='posts{id,comments, message,since=2017-11-15,until=2017-11-19}')
#print('Encontrados {} posts'.format(len(prueba['posts']['data'])))

#print(prueba['posts']['data'][0]['comments']['data'])
#print(prueba['posts']['data'][0])

allData = []
vWhile=0
vFor=0
while True:
    try:
        print("vuelta del while")
        vWhile=vWhile+1
        for dato in prueba['posts']:
            allData.append(prueba)
            print("vuelta del for")
            vFor=vFor+1
        if 'paging' in prueba and 'next' in prueba['paging']:
            prueba = requests.get(prueba['paging']['next']).json()
            print('Encontrados {} posts'.format(len(prueba['posts']['data'])))
        else:
            break
    except KeyError:
        print("ERROR")
        break

print("...vueltas del While: ")
print(vWhile)
print("...vueltas del For: ")
print(vFor)
#print(allData)

with open('data.json', 'w') as outfile:
    json.dump(allData, outfile, indent=4)


''''###while True:
    try:
        print("vuelta del while")
        for prueba['posts']['data'] in prueba:#['post']:#['data']:
            print("vuelta for prueba")
            with open('data.json', 'a') as outfile: # 'w' sobreescribir, 'a' escribir al final
                json.dump(prueba, outfile, indent=4)
        # Attempt to make a request to the next page of data, if it exists.
        prueba = requests.get(prueba['posts']['data']['paging']['next']).json()
    except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
        print("error")
        break
'''


#with open('data.json', 'w') as outfile:
#    json.dump(prueba, outfile, indent=4)

#####################

# Mostrar algo corto, funciona
# print("Imprimiento la informacion de " +nombre+ ":")
# print("Likes en la página: ")
# print(likes['fan_count'])
# print(about['about'])
