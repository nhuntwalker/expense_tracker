from pyramid.view import view_config
from ..models import Expense
from pyramid.httpexceptions import HTTPFound
import datetime


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


@view_config(route_name="create", renderer="../templates/add.jinja2")
def create_view(request):
    """Create a new expense"""
    if request.POST:
        expense = Expense(
            item=request.POST["item"],
            amount=float(request.POST["amount"]),
            paid_to=request.POST["paid_to"],
            category=request.POST["category"],
            date=datetime.datetime.now(),
            description=request.POST["description"]
        )
        request.dbsession.add(expense)
        return HTTPFound(request.route_url('list'))

    return {}


@view_config(route_name="json_list", renderer="json")
def json_list(request):
    expenses = request.dbsession.query(Expense).all()
    return {"expenses": [expense.to_json() for expense in expenses]}


@view_config(route_name="json_detail", renderer="json")
def json_detail(request):
    the_id = int(request.matchdict["id"])
    expense = request.dbsession.query(Expense).get(the_id)
    return {"expense": expense.to_json()}
