import requests
import facebook
import json

# Su Token, por alguna razon no me deja usar uno de una cuenta temporal de prueba :c
access_token = 'EAACEdEose0cBANkkc4LInviv23s3TXofmmiTaZCV0UupN0jay9ueo9jq5KkWZAAmMKzSsYWJaHJHhvEOnN87Ypd8YPRj2ceFecceug9QRlPUdZAGBXDuZCZCC9lYNy1xJA6zPtW6OBvryhxD3aYPS7geKVjpZBDbzQZASxlvfs9RJlByzDIqpTmZBHfFipmeCtgZD'

# Facebook user id de la pagina de piñera
user_id = "553775568008058"
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

prueba = graph.get_object(id=user_id, fields='posts{id,comments, message}')
print('Encontrados {} posts'.format(len(prueba['posts']['data'])))
#print(prueba['posts']['data'][0]['comments']['data'])
#print(prueba['posts']['data'][0])

while True:
    try:
        print("vueltas while")
        for prueba in prueba['post']['data']:
            print("vueltas for prueba")
            with open('data.json', 'a') as outfile: # 'w' sobreescribir, 'a' escribir al final
                json.dump(prueba, outfile, indent=4)
        # Attempt to make a request to the next page of data, if it exists.
        prueba = requests.get(prueba['posts']['data']['paging']['next']).json()
    except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
        print("error")
        break



#with open('data.json', 'w') as outfile:
#    json.dump(prueba, outfile, indent=4)

#####################

# Mostrar algo corto, funciona
# print("Imprimiento la informacion de " +nombre+ ":")
# print("Likes en la página: ")
# print(likes['fan_count'])
# print(about['about'])
