"""
URL configuration for DiplomProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from booking.views.booking import (
    BookingListCreateView,
    BookingRetrieveUpdateView,
    ConfirmBookingView, RejectBookingView,
)
from booking.views.rent import (
    RentalListCreateView,
    RentalRetrieveUpdateDeleteView,
    )
from booking.views.review import (
    ReviewListCreateView,
    ReviewRetrieveUpdateView,
    RentalReviewsView,
)
from booking.views.user import (
    RegisterUserAPIView,
    LogInAPIView,
    LogOutAPIView,
    )

schema_view = get_schema_view(
    openapi.Info(
        title='Bookings API',
        default_version='v1',
        description='Our Books API with permissions',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='test.email@gmail.com'),
        license=openapi.License(name='OUR LICENSE', url='https://example.com')
    ),
    public=False,
    permission_classes=[permissions.IsAdminUser],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LogInAPIView.as_view()),
    path('logout/', LogOutAPIView.as_view()),
    path('register/', RegisterUserAPIView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),

    path('rental/', RentalListCreateView.as_view(), name='rental-list-create'),
    path('rental/<int:pk>/', RentalRetrieveUpdateDeleteView.as_view(), name='rental-retrieve-update-delete'),
    path('rental/<int:pk>/reviews/', RentalReviewsView.as_view(), name='rental-reviews'),

    path('booking/', BookingListCreateView.as_view(), name='booking-list-create'),
    path('booking/<int:pk>/', BookingRetrieveUpdateView.as_view(), name='booking-retrieve-update'),
    path('booking/<int:pk>/confirm/', ConfirmBookingView.as_view(), name='booking-confirm'),
    path('booking/<int:pk>/reject/', RejectBookingView.as_view(), name='booking-reject'),

    path('reviews/', ReviewListCreateView.as_view(), name='reviews-list-create'),
    path('reviews/<int:pk>.', ReviewRetrieveUpdateView.as_view(), name='reviews-retrieve-update'),
]
