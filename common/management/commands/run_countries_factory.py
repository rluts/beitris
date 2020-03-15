import logging

from django.core.management.base import BaseCommand
from common.factories.factories import CountryFactory
from quiz.models import QuestionType

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Command(BaseCommand):

    def handle(self, *args, **options):
        logger.info("Get countries")
        countries_factory = CountryFactory(logger)
        category_id = countries_factory.save_data_to_db()
        QuestionType.objects.create(
            text='What the country is this?',
            category_id=category_id,
            question_wikidata_prop='P18',
            type='image'
        )
        QuestionType.objects.create(
            text='What the country is this?',
            category_id=category_id,
            question_wikidata_prop='P41',
            type='image'
        )
        QuestionType.objects.create(
            text='What the country is this?',
            category_id=category_id,
            question_wikidata_prop='P242',
            type='image'
        )
