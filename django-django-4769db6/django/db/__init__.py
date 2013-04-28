import warnings

from django.conf import settings
from django.core import signals
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import (DEFAULT_DB_ALIAS,
    DataError, OperationalError, IntegrityError, InternalError,
    ProgrammingError, NotSupportedError, DatabaseError,
    InterfaceError, Error,
    load_backend, ConnectionHandler, ConnectionRouter)

__all__ = ('backend', 'connection', 'connections', 'router', 'DatabaseError',
    'IntegrityError', 'DEFAULT_DB_ALIAS')


if settings.DATABASES and DEFAULT_DB_ALIAS not in settings.DATABASES:
    raise ImproperlyConfigured("You must define a '%s' database" % DEFAULT_DB_ALIAS)

connections = ConnectionHandler(settings.DATABASES)

router = ConnectionRouter(settings.DATABASE_ROUTERS)

# `connection`, `DatabaseError` and `IntegrityError` are convenient aliases
# for backend bits.

# DatabaseWrapper.__init__() takes a dictionary, not a settings module, so
# we manually create the dictionary from the settings, passing only the
# settings that the database backends care about. Note that TIME_ZONE is used
# by the PostgreSQL backends.
# We load all these up for backwards compatibility, you should use
# connections['default'] instead.
class DefaultConnectionProxy(object):
    """
    Proxy for accessing the default DatabaseWrapper object's attributes. If you
    need to access the DatabaseWrapper object itself, use
    connections[DEFAULT_DB_ALIAS] instead.
    """
    def __getattr__(self, item):
        return getattr(connections[DEFAULT_DB_ALIAS], item)

    def __setattr__(self, name, value):
        return setattr(connections[DEFAULT_DB_ALIAS], name, value)

    def __delattr__(self, name):
        return delattr(connections[DEFAULT_DB_ALIAS], name)

connection = DefaultConnectionProxy()
backend = load_backend(connection.settings_dict['ENGINE'])

def close_connection(**kwargs):
    warnings.warn(
        "close_connection is superseded by close_old_connections.",
        PendingDeprecationWarning, stacklevel=2)
    # Avoid circular imports
    from django.db import transaction
    for conn in connections:
        # If an error happens here the connection will be left in broken
        # state. Once a good db connection is again available, the
        # connection state will be cleaned up.
        transaction.abort(conn)
        connections[conn].close()

# Register an event to reset saved queries when a Django request is started.
def reset_queries(**kwargs):
    for conn in connections.all():
        conn.queries = []
signals.request_started.connect(reset_queries)

# Register an event to reset transaction state and close connections past
# their lifetime. NB: abort() doesn't do anything outside of a transaction.
def close_old_connections(**kwargs):
    for conn in connections.all():
        # Remove this when the legacy transaction management goes away.
        try:
            conn.abort()
        except DatabaseError:
            pass
        conn.close_if_unusable_or_obsolete()
signals.request_started.connect(close_old_connections)
signals.request_finished.connect(close_old_connections)