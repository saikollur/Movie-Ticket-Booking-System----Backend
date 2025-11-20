from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import RedirectView  # <--- Added this import

# Swagger Documentation Configuration
schema_view = get_schema_view(
   openapi.Info(
      title="Movie Booking API",
      default_version='v1',
      description="API documentation for the Movie Ticket Booking System",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # --- ADDED: Redirect root URL ('') to Swagger ---
    path('', RedirectView.as_view(url='/swagger/', permanent=False)),

    # Admin Panel
    path('admin/', admin.site.urls),
    
    # Connects to your 'bookings' app URLs
    # All endpoints will start with /api/ (e.g., /api/movies/)
    path('api/', include('bookings.urls')),
    
    # Swagger UI Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
