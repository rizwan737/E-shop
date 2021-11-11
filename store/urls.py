from django.urls import path
from store import views
from store.middleware.auth import auth_middleware
urlpatterns = [
    path('', views.Index.as_view(), name="homepage"),
    path('order', auth_middleware(views.OrderView.as_view()), name="order"),
    path('signup', views.Signup.as_view(), name="signup"),
    path('login', views.Login.as_view(), name="login"),
    path('logout', views.logout),
    path('cart', views.Cart.as_view(), name="cart"),
    path('checkout', views.CheckOut.as_view(), name="checkout"),
]