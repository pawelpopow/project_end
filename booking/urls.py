from django.urls import path

from booking import views

app_name = 'booking'


urlpatterns = [
    path('', views.index, name='index'),
    path('book/', views.book, name='book'),
    path('contact-us/', views.contact, name='contact-us'),
    path('book-now/<str:id>/', views.book_now, name='book-now'),
    path('cancel-yacht/<str:id>/', views.cancel_yacht, name='cancel-yacht'),
    path('delete-yacht/<str:id>/', views.delete_yacht, name='delete-yacht'),
    path('confirm-now-booking/', views.book_confirm, name="book-confirm")
]



