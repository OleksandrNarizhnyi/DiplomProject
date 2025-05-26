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
from django.urls import path

from booking.views.booking import (
    BookingListCreateView,
    BookingRetrieveUpdateView,
    confirm_booking,
    reject_booking,
    )
from booking.views.rent import (
    RentalListCreateView,
    RentalRetrieveUpdateDeleteView,
    )
from booking.views.review import (
    ReviewListCreateView,
    ReviewRetrieveUpdateView,
)
from booking.views.user import (
    RegisterUserAPIView,
    LogInAPIView,
    LogOutAPIView,
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LogInAPIView.as_view()),
    path('logout/', LogOutAPIView.as_view()),
    path('register/', RegisterUserAPIView.as_view()),
    path('rental/', RentalListCreateView.as_view()),
    path('rental/<int:pk>/', RentalRetrieveUpdateDeleteView.as_view()),

    path('booking/', BookingListCreateView.as_view()),
    path('booking/<int:pk>/', BookingRetrieveUpdateView.as_view()),
    path('booking/<int:pk>/confirm/', confirm_booking),
    path('booking/<int:pk>/reject/', reject_booking),

    path('reviews/', ReviewListCreateView.as_view()),
    path('reviews/<int:pk>.', ReviewRetrieveUpdateView.as_view()),
]
