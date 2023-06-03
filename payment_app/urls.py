from django.urls import path
from payment_app import views

app_name = 'Payment_App'
urlpatterns = [
    path('checkout/', views.chekout, name="checkout"),
    path('pay/', views.payment, name="payment"),
    path('paymentStatus/', views.complete, name="complete"),
    path('orders/', views.order_view, name="orders"),
    path('purchase/<val_id>/<tran_id>', views.purchase, name="purchase"),
]
