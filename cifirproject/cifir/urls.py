from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

#paths arranged alphabetically by name
app_name = 'cifir'
urlpatterns = [ 
    # path('api/data', views.get_data, name='api-data'),

    #TEST URL
    path('index/', views.indexView.as_view(), name="index_view"),

    path('home/', views.homePageView.as_view(), name="home_view"),
    path('collections/', views.collectionsPageView.as_view(), name="collections_view"),
    path('bookmarks/', views.bookmarksPageView.as_view(), name="bookmarks_view"),
    path('audiobooks/', views.audiobooksPageView.as_view(), name="audiobooks_view"),
    path('networklibraries/', views.networkLibrariesPageView.as_view(), name="networklibraries_view"),

    path('favorites/', views.favoritesPageView.as_view(), name="favorites_view"),
    path('toread/', views.toReadPageView.as_view(), name="toread_view"),
    path('haveread/', views.haveReadPageView.as_view(), name="haveread_view"),
    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)