from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Sum

from .models import Project, E0, E1, RelCalendar

from datetime import date, datetime
import time
import re


def home(request):
    return render(request, 'relapp/home.html')


def emeasumm(request):
    summary = {}

    # Determine Phase
    today = date.today().strftime('%Y-%m-%d')

    releaseid = 'R1-2018'

    try:
        release = get_object_or_404(RelCalendar, pk=releaseid)
    except Exception as e:
        print('Not Found')

    if release.planningstartdte.strftime('%Y-%m-%d') <= today <= release.planningenddte.strftime('%Y-%m-%d'):
        phase = 'Planning'
        summary['startdte'] = release.planningstartdte.strftime('%Y-%m-%d')
        summary['enddte'] = release.planningenddte.strftime('%Y-%m-%d')
    elif release.initstartdte.strftime('%Y-%m-%d') <= today <= release.initenddte.strftime('%Y-%m-%d'):
        phase = 'Initiation'
        summary['startdte'] = release.initstartdte.strftime('%Y-%m-%d')
        summary['enddte'] = release.initenddte.strftime('%Y-%m-%d')
    elif release.defnstartdte.strftime('%Y-%m-%d')  <= today <= release.defnenddte.strftime('%Y-%m-%d'):
        phase = 'Definition'
        summary['startdte'] = release.defnstartdte.strftime('%Y-%m-%d')
        summary['enddte'] = release.defnenddte.strftime('%Y-%m-%d')
    elif release.designstartdte.strftime('%Y-%m-%d')  <= today <= release.designenddte.strftime('%Y-%m-%d'):
        phase = 'Design'
        summary['startdte'] = release.designstartdte.strftime('%Y-%m-%d')
        summary['enddte'] = release.designenddte.strftime('%Y-%m-%d')
    elif release.constrstartdte.strftime('%Y-%m-%d')  <= today <= release.constrenddte.strftime('%Y-%m-%d'):
        phase = 'Construction'
        summary['startdte'] = release.constrstartdte.strftime('%Y-%m-%d')
        summary['enddte'] = release.constrenddte.strftime('%Y-%m-%d')
    elif release.valsitstartdte.strftime('%Y-%m-%d')  <= today <= release.valsitenddte.strftime('%Y-%m-%d'):
        phase = 'SIT'
        summary['startdte'] = release.valsitstartdte.strftime('%Y-%m-%d')
        summary['enddte'] = release.valsitenddte.strftime('%Y-%m-%d')
    elif release.valuatstartdte.strftime('%Y-%m-%d')  <= today <= release.valuatenddte.strftime('%Y-%m-%d'):
        phase = 'UAT'
        summary['startdte'] = release.valuatstartdte.strftime('%Y-%m-%d')
        summary['enddte'] = release.valuatenddte.strftime('%Y-%m-%d')
    elif release.implstartdte.strftime('%Y-%m-%d')  <= today <= release.implenddte.strftime('%Y-%m-%d'):
        phase = 'Implementation'
        summary['startdte'] = release.implstartdte.strftime('%Y-%m-%d')
        summary['enddte'] = release.implenddte.strftime('%Y-%m-%d')

    summary['phase'] = phase

    # count of OPPMs
    summary['oppmcount'] = Project.objects.filter(release='R1-2018').count()

    # Project list
    projects = Project.objects.filter(release='R1-2018')

    # Total release E0 & E1
    e0effort = {}
    e1effort = {}
    e0sum = 0
    e1sum = 0
    e0 = 0
    e1 = 0

    for project in projects:
        e0qset = E0.objects.filter(e0oppm__exact=project.oppm)
        for qs in e0qset:
            e0effort['e0'] = qs.e0efforts
            e0sum += qs.e0efforts

        e1qset = E1.objects.filter(e1oppm__exact=project.oppm)
        for qs in e1qset:
            e1effort['e1'] = qs.e1efforts
            e1sum += qs.e1efforts

    e0summ = {}
    e0summ['e0summ'] = e0sum

    e1summ = {}
    e1summ['e1summ'] = e1sum

    # oppm status count
    summary['analysis_wip_count'] = Project.objects.filter(
        release='R1-2018', status='Analysis WIP').count()

    summary['canc_count'] = Project.objects.filter(
        release='R1-2018', status='Canceled').count()

    summary['E1_provided_count'] = Project.objects.filter(
        release='R1-2018', status='E1 Provided').count()

    summary['E1_review_dev_count'] = Project.objects.filter(
        release='R1-2018', status='E1 Review by Dev').count()

    summary['E1_wip_count'] = Project.objects.filter(
        release='R1-2018', status='E1 WIP').count()

    summary['FR_int_review_wip_count'] = Project.objects.filter(
        release='R1-2018', status='FR Internal Review WIP').count()

    summary['FR_na_count'] = Project.objects.filter(
        release='R1-2018', status='FR NA').count()

    summary['FR_signed_off_count'] = Project.objects.filter(
        release='R1-2018', status='FR Signed Off').count()

    summary['FR_wip_count'] = Project.objects.filter(
        release='R1-2018', status='FR WIP').count()

    summary['no_cards_impact_count'] = Project.objects.filter(
        release='R1-2018', status='No Cards Impact').count()

    summary['pend_clarification_biz_count'] = Project.objects.filter(
        release='R1-2018', status='Pending Clarification from Biz').count()

    summary['pend_FR_walkthru_count'] = Project.objects.filter(
        release='R1-2018', status='Pending FR Walk Thru').count()

    summary['pend_req_count'] = Project.objects.filter(
        release='R1-2018', status='Pending Requirements').count()

    summary['sow_count'] = Project.objects.filter(
        release='R1-2018', status='SOW').count()

    # E0 efforts by status
    # for project in projects:
    #     statusqset = Project.objects.filter(status__exact = 'Analysis WIP').
    #         E0.objects.filter(e0oppm__exact=project.oppm)
    #     for qs in e0qset:
    #         e0effort['e0'] = qs.e0efforts
    #         e0sum += qs.e0efforts
    #
    #     e1qset = E1.objects.filter(e1oppm__exact=project.oppm)
    #     for qs in e1qset:
    #         e1effort['e1'] = qs.e1efforts
    #         e1sum += qs.e1efforts
    #
    # e0summ = {}
    # e0summ['e0summ'] = e0sum
    #
    # e1summ = {}
    # e1summ['e1summ'] = e1sum

    # E0 efforts by application
    ads = E0.objects.filter(e0module='ADS').aggregate(ads_e0=Sum('e0efforts'))
    summary['ads_e0'] = ads['ads_e0']

    cde = E0.objects.filter(e0module='CDE').aggregate(cde_e0=Sum('e0efforts'))
    summary['cde_e0'] = cde['cde_e0']

    eas = E0.objects.filter(e0module='EAS').aggregate(eas_e0=Sum('e0efforts'))
    summary['eas_e0'] = eas['eas_e0']

    ba = E0.objects.filter(e0module='BA').aggregate(ba_e0=Sum('e0efforts'))
    summary['ba_e0'] = ba['ba_e0']

    ecms = E0.objects.filter(e0module='ECMS').aggregate(ecms_e0=Sum('e0efforts'))
    summary['ecms_e0'] = ecms['ecms_e0']

    elts = E0.objects.filter(e0module='ELTS').aggregate(elts_e0=Sum('e0efforts'))
    summary['elts_e0'] = elts['elts_e0']

    emb = E0.objects.filter(e0module='Emb').aggregate(emb_e0=Sum('e0efforts'))
    summary['emb_e0'] = emb['emb_e0']

    epp = E0.objects.filter(e0module='EPP').aggregate(epp_e0=Sum('e0efforts'))
    summary['epp_e0'] = epp['epp_e0']

    fasb = E0.objects.filter(e0module='FASB').aggregate(fasb_e0=Sum('e0efforts'))
    summary['fasb_e0'] = fasb['fasb_e0']

    mli = E0.objects.filter(e0module='MLI').aggregate(mli_e0=Sum('e0efforts'))
    summary['mli_e0'] = mli['mli_e0']

    rws = E0.objects.filter(e0module='RWS').aggregate(rws_e0=Sum('e0efforts'))
    summary['rws_e0'] = rws['rws_e0']

    stmts= E0.objects.filter(e0module='STMTS').aggregate(stmts_e0=Sum('e0efforts'))
    summary['stmts_e0'] = stmts['stmts_e0']

    ss = E0.objects.filter(e0module='SS').aggregate(ss_e0=Sum('e0efforts'))
    summary['ss_e0'] = ss['ss_e0']

    trams = E0.objects.filter(e0module='TRAMS').aggregate(trams_e0=Sum('e0efforts'))
    summary['trams_e0'] = trams['trams_e0']

    triad = E0.objects.filter(e0module='TRIAD').aggregate(triad_e0=Sum('e0efforts'))
    summary['triad_e0'] = triad['triad_e0']

    utility = E0.objects.filter(e0module='UTILITY').aggregate(utility_e0=Sum('e0efforts'))
    summary['utility_e0'] = utility['utility_e0']

    # E1 efforts by application
    ads = E1.objects.filter(e1module='ADS').aggregate(ads_e1=Sum('e1efforts'))
    summary['ads_e1'] = ads['ads_e1']

    cde = E1.objects.filter(e1module='CDE').aggregate(cde_e1=Sum('e1efforts'))
    summary['cde_e1'] = cde['cde_e1']

    eas = E1.objects.filter(e1module='EAS').aggregate(eas_e1=Sum('e1efforts'))
    summary['eas_e1'] = eas['eas_e1']

    ba = E1.objects.filter(e1module='BA').aggregate(ba_e1=Sum('e1efforts'))
    summary['ba_e1'] = ba['ba_e1']

    ecms = E1.objects.filter(e1module='ECMS').aggregate(ecms_e1=Sum('e1efforts'))
    summary['ecms_e1'] = ecms['ecms_e1']

    elts = E1.objects.filter(e1module='ELTS').aggregate(elts_e1=Sum('e1efforts'))
    summary['elts_e1'] = elts['elts_e1']

    emb = E1.objects.filter(e1module='Emb').aggregate(emb_e1=Sum('e1efforts'))
    summary['emb_e1'] = emb['emb_e1']

    epp = E1.objects.filter(e1module='EPP').aggregate(epp_e1=Sum('e1efforts'))
    summary['epp_e1'] = epp['epp_e1']

    fasb = E1.objects.filter(e1module='FASB').aggregate(fasb_e1=Sum('e1efforts'))
    summary['fasb_e1'] = fasb['fasb_e1']

    mli = E1.objects.filter(e1module='MLI').aggregate(mli_e1=Sum('e1efforts'))
    summary['mli_e1'] = mli['mli_e1']

    rws = E1.objects.filter(e1module='RWS').aggregate(rws_e1=Sum('e1efforts'))
    summary['rws_e1'] = rws['rws_e1']

    stmts= E1.objects.filter(e1module='STMTS').aggregate(stmts_e1=Sum('e1efforts'))
    summary['stmts_e1'] = stmts['stmts_e1']

    ss = E1.objects.filter(e1module='SS').aggregate(ss_e1=Sum('e1efforts'))
    summary['ss_e1'] = ss['ss_e1']

    trams = E1.objects.filter(e1module='TRAMS').aggregate(trams_e1=Sum('e1efforts'))
    summary['trams_e1'] = trams['trams_e1']

    triad = E1.objects.filter(e1module='TRIAD').aggregate(triad_e1=Sum('e1efforts'))
    summary['triad_e1'] = triad['triad_e1']

    utility = E1.objects.filter(e1module='UTILITY').aggregate(utility_e1=Sum('e1efforts'))
    summary['utility_e1'] = utility['utility_e1']

    return render(request, 'relapp/emeasumm.html', {'phase':phase,
                                                    'projects': projects,
                                                    'e1summ': e0summ,
                                                    'e1summ': e1summ,
                                                    'e0effort': e0,
                                                    'e1effort': e1,
                                                    'summary': summary})


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
    releaseid = 'R1-2018'

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
