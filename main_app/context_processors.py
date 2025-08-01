from .models import Order

def cart_info(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, status="cart").first()
        if order:
            items = order.items.all()
            total = sum([int(item.product.price or 0) for item in items])
            count = items.count()
            return {
                "cart_items": items,
                "cart_total": total,
                "cart_count": count
            }
    return {
        "cart_items": [],
        "cart_total": 0,
        "cart_count": 0
    }
