from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .forms import SearchForm, StockForm
from .models import Printer_Ribbon_Receive_Record
from datetime import date


@login_required(login_url='/')
@permission_required('app_ribbon_inventory.add_printer_ribbon_receive_record')
def ribbonStockMgr(request):
    totalReceivedStock = 0

    searchForm = SearchForm(
        (request.GET or None),
        initial={
            'dateFrom': date(date.today().year, 1, 1)
        }
    )
    # get all records
    records = Printer_Ribbon_Receive_Record.objects.all()

    if searchForm.is_valid():
        # get the date type to search
        dateType = searchForm.cleaned_data['dateType']
        dateFrom = searchForm.cleaned_data['dateFrom']
        dateTo = searchForm.cleaned_data['dateTo']
        # start the date Search
        if dateType == 'RTP':
            records = records.filter(
                rtp_date__range=[dateFrom, dateTo]
            )
        else:
            records = records.filter(
                received_date__range=[dateFrom, dateTo]
            )

        # card type search
        ribbonType = searchForm.cleaned_data['typeSearch']
        if ribbonType:
            records = records.filter(ribbon=ribbonType)

    for record in records:
        totalReceivedStock += record.received_amount

    return render(request, 'templates_ribbons/ribbons_stock_management.html', {
        'records': records,
        'totalReceivedStock': totalReceivedStock,
        'searchForm': searchForm,
    })


@permission_required('app_ribbon_inventory.add_printer_ribbon_receive_record')
def addNewStock(request):
    legend = "Add New Stock"
    addAnotherLabel = 'Save and add another'
    saveLabel = 'Save'

    form = StockForm(request.POST or None, initial={
        'received_date': date.today(),
    })

    if form.is_valid():
        form.save()

        if request.method == 'POST' and 'btnSave' in request.POST:
            return redirect('/ribbons/stocks')
        else:
            return redirect('/ribbons/stocks/add_new_stock')

    contex = {
        "save_1": addAnotherLabel,
        "save_2": saveLabel,
        'legend': legend,
        'form': form,
    }

    return render(request, 'templates_ribbons/ribbons_add_usage_history.html', contex)


@permission_required('app_ribbon_inventory.change_printer_ribbon_receive_record')
def updateStock(request, pk=None):
    legend = "Update Stock"
    contEditingLabel = 'Update and Continue Editing'
    updateLabel = 'Update'

    obj = get_object_or_404(Printer_Ribbon_Receive_Record, id=pk)
    updateForm = StockForm((request.POST or None), instance=obj)
    if updateForm.is_valid():
        updateForm.save()

        # redirect to cards overview or add new after save
        if request.method == 'POST' and 'btnSave' in request.POST:
            return redirect('/ribbons/stocks')
        else:
            pass
            return redirect('/ribbons/stocks/{}'.format(pk))

    contex = {
        "save_1": contEditingLabel,
        "save_2": updateLabel,
        "legend": legend,
        "form": updateForm,
    }

    return render(request, 'templates_cards/cards_add_history.html', contex)
