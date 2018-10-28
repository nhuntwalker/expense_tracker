"""The main views for our expense_tracker app."""

from expense_tracker.models import Expense
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
import datetime


CATEGORIES = [
    "rent",
    "utilities",
    "groceries",
    "food",
    "diapers",
    "autoloan",
    "netflix",
    "booze",
    "therapist"
]


@view_config(route_name="list",
             renderer="../templates/list.jinja2")
def list_view(request):
    """A listing of expenses for the home page."""
    if request.POST and request.POST["category"]:
        return HTTPFound(request.route_url("category",
                                           category=request.POST["category"]))
    query = request.dbsession.query(Expense)
    expenses = query.order_by(Expense.date.desc()).all()
    return {
        "expenses": expenses,
        "categories": CATEGORIES
    }


@view_config(route_name="detail",
             renderer="../templates/detail.jinja2")
def detail_view(request):
    """The detail page for an expense."""
    the_id = int(request.matchdict["id"])

    expense = request.dbsession.query(Expense).get(the_id)
    if not expense:
        return Response("Not Found", content_type='text/plain', status=404)
    return {"expense": expense}


@view_config(
    route_name="create",
    renderer="../templates/add.jinja2"
)
def create_view(request):
    """Create a new expense."""
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


@view_config(
    route_name="edit",
    renderer="../templates/edit.jinja2"
)
def edit_view(request):
    """Edit an existing expense."""
    the_id = int(request.matchdict["id"])
    expense = request.dbsession.query(Expense).get(the_id)
    if request.POST:
        expense.item = request.POST["item"]
        expense.amount = float(request.POST["amount"])
        expense.paid_to = request.POST["paid_to"]
        expense.category = request.POST["category"]
        expense.description = request.POST["description"]
        request.dbsession.flush()
        return HTTPFound(request.route_url('list'))

    form_fill = {
        "item": expense.item,
        "amount": expense.amount,
        "paid_to": expense.paid_to,
        "category": expense.category,
        "description": expense.description
    }
    return {"data": form_fill}


@view_config(route_name="category", renderer="../templates/list.jinja2")
def category_view(request):
    """List expenses of a certain category."""
    if request.POST and request.POST["category"]:
        return HTTPFound(request.route_url("category",
                                           category=request.POST["category"]))
    query = request.dbsession.query(Expense)
    the_category = request.matchdict["category"]
    query = query.filter(Expense.category == the_category)
    expenses = query.order_by(Expense.date.desc()).all()
    return {
        "expenses": expenses,
        "categories": CATEGORIES,
        "selected": the_category
    }


@view_config(route_name="delete")
def delete_view(request):
    """To delete individual items."""
    expense = request.dbsession.query(Expense).get(request.matchdict["id"])
    request.dbsession.delete(expense)
    return HTTPFound(request.route_url("list"))


@view_config(route_name="api_list", renderer="string")
def api_list_view(request):
    expenses = request.dbsession.query(Expense).all()
    output = [item.to_json() for item in expenses]
    return output
