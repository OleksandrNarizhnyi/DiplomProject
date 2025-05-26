from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from booking.models.review import Review
from booking.serializers.review import ReviewListSerializer, ReviewCreateUpdateSerializer


class ReviewListCreateView(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ReviewListSerializer
        return ReviewCreateUpdateSerializer


