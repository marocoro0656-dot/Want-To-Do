from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo_app/', include('todo_app.urls')),
    path('user/', include('user.urls')),

    path('', RedirectView.as_view(url='/todo_app/ryofunamoto/', permanent=False)),

]
