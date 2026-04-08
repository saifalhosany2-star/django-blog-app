from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, register_request, login_request, logout_request

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_request, name='register'),
    path('login/', login_request, name='login'),
    path('logout/', logout_request, name='logout'),
]