from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('account/', include('login_app.urls')),
                  path('', include('shop_app.urls')),
                  path('shop/', include('order_app.urls')),
                  path('payment/', include('payment_app.urls')),
                  path('promotion/', include('promotion_app.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
