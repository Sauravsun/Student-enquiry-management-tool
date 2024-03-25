from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('base/',views.base),
    path('',views.index),
    path('addenquery/',views.addenquery),
    path('stations/',views.stations),
    path('searchstations/',views.searchstations),
    path('addenquerykozhikode/',views.addenquerykozhi),
    path('addenquerykollam/',views.addenquerykollam),


    path('allstudents/',views.allstudent),

    path('transactions/',views.transactions),

    path('searchwithid/',views.searchwithid),
    #======================================================
    #  KANNUR STARTS
    #======================================================
    path('kannurstudents/',views.kannurstudents),
    path('knrstudentsingleview/',views.kannurstudentsingleview),
    path('knrstudentwithpayment/',views.knrpaymentfollowups),


    path('viewkannurstudents/',views.viewkannurstudent),
    path('knrsinglview/',views.knrsinglview),
    path('knr_follups/',views.knrfollowups),
    path('knnrstureg/',views.knrupdateandregister),


    #======================================================
    #  KOLLAM STARTS
    #======================================================

    path('kollamstudents/',views.kollamstudents),
    path('kollmstusingleview/',views.kollamstudentsingleview),
    path('kollamstudentwithpayment/',views.kollampaymentfollowups),

    path('viewkollamstudents/',views.viewkollamstu),
    path('kollsingleview/',views.kollsingleview),
    path('kollamfollowups/',views.kollamfollowups),
    path('kollamstureg/',views.kollamupdateandregister),



    #======================================================
    #  KOZHIKKODE STARTS
    #======================================================
    path('kzkdstudents/',views.kozhikkodestudents),
    path('kzkdstusingleview/',views.kzkdstudentsingleview),
    path('kzkdstudentswithpayment/',views.kzkdpaymentsfollowups),


    path('viewkozhikkodestudents/',views.viewkozhikkodestu),
    path('kozhikkodesingleview/',views.kozhikkodesingleview),
    path('kzkd_flups/',views.kozhikkodefollowups),
    path('kzkdstureg/',views.kozhikkodeupdateandregister),

    
]
