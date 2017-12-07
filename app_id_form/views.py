from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ID_Form, FormFields
from app_reference.models import IDTypes, Courses, Levels, Departments, Strands
from django.contrib.auth.decorators import login_required, permission_required
from .forms import IDForm, SearchForm, SelectTypeForm
from datetime import datetime as dt
import calendar
from django.http import JsonResponse
from django.core import serializers
import json


def filterField(request):
    pollData = None
    jsonData = [{}]

    ajaxData = request.GET

    id_type = get_object_or_404(IDTypes, pk=ajaxData['id_type'])
    relDept = Departments.objects.filter(id_type__id=id_type.id)
    dept = get_object_or_404(Departments, id=relDept)

    is_course = Courses.objects.filter(dept__id=dept.id).exists()
    is_level = Levels.objects.filter(department__id=dept.id).exists()
    is_strand = Strands.objects.filter(dept__id=dept.id).exists()

    if is_course:
        try:
            pollData = Courses.objects.filter(dept__id=ajaxData['department'])
        except Exception:
            pollData = Courses.objects.all()
    elif is_level:
        try:
            pollData = Levels.objects.filter(department__id=ajaxData['department'])
        except Exception:
            pollData = Levels.objects.all()
    elif is_strand:
        try:
            pollData = Strands.objects.filter(dept__id=ajaxData['department'])
        except Exception:
            pollData = Strands.objects.all()

    if pollData is not None:
        srialData = serializers.serialize('json', pollData)
        jsonData = json.loads(srialData)

    data = {
        'data1': jsonData
    }

    return JsonResponse(data)


@login_required(login_url='/')
def formView(request):

    searchForm = SearchForm(request.GET or None)

    records = ID_Form.objects.filter(add_date=dt.now())

    if searchForm.is_valid():
        # get the date type to search
        dateFrom = searchForm.cleaned_data['dateFrom']
        dateTo = searchForm.cleaned_data['dateTo']

        records = ID_Form.objects.all()
        records = records.filter(
            add_date__range=[dateFrom, dateTo]
        )

        nameSearch = searchForm.cleaned_data['nameSearch']
        if nameSearch:
            records = records.filter(full_name__contains=nameSearch)

        id_Type = searchForm.cleaned_data['typeSearch']
        if id_Type:
            records = records.filter(id_type=id_Type)

    return render(request, 'templates_forms/forms_overview.html', {
        'records': records,
        'searchForm': searchForm,
        'totalRec': records.count(),
    })


@login_required(login_url='/')
@permission_required('app_id_form.add_id_form')
def addForm(request, pk=None):
    saveLabel = 'Submit Your Form'
    legend = get_object_or_404(IDTypes, pk=pk)

    thisYear = str(dt.today().year)
    nextYear = str(dt.today().year + 1)

    aluMonth = str(calendar.month_name[dt.today().month])
    aluNextYear = str(dt.today().year + 1)

    studentValidity = 'A.Y. {} - {}'.format(thisYear, nextYear)
    alumniValidity = '{}, {}'.format(aluMonth, aluNextYear)

    addForm = IDForm((request.POST or None), initial={
        'id_type': pk,
        'validity': studentValidity,
        'alu_validity': alumniValidity,
    }, selected=pk)

    if addForm.is_valid():
        addForm.save()
        messages.success(
            request, 'Your form was saved successfully! Please proceed for taking your picture and signature.'
        )
        return redirect('/forms/select_form_type/')

    contex = {
        "submit_form": saveLabel,
        "form": addForm,
        "legend": legend,
    }
    return render(request, 'templates_forms/forms_add.html', contex)


@login_required(login_url='/')
def selectForm(request):
    selected_id = None
    selectForm = SelectTypeForm(
        (request.POST or None),
        request=request,
    )

    if selectForm.is_valid():
        selected_id = selectForm.cleaned_data['types'].id
        return redirect('add_form/{}/'.format(int(selected_id)))

    return render(request, 'templates_forms/forms_select.html', {
        'selected_id': selected_id,
        'form': selectForm,
    })


@login_required(login_url='/')
def viewIDForm(request, pk=None):
    dictForm = {}
    records = get_object_or_404(ID_Form, id=pk)
    id_fields = FormFields.objects.filter(id_type__id=records.id_type.id)
    legend = None
    form_pk = records.id

    for field in id_fields:
        objFields = records._meta.get_fields()
        for f in objFields:
            if f.name == field.code_name:
                if f.name == 'id_type':
                    legend = getattr(records, f.name)
                else:
                    dictForm[field.code_name] = {
                        field.name: getattr(records, f.name),
                    }

    return render(request, 'templates_forms/forms_formview.html', {
        'records': dictForm,
        'legend': legend,
        'form_pk': form_pk,
    })


@login_required(login_url='/')
@permission_required('app_id_form.update_id_form')
def updateIDForm(request, pk=None, obj=None):
    newObj = get_object_or_404(ID_Form, id=obj)

    saveLabel = 'Save'
    legend = 'Updating ' + newObj.full_name + "'s details"

    updateForm = IDForm((request.POST or None), instance=newObj, initial={
        'id_type': pk,
    }, selected=pk)

    if updateForm.is_valid():
        updateForm.save()
        return redirect('/forms/')

    contex = {
        "save_2": saveLabel,
        "form": updateForm,
        "legend": legend,
    }
    return render(request, 'templates_forms/forms_add.html', contex)
