from app.models.girl import Goods, Girl
from app.models.user import User, Order

# 记录用户的购买记录
async def user_order_create(user: User, obj: Goods | Girl):
    await obj.fetch_link(obj.__class__.template)
    buy_type = obj.template.open_if
    buy_price = obj.template.open_number
    obj_type = obj.__class__.__name__
    order = Order(obj_id=obj.uuid, obj_type=obj_type, buy_type=buy_type, buy_price=buy_price, is_paid=True)
    await order.insert()
    user.orders.append(order)
    await user.save()