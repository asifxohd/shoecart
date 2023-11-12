from cart.models import CartItem
from user_authentication.models import CustomUser
def cart_count_icon(request):
    cart_count = 0
    if 'user' in request.session:
        email = request.session['user']
        user = CustomUser.objects.get(email=email)
        cart_count = CartItem.objects.filter(user=user).count()
    return {"cart_count" : cart_count}