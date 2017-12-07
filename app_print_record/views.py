from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app_cards.models import IDPrintRecord
from app_reference.models import IDTypes
from app_ribbons.models import RibbonUsageRecord
from app_overview.models import Printer_Ribbon, ID_Card, Active_Stocks
from .forms import PrintForm
from datetime import timedelta, datetime as dt
from django.contrib.admin.views.decorators import staff_member_required


def get_id_type_dict():
    DICT_ID_TYPE = {
        'COL': 'College/Graduate ID',
        'ALU': 'Alumni ID',
        'PLU': 'Alumni Plus Card',
        'SHS': 'Senior High School ID',
        'HSC': 'High School',
        'ELM': 'Elementary/CCD ID',
        'EMP': 'Employee ID',
        'HOS': 'Hospital ID',
    }
    return DICT_ID_TYPE


@login_required(login_url='/')
@staff_member_required
def report(request):
    # print form ===============================
    printForm = PrintForm((request.GET or None))

    dictCardsTotal = {}
    objDict = {}
    dayDict = {}
    OASuccess = 0
    OAError = 0
    OATotal = 0
    reportDate = 'DATE'
    ribbonStockObj = None
    ribbonTotalUsed = None
    ribbonObj = None

    if printForm.is_valid():

        dateFrom = printForm.cleaned_data['dateFrom']
        dateTo = printForm.cleaned_data['dateTo']

        if dateFrom == dateTo:
            reportDate = '{:%B %d, %Y}'.format(dateTo)
        else:
            reportDate = '{:%B %d} to {:%B %d, %Y}'.format(dateFrom, dateTo)

        objIDTypes = IDTypes.objects.all()

        obj = IDPrintRecord.objects.all()
        fObject = obj.filter(
            print_date__range=[dateFrom, dateTo]
        )

        idtypeSearch = printForm.cleaned_data['idtypeSearch']
        if idtypeSearch:
            fObject = obj.filter(id_type=idtypeSearch)

        currDay = dateFrom
        while currDay <= dateTo:
            dateObj = fObject.filter(print_date=currDay)
            totalSuccess = 0
            totalError = 0
            totalOfTotal = 0

            for idType in objIDTypes:
                mainObj = dateObj.filter(id_type=idType)
                # CALCULATE SUCCESS
                success = mainObj.count()
                totalSuccess += success
                # CALCULATE BAD PRINT
                error = 0
                for obj in mainObj:
                    error += obj.bad_print
                totalError += error
                # CALCULATE TOTAL
                total = success + error
                totalOfTotal += total
                objDict[idType.short] = [success, error, total]

            OASuccess += totalSuccess
            OAError += totalError
            OATotal += totalOfTotal

            objDict['total'] = [totalSuccess, totalError, totalOfTotal]

            dayDict[currDay] = objDict.copy()
            currDay = currDay + timedelta(days=1)

        # CARDS STOCKS
        mainCardStockObj = ID_Card.objects.all()
        activeCardStockObj = Active_Stocks.objects.all()
        for main in mainCardStockObj:
            for active in activeCardStockObj:
                if main.card_type == active.card_type.card_type:
                    totalstock = main.amount + active.amount
                    dictCardsTotal[main.card_type] = totalstock

        # FOR RIBBONS
        ribbonObj = RibbonUsageRecord.objects.filter(
            ribbon_use_date__range=[dateFrom, dateTo]
        )
        ribbonTotalUsed = ribbonObj.count()
        ribbonStockObj = Printer_Ribbon.objects.all()

    contex = {
        "dictCardsTotal": dictCardsTotal,
        "ribbonStockObj": ribbonStockObj,
        "ribbonTotalUsed": ribbonTotalUsed,
        "ribbonObj": ribbonObj,
        "dictIDType": get_id_type_dict(),
        "searchForm": printForm,
        "objDict": dayDict,
        "OASuccess": OASuccess,
        "OAError": OAError,
        "OATotal": OATotal,
        "reportDate": reportDate.upper(),
    }
    return render(request, 'templates_reports/print_report.html', contex)


@login_required(login_url='/')
@staff_member_required
def recordReport(request):
    DICT_ID_STATUS = {
        'CLA': 'Claimed',
        'PRI': 'Printed',
    }

    totalBadPrint = 0
    totalSuccess = 0
    totalPrint = 0

    printForm = PrintForm((request.GET or None))

    reportDate = 'DATE'

    obj = IDPrintRecord.objects.all()
    fObject = obj.filter(print_date=dt.now())

    if printForm.is_valid():

        dateFrom = printForm.cleaned_data['dateFrom']
        dateTo = printForm.cleaned_data['dateTo']

        if dateFrom == dateTo:
            reportDate = '{:%B %d, %Y}'.format(dateTo)
        else:
            reportDate = '{:%B %d} to {:%B %d, %Y}'.format(dateFrom, dateTo)

        fObject = obj.filter(
            print_date__range=[dateFrom, dateTo]
        ).order_by('name')

        idtypeSearch = printForm.cleaned_data['idtypeSearch']
        if idtypeSearch:
            fObject = fObject.filter(id_type=idtypeSearch).order_by('name')

        for obj in fObject:
            totalBadPrint += obj.bad_print

        totalSuccess = fObject.count()
        totalPrint = totalSuccess + totalBadPrint

    contex = {
        "totalBadPrint": totalBadPrint,
        "dictIDStatus": DICT_ID_STATUS,
        "searchForm": printForm,
        "fObject": fObject,
        "reportDate": reportDate.upper(),
        "totalSuccess": totalSuccess,
        "totalPrint": totalPrint,
    }
    return render(request, 'templates_reports/record_report.html', contex)
