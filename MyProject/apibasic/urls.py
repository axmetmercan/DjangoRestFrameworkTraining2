from django.urls import path
from .views import article_detail, article_list, ArticleApiView, ArticleDetails, GenericApiView

urlpatterns = [
    path('fbarticle/', article_list),
    path('fbdetail/<int:pk>', article_detail),
    path('cbarticle/', ArticleApiView.as_view()),
    path('cbdetail/<int:pk>', ArticleDetails.as_view()),
    path('gcbarticle/<int:id>', GenericApiView.as_view()),
    path('gcbarticle/', GenericApiView.as_view()),



]
