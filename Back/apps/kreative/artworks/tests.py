# apps/kreative/artworks/tests.py

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from kreative.artworks.models import Exhibition, Artwork

# --- Model Tests ---

class ExhibitionModelTests(TestCase):
    def test_create_exhibition(self):
        exhibition = Exhibition.objects.create(
            name="Modern Art Expo",
            description="An exhibition showcasing modern artworks.",
            start_date="2025-05-01",
            end_date="2025-05-10",
            location="Gallery XYZ"
        )
        self.assertEqual(exhibition.name, "Modern Art Expo")
        self.assertEqual(exhibition.location, "Gallery XYZ")
        self.assertIn("Modern Art Expo", str(exhibition))

class ArtworkModelTests(TestCase):
    def setUp(self):
        self.exhibition = Exhibition.objects.create(
            name="Contemporary Art Show",
            description="Exhibition for contemporary art.",
            start_date="2025-06-01",
            end_date="2025-06-15",
            location="Art Center"
        )
    
    def test_create_artwork(self):
        artwork = Artwork.objects.create(
            title="Sunset Overdrive",
            description="A painting of a vibrant sunset.",
            image="artworks/sunset_overdrive.jpg",
            metadata={"medium": "oil on canvas", "dimensions": "80x120cm"},
            exhibition=self.exhibition
        )
        self.assertEqual(artwork.title, "Sunset Overdrive")
        self.assertEqual(artwork.metadata["medium"], "oil on canvas")
        self.assertEqual(artwork.exhibition, self.exhibition)
        self.assertIn("Sunset Overdrive", str(artwork))

# --- API Tests ---

class ExhibitionAPITests(APITestCase):
    def setUp(self):
        self.exhibition = Exhibition.objects.create(
            name="API Exhibition",
            description="Exhibition created via API.",
            start_date="2025-07-01",
            end_date="2025-07-10",
            location="API Gallery"
        )
    
    def test_list_exhibitions(self):
        url = reverse("exhibition-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_exhibition_api(self):
        url = reverse("exhibition-list")
        data = {
            "name": "New API Exhibition",
            "description": "Exhibition created via API POST.",
            "start_date": "2025-08-01",
            "end_date": "2025-08-10",
            "location": "API New Gallery"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exhibition.objects.filter(name="New API Exhibition").count(), 1)

class ArtworkAPITests(APITestCase):
    def setUp(self):
        self.exhibition = Exhibition.objects.create(
            name="API Artwork Exhibition",
            description="Exhibition for testing artworks via API.",
            start_date="2025-09-01",
            end_date="2025-09-10",
            location="API Art Center"
        )
        self.artwork = Artwork.objects.create(
            title="API Masterpiece",
            description="An artwork created via API.",
            image="artworks/api_masterpiece.jpg",
            metadata={"style": "abstract"},
            exhibition=self.exhibition
        )
    
    def test_list_artworks(self):
        url = reverse("artwork-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_artwork_api(self):
        url = reverse("artwork-list")
        data = {
            "title": "New API Artwork",
            "description": "Artwork created via API.",
            "image": "artworks/new_api_artwork.jpg",
            "metadata": {"style": "modern"},
            "exhibition": self.exhibition.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Artwork.objects.filter(title="New API Artwork").count(), 1)
