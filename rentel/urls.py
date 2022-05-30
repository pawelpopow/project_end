from django.urls import path

from rentel import views

app_name = 'rentel'

urlpatterns = [
    path('next/', views.dashboard, name="manager-dashboard"),
    path('new/', views.add_rental, name="add-rental"),
    path('update/<int:name_yacht>/', views.update_rental, name="update-rental"),

]
    # path('dashboard1/', include('rentel.urls')),
    # path('add-rentel/', include('rentel.urls')),