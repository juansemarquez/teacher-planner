from django.urls import path
from . import views

urlpatterns = [
        path("", views.index, name="index"),
        path("login/", views.login_view, name="login_view"),
        path("logout", views.logout_view, name="logout"),
        path("register", views.register, name="register"),
        #Get->index #post->store
        path("schools", views.schools, name="schools"), 
        #Get->show #post->update
        path("schools/<int:school_id>", views.schools_show, name="school"),
        path("schools/create", views.schools_create, name="school_create"),
        path("schools/<int:school_id>/edit", views.schools_edit, 
             name="school_edit"),
        path("schools/<int:school_id>/delete", views.schools_delete, 
             name="school_delete")
        ]
