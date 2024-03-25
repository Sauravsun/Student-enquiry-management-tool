from django.shortcuts import render,redirect
from .models import enkannur,enkollam,enkozhikode,knrflups,kollmflups,knrregistraion,kannurpayment,kollamregistration,kozhikodeflups,kzkdregistration,kzkdpayment,kollampayment

from django.contrib.auth.hashers  import make_password, check_password
from django.shortcuts import get_object_or_404,HttpResponse

from django.utils.datastructures import MultiValueDictKeyError

from django.db.models import Max
from django.db.models import Sum
# import datetime
import calendar
# from datetime import datetime
from itertools import chain
from calendar import monthrange,month_name
from datetime import datetime, timedelta
from django.http import QueryDict

from operator import attrgetter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain,groupby






# Create your views here.

def base(request):
    return render(request,'base.html')

def index(request):
    return render(request,'index.html')

def allstudent(request):
    return render(request,'allstudent.html')




    




def stations(request):
    return render(request,'stations.html')

def searchstations(request):
    return render(request,'searchstations.html')


#--------------------------------------------------------------------------
#==========================================================================
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#==========================================================================
#--------------------------------------------------------------------------
# KANNUR STARTS HERE



def addenquery(request):
    if request.method == 'POST':
        ka_fname = request.POST['fname']
        ka_lname = request.POST['lname']
        ka_place = request.POST['place']
        ka_quali = request.POST['quali']
        ka_phone = request.POST['phone']
        ka_course = request.POST['course']
        ka_date = request.POST['date']
        ka_status = request.POST['status']

        add = enkannur(fname=ka_fname,lname=ka_lname,place=ka_place,
                       qualification=ka_quali,phone=ka_phone,course=ka_course,
                       date=ka_date,staus=ka_status)
        add.save()
        return render(request,'index.html')
    else:
        return render(request,'addenquery.html')




def viewkannurstudent(request):
    
    data = enkannur.objects.all()
    return render(request,'viewkannurstu.html',{'data1':data})


def knrsinglview(request):
    knrid = request.GET['knid']
    knrdata = get_object_or_404(enkannur, id=knrid)
    knrflups_data = knrflups.objects.filter(enkannurfl=knrdata)

    return render(request, 'knrsinglview.html', {'knrdata': [knrdata],'knrfldata':knrflups_data})

        


def knrfollowups(request):
    if request.method == 'POST':
        knrid = request.POST.get('knid', '')
        if knrid:
            enkannur_instances = enkannur.objects.filter(id=knrid)

            knfl_date = request.POST['date']
            knfl_response = request.POST['response']

            for enkannur_instance in enkannur_instances:
                add = knrflups(date1=knfl_date, response1=knfl_response, enkannurfl=enkannur_instance)
                add.save()

            return redirect('/viewkannurstudents/')

    return render(request, 'viewkannurstu.html')





def knrupdateandregister(request):
    if request.method == 'GET':
        knrid = request.GET.get('knid', '')
        knrdata = enkannur.objects.filter(id=knrid)
        next_student_id = knrregistraion.objects.order_by('-stu_id').first().stu_id + 1 if knrregistraion.objects.exists() else 1001
        return render(request, 'knnrstureg.html', {'data2': knrdata, "next_student_id": next_student_id, "enquiry_id": knrid})

    elif request.method == 'POST':
        s_id = request.POST['sid']
        enq_id = request.POST["enq_id"]
        kn_fname = request.POST['fname']
        kn_lname = request.POST['lname']
        kn_faname = request.POST['faname']
        kn_moname = request.POST['moname']
        kn_place = request.POST['place']
        kn_qualification = request.POST['quali']
        kn_course = request.POST['course']
        kn_phone = request.POST['phone']
        kn_coursefee = request.POST['fee']

        kn_new = knrregistraion(stu_id=s_id, knr_fname=kn_fname, knr_lname=kn_lname, knr_fathername=kn_faname,
                                knr_mothername=kn_moname, knr_place=kn_place, 
                                knr_qualification=kn_qualification,knr_course=kn_course, knr_phone=kn_phone,
                                knr_coursefee=kn_coursefee)
        kn_new.save()
        
        table1 = enkannur.objects.filter(id=enq_id).delete()

        return render(request,'index.html')
    else:
        return render(request, 'knrsinglview.html')



def kannurstudents(request):
    data3 = knrregistraion.objects.all()
    return render(request,'kannurstudents.html',{'data3':data3})


def kannurstudentsingleview(request):
    knr_paymentid = request.GET['knpayid']
    stu_paydata = get_object_or_404(knrregistraion, stu_id=knr_paymentid)
    knr_paymentdata = kannurpayment.objects.filter(knrpaymentid = stu_paydata)
    total_paid_amount = knr_paymentdata.aggregate(total_paid=Sum('paymentamount'))['total_paid']

    return render(request,'knrstudentsingleview.html',{'stu_paydata':[stu_paydata],'knrpayment':knr_paymentdata, 'total_paid_amount': total_paid_amount})


def knrpaymentfollowups(request):
    if request.method == 'POST':
        knr_paymentid = request.POST.get('knpayid', '')
        if knr_paymentid:
            stukannur_instances = knrregistraion.objects.filter(stu_id=knr_paymentid).first()


            if stukannur_instances:
                knfl_date = request.POST['date']
                knfl_amount = float(request.POST['amount'])
                knfl_mod = request.POST['mod']


                previous_payments = kannurpayment.objects.filter(knrpaymentid=stukannur_instances)
                total_paid_amount = sum(payment.paymentamount for payment in previous_payments)

                # Calculate the remaining balance
                course_fee = float(stukannur_instances.knr_coursefee)
                knfl_balance = course_fee - total_paid_amount - knfl_amount

                print(knfl_balance)

                add = kannurpayment(paymentdate=knfl_date, mod_payment=knfl_mod, paymentamount=knfl_amount, paymentbalance=knfl_balance, knrpaymentid=stukannur_instances)
                add.save()

                return redirect(f'/kannurstudents/?knfl_balance={knfl_balance}')

    return render(request, 'kannurstudents.html',{'knfl_balance': knfl_balance})
  



# KANNUR ENDS HERE
#--------------------------------------------------------------------------
#==========================================================================
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
#==========================================================================
#--------------------------------------------------------------------------
#  KOLLAM STARTS HERE
    
def addenquerykollam(request):
    if request.method == 'POST':
        ko_fname = request.POST['fname']
        ko_lname = request.POST['lname']
        ko_place = request.POST['place']
        ko_quali = request.POST['quali']
        ko_phone = request.POST['phone']
        ko_course = request.POST['course']
        ko_date = request.POST['date']
        ko_status = request.POST['status']
        add = enkollam(fname=ko_fname,lname=ko_lname,place=ko_place,
                       qualification=ko_quali,phone=ko_phone,course=ko_course,
                       date=ko_date,staus=ko_status)
        add.save()
        return render(request,'index.html')
    else:
        return render(request,'addenquerykollam.html')





def viewkollamstu(request):
    kodata = enkollam.objects.all()
    return render(request,'viewkollamstu.html',{'kodata':kodata})



def kollsingleview(request):
    kollmid = request.GET['koid']
    kodata = get_object_or_404(enkollam, id=kollmid)
    kollmflups_data = kollmflups.objects.filter(enkollmfl=kodata)

    return render(request,'kollsingleview.html',{'kodata':[kodata],'kollmfldata':kollmflups_data})



def kollamfollowups(request):
    if request.method == 'POST':
        kollmid = request.POST.get('koid', '')
        if kollmid:
            enkollam_instances = enkollam.objects.filter(id=kollmid)

            kofl_date = request.POST['date']
            kofl_response = request.POST['response']

            for enkollam_instance in enkollam_instances:
                add = kollmflups(date1=kofl_date, response1=kofl_response, enkollmfl=enkollam_instance)
                add.save()

            return redirect('/viewkollamstudents/')

    return render(request, 'viewkollamstu.html')





def kollamupdateandregister(request):
    if request.method == 'GET':
        kllmid = request.GET.get('koid', '')
        kodata  = enkollam.objects.filter(id = kllmid)
        next_student_id = kollamregistration.objects.order_by('-stu_id').first().stu_id + 1 if kollamregistration.objects.exists() else 2001

        return render(request,'kollamstureg.html',{'data5':kodata,'next_student_id':next_student_id,'enquery_id':kllmid})
    elif request.method == 'POST':
        s_id = request.POST['sid']
        klenq_id = request.POST["enq_id"]
        klm_fname = request.POST['fname']
        klm_lname = request.POST['lname']
        klm_faname = request.POST['faname']
        klm_moname = request.POST['moname']
        klm_place = request.POST['place']
        klm_qualification = request.POST['quali']
        klm_course = request.POST['course']
        klm_phone = request.POST['phone']
        klm_coursefee = request.POST['fee']
        new = kollamregistration(stu_id=s_id,ko_fname=klm_fname,ko_lname=klm_lname,
                                 ko_fathername=klm_faname,ko_mothername=klm_moname,ko_place=klm_place,
                                 ko_qualification=klm_qualification,ko_course=klm_course,ko_phone=klm_phone,ko_coursefee=klm_coursefee)
        new.save()
        table2 = enkollam.objects.filter(id=klenq_id).delete()
        return render(request,'index.html')
    else:
        return render(request,'kollsingleview.html')
    


def kollamstudents(request):
    data = kollamregistration.objects.all()
    return render(request,'kollamstudents.html',{'data10':data})


def kollamstudentsingleview(request):
    kollam_paymentid = request.GET['kopayid']
    stu_paydata = get_object_or_404(kollamregistration, stu_id=kollam_paymentid)
    kollam_paymentdata = kollampayment.objects.filter(kollampaymentid = stu_paydata)
    total_paid_amount = kollam_paymentdata.aggregate(total_paid=Sum('paymentamount'))['total_paid']

    return render(request,'kollamstudentsingleview.html',{'stu_paydata':[stu_paydata],'kollam_payment':kollam_paymentdata,'total_paid_amount':total_paid_amount})


def kollampaymentfollowups(request):
    if request.method == 'POST':
        kollam_paymentid = request.POST.get('kopayid', '')
        if kollam_paymentid:
            stukollam_instances = kollamregistration.objects.filter(stu_id = kollam_paymentid).first()
            if stukollam_instances:
                kofl_date = request.POST['date']
                kofl_amount = float(request.POST['amount'])
                kofl_mod = request.POST['mod']

                previous_payments = kollampayment.objects.filter(kollampaymentid=stukollam_instances)
                total_paid_amount = sum(payment.paymentamount for payment in previous_payments)

                course_fee = float(stukollam_instances.ko_coursefee)
                kofl_balance = course_fee - total_paid_amount - kofl_amount

                add = kollampayment(paymentdate=kofl_date,paymentamount=kofl_amount,mod_payment=kofl_mod,paymentbalance=kofl_balance,kollampaymentid=stukollam_instances)
                add.save()

                return redirect(f'/kollamstudents/?kofl_balance={kofl_balance}')

    return render(request,'kollamstudents.html',{'kofl_balance': kofl_balance})




#  KOLLAM ENDS HERE
#--------------------------------------------------------------------------
#==========================================================================
#--------------------------------------------------------------------------
    
#--------------------------------------------------------------------------
#==========================================================================
#--------------------------------------------------------------------------
#  KOZHIKKODE STARTS HERE
    
def addenquerykozhi(request):
    if request.method == 'POST':
        ko_fname = request.POST['fname']
        ko_lname = request.POST['lname']
        ko_place = request.POST['place']
        ko_quali = request.POST['quali']
        ko_phone = request.POST['phone']
        ko_course = request.POST['course']
        ko_date = request.POST['date']
        ko_status = request.POST['status']
        add = enkozhikode(fname=ko_fname,lname=ko_lname,place=ko_place,
                          qualification=ko_quali,phone=ko_phone,course=ko_course,
                          date=ko_date,staus=ko_status)
        add.save()
        return render(request,'index.html')
    else:
        return render(request,"addenquerykozhi.html")




def viewkozhikkodestu(request):
    kzdata = enkozhikode.objects.all()
    return render(request,'viewkozhikodestu.html',{'kzdata':kzdata})


def kozhikkodesingleview(request):
    kzkdid = request.GET['kzid']
    kzdata = get_object_or_404(enkozhikode, id=kzkdid)
    kzkdflups_data = kozhikodeflups.objects.filter(enkzkdfl=kzdata)
    return render(request,'kzkdsingleview.html',{'kzdata':[kzdata],'kzkdfl':kzkdflups_data})


def kozhikkodefollowups(request):
    if request.method =='POST':
        kzkdid = request.POST.get('kzid', '')
        if kzkdid:
            enkozhikkode_instances = enkozhikode.objects.filter(id=kzkdid)

            kzfl_date = request.POST['date']
            kzfl_response = request.POST['response']

            for enkozhikkode_instance in enkozhikkode_instances:
                add = kozhikodeflups(date1=kzfl_date, response1=kzfl_response,enkzkdfl=enkozhikkode_instance)
                add.save()
            return redirect('/viewkozhikkodestudents/')

    return render(request,'viewkozhikodestu.html')




def kozhikkodeupdateandregister(request):
    if request.method == 'GET':
        kzkdid = request.GET.get('kzid', '')
        kzdata = enkozhikode.objects.filter(id=kzkdid)
        next_student_id = kzkdregistration.objects.order_by('-kzstu_id').first().kzstu_id + 1 if kzkdregistration.objects.exists() else 3001
        return render(request,'kzkdstureg.html',{'data6':kzdata, 'next_student_id':next_student_id, 'enquery_id':kzkdid})
    
    elif request.method == 'POST':
        kzhs_id = request.POST['kzsid']
        kzhenq_id = request.POST["kzenq_id"]

        kzh_fname = request.POST['fname']
        kzh_lname = request.POST['lname']
        kzh_faname = request.POST['faname']
        kzh_moname = request.POST['moname']
        kzh_place = request.POST['place']
        kzh_qualification = request.POST['quali']
        kzh_course = request.POST['course']
        kzh_phone = request.POST['phone']
        kzh_coursefee = request.POST['fee']

        kz_new = kzkdregistration(kzstu_id=kzhs_id,kz_fname=kzh_fname,kz_lname=kzh_lname,kz_fathername=kzh_faname,
                                  kz_mothername=kzh_moname,kz_place=kzh_place,kz_qualification=kzh_qualification,
                                  kz_course=kzh_course,kz_phone=kzh_phone,kz_coursefee=kzh_coursefee)
        kz_new.save()

        
        table3 = enkozhikode.objects.get(id=kzhenq_id).delete()
        

        return render(request,'index.html')
    else:
        return render(request,'kzkdsingleview.html')
    


def kozhikkodestudents(request):
    data = kzkdregistration.objects.all()
    return render(request,'kozhikkodestudents.html',{'data11':data})


def kzkdstudentsingleview(request):
    kzkd_paymentid = request.GET['kzpayid']
    stu_paydata = get_object_or_404(kzkdregistration, kzstu_id=kzkd_paymentid)
    kzkd_paymentdata = kzkdpayment.objects.filter(kzkdpaymentid = stu_paydata)
    total_paid_amount = kzkd_paymentdata.aggregate(total_paid=Sum('paymentamount'))['total_paid']

    return render(request,'kozhikkodestudentsingleview.html',{'stu_paydata':[stu_paydata],'kzkdpayment':kzkd_paymentdata,'total_paid_amount':total_paid_amount})



def kzkdpaymentsfollowups(request):
    if request.method == 'POST':
        kzkd_paymentid = request.POST.get('kzpayid', '')
        if kzkd_paymentid:
            stukzkd_instances = kzkdregistration.objects.filter(kzstu_id = kzkd_paymentid).first()
            if stukzkd_instances:
                kzfl_date = request.POST['date']
                kzfl_amount = float(request.POST['amount'])
                kzfl_mod = request.POST['mod']

                previous_payments = kzkdpayment.objects.filter(kzkdpaymentid=stukzkd_instances)
                total_paid_amount = sum(payment.paymentamount for payment in previous_payments)

                course_fee = float(stukzkd_instances.kz_coursefee)
                kzfl_balance =float( course_fee - total_paid_amount - kzfl_amount)

                add = kzkdpayment(paymentdate=kzfl_date,paymentamount=kzfl_amount,mod_payment=kzfl_mod,paymentbalance=kzfl_balance,kzkdpaymentid=stukzkd_instances)
                add.save()

                return redirect(f'/kzkdstudents/?kzfl_balance={kzfl_balance}')
    return render(request,'kozhikkodestudents.html',{'kzfl_balance':kzfl_balance})

# KOZHIKKODE ENDS HERE
#--------------------------------------------------------------------------
#==========================================================================
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#==========================================================================
#--------------------------------------------------------------------------

# def transactions(request):
#     kzkdpayments = kzkdpayment.objects.all()
#     kannurpayments = kannurpayment.objects.all()
#     kollampayments = kollampayment.objects.all()
#     all_payments = list(kzkdpayments) + list(kannurpayments) + list(kollampayments)
#     sorted_payments = sorted(all_payments, key=lambda x: x.paymentdate ,reverse=True)

#     paginator = Paginator(sorted_payments, 10)
#     page = request.GET.get('page')
#     try:
#         paginated_payments = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver first page.
#         paginated_payments = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver last page of results.
#         paginated_payments = paginator.page(paginator.num_pages)

#     return render(request,'alltransactions.html',{'data15':paginated_payments})


def searchwithid(request):
    if request.method == 'GET':
        student_id = request.GET.get('student_id', '')
        
        # Fetch student data from different tables
        student_data_knr = knrregistraion.objects.filter(stu_id=student_id).first()
        student_data_kollam = kollamregistration.objects.filter(stu_id=student_id).first()
        student_data_kzkd = kzkdregistration.objects.filter(kzstu_id=student_id).first()
        
        # Check if student data exists in any table
        if student_data_knr:
            student_data = student_data_knr
        elif student_data_kollam:
            student_data = student_data_kollam
        elif student_data_kzkd:
            student_data = student_data_kzkd
        else:
            return render(request, 'error.html', {'message': 'No student found with the provided ID.'})
        
        # Fetch payment data based on the found student data
        payment_data_kannur = kannurpayment.objects.filter(knrpaymentid=student_data) if student_data == student_data_knr else None
        payment_data_kollam = kollampayment.objects.filter(kollampaymentid=student_data) if student_data == student_data_kollam else None
        payment_data_kzkd = kzkdpayment.objects.filter(kzkdpaymentid=student_data) if student_data == student_data_kzkd else None
        
        # Calculate total paid amount if payment data exists
        total_paid_amount_kannur = payment_data_kannur.aggregate(total_paid=Sum('paymentamount'))['total_paid'] if payment_data_kannur else 0
        total_paid_amount_kollam = payment_data_kollam.aggregate(total_paid=Sum('paymentamount'))['total_paid'] if payment_data_kollam else 0
        total_paid_amount_kzkd = payment_data_kzkd.aggregate(total_paid=Sum('paymentamount'))['total_paid'] if payment_data_kzkd else 0
        
        # Render appropriate template based on payment data availability
        if payment_data_kannur:
            return render(request, 'knrstudentsingleview.html', {'stu_paydata': [student_data], 'knrpayment': payment_data_kannur, 'total_paid_amount': total_paid_amount_kannur})
        elif payment_data_kollam:
            return render(request, 'kollamstudentsingleview.html', {'stu_paydata': [student_data], 'kollam_payment': payment_data_kollam, 'total_paid_amount': total_paid_amount_kollam})
        elif payment_data_kzkd:
            return render(request,'kozhikkodestudentsingleview.html', {'stu_paydata': [student_data], 'kzkdpayment': payment_data_kzkd, 'total_paid_amount': total_paid_amount_kzkd})
        else:
            return render(request, 'error.html', {'message': 'No payment data found for the student.'})
    else:
        # Handle other HTTP methods if needed
        return render(request, 'error.html', {'message': 'Invalid HTTP method.'})



import datetime

def transactions(request):
    today = datetime.datetime.today().date()  # Get the current date and time
    period = request.GET.get('period')
    selected_month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))
    month_choices = [(i, calendar.month_name[i]) for i in range(1, 13)]
    
    if period == 'daily':
        all_payments = list(chain(
            kzkdpayment.objects.filter(paymentdate=today),
            kannurpayment.objects.filter(paymentdate=today),
            kollampayment.objects.filter(paymentdate=today)
        ))
        period_label = today.strftime('%B %d, %Y')  # Format: Month Day, Year
    elif period == 'weekly':
        week_str = request.GET.get('week')
        if week_str:
            year, week_number = map(int, week_str.split('-W'))
            start_of_week = datetime.datetime.strptime(f'{year}-W{week_number}-1', "%Y-W%W-%w").date()
            end_of_week = start_of_week + datetime.timedelta(days=6)
        else:
            start_of_week = today - datetime.timedelta(days=today.weekday())
            end_of_week = start_of_week + datetime.timedelta(days=6)
        
        all_payments = list(chain(
            kzkdpayment.objects.filter(paymentdate__range=[start_of_week, end_of_week]),
            kannurpayment.objects.filter(paymentdate__range=[start_of_week, end_of_week]),
            kollampayment.objects.filter(paymentdate__range=[start_of_week, end_of_week])
        ))
        period_label = f'{start_of_week.strftime("%B %d")} - {end_of_week.strftime("%B %d, %Y")}'
    elif period == 'monthly':
        start_of_month = datetime.datetime(year, selected_month, 1).date()
        end_of_month = datetime.datetime(year, selected_month, calendar.monthrange(year, selected_month)[1]).date()
        all_payments = list(chain(
            kzkdpayment.objects.filter(paymentdate__range=[start_of_month, end_of_month]),
            kannurpayment.objects.filter(paymentdate__range=[start_of_month, end_of_month]),
            kollampayment.objects.filter(paymentdate__range=[start_of_month, end_of_month])
        ))
        period_label = start_of_month.strftime('%B %Y')  # Format: Month Year
    elif period == 'yearly':
        start_of_year = datetime.datetime(year, 1, 1).date()
        end_of_year = datetime.datetime(year, 12, 31).date()
        all_payments = list(chain(
            kzkdpayment.objects.filter(paymentdate__range=[start_of_year, end_of_year]),
            kannurpayment.objects.filter(paymentdate__range=[start_of_year, end_of_year]),
            kollampayment.objects.filter(paymentdate__range=[start_of_year, end_of_year])
        ))
        period_label = year  # Show the selected year
    else:
        all_payments = list(chain(
            kzkdpayment.objects.all(),
            kannurpayment.objects.all(),
            kollampayment.objects.all()
        ))
        period_label = 'All Time'
    
    all_payments.sort(key=attrgetter('paymentdate'))
    total_amount = sum(payment.paymentamount for payment in all_payments)
    
    # Group payments by month
    grouped_payments = {}
    for month_num in range(1, 13):
        start_of_month = datetime.datetime(year, month_num, 1).date()
        end_of_month = datetime.datetime(year, month_num, calendar.monthrange(year, month_num)[1]).date()
        month_payments = [payment for payment in all_payments if start_of_month <= payment.paymentdate <= end_of_month]
        grouped_payments[month_num] = {
            'month_name': calendar.month_name[month_num],
            'total_amount': sum(payment.paymentamount for payment in month_payments)
        }
    
    paginator = Paginator(all_payments, 10)
    page = request.GET.get('page')
    try:
        paginated_payments = paginator.page(page)
    except PageNotAnInteger:
        paginated_payments = paginator.page(1)
    except EmptyPage:
        paginated_payments = paginator.page(paginator.num_pages)
    
    return render(request, 'alltransactions.html', {
        'data15': paginated_payments,
        'total_amount': total_amount,
        'period_label': period_label,
        'grouped_payments': grouped_payments,
        'selected_month': selected_month,
        'month_choices': month_choices,
        'period': period  # Pass period to template for highlighting the selected period
    })




# def transactions(request):
#     today = datetime.today().date()
#     period = request.GET.get('period')
#     selected_month = int(request.GET.get('month', today.month))
#     month_choices = [(i, calendar.month_name[i]) for i in range(1, 13)]
    
#     if period == 'daily':
#         all_payments = list(chain(
#             kzkdpayment.objects.filter(paymentdate=today),
#             kannurpayment.objects.filter(paymentdate=today),
#             kollampayment.objects.filter(paymentdate=today)
#         ))
#         period_label = today.strftime('%B %d, %Y')  # Format: Month Day, Year
#     elif period == 'weekly':
#         week_str = request.GET.get('week')
#         if week_str:
#             year, week_number = map(int, week_str.split('-W'))
#             start_of_week = datetime.strptime(f'{year}-W{week_number}-1', "%Y-W%W-%w").date()
#             end_of_week = start_of_week + timedelta(days=6)
#         else:
#             start_of_week = today - timedelta(days=today.weekday())
#             end_of_week = start_of_week + timedelta(days=6)
        
#         all_payments = list(chain(
#             kzkdpayment.objects.filter(paymentdate__range=[start_of_week, end_of_week]),
#             kannurpayment.objects.filter(paymentdate__range=[start_of_week, end_of_week]),
#             kollampayment.objects.filter(paymentdate__range=[start_of_week, end_of_week])
#         ))
#         period_label = f'{start_of_week.strftime("%B %d")} - {end_of_week.strftime("%B %d, %Y")}'
#     elif period == 'monthly':
#         start_of_month = today.replace(month=selected_month, day=1)
#         end_of_month = today.replace(month=selected_month, day=calendar.monthrange(today.year, selected_month)[1])
#         all_payments = list(chain(
#             kzkdpayment.objects.filter(paymentdate__range=[start_of_month, end_of_month]),
#             kannurpayment.objects.filter(paymentdate__range=[start_of_month, end_of_month]),
#             kollampayment.objects.filter(paymentdate__range=[start_of_month, end_of_month])
#         ))
#         period_label = start_of_month.strftime('%B %Y')  # Format: Month Year
#     elif period == 'yearly':
#         start_of_year = today.replace(month=1, day=1)
#         end_of_year = today.replace(month=12, day=31)
#         all_payments = list(chain(
#             kzkdpayment.objects.filter(paymentdate__range=[start_of_year, end_of_year]),
#             kannurpayment.objects.filter(paymentdate__range=[start_of_year, end_of_year]),
#             kollampayment.objects.filter(paymentdate__range=[start_of_year, end_of_year])
#         ))
#         period_label = start_of_year.strftime('%Y')  # Format: Year
#     else:
#         all_payments = list(chain(
#             kzkdpayment.objects.all(),
#             kannurpayment.objects.all(),
#             kollampayment.objects.all()
#         ))
#         period_label = 'All Time'
    
#     all_payments.sort(key=attrgetter('paymentdate'))
#     total_amount = sum(payment.paymentamount for payment in all_payments)
#     grouped_payments = {date: list(items) for date, items in groupby(all_payments, key=attrgetter('paymentdate'))}

#     paginator = Paginator(all_payments, 10)
#     page = request.GET.get('page')
#     try:
#         paginated_payments = paginator.page(page)
#     except PageNotAnInteger:
#         paginated_payments = paginator.page(1)
#     except EmptyPage:
#         paginated_payments = paginator.page(paginator.num_pages)
    
#     return render(request, 'alltransactions.html', {
#         'data15': paginated_payments,
#         'total_amount': total_amount,
#         'period_label': period_label,
#         'grouped_payments': grouped_payments,
#         'selected_month': selected_month,
#         'month_choices': month_choices,
#         'period': period  # Pass period to template for highlighting the selected period
#     })
