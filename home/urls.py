from django.urls import path
from home import views

app_name = "home"

urlpatterns = [
    path('', views.interface, name="interface"),
    path('login', views.Mylogin, name="login"),

    path('addColl', views.addCollection, name="addCollection"),
    path('editColl/<str:key>', views.editCollection, name="editCollection"),
    path('delColl/<str:key>', views.delCollection, name="delCollection"),
]