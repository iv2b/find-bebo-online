from unittest import TestCase
from django.contrib.auth.models import User
from tweb.models import CustomUser, Score


class SimpleTest(TestCase):
    baseUser1 = None
    baseUser2 = None

    def setUp(self):
        self.baseUser1 = User.objects.create(username="u1", password="hunter2")
        self.baseUser2 = User.objects.create(username="u2", password="hunter2")

        user1 = User.objects.get(username="u1")
        user2 = User.objects.get(username="u2")

        score1 = Score.objects.create(user=user1, rating=123, time=100)
        score2 = Score.objects.create(user=user2, rating=1234, time=20)

        pass

    def test_scores(self):
        user1 = User.objects.get(username="u1")
        user2 = User.objects.get(username="u2")

        self.assertEqual(user1.username, "u1")
        self.assertEqual(user2.username, "u2")

        score1 = Score.objects.get(user=user1.id)
        score2 = Score.objects.get(user=user2.id)

        self.assertEqual(score1.rating, 123)
        self.assertEqual(score2.rating, 1234)
        self.assertEqual(score1.time, 100)
        self.assertEqual(score2.time, 20)
