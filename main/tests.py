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
        self.other_lost_item = LostItem.objects.create(
            user=self.user,
            title="Lost Phone",
            description="Blue phone",
            category="electronics",
            location="Bus Stand",
            date_lost="2026-03-12",
        )
        self.other_found_item = FoundItem.objects.create(
            user=self.user,
            title="Found Bag",
            description="Grey backpack",
            category="other",
            location="Station Road",
            date_found="2026-03-13",
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

    def test_profile_can_delete_own_lost_item(self):
        self.client.login(username="member", password="password123")

        response = self.client.post(
            reverse("delete_lost_item", args=[self.other_lost_item.id]),
        )

        self.assertRedirects(response, reverse("profile"))
        self.assertFalse(LostItem.objects.filter(id=self.other_lost_item.id).exists())

    def test_profile_cannot_delete_other_users_found_item(self):
        owner_found_item = FoundItem.objects.filter(user=self.owner).first()
        self.client.login(username="member", password="password123")

        response = self.client.post(
            reverse("delete_found_item", args=[owner_found_item.id]),
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(FoundItem.objects.filter(id=owner_found_item.id).exists())

    def test_lost_page_shows_recent_found_items_section(self):
        response = self.client.get(reverse("lost_items"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Recently Found Items")
        self.assertContains(response, self.other_found_item.title)

    def test_found_page_shows_recent_lost_items_section(self):
        response = self.client.get(reverse("found_items"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Recently Lost Items")
        self.assertContains(response, self.other_lost_item.title)

    def test_report_found_prefills_when_matching_lost_item(self):
        self.client.login(username="member", password="password123")
        lost_item = LostItem.objects.filter(user=self.owner).first()

        response = self.client.get(
            reverse("report_found") + f"?lost_item={lost_item.id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Selected lost item")
        self.assertContains(response, lost_item.title)

    def test_report_found_can_create_match_from_lost_item(self):
        self.client.login(username="member", password="password123")
        lost_item = LostItem.objects.filter(user=self.owner).first()

        response = self.client.post(
            reverse("report_found"),
            {
                "lost_item_id": lost_item.id,
                "location": "Platform 2",
                "date_found": "2026-03-15",
                "found_time": "10:30",
                "handover_location": "Station help desk",
            },
        )

        self.assertRedirects(response, reverse("found_items"))
        matched_found_item = FoundItem.objects.exclude(matched_lost_item=None).latest("id")
        self.assertEqual(matched_found_item.matched_lost_item, lost_item)
        self.assertEqual(matched_found_item.title, lost_item.title)
        self.assertEqual(matched_found_item.handover_location, "Station help desk")
