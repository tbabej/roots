from django.test import TestCase

import problems.models
from models import Competition
from django.contrib.auth.models import Group

from django.db import IntegrityError

class CompetitionCreationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.group = Group(name="TestOrganizers")
        cls.group.save()

    def test_create_simple_competition(self):
        competition = Competition(name="TestCompetition")
        competition.save()

    def test_create_competition_with_organizer_group(self):
        competition = Competition(name="TestCompetition",
                                  organizer_group=self.group)
        competition.save()

    def test_create_duplicate_competitions(self):
        competition1 = Competition(name="DuplicateCompetition")
        competition2 = Competition(name="DuplicateCompetition")

        with self.assertRaises(IntegrityError):
            competition1.save()
            competition2.save()
