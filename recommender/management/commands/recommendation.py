from django.core.management.base import BaseCommand
from recommender.domain import RecommendationCommand

class Command(BaseCommand):

    def handle(self, *arg, **options):

        RecommendationCommand.run()
