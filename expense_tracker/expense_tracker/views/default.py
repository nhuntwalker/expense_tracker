from pyramid.view import view_config
from ..models import Expense


@view_config(route_name="list",
    renderer="../templates/list.jinja2")
def list_view(request):
    """A listing of expenses for the home page."""
    query = request.dbsession.query(Expense).all()
    return {"expenses": query}