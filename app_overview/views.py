from django.shortcuts import render
from app_card_inventory.models import ID_Card
from app_cards.models import IDPrintRecord
from app_ribbon_inventory.models import Printer_Ribbon
from .models import Active_Stocks
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime


@login_required(login_url='/')
def overview(request):
    cards = ID_Card.objects.all()
    ribbons = Printer_Ribbon.objects.all()
    active_cards = Active_Stocks.objects.all()

    return render(request, 'templates_overview/overview.html', {
        'cards': cards,
        'ribbons': ribbons,
        'active': active_cards,
    })


@login_required(login_url='/')
@api_view()
def get_total_data(request):
    totalData = []
    successData = []
    spoiledData = []

    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    records = IDPrintRecord.objects.all()

    month = 1
    today = datetime.date.today()
    for month in range(1, 13):
        spoiled = 0
        success = 0
        total = 0
        newRecs = records.filter(print_date__year=today.year, print_date__month=month)
        total = newRecs.count()
        success = total
        for newRec in newRecs:
            spoiled += newRec.bad_print
        totalData.append(total)
        successData.append(success)
        spoiledData.append(spoiled)

    newRecs = records.filter(print_date__year=today.year)
    typeData = [
        newRecs.filter(id_type__id=1).count(),
        newRecs.filter(id_type__id=2).count() + newRecs.filter(id_type__id=3).count(),
        newRecs.filter(id_type__id=4).count(),
        newRecs.filter(id_type__id=5).count(),
        newRecs.filter(id_type__id=6).count(),
        newRecs.filter(id_type__id=7).count(),
        newRecs.filter(id_type__id=8).count(),
    ]

    data = {
        "totalData": totalData,
        "successData": successData,
        "spoiledData": spoiledData,
        "typeData": typeData,
        "labels": labels,
    }
    return Response(data)
