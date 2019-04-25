from django.urls import path
from .views import homepage, singlepost, userpanel, createpost, editpost, login, registration, logout, delete, liketopost

urlpatterns = [
    path('', homepage, name="homepage"),
    path('post/<int:id>/', singlepost, name='singlepost'),
    path('user/', userpanel, name='userpanel'),
    path('create-post/', createpost, name='createpost'),
    path('edit-post/<int:id>/', editpost, name='editpost'),
    path('delete-post/<int:id>/', delete, name='deletepost'),
    path('liketopost/<int:id>', liketopost, name='liketopost'),
    path('login/', login, name='login'),
    path('logout', logout, name='logout'),
    path('registration/', registration, name='registration'),


]