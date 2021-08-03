from django.db import models
from django.db.models.fields import related
from django_elasticsearch_dsl import (
    Document,
    fields,
    Index,
)
from django_elasticsearch_dsl.registries import registry
from .models import InsuranceService
from django.contrib.auth import get_user_model


@registry.register_document
class InsuranceServiceDocument(Document):

    category = fields.TextField(attr='get_category_display')
    company = fields.ObjectField(
        properties={
            'company_name': fields.TextField()
        }
    )
    service_title = fields.TextField(attr='get_service_title')

    class Index:
        name = 'insurance_services'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = InsuranceService
        fields = [
            'minimal_payment',
            'term',
            'description'
        ]

        related_models = [get_user_model()]

    def get_queryset(self):
        return super(InsuranceServiceDocument, self).get_queryset().select_related(
            'company'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, get_user_model()):
            return related_instance.insuranceservice_set.all()
