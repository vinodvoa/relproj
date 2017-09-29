from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Sum

from .models import Project, E0, E1, RelCalendar

from datetime import date
import time
import re


def home(request):
    return render(request, 'relapp/home.html')


def emeasumm(request):
    # Determine Phase
    # today = date.today() #yyyy-mm-dd
    # mth = today.month
    #
    # # if mth in range()
    # year = today.year

    # releaseid = 'R1-2018'
    #
    # try:
    #     release = get_object_or_404(RelCalendar, pk=releaseid)
    # except Exception as e:
    #     print('Not Found')
    #
    # print(today)
    # tupledate = []
    # tupledate.append(release.initstartdte)
    # print(date.year(tupledate[0]))
    # print(time.strftime('%Y-%m-%d',tupledate))

    # if today in range(release.planningstartdte, release.planningenddte):
    #     phase = 'Planning'
    # elif today in range(release.initstartdte, release.initenddte):
    #     phase = 'Initiation'
    # elif today in range(release.defnstartdte, release.defnenddte):
    #     phase = 'Definition'
    # elif today in range(release.designstartdte, release.designenddte):
    #     phase = 'Design'
    # elif today in range(release.constrstartdte, release.constrenddte):
    #     phase = 'Construction'
    # elif today in range(release.valsitstartdte, release.valsitenddte):
    #     phase = 'SIT'
    # elif today in range(release.valuatstartdte, release.valuatenddte):
    #     phase = 'UAT'
    # elif today in range(release.implstartdte, release.implenddte):
    #     phase = 'Implementation'
    #
    # print(phase)

    # count of OPPMs
    summary = {}

    summary['oppmcount'] = Project.objects.filter(release='R1-2018').count()

    # status count
    summary['pend_req_count'] = Project.objects.filter(
        release='R1-2018', status='Pending Requirements').count()

    summary['pend_clar_count'] = Project.objects.filter(
        release='R1-2018', status='Pending Clarifications').count()

    summary['pend_e0wip_count'] = Project.objects.filter(
        release='R1-2018', status='E0 WIP').count()

    summary['pend_e1wip_count'] = Project.objects.filter(
        release='R1-2018', status='E1 WIP').count()

    # # total E0 by status
    # pend_req_sum_e0 = Project.objects.filter(
    #     status='Pending Requirements').aggregate(Sum('status'))
    # print(pend_req_sum_e0)
    #
    # pend_clar_sum_e0 = Project.objects.filter(
    #     status='Pending Clarifications').aggregate(Sum('status'))
    # print(pend_clar_sum_e0)
    #
    # pend_e0wip_sum_e0 = Project.objects.filter(
    #     status='E0 WIP').aggregate(Sum('status'))
    # print(pend_e0wip_sum_e0)
    #
    # pend_e1wip_sum_e0 = Project.objects.filter(
    #     status='E1 WIP').aggregate(Sum('status'))
    # print(pend_e1wip_sum_e0)

    # E0 efforts by application
    summary['ads_e0'] = E0.objects.filter(
        e0module='ADS').aggregate(Sum('e0efforts'))
    summary['cde_e0'] = E0.objects.filter(
        e0module='CDE').aggregate(Sum('e0efforts'))
    summary['eas_e0'] = E0.objects.filter(
        e0module='EAS').aggregate(Sum('e0efforts'))
    summary['ba_e0'] = E0.objects.filter(
        e0module='BA').aggregate(Sum('e0efforts'))
    summary['ecms_e0'] = E0.objects.filter(
        e0module='ECMS').aggregate(Sum('e0efforts'))
    summary['elts_e0'] = E0.objects.filter(
        e0module='ELTS').aggregate(Sum('e0efforts'))
    summary['emb_e0'] = E0.objects.filter(
        e0module='Emb').aggregate(Sum('e0efforts'))
    summary['epp_e0'] = E0.objects.filter(
        e0module='EPP').aggregate(Sum('e0efforts'))
    summary['fasb_e0'] = E0.objects.filter(
        e0module='FASB').aggregate(Sum('e0efforts'))
    summary['mli_e0'] = E0.objects.filter(
        e0module='MLI').aggregate(Sum('e0efforts'))
    summary['rws_e0'] = E0.objects.filter(
        e0module='RWS').aggregate(Sum('e0efforts'))
    summary['stmts_e0'] = E0.objects.filter(
        e0module='STMTS').aggregate(Sum('e0efforts'))
    summary['ss_e0'] = E0.objects.filter(
        e0module='SS').aggregate(Sum('e0efforts'))
    summary['trams_e0'] = E0.objects.filter(
        e0module='TRIAD').aggregate(Sum('e0efforts'))
    summary['utility_e0'] = E0.objects.filter(
        e0module='UTILITY').aggregate(Sum('e0efforts'))

    # E1 efforts by application
    summary['ads_e1'] = E1.objects.filter(
        e1module='ADS').aggregate(Sum('e1efforts'))
    summary['cde_e1'] = E1.objects.filter(
        e1module='CDE').aggregate(Sum('e1efforts'))
    summary['eas_e1'] = E1.objects.filter(
        e1module='EAS').aggregate(Sum('e1efforts'))
    summary['ba_e1'] = E1.objects.filter(
        e1module='BA').aggregate(Sum('e1efforts'))
    summary['ecms_e1'] = E1.objects.filter(
        e1module='ECMS').aggregate(Sum('e1efforts'))
    summary['elts_e1'] = E1.objects.filter(
        e1module='ELTS').aggregate(Sum('e1efforts'))
    summary['emb_e1'] = E1.objects.filter(
        e1module='Emb').aggregate(Sum('e1efforts'))
    summary['epp_e1'] = E1.objects.filter(
        e1module='EPP').aggregate(Sum('e1efforts'))
    summary['fasb_e1'] = E1.objects.filter(
        e1module='FASB').aggregate(Sum('e1efforts'))
    summary['mli_e1'] = E1.objects.filter(
        e1module='MLI').aggregate(Sum('e1efforts'))
    summary['rws_e1'] = E1.objects.filter(
        e1module='RWS').aggregate(Sum('e1efforts'))
    summary['stmts_e1'] = E1.objects.filter(
        e1module='STMTS').aggregate(Sum('e1efforts'))
    summary['ss_e1'] = E1.objects.filter(
        e1module='SS').aggregate(Sum('e1efforts'))
    summary['trams_e1'] = E1.objects.filter(
        e1module='TRAMS').aggregate(Sum('e1efforts'))
    summary['triad_e1'] = E1.objects.filter(
        e1module='TRIAD').aggregate(Sum('e1efforts'))
    summary['utility_e1'] = E1.objects.filter(
        e1module='UTILITY').aggregate(Sum('e1efforts'))

    print(summary)
    return render(request, 'relapp/emeasumm.html', {'summary': summary})


def emeasearch(request):
    if (request.method == 'POST'):
        srchstr = request.POST['srch']
        srchstr = srchstr.upper().strip()

        if (re.match('[A-Z]-[0-9]+', srchstr) and (srchstr != '')):
            project = get_object_or_404(Project, pk=srchstr)
            e0 = E0.objects.filter(e0oppm__exact=srchstr)
            e1 = E1.objects.filter(e1oppm__exact=srchstr)

            return render(request, 'relapp/emeacard.html', {'project': project, 'e0': e0, 'e1': e1})

        elif (re.match('[P][0-9]+', srchstr) and (srchstr != '')):
            proj = Project.objects.filter(pv__exact=srchstr).values()
            project = get_object_or_404(Project, pk=proj[0]['oppm'])
            e0 = E0.objects.filter(e0oppm__exact=proj[0]['oppm'])
            e1 = E1.objects.filter(e1oppm__exact=proj[0]['oppm'])

            return render(request, 'relapp/emeacard.html', {'project': project, 'e0': e0, 'e1': e1})

        elif (re.match('[R][1-4]-[0-9]+', srchstr) and (srchstr != '')):
            projects = Project.objects.filter(release__exact=srchstr)
            return render(request, 'relapp/emeadtls.html', {'projects': projects})

        elif (re.match('[A-Za-z1-9]+', srchstr) and (srchstr != '')):
            projects = Project.objects.filter(title__icontains=srchstr)
            return render(request, 'relapp/emeadtls.html', {'projects': projects})

        else:
            return render(request, 'relapp/emeacard.html')
    else:
        return render(request, 'relapp/emeacard.html')


def emeadtls(request):
    project = Project.objects.order_by('oppm')
    return render(request, 'relapp/emeadtls.html', {'project': project})


def emeacard(request, oppm):
    project = get_object_or_404(Project, pk=oppm)
    return render(request, 'relapp/emeacard.html', {'project': project})


# Add project


def emeaadd(request):
    if request.method == 'POST':
        oppmerror = pverror = titleerror = False

        if (re.match('[A-Z]-[0-9]+', request.POST['oppm'])):
            pass
        else:
            oppmerror = True

        if (re.match('[P][0-9]+', request.POST['pv'])):
            pass
        else:
            pverror = True

        if (request.POST['title'] == ''):
            titleerror = True

        if (oppmerror or pverror or titleerror):
            saveform = addform.objects.all()
            messages.info(request, 'OPPM or PV format is incorrect or Title is blank')
            return HttpResponseRedirect('relapp/emeadtls.html')

        if request.POST.get('reset'):
            return HttpResponseRedirect('relapp/emeadtls.html')
        elif request.POST.get('add'):
            Project.objects.create(oppm=request.POST['oppm'],
                                   release=request.POST['release'],
                                   title=request.POST['title'],
                                   pv=request.POST['pv'],
                                   funding=request.POST['funding'],
                                   bsgleadba=request.POST['bsgleadba'],
                                   bsgba=request.POST['bsgba'],
                                   pm=request.POST['pm'],
                                   requestchannel=request.POST['requestchannel'],
                                   impactedcountries=request.POST['impactedcountries'],
                                   impactedpps=request.POST['impactedpps'],
                                   status=request.POST['status'],
                                   invtype=request.POST['invtype'],
                                   invcat=request.POST['invcat'],
                                   adddte=date.today(),
                                   remarks=request.POST['remarks'],
                                   )
            messages.info(request, 'Record added')
            return HttpResponseRedirect('relapp/emeadtls.html')
    else:
        # projects = Project.objects.order_by('oppm')
        return render(request, 'relapp/emeaadd.html')

# Add E0


def emeaadde0(request):
    if request.method == 'POST':
        if (re.match('[A-Z]-[0-9]+', request.POST['e0oppm'])):
            try:
                project = get_object_or_404(Project, pk=request.POST['e0oppm'])
            except Exception as e:
                messages.info(request, 'Error1: Project not found')
                return HttpResponseRedirect('relapp/emeaadde0.html')
        else:
            messages.info(request, 'Error2: OPPM invalid')
            return HttpResponseRedirect('relapp/emeaadde0.html')

        mod = []
        err = []
        dup = []

        if request.POST['module1'] != "" and request.POST['e01'] != "":
            mod.append(request.POST['module1'])
        else:
            err.append(request.POST['module1'])

        if request.POST['module2'] != "" and request.POST['e02'] != "":
            if request.POST['module2'] in mod:
                dup.append(request.POST['module2'])
            else:
                mod.append(request.POST['module2'])
        else:
            err.append(request.POST['module2'])

        if len(err) > 0:
            messages.info(request, 'Error3: Module / E0 not entered')
            return HttpResponseRedirect('relapp/emeaadde0.html')

        if len(dup) > 0:
            messages.info(request, 'Error4: Duplicate module')
            return HttpResponseRedirect('relapp/emeaadde0.html')

        writecount = len(mod)

        if request.POST.get('add'):
            E0.objects.create(e0oppm=request.POST['e0oppm'],
                              e0module=request.POST['module1'],
                              e0efforts=request.POST['e01'],
                              e0updtdte=date.today()
                              )
            writecount -= 1

            if writecount != 0:
                E0.objects.create(e0oppm=request.POST['e0oppm'],
                                  e0module=request.POST['module2'],
                                  e0efforts=request.POST['e02'],
                                  e0updtdte=date.today()
                                  )

            writecount -= 1

            messages.info(request, 'E0 record added')
            return HttpResponseRedirect('relapp/emeaadde0.html')
    else:
        return render(request, 'relapp/emeaadde0.html')

# Add E1


def emeaadde1(request):
    if request.method == 'POST':
        if (re.match('[A-Z]-[0-9]+', request.POST['e1oppm'])):
            try:
                project = get_object_or_404(Project, pk=request.POST['e1oppm'])
            except Exception as e:
                messages.info(request, 'Error1: Project not found')
                return HttpResponseRedirect('relapp/emeaadde1.html')
        else:
            messages.info(request, 'Error2: OPPM invalid')
            return HttpResponseRedirect('relapp/emeaadde1.html')

        mod = []
        err = []
        dup = []

        if request.POST['module1'] != "" and request.POST['e11'] != "":
            mod.append(request.POST['module1'])
        else:
            err.append(request.POST['module1'])

        if request.POST['module2'] != "" and request.POST['e12'] != "":
            if request.POST['module2'] in mod:
                dup.append(request.POST['module2'])
            else:
                mod.append(request.POST['module2'])
        else:
            err.append(request.POST['module2'])

        if len(err) > 0:
            messages.info(request, 'Error3: Module / E1 not entered')
            return HttpResponseRedirect('relapp/emeaadde1.html')

        if len(dup) > 0:
            messages.info(request, 'Error4: Duplicate module')
            return HttpResponseRedirect('relapp/emeaadde1.html')

        writecount = len(mod)

        if request.POST.get('add'):
            obj, created = E1.objects.get_or_create(e1oppm=request.POST['e1oppm'],
                                                    e1module=request.POST['module1'],
                                                    e1efforts=request.POST['e11'],
                                                    e1providedte=date.today()
                                                    )
            writecount -= 1

            if writecount != 0:
                E1.objects.create(e1oppm=request.POST['e1oppm'],
                                  e1module=request.POST['module2'],
                                  e1efforts=request.POST['e12'],
                                  e1providedte=date.today()
                                  )

            writecount -= 1

            messages.info(request, 'E1 record added')
            return HttpResponseRedirect('relapp/emeaadde1.html')
    else:
        return render(request, 'relapp/emeaadde1.html')


def emeaeditprj(request):
    return render(request, 'relapp/emeaeditprj.html')


def emeaedite0(request):
    return render(request, 'relapp/emeaedite0.html')


def emeaedite1(request):
    return render(request, 'relapp/emeaedite1.html')


def emeacal(request):
    releaseid = 'R4-2017'

    try:
        release = get_object_or_404(RelCalendar, pk=releaseid)

    except Exception as e:
        messages.info(request, 'Error1: Calendar not found')
        return render(request, 'relapp/emeacal.html')

    return render(request, 'relapp/emeacal.html', {'release': release})


def emeacaladd(request):
    if request.method == 'POST':
        if (re.match('[R][1-4]-[0-9]+', request.POST['release'])):
            if request.POST.get('add'):
                RelCalendar.objects.create(releaseid=request.POST['release'],
                                           planningstartdte=request.POST['planstrtdte'],
                                           planningenddte=request.POST['planenddte'],
                                           initstartdte=request.POST['initstrtdte'],
                                           initenddte=request.POST['initenddte'],
                                           defnstartdte=request.POST['defstrtdte'],
                                           defnenddte=request.POST['defenddte'],
                                           designstartdte=request.POST['desstrtdte'],
                                           designenddte=request.POST['desenddte'],
                                           constrstartdte=request.POST['constrtdte'],
                                           constrenddte=request.POST['conenddte'],
                                           valsitstartdte=request.POST['sitstrtdte'],
                                           valsitenddte=request.POST['sitenddte'],
                                           valuatstartdte=request.POST['uatstrtdte'],
                                           valuatenddte=request.POST['uatenddte'],
                                           implstartdte=request.POST['implstrtdte'],
                                           implenddte=request.POST['implenddte']
                                           )
                messages.info(request, 'Record added')
                return render(request, 'relapp/emeacaladd.html')
            else:
                pass
        else:
            messages.info(request, 'Error: Release ID invalid')
            return HttpResponseRedirect('relapp/emeacaladd.html')
    else:
        return render(request, 'relapp/emeacaladd.html')


def emeacontact(request):
    return render(request, 'relapp/emeacontact.html')
