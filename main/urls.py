from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='main'),
    path('package_detail/<int:package_id>/<slug:package_slug>/', views.PackageDetailView.as_view(),
         name='package_detail'),
    path('category/<str:category_name>/', views.ShowPackagesView.as_view(), name='category_filter'),
    path('packages/show', views.ShowPackagesView.as_view(), name='show_package'),
    path('reply/<int:package_id>/<int:comment_id>', views.PackageReplyCommentView.as_view(), name='reply_comment'),
    path('save/<int:package_id>/', views.PackageSaveView.as_view(), name='package_save'),
    path('unsave/<int:package_id>/', views.PackageUnSaveView.as_view(), name='package_un_save'),
    path('send_email/', views.SendEmailView.as_view(), name='send_email')

]
