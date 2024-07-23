"""workez URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from workapp import views

urlpatterns = [
    path('admin'),
    path('', views.default),
    path('login_post',views.login_post),
    path('admin_homepage_request', views.admin_homepage_request),

    path('admin_add_category', views.admin_add_category),
    path('admin_addcategory_post',views.admin_addcategory_post),
    path('admin_edit_category/<id>', views.admin_edit_category),
    path('admin_edit_category_post/<id>', views.admin_edit_category_post),
    path('admin_delete_category/<id>', views.admin_delete_category),
    path('admin_view_category', views.admin_view_category),


    path('worker_approval',views.worker_approval),
    path('worker_approval_post/<id>',views.worker_approval_post),
    path('worker_reject/<id>',views.worker_reject),
    path('worker_view_list', views.worker_view_list),
    path('workerblacklist',views.workerblacklist),
    path('blacklistdelete',views.blacklistdelete),
    path('admin_view_customer', views.admin_view_customer),

    path('user_view_complaint',views.user_view_complaint),
    path('worker_view_complaint',views.worker_view_complaint),
    path('cmp_reply/<id>', views.cmp_reply),
    path('cmp_replypost/<id>',views.cmp_replypost),
    path('cmp_replyy/<id>', views.cmp_replyy),
    path('cmp_replyypost/<id>', views.cmp_replyypost),
    path('rating_view_request/<id>', views.rating_view_request),
    path('feedback_view_request', views.feedback_view_request),


    path('admin_changepass_request', views.admin_changepass_request),
    path('admin_changepass_post',views.admin_changepass_post),
    path('logout',views.logout),

   #worker
    path('workerhome',views.workerhome),

    path('workeradd',views.workeradd),
    path('workeraddpost',views.workeraddpost),
    path('workerprofileview',views.workerprofileview),
    path('workerprofileedit/<id>',views.workerprofileedit),
    path('workerprofileedit_post/<id>',views.workerprofileedit_post),


    path('workerscheduleadd',views.workerscheduleadd),
    path('workerscheduleadd_post',views.workerscheduleadd_post),
    path('workerschedule',views.workerschedule),
    path('workrequest',views.workrequest),
    path('workrequestaccept/<id>', views.workrequestaccept),
    path('workrequestaccept_post/<id>',views.workrequestaccept_post),
    path('workreject_post/<id>',views.workreject_post),
    path('wrker_delete_schedule/<id>',views.wrker_delete_schedule),
    path('schedulebooking/<id>',views.schedulebooking),
    path('orderstatus',views.orderstatus),
    path('todaysbooking',views.todaysbooking),


    path('wcomplaint',views.wcomplaint),
    path('wcomplaint_post',views.wcomplaint_post),
    path('workercmpreply',views. workercmpreply),
    path('worker_changepass_request',views.worker_changepass_request),
    path('worker_changepass_post',views.worker_changepass_post),
    path('orderstatus',views.orderstatus),
    path('wreview',views.wreview),



   #androidd
    path('and_login',views.and_login),
    path('customer_registration',views.customer_registration),
    path('customer_changepass',views.customer_changepass),
    path('Complaint',views.Complaint),
    path('and_feedback',views.and_feedback),
    path('view_profile',views.view_profile),
    path('viewlistworker',views.viewlistworker),
    path('booking',views.booking),
    path('Viewrequest',views.Viewrequest),
    path('cancelrequest',views.cancelrequest),
    path('sendrating',views.sendrating),
    path('customer_profile_update',views.customer_profile_update),
    path('shortview',views.shortview),
    path('view_schedule',views.view_schedule),
    path('and_blacklist',views.and_blacklist),
    path('customhome', views.customhome),

]
