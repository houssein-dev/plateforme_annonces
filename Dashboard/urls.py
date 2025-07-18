from django.urls import  path
from .views import *


urlpatterns = [
    
    path(''               , annonces_dash         , name='annonces_dash'),
    path('annonces_dash/<str:pk>'       , update_annonce_dash   , name='update_annonce_dash'),
    path('annonces_delete_dash/<str:pk>', delete_annonce_dash   , name='delete_annonce_dash'),
    path('annonce_detail_dash/<str:pk>' , annonce_detail_dash   , name='annonce_detail_dash'),

    path('utilisateurs_dash/'           , utilisateurs_dash     , name='utilisateurs_dash'),
    path('update_user_dash/<str:pk>'    , update_user_dash      , name='update_user_dash'),
    path('delete_user_dash/<str:pk>'    , delete_user_dash      , name='delete_user_dash'),
    path('user_detail_dash/<str:pk>'    , user_detail_dash      , name='user_detail_dash'),
    
    path('catagories_dash/'             , catagories_dash       , name='catagories_dash'),
    path('update_catag_dash/<str:pk>'   , update_catag_dash     , name='update_catag_dash'),
    path('delete_catag_dash/<str:pk>'   , delete_catag_dash     , name='delete_catag_dash'),
    path('403/', get_403, name='page403'),

]