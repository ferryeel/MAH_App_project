
from django.contrib import admin
from django.urls import include, path
from graphene_django.views import GraphQLView

from MAH_App import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MAH_App.urls')),
    path('api/', include('MAH_App.urls')),
    path("graphql/", GraphQLView.as_view(graphiql=True)),
    path('', views.dashboard_view, name='dashboard'),
]


