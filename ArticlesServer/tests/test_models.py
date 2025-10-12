from django.apps import apps
from django.db import models as djmodels
from django.core.exceptions import FieldDoesNotExist
import pytest


def test_article_model_exists():
    """Verifica que el modelo `Article` exista en la app `ArticlesServer` y sea un modelo de Django.

    - Si el modelo no existe, el test falla con un mensaje claro.
    - Si existe, se comprueba que herede de `django.db.models.Model`.
    """
    try:
        Article = apps.get_model('ArticlesServer', 'Article')
    except LookupError:
        pytest.fail("Article model not found in app 'ArticlesServer'")

    assert issubclass(Article, djmodels.Model), "Article exists but is not a Django model"


def test_article_fields_exist_and_types():
    """Verifica que los campos `title`, `author`, `text` y `release_date` existen y tienen tipos razonables.

    - `title`: CharField
    - `text`: TextField
    - `author`: ForeignKey (habitual) o CharField
    - `release_date`: DateField o DateTimeField
    """
    try:
        Article = apps.get_model('ArticlesServer', 'Article')
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
        try:
            field = Article._meta.get_field(field_name)
        except FieldDoesNotExist:
            pytest.fail(f"Field '{field_name}' not found in Article model")

        # For ForeignKey and OneToOneField, isinstance works against the field class
        if not isinstance(field, allowed_types):
            allowed_names = ', '.join(t.__name__ for t in allowed_types)
            pytest.fail(f"Field '{field_name}' exists but is not one of expected types: {allowed_names} (got {type(field).__name__})")


def test_article_id_is_uuid():
    """Verifica que el campo `id` del modelo `Article` exista y sea un UUIDField.

    - Si no existe, el test falla con un mensaje claro.
    - Si existe pero no es UUIDField, falla indicando el tipo actual.
    """
    try:
        Article = apps.get_model('ArticlesServer', 'Article')
    except LookupError:
        pytest.fail("Article model not found in app 'ArticlesServer'")

    try:
        id_field = Article._meta.get_field('id')
    except FieldDoesNotExist:
        pytest.fail("Field 'id' not found in Article model")

    if not isinstance(id_field, djmodels.UUIDField):
        pytest.fail(f"Field 'id' is not UUIDField (got {type(id_field).__name__})")
