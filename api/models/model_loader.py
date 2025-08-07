from . import customers, resources, menu_items, menu_item_ingredients, orders, order_details, payments, promotions, reviews

from ..dependencies.database import engine


def index():
    customers.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    menu_item_ingredients.Base.metadata.create_all(engine)
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    payments.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)
    reviews.Base.metadata.create_all(engine)