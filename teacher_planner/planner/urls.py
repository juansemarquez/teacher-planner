from django.urls import path
from .views import views_auth, views_schools, views_classes

urlpatterns = [
        path("", views_auth.index, name="index"),
        path("login/", views_auth.login_view, name="login_view"),
        path("logout", views_auth.logout_view, name="logout"),
        path("register", views_auth.register, name="register"),
        
        ### SCHOOLS ###
        #Get->index #post->store
        path("schools", views_schools.schools, name="schools"), 
        #Get->show #post->update
        path("schools/<int:school_id>", views_schools.schools_show, name="school"),
        path("schools/create", views_schools.schools_create, name="school_create"),
        path("schools/<int:school_id>/edit", views_schools.schools_edit, 
             name="school_edit"),
        path("schools/<int:school_id>/delete", views_schools.schools_delete, 
             name="school_delete"),

        ### CLASS GROUPS ###
        path("classes", views_classes.index, name="classes"),
        path("classes/<int:class_id>", views_classes.show, name="one_class"),
        path("classes/create", views_classes.create, name="class_create"),
        path("classes/<int:class_id>/edit", views_classes.edit, 
            name="class_edit"),
        path("classes/<int:class_id>/delete", views_classes.delete, 
            name="class_delete"),
        path("classes/<int:class_id>/create_schedule", 
            views_classes.store_schedule, name="create_schedule"),
        path("classes/update_schedule/<int:schedule_id>",
            views_classes.update_schedule, name="update_schedule"),
        path("classes/delete_schedule/<int:schedule_id>",
            views_classes.delete_schedule, name="delete_schedule"),
        ]
