from django.urls import path
from .views import views_auth, views_schools

urlpatterns = [
        path("", views_auth.index, name="index"),
        path("login/", views_auth.login_view, name="login_view"),
        path("logout", views_auth.logout_view, name="logout"),
        path("register", views_auth.register, name="register"),
        #Get->index #post->store
        path("schools", views_schools.schools, name="schools"), 
        #Get->show #post->update
        path("schools/<int:school_id>", views_schools.schools_show, name="school"),
        path("schools/create", views_schools.schools_create, name="school_create"),
        path("schools/<int:school_id>/edit", views_schools.schools_edit, 
             name="school_edit"),
        path("schools/<int:school_id>/delete", views_schools.schools_delete, 
             name="school_delete")
        ]
