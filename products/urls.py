from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/", views.catalog, name="catalog"),
    path("about/", views.about, name="about"),
    path("blog/", views.blog_list, name="blog"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("account/", views.account, name="account"),
    path("account/logout/", views.logout_view, name="logout"),
    path("basket/", views.cart_view, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("product/<slug:slug>/add/", views.add_to_cart, name="add_to_cart"),
    path("basket/update/<int:product_id>/", views.update_cart, name="update_cart"),
    path("basket/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
]
