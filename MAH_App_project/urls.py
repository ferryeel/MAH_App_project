
from django.contrib import admin
from django.urls import include, path
from graphene_django.views import GraphQLView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('MAH_App.urls')),
    path("graphql/", GraphQLView.as_view(graphiql=True)),
]


