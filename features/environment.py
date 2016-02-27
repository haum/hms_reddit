from unittest.mock import Mock

from reddithaum.retrieve import Retriever


def before_all(context):
    context.notifier = Mock()
    context.notifier.notify = Mock()

    context.retriever = Retriever(context.notifier)
    context.retriever.mark_posted = Mock()
