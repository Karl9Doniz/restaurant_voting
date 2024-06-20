from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from core.models import Restaurant, Menu, Vote

User = get_user_model()

VOTING_RESULTS_URL = reverse("restaurant:voting-list")


def create_user(**params):
    """Helper function to create a new user"""
    return User.objects.create_user(**params)


def create_restaurant(**params):
    """Helper function to create a new restaurant"""
    defaults = {
        "name": "Sample Restaurant",
    }
    defaults.update(params)
    return Restaurant.objects.create(**defaults)


def create_menu(restaurant, **params):
    """Helper function to create a new menu"""
    defaults = {
        "date": timezone.now().date(),
        "items": "Pizza, Salad, Pasta",
    }
    defaults.update(params)
    return Menu.objects.create(restaurant=restaurant, **defaults)


def create_vote(employee, menu):
    """Helper function to create a new vote"""
    return Vote.objects.create(employee=employee, menu=menu)


class VotingResultsTests(TestCase):
    """Test voting results functionality"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="test@example.com",
                                password="testpass123")
        self.client.force_authenticate(self.user)

    def test_no_votes(self):
        """Test case when no votes have been cast"""
        res = self.client.get(VOTING_RESULTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_single_vote(self):
        """Test case with a single vote"""
        restaurant = create_restaurant()
        menu = create_menu(restaurant)
        create_vote(self.user, menu)
        res = self.client.get(VOTING_RESULTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_multiple_votes(self):
        """Test case with multiple votes for the same menu"""
        restaurant = create_restaurant()
        menu = create_menu(restaurant)
        create_vote(self.user, menu)
        another_user = create_user(email="another@example.com",
                                   password="testpass123")
        create_vote(another_user, menu)
        res = self.client.get(VOTING_RESULTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_votes_across_menus(self):
        """Test case with votes across multiple menus"""
        restaurant = create_restaurant()
        menu1 = create_menu(restaurant)
        menu2 = create_menu(
            restaurant, date=timezone.now().date() + timezone.timedelta(days=1)
        )
        create_vote(self.user, menu1)
        another_user = create_user(email="another@example.com",
                                   password="testpass123")
        create_vote(another_user, menu2)
        res = self.client.get(VOTING_RESULTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
