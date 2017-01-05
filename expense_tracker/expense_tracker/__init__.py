from pyramid.config import Configurator


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('expense_tracker.models')
    config.include('expense_tracker.routes')
    config.include('expense_tracker.security')
    config.scan()
    return config.make_wsgi_app()
