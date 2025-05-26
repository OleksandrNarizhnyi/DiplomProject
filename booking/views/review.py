from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from booking.models.review import Review
from booking.permissions.custom_permissions import IsBookingOwner
from booking.serializers.review import ReviewListSerializer, ReviewCreateUpdateSerializer


class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.select_related(
        'user', 'rental',
    ).all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ReviewListSerializer
        return ReviewCreateUpdateSerializer


class ReviewRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ReviewListSerializer
        return ReviewCreateUpdateSerializer

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsBookingOwner()]
        return [IsAuthenticated()]

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You can only edit your reviews")
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class RentalReviewsView(ListAPIView):
    serializer_class = ReviewListSerializer

    def get_queryset(self):
        rental_id = self.kwargs.get('pk')
        return Review.objects.filter(rental_id=rental_id).order_by('-created_at')