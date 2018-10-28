"""Configuration for this app's routes."""


def includeme(config):
    """Configuration for this app's routes."""
    config.add_static_view('static', 'expense_tracker:static')
    config.add_route('list', '/')
    config.add_route('create', '/expense')
    config.add_route('detail', '/expense/{id:\d+}')
    config.add_route('edit', '/expense/{id:\d+}/edit')
    config.add_route('category', '/expense/{category:\w+}')
    config.add_route('delete', '/expense/{id:\d+}/delete')
    config.add_route('api_list', '/api/v1/expense')
