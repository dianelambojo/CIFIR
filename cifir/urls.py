from re import template
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView
from django.urls import reverse_lazy


#API
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from .views import CreateUserAPIView, LogoutUserAPIView

from django.urls import path

from .views import *

#paths arranged alphabetically by name
app_name = 'cifir'
urlpatterns = [ 
    # path('api/data', views.get_data, name='api-data'),

    #TURL
    path('index/', views.loginPageView.as_view(), name="login_view"),
    path('logout/', views.logoutPage, name='logout_view'),
    path('admin/', views.adminPageView.as_view(), name='admin_view'),
    path('home/', views.homePageView.as_view(), name='home_view'),
    path('collections/', views.collectionsPageView.as_view(), name="collections_view"),
    path('networklibraries/', views.networkLibrariesPageView.as_view(), name="networklibraries_view"),
    path('books/', views.viewBook.as_view(), name="book_view"),
    #path('books/', views.book, name="files_view"),
    path('favorites/', views.favoritesPageView.as_view(), name="favorites_view"),
    path('toread/', views.toReadPageView.as_view(), name="toread_view"),
    path('haveread/', views.haveReadPageView.as_view(), name="haveread_view"),
    path('epub/', views.epubReadpageView.as_view(), name="epub_view"),
    path('pdf/', views.pdfReadpageView.as_view(), name="pdf_view"),
    path('profile/', views.profilePageView.as_view(), name="profile_view"),
    path('password/', 
        auth_views.PasswordChangeView.as_view(template_name = 'changePassword.html', 
        success_url = reverse_lazy('cifir:login_view')),name="changePassword_view"),

    url(r'^auth/login/$',
        obtain_auth_token,
        name='auth_user_login'),
    url(r'^auth/register/$',
        CreateUserAPIView.as_view(),
        name='auth_user_create'),
    url(r'^auth/logout/$',
        LogoutUserAPIView.as_view(),
        name='auth_user_logout'),
    path('book/',
         views.BookList.as_view(),
         name='booklist'),
    path('bookdetails/<int:id>/',
         views.BookDetails.as_view(),
         name='bookdetails'),
    path('collection/',
         views.CollectionList.as_view(),
         name='collectionlist'),
    path('collectiondetails/<int:id>/',
         views.CollectionDetails.as_view(),
         name='collectiondetails'),


    
               
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

