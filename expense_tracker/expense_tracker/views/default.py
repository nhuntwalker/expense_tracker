from pyramid.view import view_config
from ..models import Expense


@view_config(route_name="list",
             renderer="../templates/list.jinja2")
def list_view(request):
    """A listing of expenses for the home page."""
    expenses = request.dbsession.query(Expense).all()
    return {"expenses": expenses}


@view_config(route_name="detail",
             renderer="../templates/detail.jinja2")
def detail_view(request):
    """The detail page for an expense."""
    the_id = int(request.matchdict["id"])
    expense = request.dbsession.query(Expense).get(the_id)
    return {"expense": expense}
