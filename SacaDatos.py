import requests
import facebook

# Su Token, por alguna razon no me deja usar uno de una cuenta temporal de prueba :c
access_token = 'EAACEdEose0cBAPZCkZAZCLOF4AM0XiqbHHsbkDCFzpgvHB7GVlZAiArqPEZAazmOEX2Bmt2JbpafNybUS4wI8a0OGpLddN9CDtFbAZAxIQqejJFB6RhvWlIrR5LPZBAM6C3EAyV62bK0OxQTZCNPccil9I24ycwG6qcM9RrGT0SuzR7lXVr4cZA29AXtRu2D4FZAIZD'

# Facebook user id de la pagina de piñera
user_id = "553775568008058"

# post id de una publicacion de la pagina de piñera
post_id = "1698259343559669"

# conectar con la api graph de facebook
graph = facebook.GraphAPI(access_token=access_token, version="2.10")

# obtener el usuario, esto retorna un diccionario(si no me equivoco) con un id y nombre
usuario = graph.get_object(id=user_id, fields='name')
# del diccionario usuario, guardo el campo de nombre nomas
nombre = usuario['name']

# empece a probar con varios que encontré
about = graph.get_object(id=user_id, fields='about')
categoria = graph.get_object(id=user_id, fields='category')
hablando = graph.get_object(id=user_id, fields='talking_about_count')
likes = graph.get_object(id=user_id, fields='fan_count')  # likes en la página
# Esta la encontré util por si hacemos automatico la busqueda de los candidatos(asegurarnos que sea la oficial)
es_verificada = graph.get_object(id=user_id, fields='is_verified')
#####################
# ESTAS SON LAS IMPORTANTES
# saca los comentarios de una publicacion de piñera(id=idPiñera_idPost), pero solo de un post dado
comentarios = graph.get_object(id="553775568008058_1698259343559669", fields='comments')
#print(comentarios['comments'])

# Busca las publicaciones del usuario y entrega en un diccionario
# el id de la publicación, y los comentarios, que a su vez tienen mas "ramificaciones"
# como la fecha del comentario, el mensaje en si y la persona que comenta junto a su id
# saca MUCHOS comentarios, falta ver como separarlos todos
prueba = graph.get_object(id=user_id, fields='posts{id,comments}')
print('Encontrados {} posts'.format(len(prueba['posts'])))
print(prueba)

#####################


# Intento de llegar a alguna de las ramificaciones, ta malo :(
# Alguien intente sacar usando for algun comentario unico
# print(prueba['posts'])
# for id in prueba['posts']:
#    print(id)

# Mostrar algo corto, funciona
# print("Imprimiento la informacion de " +nombre+ ":")
# print("Likes en la página: ")
# print(likes['fan_count'])
# print(about['about'])
