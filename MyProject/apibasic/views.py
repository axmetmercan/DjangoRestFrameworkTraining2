
from operator import imod
from os import stat
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.









@api_view(['GET', 'POST'])
def article_list(request):

    if request.method == 'GET':
        articles = Article.objects.all()
        serialazier = ArticleSerializer(articles, many= True)

        return Response(serialazier.data)

    elif request.method == 'POST':
        
        serialazier = ArticleSerializer(data = request.data)


        if serialazier.is_valid():
            serialazier.save()
            return Response(serialazier.data, status = status.HTTP_201_CREATED)
        return Response(serialazier.errors, status = status.HTTP_400_BAD_REQUEST)

###Function Based Views
@api_view(['GET','PUT', 'DELETE'])
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk = pk)
    except Article.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serialazier = ArticleSerializer(article)

        return Response(serialazier.data)
     
    elif request.method == 'PUT':
        serialazier = ArticleSerializer(article, data = request.data)

        if serialazier.is_valid():
            serialazier.save()
            return Response(serialazier.data)
        return Response(serialazier.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':

        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


###Class Based Views


class ArticleApiView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serialazier = ArticleSerializer(articles, many= True)

        return Response(serialazier.data)

    def post(self, request):
        serialazier = ArticleSerializer(data = request.data)

        if serialazier.is_valid():
            serialazier.save()
            return Response(serialazier.data, status = status.HTTP_201_CREATED)
        return Response(serialazier.errors, status = status.HTTP_400_BAD_REQUEST)


class ArticleDetails(APIView):

    def get_object(self, pk):
        try:
            return Article.objects.get(pk = pk)
        except Article.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        article = self.get_object((pk))
        serialazier = ArticleSerializer(article)
        return Response(serialazier.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serialazier = ArticleSerializer(article, data = request.data)

        if serialazier.is_valid():
            serialazier.save()
            return Response(serialazier.data)
        return Response(serialazier.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)



class GenericApiView(generics.GenericAPIView, mixins.ListModelMixin,
                                              mixins.CreateModelMixin,
                                              mixins.UpdateModelMixin,
                                              mixins.DestroyModelMixin,
                                              mixins.RetrieveModelMixin
                                              ):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_field = 'id'
    def get(self, request, id = None):

        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id= None):
        return self.update(request, id)

    def delete(self, request, id):
        self.destroy(request, id)