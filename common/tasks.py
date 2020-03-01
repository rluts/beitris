from celery import shared_task
from celery.utils.log import get_task_logger
from .factories.base_factory import ObjectFactory
from .models import Factory as FactoryModel

logger = get_task_logger(__name__)


@shared_task
def run_factory(factory_id):
    logger.info('Starting to create objects')
    try:
        factory_db_obj = FactoryModel.objects.get(pk=factory_id)
    except FactoryModel.DoesNotExist:
        logger.error('Factory model does not exist')
        return {'error': True, 'message': "Factory model does not exist"}
    filters = [
        {'property': object_filter.property, 'entity': object_filter.entity}
        for object_filter in factory_db_obj.factoryfilter_set.all()]
    aliases = [alias.property for alias in factory_db_obj.alias_set.all()]
    if not filters:
        logger.error("Filters don't exists")
        return {'error': True, 'message': "Filters don't exists"}
    factory = ObjectFactory(
        logger, filters=filters, aliases=aliases,
        category_name=factory_db_obj.category_name,
        language=factory_db_obj.language)
    factory.save_data_to_db()