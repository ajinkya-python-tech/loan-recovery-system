from django.urls import path
from . import views

urlpatterns = [

    # LOGIN
    path(
        '',
        views.home_view,
        name='home'
    ),
    path(
    'login/',
    views.login_view,
    name='login'
),
    # SIGNUP
    path(
        'signup/',
        views.signup_view,
        name='signup'
    ),

    # LOGOUT
    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # ADD CASE
    path(
        'add-case/',
        views.add_case,
        name='add_case'
    ),

    # ANALYTICS DASHBOARD
    path(
        'dashboard/',
        views.dashboard_view,
        name='dashboard'
    ),

    # CASE LIST
    path(
        'cases/',
        views.case_list,
        name='case_list'
    ),

    # EDIT CASE
    path(
        'edit-case/<int:case_id>/',
        views.edit_case,
        name='edit_case'
    ),

    # DELETE CASE
    path(
        'delete-case/<int:case_id>/',
        views.delete_case,
        name='delete_case'
    ),

]