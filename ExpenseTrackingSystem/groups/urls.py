from django.urls import path,include
from django.conf.urls import url
from groups.views import home,signup, account_activation_sent,activate, group_view


urlpatterns = [
    path('', home,name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/create/',signup,name='signup'),
    path('account_activation_sent/',account_activation_sent,name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    path('groups/<int:pk>/', group_view, name='group_view')
]
