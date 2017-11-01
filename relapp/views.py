from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Sum

from datetime import date, datetime
import time
import re
from .models import Project, E0, E1, RelCalendar

################################################################################


def home(request):
    return render(request, 'relapp/home.html')

################################################################################


def emeasearch(request):
    if (request.method == 'POST'):
        srchstr = request.POST['srch']
        srchstr = srchstr.upper().strip()

        # if srchstr == '':
        #     messages.set_level(request, messages.INFO)
        #     messages.error(request, 'No search string provided')
        #     return render(request, 'relapp/emeacard.html')

        # search by OPPM
        if (re.match('[A-Z]-[0-9]+', srchstr) and (srchstr != '')):
            try:
                project = get_object_or_404(Project, pk=srchstr)

            except Exception as e:
                messages.set_level(request, messages.ERROR)
                messages.error(request, 'OPPM not found in Project DB')
                return render(request, 'relapp/emeacard.html')

            e0recs = E0.objects.filter(e0oppm__exact=srchstr)
            e1recs = E1.objects.filter(e1oppm__exact=srchstr)

            return render(request, 'relapp/emeacard.html', {'project': project,
                                                            'e0recs': e0recs,
                                                            'e1recs': e1recs})

        # search by PV
        elif (re.match('[P][0-9]+', srchstr) and (srchstr != '')):
            try:
                proj = Project.objects.filter(pv__exact=srchstr).values()

            except Exception as e:
                messages.set_level(request, messages.ERROR)
                messages.error(request, 'PV not found in Project DB')
                return render(request, 'relapp/emeacard.html')

            try:
                project = get_object_or_404(Project, pk=proj[0]['oppm'])

            except Exception as e:
                messages.set_level(request, messages.ERROR)
                messages.error(request, 'OPPM not found in Project DB')
                return render(request, 'relapp/emeacard.html')

            e0recs = E0.objects.filter(e0oppm__exact=proj[0]['oppm'])
            e1recs = E1.objects.filter(e1oppm__exact=proj[0]['oppm'])

            return render(request, 'relapp/emeacard.html', {'project': project,
                                                            'e0recs': e0recs,
                                                            'e1recs': e1recs})

        # search by Release
        elif (re.match('[R][1-4]-[0-9]+', srchstr) and (srchstr != '')):
            try:
                projects = Project.objects.filter(release__exact=srchstr)

            except Exception as e:
                messages.set_level(request, messages.ERROR)
                messages.error(request, 'Release not found in Project DB')
                return render(request, 'relapp/emeacard.html')

            return render(request, 'relapp/emeadtls.html', {'projects': projects})

        # search by Title
        elif (re.match('[A-Za-z1-9]+', srchstr) and (srchstr != '')):
            try:
                projects = Project.objects.filter(title__icontains=srchstr)

            except Exception as e:
                messages.set_level(request, messages.ERROR)
                messages.error(request, 'Title not found in Project DB')
                return render(request, 'relapp/emeacard.html')

            return render(request, 'relapp/emeadtls.html', {'projects': projects})

        # Invalid search string
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Invalid search string')
            return render(request, 'relapp/emeacard.html')
    # GET
    else:
        return render(request, 'relapp/emeacard.html')


################################################################################

def emeasumm(request):
    summary = {}

    # Determine Release Phase
    today = date.today().strftime('%Y-%m-%d')

    releaseid = 'R1-2018'

    try:
        release = get_object_or_404(RelCalendar, pk=releaseid)

    except Exception as e:
        messages.set_level(request, messages.ERROR)
        messages.error(request, 'Requested release not found in Release DB')
        return render(request, 'relapp/emeasumm.html')

    if release.planningstartdte.strftime('%Y-%m-%d') <= today <= release.planningenddte.strftime('%Y-%m-%d'):
        phase = 'Planning'
        summary['startdte'] = release.planningstartdte.strftime('%Y-%m-%d')
        summary['enddte'] = release.planningenddte.strftime('%Y-%m-%d')

    elif release.initstartdte.strftime('%Y-%m-%d') <= today <= release.initenddte.strftime('%Y-%m-%d'):
        phase = 'Initiation'
        summary['startdte'] = release.initstartdte.strftime('%Y-%m-%d')
        summary['enddte'] = release.initenddte.strftime('%Y-%m-%d')

    elif release.defnstartdte.strftime('%Y-%m-%d') <= today <= release.defnenddte.strftime('%Y-%m-%d'):
        phase = 'Definition'
        summary['startdte'] = release.defnstartdte.strftime('%Y-%m-%d')
        summary['enddte'] = release.defnenddte.strftime('%Y-%m-%d')

    elif release.designstartdte.strftime('%Y-%m-%d') <= today <= release.designenddte.strftime('%Y-%m-%d'):
        phase = 'Design'
        summary['startdte'] = release.designstartdte.strftime('%Y-%m-%d')
        summary['enddte'] = release.designenddte.strftime('%Y-%m-%d')

    elif release.constrstartdte.strftime('%Y-%m-%d') <= today <= release.constrenddte.strftime('%Y-%m-%d'):
        phase = 'Construction'
        summary['startdte'] = release.constrstartdte.strftime('%Y-%m-%d')
        summary['enddte'] = release.constrenddte.strftime('%Y-%m-%d')

    elif release.valsitstartdte.strftime('%Y-%m-%d') <= today <= release.valsitenddte.strftime('%Y-%m-%d'):
        phase = 'SIT'
        summary['startdte'] = release.valsitstartdte.strftime('%Y-%m-%d')
        summary['enddte'] = release.valsitenddte.strftime('%Y-%m-%d')

    elif release.valuatstartdte.strftime('%Y-%m-%d') <= today <= release.valuatenddte.strftime('%Y-%m-%d'):
        phase = 'UAT'
        summary['startdte'] = release.valuatstartdte.strftime('%Y-%m-%d')
        summary['enddte'] = release.valuatenddte.strftime('%Y-%m-%d')

    elif release.implstartdte.strftime('%Y-%m-%d') <= today <= release.implenddte.strftime('%Y-%m-%d'):
        phase = 'Implementation'
        summary['startdte'] = release.implstartdte.strftime('%Y-%m-%d')
        summary['enddte'] = release.implenddte.strftime('%Y-%m-%d')

    summary['phase'] = phase

    # count of OPPMs
    summary['oppmcount'] = Project.objects.filter(release='R1-2018').count()

    # Project list
    try:
        projects = Project.objects.filter(release='R1-2018')

    except Exception as e:
        messages.set_level(request, messages.ERROR)
        messages.error(request, 'No projects in the requested release')
        return render(request, 'relapp/emeasumm.html')

    # Total release E0 & E1
    e0effort = {}
    e1effort = {}

    e0sum = 0
    e1sum = 0
    e0 = 0
    e1 = 0

    for project in projects:
        try:
            e0qset = E0.objects.filter(e0oppm__exact=project.oppm)

        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'OPPM from project not found in E0 DB')
            return render(request, 'relapp/emeasumm.html')

        for qs in e0qset:
            e0effort['e0'] = qs.e0efforts
            e0sum += qs.e0efforts

        try:
            e1qset = E1.objects.filter(e1oppm__exact=project.oppm)

        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'OPPM from project not found in E1 DB')
            return render(request, 'relapp/emeasumm.html')

        for qs in e1qset:
            e1effort['e1'] = qs.e1efforts
            e1sum += qs.e1efforts

    e0summ = {}
    e0summ['e0summ'] = e0sum

    e1summ = {}
    e1summ['e1summ'] = e1sum

    # oppm status count
    try:
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

    except Exception as e:
        messages.set_level(request, messages.ERROR)
        messages.error(request, 'Status not found in Project DB')
        return render(request, 'relapp/emeasumm.html')

    # RAG status

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
    try:
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

        stmts = E0.objects.filter(e0module='STMTS').aggregate(stmts_e0=Sum('e0efforts'))
        summary['stmts_e0'] = stmts['stmts_e0']

        ss = E0.objects.filter(e0module='SS').aggregate(ss_e0=Sum('e0efforts'))
        summary['ss_e0'] = ss['ss_e0']

        trams = E0.objects.filter(e0module='TRAMS').aggregate(trams_e0=Sum('e0efforts'))
        summary['trams_e0'] = trams['trams_e0']

        triad = E0.objects.filter(e0module='TRIAD').aggregate(triad_e0=Sum('e0efforts'))
        summary['triad_e0'] = triad['triad_e0']

        utility = E0.objects.filter(e0module='UTILITY').aggregate(utility_e0=Sum('e0efforts'))
        summary['utility_e0'] = utility['utility_e0']

    except Exception as e:
        messages.set_level(request, messages.ERROR)
        messages.error(request, 'Module aggregation failure in E0 DB')
        return render(request, 'relapp/emeasumm.html')

    # E1 efforts by application
    try:
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

        stmts = E1.objects.filter(e1module='STMTS').aggregate(stmts_e1=Sum('e1efforts'))
        summary['stmts_e1'] = stmts['stmts_e1']

        ss = E1.objects.filter(e1module='SS').aggregate(ss_e1=Sum('e1efforts'))
        summary['ss_e1'] = ss['ss_e1']

        trams = E1.objects.filter(e1module='TRAMS').aggregate(trams_e1=Sum('e1efforts'))
        summary['trams_e1'] = trams['trams_e1']

        triad = E1.objects.filter(e1module='TRIAD').aggregate(triad_e1=Sum('e1efforts'))
        summary['triad_e1'] = triad['triad_e1']

        utility = E1.objects.filter(e1module='UTILITY').aggregate(utility_e1=Sum('e1efforts'))
        summary['utility_e1'] = utility['utility_e1']

    except Exception as e:
        messages.set_level(request, messages.ERROR)
        messages.error(request, 'Module aggregation failure in E1 DB')
        return render(request, 'relapp/emeasumm.html')

    return render(request, 'relapp/emeasumm.html', {'phase': phase,
                                                    'projects': projects,
                                                    'e0summ': e0summ,
                                                    'e1summ': e1summ,
                                                    'e0effort': e0,
                                                    'e1effort': e1,
                                                    'summary': summary})

################################################################################


def emeadtls(request):
    project = Project.objects.order_by('oppm')

    return render(request, 'relapp/emeadtls.html', {'project': project})

################################################################################


def emeacard(request, oppm):
    try:
        project = get_object_or_404(Project, pk=oppm)

    except Exception as e:
        messages.set_level(request, messages.ERROR)
        messages.error(request, 'OPPM not found in Project DB')
        return render(request, 'relapp/emeacard.html')

    e0recs = E0.objects.filter(e0oppm__exact=oppm)
    e1recs = E1.objects.filter(e1oppm__exact=oppm)

    return render(request, 'relapp/emeacard.html', {'project': project,
                                                    'e0recs': e0recs,
                                                    'e1recs': e1recs})

################################################################################
# Add project


def emeaadd(request):
    if request.method == 'POST':
        if request.POST.get('reset'):
            return HttpResponseRedirect('relapp/emeaadd.html')

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
            # saveform = addform.objects.all()
            messages.info(request, 'OPPM or PV format is incorrect or Title is blank')

            return HttpResponseRedirect('relapp/emeaadd.html')

        if request.POST.get('add'):
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
        return render(request, 'relapp/emeaadd.html')

################################################################################


def emeaadde0(request):
    if request.method == 'POST':
        if (re.match('[A-Z]-[0-9]+', request.POST['e0oppm'])):
            try:
                project = get_object_or_404(Project, pk=request.POST['e0oppm'])

            except Exception as e:
                messages.info(request, 'Project not found')
                return HttpResponseRedirect('relapp/emeaadde0.html')
        else:
            messages.info(request, 'OPPM invalid')
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

        if request.POST['module3'] != "" and request.POST['e03'] != "":
            if request.POST['module3'] in mod:
                dup.append(request.POST['module3'])
            else:
                mod.append(request.POST['module3'])
        else:
            err.append(request.POST['module3'])

        if request.POST['module24'] != "" and request.POST['e04'] != "":
            if request.POST['module4'] in mod:
                dup.append(request.POST['module4'])
            else:
                mod.append(request.POST['module4'])
        else:
            err.append(request.POST['module4'])

        if request.POST['module5'] != "" and request.POST['e05'] != "":
            if request.POST['module5'] in mod:
                dup.append(request.POST['module5'])
            else:
                mod.append(request.POST['module5'])
        else:
            err.append(request.POST['module5'])

        if request.POST['module6'] != "" and request.POST['e06'] != "":
            if request.POST['module6'] in mod:
                dup.append(request.POST['module6'])
            else:
                mod.append(request.POST['module6'])
        else:
            err.append(request.POST['module6'])

        if request.POST['module7'] != "" and request.POST['e07'] != "":
            if request.POST['module7'] in mod:
                dup.append(request.POST['module7'])
            else:
                mod.append(request.POST['module7'])
        else:
            err.append(request.POST['module7'])

        if request.POST['module8'] != "" and request.POST['e08'] != "":
            if request.POST['module8'] in mod:
                dup.append(request.POST['module8'])
            else:
                mod.append(request.POST['module8'])
        else:
            err.append(request.POST['module8'])

        if request.POST['module9'] != "" and request.POST['e09'] != "":
            if request.POST['module9'] in mod:
                dup.append(request.POST['module9'])
            else:
                mod.append(request.POST['module9'])
        else:
            err.append(request.POST['module9'])

        if request.POST['module10'] != "" and request.POST['e010'] != "":
            if request.POST['module10'] in mod:
                dup.append(request.POST['module10'])
            else:
                mod.append(request.POST['module10'])
        else:
            err.append(request.POST['module10'])

        print(err)
        print(dup)
        print(mod)

        if len(err) > 0:
            messages.info(request, 'Module / E0 not entered')
            return HttpResponseRedirect('relapp/emeaadde0.html')

        if len(dup) > 0:
            messages.info(request, 'Duplicate module')
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

            if writecount != 0:
                E0.objects.create(e0oppm=request.POST['e0oppm'],
                                  e0module=request.POST['module3'],
                                  e0efforts=request.POST['e03'],
                                  e0updtdte=date.today()
                                  )

            writecount -= 1

            if writecount != 0:
                E0.objects.create(e0oppm=request.POST['e0oppm'],
                                  e0module=request.POST['module4'],
                                  e0efforts=request.POST['e04'],
                                  e0updtdte=date.today()
                                  )

            writecount -= 1

            if writecount != 0:
                E0.objects.create(e0oppm=request.POST['e0oppm'],
                                  e0module=request.POST['module5'],
                                  e0efforts=request.POST['e05'],
                                  e0updtdte=date.today()
                                  )

            writecount -= 1

            if writecount != 0:
                E0.objects.create(e0oppm=request.POST['e0oppm'],
                                  e0module=request.POST['module6'],
                                  e0efforts=request.POST['e06'],
                                  e0updtdte=date.today()
                                  )

            writecount -= 1

            if writecount != 0:
                E0.objects.create(e0oppm=request.POST['e0oppm'],
                                  e0module=request.POST['module7'],
                                  e0efforts=request.POST['e07'],
                                  e0updtdte=date.today()
                                  )

            writecount -= 1

            if writecount != 0:
                E0.objects.create(e0oppm=request.POST['e0oppm'],
                                  e0module=request.POST['module8'],
                                  e0efforts=request.POST['e08'],
                                  e0updtdte=date.today()
                                  )

            writecount -= 1

            if writecount != 0:
                E0.objects.create(e0oppm=request.POST['e0oppm'],
                                  e0module=request.POST['module9'],
                                  e0efforts=request.POST['e09'],
                                  e0updtdte=date.today()
                                  )

            writecount -= 1

            if writecount != 0:
                E0.objects.create(e0oppm=request.POST['e0oppm'],
                                  e0module=request.POST['module10'],
                                  e0efforts=request.POST['e010'],
                                  e0updtdte=date.today()
                                  )

            writecount -= 1

            messages.info(request, 'E0 record added')
            return HttpResponseRedirect('relapp/emeaadde0.html')
    else:
        return render(request, 'relapp/emeaadde0.html')

################################################################################


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

        if request.POST['module3'] != "" and request.POST['e13'] != "":
            if request.POST['module3'] in mod:
                dup.append(request.POST['module3'])
            else:
                mod.append(request.POST['module3'])
        else:
            err.append(request.POST['module3'])

        if request.POST['module4'] != "" and request.POST['e14'] != "":
            if request.POST['module4'] in mod:
                dup.append(request.POST['module4'])
            else:
                mod.append(request.POST['module4'])
        else:
            err.append(request.POST['module4'])

        if request.POST['module5'] != "" and request.POST['e15'] != "":
            if request.POST['module5'] in mod:
                dup.append(request.POST['module5'])
            else:
                mod.append(request.POST['module5'])
        else:
            err.append(request.POST['module5'])

        if request.POST['module6'] != "" and request.POST['e16'] != "":
            if request.POST['module6'] in mod:
                dup.append(request.POST['module6'])
            else:
                mod.append(request.POST['module6'])
        else:
            err.append(request.POST['module6'])

        if request.POST['module7'] != "" and request.POST['e17'] != "":
            if request.POST['module7'] in mod:
                dup.append(request.POST['module7'])
            else:
                mod.append(request.POST['module7'])
        else:
            err.append(request.POST['module7'])

        if request.POST['module8'] != "" and request.POST['e18'] != "":
            if request.POST['module8'] in mod:
                dup.append(request.POST['module8'])
            else:
                mod.append(request.POST['module8'])
        else:
            err.append(request.POST['module8'])

        if request.POST['module9'] != "" and request.POST['e19'] != "":
            if request.POST['module9'] in mod:
                dup.append(request.POST['module9'])
            else:
                mod.append(request.POST['module9'])
        else:
            err.append(request.POST['module9'])

        if request.POST['module10'] != "" and request.POST['e110'] != "":
            if request.POST['module100'] in mod:
                dup.append(request.POST['module10'])
            else:
                mod.append(request.POST['module10'])
        else:
            err.append(request.POST['module10'])

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

            if writecount != 0:
                E1.objects.create(e1oppm=request.POST['e1oppm'],
                                  e1module=request.POST['module3'],
                                  e1efforts=request.POST['e13'],
                                  e1providedte=date.today()
                                  )

            writecount -= 1

            if writecount != 0:
                E1.objects.create(e1oppm=request.POST['e1oppm'],
                                  e1module=request.POST['module4'],
                                  e1efforts=request.POST['e14'],
                                  e1providedte=date.today()
                                  )

            writecount -= 1

            if writecount != 0:
                E1.objects.create(e1oppm=request.POST['e1oppm'],
                                  e1module=request.POST['module5'],
                                  e1efforts=request.POST['e15'],
                                  e1providedte=date.today()
                                  )

            writecount -= 1

            if writecount != 0:
                E1.objects.create(e1oppm=request.POST['e1oppm'],
                                  e1module=request.POST['module6'],
                                  e1efforts=request.POST['e16'],
                                  e1providedte=date.today()
                                  )

            writecount -= 1

            if writecount != 0:
                E1.objects.create(e1oppm=request.POST['e1oppm'],
                                  e1module=request.POST['module7'],
                                  e1efforts=request.POST['e17'],
                                  e1providedte=date.today()
                                  )

            writecount -= 1

            if writecount != 0:
                E1.objects.create(e1oppm=request.POST['e1oppm'],
                                  e1module=request.POST['module8'],
                                  e1efforts=request.POST['e18'],
                                  e1providedte=date.today()
                                  )

            writecount -= 1

            if writecount != 0:
                E1.objects.create(e1oppm=request.POST['e1oppm'],
                                  e1module=request.POST['module9'],
                                  e1efforts=request.POST['e19'],
                                  e1providedte=date.today()
                                  )

            writecount -= 1

            if writecount != 0:
                E1.objects.create(e1oppm=request.POST['e1oppm'],
                                  e1module=request.POST['module10'],
                                  e1efforts=request.POST['e110'],
                                  e1providedte=date.today()
                                  )

            writecount -= 1

            messages.info(request, 'E1 record added')
            return HttpResponseRedirect('relapp/emeaadde1.html')
    else:
        return render(request, 'relapp/emeaadde1.html')

################################################################################


def emeaeditprj(request):
    return render(request, 'relapp/emeaeditprj.html')

################################################################################


def emeaedite0(request):
    return render(request, 'relapp/emeaedite0.html')

################################################################################


def emeaedite1(request):
    return render(request, 'relapp/emeaedite1.html')

################################################################################


def emeacal(request):
    releaseid = 'R1-2018'

    try:
        release = get_object_or_404(RelCalendar, pk=releaseid)

    except Exception as e:
        messages.info(request, 'Error1: Calendar not found')
        return render(request, 'relapp/emeacal.html')

    return render(request, 'relapp/emeacal.html', {'release': release})

################################################################################


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

################################################################################


def emeacontact(request):
    return render(request, 'relapp/emeacontact.html')

################################################################################
