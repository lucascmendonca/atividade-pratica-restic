from typing import Any
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Livro
from .serializers import LivroSerializer

# Objeto para renderizar as response em JSON
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def livro_list_create(request):
    
    #Ajustei os blocos condicionais para uma leitura de if/elif mais familiar para mim
    if request.method == 'GET':
        livros = Livro.objects.all()
        serializer = LivroSerializer(livros, many = True)
        return JSONResponse(serializer.data)
    
    elif request.method == 'POST':
        #Aplicando um Parse de json para que seja possível a leitura das informações
        livro_data = JSONParser().parse(request)
        serializer = LivroSerializer(data = livro_data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status = status.HTTP_201_CREATED)
        return JSONResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    # Coloquei um eles para caso a request do usuário não de em nada
    else:
        return JSONResponse(status = status.HTTP_406_NOT_ACCEPTABLE)

@csrf_exempt
def livro_detail(request,pk):
    
    livro = Livro.objects.get(pk=pk)

    if request.method == 'GET':
        serializer = LivroSerializer(livro)
        return JSONResponse(serializer.data)
    
    elif request.method == 'PUT':
        livro_data = JSONParser().parse(request)
        serializer = LivroSerializer(livro, data = livro_data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        livro.delete()
        return JSONResponse(status = status.HTTP_204_NO_CONTENT)
    
    else:
        return JSONResponse(status = status.HTTP_406_NOT_ACCEPTABLE)
