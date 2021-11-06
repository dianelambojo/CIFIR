from re import template
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView
from django.urls import reverse_lazy
#paths arranged alphabetically by name
app_name = 'cifir'
urlpatterns = [ 
    # path('api/data', views.get_data, name='api-data'),

    #TURL
    path('login/', views.loginPageView.as_view(), name="login_view"),
    path('logout/', views.logoutPage, name='logout_view'),
    path('home/', views.homePageView.as_view(), name="home_view"),
    path('collections/', views.collectionsPageView.as_view(), name="collections_view"),
    path('bookmarks/', views.bookmarksPageView.as_view(), name="bookmarks_view"),
    path('audiobooks/', views.audiobooksPageView.as_view(), name="audiobooks_view"),
    path('networklibraries/', views.networkLibrariesPageView.as_view(), name="networklibraries_view"),
    path('books/', views.viewBook.as_view(), name="book_view"),
    #path('books/', views.book, name="files_view"),
    path('favorites/', views.favoritesPageView.as_view(), name="favorites_view"),
    path('toread/', views.toReadPageView.as_view(), name="toread_view"),
    path('haveread/', views.haveReadPageView.as_view(), name="haveread_view"),
    path('epub/', views.epubReadpageView.as_view(), name="epub_view"),
    path('profile/', views.profilePageView.as_view(), name="profile_view"),
    path('password/', auth_views.PasswordChangeView.as_view(template_name = 'changePassword.html'),name="changePassword_view"),

    #ResetPassword
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name="password_reset"),
                
                # subject_template_name='commons/password-reset/password_reset_subject.txt',
                # email_template_name='commons/password-reset/password_reset_email.html',
                # success_url='/login/' ), 
     path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name="password_reset_done"),
             
     path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view( template_name='password_reset_confirm.html'), name="password_reset_confirm"),
                
      path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),
               
 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)