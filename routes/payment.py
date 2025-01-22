from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user, login_required
from models import storage
from sqlalchemy.orm import joinedload
from models.order import Order
from models.order_item import OrderItem
from models.menu_item import MenuItem

payment_routes = Blueprint("payment_routes", __name__)


@payment_routes.route("/payment")
@login_required
def payment():
    """Display payment page with order details"""
    try:
        # Get active order and its items
        active_order = None
        orders = storage.all(Order).values()
        for order in orders:
            if (
                order.client_id == current_user.id
                and order.status == "active"
            ):
                active_order = order
                break

        if not active_order:
            return render_template(
                "payment.html", subtotal="0.00", total="5.00", items=[]
            )

        # Get menu items details
        order_items = []
        for item in active_order.order_items:
            menu_item = storage.get(MenuItem, item.menu_item_id)
            if menu_item:
                order_items.append(
                    {
                        "name": menu_item.name,
                        "quantity": item.quantity,
                        "price": float(menu_item.price),
                    }
                )

        subtotal = float(active_order.total_price)
        delivery_fee = 5.00
        total = subtotal + delivery_fee

        return render_template(
            "payment.html",
            subtotal="{:.2f}".format(subtotal),
            total="{:.2f}".format(total),
            items=order_items,
        )

    except Exception as e:
        storage.rollback()
        return jsonify({"error": str(e)}), 500


@payment_routes.route("/api/v1/payment/totals")
@login_required
def get_totals():
    """Get order totals for AJAX updates"""
    try:
        with storage.session_scope() as session:
            # Update query to use proper model relationships
            active_order = (
                session.query(Order)
                .filter_by(client_id=current_user.id, status="active")
                .options(
                    joinedload(Order.order_items)
                    .joinedload(OrderItem.menu_item)
                )
                .first()
            )

            subtotal = float(
                active_order.total_price) if active_order else 0.00
            delivery_fee = 5.00
            total = subtotal + delivery_fee

            return jsonify({
                "success": True,
                "subtotal": "{:.2f}".format(subtotal),
                "delivery_fee": "{:.2f}".format(delivery_fee),
                "total": "{:.2f}".format(total),
            })

    except Exception as e:
        print(f"Payment totals error: {e}")
        return jsonify({"error": str(e)}), 500
