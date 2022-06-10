from django.urls import path
from . import views
from .views import TaskCreateAndList, Login, Register, TaskViewSet
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', TaskViewSet.as_view(), name='home'),
    # path('task-create/', TaskCreate.as_view(), name='create'),
    path('all-delete/', views.delete, name='all-delete'),
    path('completed-delete/', views.completed_delete, name='completed-delete'),
    path('completed/<int:pk>/', views.task_complete, name='complete'),
    path('profile/', views.profile, name='profile'),

    path('login/', Login.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', Register.as_view(), name='register'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="base/registration/password_reset_form.html"), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="base/registration/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="base/registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="base/registration/password_reset_complete.html"), name="password_reset_complete"),

]
