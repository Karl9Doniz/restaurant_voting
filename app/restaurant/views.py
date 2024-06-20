from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from core.models import Restaurant, Menu, Vote
from .serializers import RestaurantSerializer, MenuSerializer, VotingResultSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Menu.objects.all()
        date = self.request.query_params.get("date", None)
        if date is not None:
            queryset = queryset.filter(date=date)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class VotingResultsViewSet(viewsets.ViewSet):
    def list(self, request):
        today = timezone.now().date()
        votes = Vote.objects.filter(menu__date=today)
        menus = Menu.objects.filter(date=today).prefetch_related("votes")

        voting_results = []
        for menu in menus:
            menu_votes = votes.filter(menu=menu)
            vote_count = menu_votes.count()
            voting_results.append(
                {"menu": menu, "vote_count": vote_count, "votes": menu_votes}
            )

        serializer = VotingResultSerializer(voting_results, many=True)
        return Response(serializer.data)
