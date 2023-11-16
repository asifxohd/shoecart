from cart.models import CartItem,Wishlist
from user_authentication.models import CustomUser

def cart_count_icon(request):
    cart_count = 0
    if 'user' in request.session:
        email = request.session['user']
        user = CustomUser.objects.get(email=email)
        cart_count = CartItem.objects.filter(user=user).count()
    return {"cart_count" : cart_count}


def wishlist_icon_count(request):
    wishlist_count = 0
    if 'user' in request.session:
        email = request.session['user']
        user=CustomUser.objects.get(email=email)
        wishlist_count = Wishlist.objects.filter(user=user).count()
    return {"wishlist_count" : wishlist_count}