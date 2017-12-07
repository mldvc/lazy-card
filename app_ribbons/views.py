from django.shortcuts import render, redirect, get_object_or_404
from app_overview.models import Printer_Ribbon
from .models import RibbonUsageRecord
from .forms import RibbonUsageForm, CRUDRibbonUsageForm
from django.contrib.auth.decorators import login_required, permission_required
from datetime import date


@login_required(login_url='/')
@permission_required('app_ribbons.add_ribbonusagerecord')
def ribbons(request):
    totalRibbonUsed = 0

    # Search Form ====================================================
    searchForm = RibbonUsageForm((request.GET or None), initial={
        'dateFrom': date(date.today().year, 1, 1)
    })

    activeRibbons = RibbonUsageRecord.objects.filter(ribbon_status='A')
    usageHistory = RibbonUsageRecord.objects.all()

    if searchForm.is_valid():
        usageHistory = RibbonUsageRecord.objects.filter(
            ribbon_use_date__range=[
                searchForm.cleaned_data['dateFrom'],
                searchForm.cleaned_data['dateTo']
            ]
        )
        print(usageHistory)
        ribbonTypeSearch = searchForm.cleaned_data['ribbonTypeSearch']
        if ribbonTypeSearch:
            usageHistory = usageHistory.filter(ribbon_type=ribbonTypeSearch)

        ribbonNumberSearch = searchForm.cleaned_data['ribbonNumberSearch']
        if ribbonNumberSearch:
            usageHistory = usageHistory.filter(
                ribbon_number=ribbonNumberSearch
            )

        ribbonSearchForm = searchForm.cleaned_data['statusSearch']
        if ribbonSearchForm != 'ALL':
            usageHistory = usageHistory.filter(ribbon_status=ribbonSearchForm)

    totalRibbonUsed = usageHistory.count()

    return render(request, 'templates_ribbons/ribbons_overview.html', {
        'searchForm': searchForm,
        'usageHistory': usageHistory,
        'activeRibbons': activeRibbons,
        'totalRibbonUsed': totalRibbonUsed,
    })


@permission_required('app_ribbons.add_ribbonusagerecord')
def addRibbonUsageHistory(request):
    addAnotherLabel = 'Save and add another'
    saveLabel = 'Save'
    legend = "Add Ribbon Usage History"

    form = CRUDRibbonUsageForm((request.POST or None), initial={
        'ribbon_use_date': date.today(),
        'ribbon_total_printed': 0,
        'ribbon_status': 'A',
    })

    if form.is_valid():
        form.save()

        #redirect to cards overview or add new after save
        if request.method == 'POST' and 'btnSave' in request.POST:
            return redirect('/ribbons')
        else:
            return redirect('/ribbons/add_ribbon_usage_history')

    contex = {
        "save_1": addAnotherLabel,
        "save_2": saveLabel,
        "legend": legend,
        "form": form
    }
    return render(request, 'templates_ribbons/ribbons_add_usage_history.html', contex)


@permission_required('app_ribbons.change_ribbonusagerecord')
def updateRibbonUsageHistory(request, ribbon_number=None):

    contEditingLabel = 'Update and Continue Editing'
    updateLabel = 'Update'
    legend = 'Update Ribbon ' + str(ribbon_number)

    obj = get_object_or_404(RibbonUsageRecord, ribbon_number=ribbon_number)
    updateForm = CRUDRibbonUsageForm((request.POST or None), instance=obj)
    if updateForm.is_valid():
        updateForm.save()
        #redirect to cards overview or add new after save
        if request.method == 'POST' and 'btnSave' in request.POST:
            return redirect('/ribbons')
        else:
            return redirect('/ribbons/{}'.format(str(updateForm.cleaned_data['ribbon_number'])))

    contex = {
        "save_1": contEditingLabel,
        "save_2": updateLabel,
        "legend": legend,
        "form": updateForm
    }
    return render(request, 'templates_ribbons/ribbons_add_usage_history.html', contex)
