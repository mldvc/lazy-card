from django.shortcuts import render, get_object_or_404, redirect
from .forms import PrintIDForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from app_id_form.models import ID_Form, FormFields
from app_reference.models import CardsLayout, EmploymentTypes
from django.http import JsonResponse


# def getLayout(request):
#     ajaxData = request.GET
#     layoutID = ajaxData['id-layout']
#     layout = get_object_or_404(CardsLayout, id=layoutID)
#     data = {
#         'layout-front': layout.layout_front.url,
#         'layout-back': layout.layout_back.url
#     }
#     return JsonResponse(data)


@login_required(login_url='/')
def printID(request, pk=None):
    dictData = {}
    records = get_object_or_404(ID_Form, id=pk)
    id_fields = FormFields.objects.filter(id_type__id=records.id_type.id)
    layout = CardsLayout.objects.filter(id_type__id=records.id_type.id)
    layout = layout[0]

    if records.emp_type:
        layout = get_object_or_404(CardsLayout, id=records.emp_type.layout.id)

    print(layout.layout_code)

    data_pk = records.id

    for field in id_fields:
        objFields = records._meta.get_fields()
        for f in objFields:
            if f.name == field.code_name:
                dictData[field.code_name] = getattr(records, f.name)

    if records.picture:
        dictData['picture'] = records.picture.url
    else:
        dictData['picture'] = ""

    if records.signature:
        dictData['signature'] = records.signature.url
    else:
        dictData['signature'] = ""

    printIDForm = PrintIDForm(
        (request.POST or None),
        (request.FILES or None),
        instance=records,
        initial={'id_type': records.id_type.id},
        selected=records.id_type.id
    )

    if printIDForm.is_valid():
        printIDForm.save()
        # messages.success(
        #     request, 'Picture was saved successfully!'
        # )
        return redirect('/printid/{}/'.format(str(pk)))

    contex = {
        'printIDForm': printIDForm,
        'layout_front': layout.layout_front.url,
        'layout_back': layout.layout_back.url,
        'dictData': dictData,
        'data_pk': data_pk
    }

    return render(
        request,
        'templates_printid/{}.html'.format(layout.layout_code),
        contex
    )
