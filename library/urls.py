from django.urls import path
from rest_framework.routers import DefaultRouter

from library.views import BookViewSet, AuthorViewSet, GenreViewSet, RentalViewSet
from users.apps import UsersConfig
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name


router = DefaultRouter()
router.register(r"books", BookViewSet, basename="books")
router.register(r"authors", AuthorViewSet, basename="authors")
router.register(r"genres", GenreViewSet, basename="genres")
router.register(r"rent", RentalViewSet, basename="rent")


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
