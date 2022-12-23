from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import Unit, Elevator, DocumentType, Document, ElevatorKind, ElevatorType
from .forms import ElevatorForm, DocumentForm
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


@login_required(login_url='/asansor/login/')
def index(request):
    if request.user.is_superuser:
        liste=Elevator.objects.all()
    else:
        liste=Elevator.objects.filter(unit=Unit.objects.get(id=request.user.username))
    return render(request,'appmain/index.html',{'liste':liste})

def login_wrapper(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('/asansor/index')
        else:
            messages.error(request, 'Kullanıcı bulunamadı.')
            return redirect('/asansor/login')

    return render(request,'registration/login.html')

def logout_wrapper(request):
    logout(request)
    return redirect('/asansor/index')

@login_required(login_url='/asansor/login/')
def addelevator(request):
    msg=""
    form=ElevatorForm()
    if request.method == 'POST':
        form = ElevatorForm(request.POST)
        if form.is_valid():
            elevator=form.save(commit=False)
            unit=Unit.objects.get(id=request.user.username)
            unit.has_elevator=True
            unit.save()
            elevator.unit=unit
            elevator.save()
            return redirect('/asansor/success')
        else:
            return redirect('/asansor/addelevator')
    return render(request,'appmain/addelevator.html', {'form':form, 'msg':msg})


def find_recent(documents):
    document_list=list(documents)
    print(len(document_list))
    last_date=document_list[0].expire_date
    result=document_list[0]
    for document in document_list:
        if document.expire_date>last_date:
            last_date=document.expire_date
            result=document
    return result

@login_required(login_url='/asansor/login/')
def elevator_detail(request,id):
    try:
        elevator=Elevator.objects.get(id=id)
        documents=Document.objects.filter(elevator=elevator)
        document_aylik=documents.filter(document_type_id="3")
        if document_aylik.exists():
            document_aylik=find_recent(document_aylik)
        document_yillik=documents.filter(document_type_id="2")
        if document_yillik.exists():
            document_yillik=find_recent(document_yillik)
        document_bakim_sozlesmesi=documents.filter(document_type_id="1")
        if document_bakim_sozlesmesi.exists():
            document_bakim_sozlesmesi=find_recent(document_bakim_sozlesmesi)
    except ObjectDoesNotExist:
        return redirect("/asansor/index")
    return render(request,'appmain/elevator_detail.html', {'elevator':elevator,
                                                            'document_aylik':document_aylik,
                                                            'document_yillik':document_yillik,
                                                            'document_bakim_sozlesmesi':document_bakim_sozlesmesi})


@login_required(login_url='/asansor/login/')
def adddocument(request):
    msg=""
    form=DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document=form.save(commit=False)
            document.unit=document.elevator.unit
            document.id=document.elevator.id+"-"+document.document_number
            document.save()
            return redirect('/asansor/success')
        else:
            return redirect('/asansor/error')
    return render(request,'appmain/adddocument.html', {'form':form, 'msg':msg})

@login_required(login_url='/asansor/login/')
def document_detail(request,id):
    try:
        document=Document.objects.get(id=id)
    except ObjectDoesNotExist:
        return redirect("/asansor/index")
    return render(request,'appmain/document_detail.html', { 'document':document})



@login_required(login_url='/asansor/login/')
def report(request):
    if request.user.is_superuser:
        units=Unit.objects.filter(has_elevator=True)
        kinds=ElevatorKind.objects.all()
        show_expired=""
        elevators=Elevator.objects.all()
        if request.method=="POST":
            which_unit=request.POST.get("which_unit")
            which_kind=request.POST.get("which_kind")
            show_expired=request.POST.get("show_expired")
            if which_unit!="all":
                elevators=elevators.filter(unit=which_unit)
            if which_kind!="all":
                elevators=elevators.filter(kind=int(which_kind))
    else:
        return redirect("/asansor/index")
    documents=Document.objects.all()
    elevatordict={}
    for elevator in elevators:

        has_problem=False
        elevator_documents=documents.filter(elevator=elevator)
        document_bakim_sozlesmesi=elevator_documents.filter(document_type_id="1")
        if document_bakim_sozlesmesi.exists():
            has_problem=find_recent(document_bakim_sozlesmesi).is_expired or has_problem
        else:
            has_problem=True
        document_yillik=elevator_documents.filter(document_type_id="2")
        if document_yillik.exists():
            has_problem=find_recent(document_yillik).is_expired or has_problem
        else:
            has_problem=True
        document_aylik=elevator_documents.filter(document_type_id="3")
        if document_aylik.exists():
            has_problem=find_recent(document_aylik).is_expired or has_problem
        else:
            has_problem=True
        if show_expired=="show_expired":
            if has_problem:
                elevatordict[elevator]=elevator_documents
                elevatordict[elevator]=has_problem
        else:
            elevatordict[elevator]=elevator_documents
            elevatordict[elevator]=has_problem

    return render(request,'appmain/report.html',{'liste':elevatordict,
                                                'units':units,
                                                'kinds':kinds
                                                })


@login_required(login_url='/asansor/login/')
def success(request):
    return render(request,"appmain/success.html")

@login_required(login_url='/asansor/login/')
def error(request):
    return render(request,"appmain/error.html")


"""#### asansör için

import csv
from django.contrib.auth.models import User
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

##localde 45 sn sürdü
@user_passes_test(lambda user:user.is_superuser)
def addusers(request):
    file=open(str(BASE_DIR)+'/appmain/kurum_sifreler.csv')
    csvr=csv.reader(file)
    rows=[]
    for row in csvr:
    	rows.append(row)
    for row in rows:
        user = User.objects.create_user(username=row[0], password=row[1])
        user.save()

    return render(request,'appmain/index.html')





@user_passes_test(lambda user:user.is_superuser)
def unitsadd(request):
    file=open(str(BASE_DIR)+'/appmain/kurum_kodlari.csv')
    csvr=csv.reader(file)
    rows=[]
    for row in csvr:
    	rows.append(row)
    for row in rows:
        unit = Unit(id=row[0], name=row[1], address=row[2], user=User.objects.get(username=row[0]))
        unit.save()

    return render(request,'appmain/index.html')
"""
