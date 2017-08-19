from django.shortcuts import render, render_to_response, get_object_or_404
from .models import Project, Release
from datetime import date
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import re


def home(request):
    return render(request, 'relapp/home.html')


def emeasumm(request):
    # today = date.today()
    # release = get_object_or_404(Project, pk=srchstr)
    #
    # if release.
    return render(request, 'relapp/emeasumm.html')


def emeasearch(request):
    if (request.method == 'POST'):
        srchstr = request.POST['srch']
        srchstr = srchstr.upper().strip()

        if (re.match('[A-Z]-[0-9]+', srchstr) and (srchstr != '')):
            project = get_object_or_404(Project, pk=srchstr)
            return render(request, 'relapp/emeacard.html', {'project': project})

        elif (re.match('[P][0-9]+', srchstr) and (srchstr != '')):
            oppmid = Project.objects.filter(pv__exact=srchstr)
            project = get_object_or_404(Project, pk=oppmid)
            return render(request, 'relapp/emeacard.html', {'project': project})

        elif (re.match('[R][1-4]-[0-9]+', srchstr) and (srchstr != '')):
            projects = Project.objects.filter(release__exact=srchstr)
            return render(request, 'relapp/emeadtls.html', {'projects': projects})

        elif (srchstr != ''):
            oppmid = Project.objects.filter(title__icontains=srchstr)
            project = get_object_or_404(Project, pk=oppmid)
            return render(request, 'relapp/emeacard.html', {'project': project})

        else:
            return render(request, 'relapp/emeacard.html')
    else:
        return render(request, 'relapp/home.html')


def emeacard(request, oppm):
    project = get_object_or_404(Project, pk=oppm)
    return render(request, 'relapp/emeacard.html', {'project': project})


def emeadtls(request):
    projects = Project.objects.order_by('oppm')
    return render(request, 'relapp/emeadtls.html', {'projects': projects})


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
            return HttpResponseRedirect(reverse('emeaadd'), saveform)

        if request.POST.get('reset'):
            return HttpResponseRedirect('emeaadd')
        elif request.POST.get('add'):
            Project.objects.create(oppm=request.POST['oppm'],
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
                                   #    invsubcat=request.POST['invsubcat'],
                                   adddte=date.today(),
                                   remarks=request.POST['remarks']
                                   )
            messages.info(request, 'Record added')
            return render(request, 'relapp/emeaadd.html')
    else:
        # projects = Project.objects.order_by('oppm')
        return render(request, 'relapp/emeaadd.html')


def emeacal(request):
    releases = Release.objects.order_by('releaseid')
    return render(request, 'relapp/emeacal.html', {'releases': releases})


def emeacontact(request):
    return render(request, 'relapp/emeacontact.html')
