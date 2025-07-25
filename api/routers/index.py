from . import orders, order_details, resources, menu_item_ingredients, menu_items, payments, customers


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(resources.router)
    app.include_router(menu_item_ingredients.router)
    app.include_router(menu_items.router)
    app.include_router(payments.router)
    app.include_router(customers.router)