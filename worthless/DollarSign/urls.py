from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('delete_stock/<int:id>/', views.delete_stock, name='delete_stock'),
    path('register/', register, name='register'),  
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('store_data/', views.store_data_in_session, name='store_data'),
    path('retrieve_data/', views.retrieve_data_from_session, name='retrieve_data'),
    path('stock_results/', views.stock_results, name='stock_results'),
    path('get_portfolio_value/', views.get_portfolio_value, name='get_portfolio_value'),
    path('export/', views.export_portfolio, name='export_portfolio'),
    path('import/', views.import_portfolio, name='import_portfolio'),

    # ...
]
