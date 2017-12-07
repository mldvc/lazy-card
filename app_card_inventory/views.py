from django.shortcuts import render, redirect, get_object_or_404
from .models import ID_Card_Receive_Record
from django.contrib.auth.decorators import login_required, permission_required
from .forms import SearchForm, StockForm
from datetime import date


@login_required(login_url='/')
@permission_required('app_card_inventory.add_id_card_receive_record')
def cardStockMgr(request):
    totalReceivedStock = 0

    searchForm = SearchForm(
        (request.GET or None),
        initial={
            'dateFrom': date(date.today().year, 1, 1)
        }
    )

    records = ID_Card_Receive_Record.objects.all()# get all records

    if searchForm.is_valid():
        # get the date type to search
        dateType = searchForm.cleaned_data['dateType']
        dateFrom = searchForm.cleaned_data['dateFrom']
        dateTo = searchForm.cleaned_data['dateTo']
        if dateType == 'RTP':# start the date Search
            records = records.filter(
                rtp_date__range=[dateFrom, dateTo]
            )
        else:
            records = records.filter(
                received_date__range=[dateFrom, dateTo]
            )

        # card type search
        cardType = searchForm.cleaned_data['typeSearch']
        if cardType:
            records = records.filter(card=cardType)

    for record in records:
        totalReceivedStock += record.received_amount

    return render(request, 'templates_cards/cards_stock_management.html', {
        'records': records,
        'totalReceivedStock': totalReceivedStock,
        'searchForm': searchForm,
    })


@permission_required('app_card_inventory.add_id_card_receive_record')
def addNewStock(request):
    legend = "Add New Stock"
    addAnotherLabel = 'Save and add another'
    saveLabel = 'Save'

    form = StockForm(request.POST or None, initial={
        'received_date': date.today(),
    })

    if form.is_valid():
        # instance = form.save(commit=False)
        form.save()

        if request.method == 'POST' and 'btnSave' in request.POST:
            return redirect('/cards/stocks')
        else:
            return redirect('/cards/stocks/add_new_stock')

    return render(request, 'templates_cards/cards_add_history.html', {
        "save_1": addAnotherLabel,
        "save_2": saveLabel,
        'legend': legend,
        'form': form,
    })


@permission_required('app_card_inventory.change_id_card_receive_record')
def updateStock(request, pk=None):
    legend = "Update Stock"
    contEditingLabel = 'Update and Continue Editing'
    updateLabel = 'Update'

    obj = get_object_or_404(ID_Card_Receive_Record, id=pk)
    updateForm = StockForm((request.POST or None), instance=obj)
    if updateForm.is_valid():
        updateForm.save()

        # redirect to cards overview or add new after save
        if request.method == 'POST' and 'btnSave' in request.POST:
            return redirect('/cards/stocks')
        else:
            pass
            return redirect('/cards/stocks/{}'.format(pk))

    contex = {
        "save_1": contEditingLabel,
        "save_2": updateLabel,
        "legend": legend,
        "form": updateForm,
    }

    return render(request, 'templates_cards/cards_add_history.html', contex)
