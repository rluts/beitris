import re

from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.Wrapper import EndPointInternalError
from urllib.error import HTTPError
from wikidata.client import Client

from common.exceptions import WikidataSparQLError, WikidataResultError
from quiz.models import Object, Category, ObjectAlias
from .constants import SPARQL_BASE_URL, SPARQL_WIKIDATA_QUERY, USER_AGENT


class ObjectFactory:

    filters = []  # [{'property': 'P31', 'entity': 'Q3624078'}]
    language = 'en'
    category_name = None
    aliases = []

    def __init__(self, logger, filters=None, language=None, aliases=None,
                 category_name=None, query=None):
        self.filters = filters or self.filters
        self.language = language or self.language
        self.aliases = aliases or self.aliases
        self.category_name = category_name or self.category_name
        logger.info("Started task ")
        if (not self.filters or not self.category_name) and not query:
            raise NotImplementedError('Set filters and category name')
        self.logger = logger
        self.query = query or self.prepare_query()
        self.data = self.load_data()
        self.client = None

    def prepare_query(self):
        self.logger.info('Generating query')
        return SPARQL_WIKIDATA_QUERY.format(
            language=self.language,
            filters=self.generate_filter()
        )

    def generate_filter(self):
        wd_filters = ''
        for wd_filter in self.filters:
            wd_prop, wd_entity = wd_filter.values()
            wd_filters += f'    ?item wdt:{wd_prop} wd:{wd_entity}.\n'
        return wd_filters

    def load_data(self):
        try:
            self.logger.info('Start to load data')
            sparql = SPARQLWrapper(SPARQL_BASE_URL, agent=USER_AGENT)
            self.logger.info('Get SparQL request from Wikidata')
            sparql.setQuery(self.query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            self.logger.info('Data loaded')
        except (HTTPError, EndPointInternalError):
            raise WikidataSparQLError

        try:
            return self.parse_wikidata_results(results)
        except KeyError:
            raise WikidataResultError

    def save_data_to_db(self):
        self.logger.info('Starting to save data')
        self.client = Client()
        category = Category.objects.create(name=self.category_name, language=self.language)
        props = [self.client.get(alias, load=True) for alias in self.aliases]
        for obj in self.data:
            try:
                db_obj = Object.objects.create(category_id=category.id, **obj)

                self.logger.info(f"Saved {obj['name']} to database")
                wikidata_obj = self.client.get(obj['wikidata_id'], load=True)
                self.logger.info("Aliases loaded")
                self.save_aliases(wikidata_obj, props, db_obj)
            except Exception as e:
                self.logger.error(f'Can not save to db: {obj}. Error: {e}')
        return category.id

    def save_aliases(self, wikidata_obj, props, db_obj):
        try:
            aliases = []

            for alias in wikidata_obj.attributes['aliases'][self.language]:
                if alias.get('value') and re.match(r'\w+', alias['value']):
                    self.logger.info(f"{alias['value']} found. Saving to db")
                    aliases.append(ObjectAlias(name=alias['value'],
                                               object_id=db_obj.id))
        except Exception as e:
            self.logger.error(f'Unexpected error while loading aliases: {e}')
        else:
            ObjectAlias.objects.bulk_create(aliases)

        aliases = []
        try:
            for prop in props:
                alias = wikidata_obj.get(prop)
                if alias and getattr(alias, 'label', None) and alias.get(self.language):
                    self.logger.info(f"Alias {alias.label[self.language]} found."
                                     f" Saving to db")
                    aliases.append(ObjectAlias(name=alias.label[self.language],
                                               object_id=db_obj.id))
        except Exception as e:
            self.logger.error(f'Unexpected error while loading aliases: {e}')
        else:
            ObjectAlias.objects.bulk_create(aliases)

    def parse_wikidata_results(self, results):
        return list(map(self._parse_obj, results['results']['bindings']))

    @staticmethod
    def _parse_obj(obj):
        return {
            'name': obj['itemLabel']['value'],
            'wikidata_id': obj['item']['value'].split('/')[-1]}
