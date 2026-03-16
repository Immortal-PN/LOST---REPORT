from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage, FoundItem, LostItem


class CorePageTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="password123",
            email="owner@example.com",
        )
        self.user = User.objects.create_user(
            username="member",
            password="password123",
            email="member@example.com",
        )
        LostItem.objects.create(
            user=self.owner,
            title="Lost Wallet",
            description="Black leather wallet",
            category="wallet",
            location="Library",
            date_lost="2026-03-10",
        )
        FoundItem.objects.create(
            user=self.owner,
            title="Found Keys",
            description="Keys with a blue keychain",
            category="keys",
            location="Cafeteria",
            date_found="2026-03-11",
        )

    def test_home_page_renders(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "LostLink")

    def test_protected_pages_redirect_to_login(self):
        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_profile_page_renders_for_logged_in_user(self):
        self.client.login(username="member", password="password123")

        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your Activity")

    def test_inbox_page_renders_existing_messages(self):
        ContactMessage.objects.create(
            sender=self.user,
            receiver=self.owner,
            message="I think I found your wallet.",
        )
        self.client.login(username="owner", password="password123")

        response = self.client.get(reverse("inbox"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I think I found your wallet.")

    def test_contact_user_rejects_empty_message(self):
        self.client.login(username="member", password="password123")

        response = self.client.post(
            reverse("contact_user", args=[self.owner.id]),
            {"message": "   "},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contact_user_creates_message(self):
        self.client.login(username="member", password="password123")

        response = self.client.post(
            reverse("contact_user", args=[self.owner.id]),
            {"message": "Please check your inbox."},
        )

        self.assertRedirects(response, reverse("home"))
        self.assertEqual(ContactMessage.objects.count(), 1)
