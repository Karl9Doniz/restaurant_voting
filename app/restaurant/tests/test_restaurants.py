from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Restaurant, Menu
from django.utils import timezone
from django.contrib.auth import get_user_model

RESTAURANTS_URL = reverse("restaurant:restaurant-list")
MENUS_URL = reverse("restaurant:menu-list")


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
        "date": "2024-06-20",
        "items": "Pizza, Salad, Pasta",
    }
    defaults.update(params)
    return Menu.objects.create(restaurant=restaurant, **defaults)


class PublicRestaurantAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_restaurants(self):
        """Test authentication is required to access restaurants"""
        res = self.client.get(RESTAURANTS_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_required_for_menus(self):
        """Test authentication is required to access menus"""
        res = self.client.get(MENUS_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateRestaurantAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.client.force_authenticate(self.user)

    def test_create_restaurant(self):
        """Test creating a restaurant"""
        payload = {"name": "New Restaurant"}
        res = self.client.post(RESTAURANTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        restaurant = Restaurant.objects.get(id=res.data["id"])
        self.assertEqual(restaurant.name, payload["name"])

    def test_list_restaurants(self):
        """Test listing restaurants for authenticated user"""
        restaurant = create_restaurant()
        res = self.client.get(RESTAURANTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], restaurant.name)

    def test_create_menu(self):
        """Test creating a menu for a restaurant"""
        restaurant = create_restaurant()
        payload = {
            "restaurant": restaurant.id,
            "date": "2024-06-21",
            "items": "Burger, Fries, Soda",
        }
        res = self.client.post(MENUS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        menu = Menu.objects.get(id=res.data["id"])
        self.assertEqual(menu.restaurant, restaurant)
        self.assertEqual(menu.items, payload["items"])


def test_list_menus(self):
    """Test listing menus for a restaurant"""
    restaurant = create_restaurant()
    menu1 = create_menu(restaurant=restaurant, date="2024-06-20")
    menu2 = create_menu(restaurant=restaurant, date="2024-06-21")
    res = self.client.get(MENUS_URL)
    self.assertEqual(res.status_code, status.HTTP_200_OK)

    self.assertTrue(isinstance(res.data, list))

    self.assertEqual(len(res.data), 2)
    self.assertEqual(res.data[0]["restaurant"]["name"], restaurant.name)
    self.assertEqual(res.data[1]["restaurant"]["name"], restaurant.name)


def test_get_current_day_menu(self):
    """Test getting the current day's menu"""
    today = timezone.now().date()
    restaurant = create_restaurant()
    create_menu(restaurant=restaurant, date=today)
    create_menu(restaurant=restaurant, date=today - timezone.timedelta(days=1))
    url = f"{MENUS_URL}?date={today}"
    res = self.client.get(url)
    self.assertEqual(res.status_code, status.HTTP_200_OK)

    self.assertTrue(isinstance(res.data, list))

    self.assertEqual(len(res.data), 1)
    self.assertEqual(res.data[0]["date"], str(today))
