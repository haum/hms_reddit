from unittest.mock import Mock
from datetime import datetime, timedelta

@given('que aucun lien n’a été posté')
def step_impl(context):
    context.retriever._retrieve_submissions = Mock(return_value=[])


@given('qu’un lien a été posté')
def step_impl(context):
    context.link = {
        'id': '123abc',
        'title': 'test',
        'author': 'someone',
        'url': 'http://example.com',
    }
    context.retriever._retrieve_submissions = Mock(return_value=[context.link])


@when('le programme vérifie les nouveaux liens postés')
def step_impl(context):
    context.exception = None

    try:
        context.retriever.check_submissions()
    except RuntimeError as e:
        context.exception = e


@then('il n’envoie aucune notification')
def step_impl(context):
    pass


@then('il envoie une notification avec le nouveau lien')
def step_impl(context):
    context.notifier.notify.assert_called_with(context.link)


@given('que les nouveaux liens ont été vérifiés "{seconds:d}" secondes auparavant')
def step_impl(context, seconds):
    before = datetime.now() - timedelta(seconds=seconds)
    context.retriever.last_retrieve = before

@then('aucune erreur ne se produit')
def step_impl(context):
    assert context.exception is None


@then('une sécurité empêche la requête vers l’API')
def step_impl(context):
    assert context.exception is not None
