from django.urls import path

from customer import views

app_name = 'customer'

urlpatterns = [
    path('news/', views.dashboard, name='user-dashboard'),
    path('details/<int:id>/<int:booking_id>', views.details, name='user-details')
]
