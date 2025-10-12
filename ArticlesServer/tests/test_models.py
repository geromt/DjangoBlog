from typing import Any, cast
from django.apps import apps
from django.db import models as djmodels
from django.core.exceptions import FieldDoesNotExist
import pytest


def test_article_model_exists():
    Article: Any = None
    try:
        Article = cast(Any, apps.get_model('ArticlesServer', 'Article'))
    except LookupError:
        pytest.fail("Article model not found in app 'ArticlesServer'")

    assert issubclass(Article, djmodels.Model), "Article exists but is not a Django model"


def test_article_fields_exist_and_types():
    Article: Any = None
    try:
        Article = cast(Any, apps.get_model('ArticlesServer', 'Article'))
    except LookupError:
        pytest.fail("Article model not found in app 'ArticlesServer'")

    expected = {
        'title': (djmodels.CharField, ),
        'content': (djmodels.TextField, ),
        'author': (djmodels.ForeignKey, djmodels.CharField, djmodels.OneToOneField),
        'created_at': (djmodels.DateField, djmodels.DateTimeField),
        'updated_at': (djmodels.DateField, djmodels.DateTimeField),
    }

    for field_name, allowed_types in expected.items():
        field: Any = None
        try:
            field = Article._meta.get_field(field_name)
        except FieldDoesNotExist:
            pytest.fail(f"Field '{field_name}' not found in Article model")

        if not isinstance(field, allowed_types):
            allowed_names = ', '.join(t.__name__ for t in allowed_types)
            pytest.fail(f"Field '{field_name}' exists but is not one of expected types: {allowed_names} (got {type(field).__name__})")


def test_article_id_is_uuid():
    Article: Any = None
    try:
        Article = cast(Any, apps.get_model('ArticlesServer', 'Article'))
    except LookupError:
        pytest.fail("Article model not found in app 'ArticlesServer'")

    id_field: Any = None
    try:
        id_field = Article._meta.get_field('id')
    except FieldDoesNotExist:
        pytest.fail("Field 'id' not found in Article model")

    if not isinstance(id_field, djmodels.UUIDField):
        pytest.fail(f"Field 'id' is not UUIDField (got {type(id_field).__name__})")
