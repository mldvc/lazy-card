from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PrintHistoryForm, SearchForm
from .models import IDPrintRecord
from app_ribbons.models import RibbonUsageRecord
from app_id_form.models import ID_Form
from datetime import date, datetime as dt


@login_required(login_url='/')
def cards(request):
    totalBadPrints = 0
    totalPrints = 0
    totalSuccessPrints = 0
    totalRibbonUsed = 0

    # Search form ============================================
    searchForm = SearchForm(request.GET or None)
    page = request.GET.get('page')

    # populate table with initial data
    printHistory = IDPrintRecord.objects.filter(print_date=dt.now())

    if searchForm.is_valid():
        # date search
        printHistory = IDPrintRecord.objects.all()
        printHistory = IDPrintRecord.objects.filter(
            print_date__range=[
                searchForm.cleaned_data['dateFrom'],
                searchForm.cleaned_data['dateTo']
            ]
        )
        # name search
        nameSearch = searchForm.cleaned_data['nameSearch']
        if nameSearch:
            printHistory = printHistory.filter(name__contains=nameSearch)
        # type search
        typeSearch = searchForm.cleaned_data['typeSearch']
        if typeSearch:
            printHistory = printHistory.filter(id_type=typeSearch)
        # status search
        statusSearch = searchForm.cleaned_data['statusSearch']
        if statusSearch != "ALL":
            printHistory = printHistory.filter(id_status=statusSearch)
        # ribbon search
        ribbonSearch = searchForm.cleaned_data['ribbonSearch']
        if ribbonSearch:
            printHistory = printHistory.filter(ribbon=ribbonSearch)
    # !Search form ============================================

    for history in printHistory:
        totalBadPrints += history.bad_print
    # can be improved but will be too long its not nece
    totalRibbonUsed = RibbonUsageRecord.objects.count()
    totalSuccessPrints = printHistory.count()
    totalPrints = totalSuccessPrints + totalBadPrints

    # Show 25 contacts per page
    paginator = Paginator(printHistory, 20)

    try:
        printHistory_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        printHistory_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        printHistory_list = paginator.page(paginator.num_pages)

    # search_path = (
    #     "?csrfmiddlewaretoken={{ request.GET.csrfmiddlewaretoken }}" +
    #     "&dateFrom={{ request.GET.dateFrom }}" +
    #     "&dateTo={{ request.GET.dateTo }}" +
    #     "&nameSearch={{ request.GET.nameSearch }}" +
    #     "&typeSearch={{ request.GET.typeSearch }}" +
    #     "&statusSearch={{ request.GET.statusSearch }}" +
    #     "&ribbonSearch={{ request.GET.ribbonSearch }}" +
    #     "&btnSearch={{ request.GET.btnSearch }}"
    # )

    return render(request, 'templates_cards/cards_overview.html', {
        # 'printHistory': printHistory_list.order_by('-id'),
        'printHistory': printHistory_list,
        'totalSuccessPrints': totalSuccessPrints,
        'totalPrints': totalPrints,
        'totalBadPrints': totalBadPrints,
        'searchForm': searchForm,
        'totalRibbonUsed': totalRibbonUsed,
        # 'search_path': search_path
    })


@permission_required('app_cards.add_idprintrecord')
def add_print_history(request, pk=None):

    userForm = None
    dictInit = None
    legend = "Add Print History"
    default_bad_print = 0
    addAnotherLabel = 'Save and add another'
    saveLabel = 'Save'

    if pk:
        userForm = get_object_or_404(ID_Form, id=pk)
        userIDNum = userForm.id_number
        userFname = userForm.full_name
        userIDType = userForm.id_type.id
        dictInit = {
            'bad_print': default_bad_print,
            'print_date': date.today(),
            'id_number': userIDNum,
            'name': userFname,
            'id_type': userIDType,
        }
    else:
        dictInit = {
            'bad_print': default_bad_print,
            'print_date': date.today(),
        }

    form = PrintHistoryForm(
        (request.POST or None),
        initial=dictInit,
        request=request
    )

    if form.is_valid():
        form.save()

        if request.method == 'POST' and 'btnSave' in request.POST:
            if pk:
                return redirect('/forms')
            else:
                return redirect('/cards')
        else:
            if pk:
                return redirect('/forms')
            else:
                return redirect('/cards/add_print_history')

    contex = {
        "save_1": addAnotherLabel,
        "save_2": saveLabel,
        "legend": legend,
        "form": form
    }
    return render(request, 'templates_cards/cards_add_history.html', contex)


@permission_required('app_cards.change_idprintrecord')
def update_print_history(request, pk=None):
    legend = "Update Print History"
    contEditingLabel = 'Update and Continue Editing'
    updateLabel = 'Update'

    obj = get_object_or_404(IDPrintRecord, id=pk)
    updateForm = PrintHistoryForm(
        (request.POST or None),
        instance=obj,
        request=request
    )

    if updateForm.is_valid():
        updateForm.save()

        if request.method == 'POST' and 'btnSave' in request.POST:
            return redirect('/cards')
        else:
            return redirect('/cards/{}'.format(str(pk)))

    contex = {
        "save_1": contEditingLabel,
        "save_2": updateLabel,
        "legend": legend,
        "form": updateForm,
    }

    return render(request, 'templates_cards/cards_add_history.html', contex)
