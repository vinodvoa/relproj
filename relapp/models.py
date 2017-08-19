from django.db import models


class Project(models.Model):
    oppm = models.CharField(max_length=12, primary_key=True)
    release = models.CharField(max_length=7)
    title = models.CharField(max_length=100)
    pv = models.CharField(max_length=10)
    impactedcountries = models.CharField(max_length=20)
    impactedpps = models.CharField(max_length=50)
    funding = models.CharField(max_length=20)
    invtype = models.CharField(max_length=20)
    invcat = models.CharField(max_length=20)
    invsubcat = models.CharField(max_length=20)
    requestchannel = models.CharField(max_length=10)
    bsgleadba = models.CharField(max_length=30)
    bsgba = models.CharField(max_length=7)
    pm = models.CharField(max_length=30)
    # rcrindte = models.DateTimeField()
    # rcroutdte = models.DateTimeField()
    adddte = models.DateTimeField()
    status = models.CharField(max_length=20)
    remarks = models.TextField()

    def __str__(self):
        return(self.oppm)

class Release(models.Model):
    releaseid = models.CharField(max_length=7, primary_key=True),
    planningstartdte = models.DateTimeField(),
    planningenddte = models.DateTimeField(),
    initstartdte = models.DateTimeField(),
    initenddte = models.DateTimeField(),
    defnstartdte = models.DateTimeField(),
    defnenddte = models.DateTimeField(),
    designstartdte = models.DateTimeField(),
    designenddte = models.DateTimeField(),
    constrstartdte = models.DateTimeField(),
    constrenddte = models.DateTimeField(),
    validnstartdte = models.DateTimeField(),
    validnenddte = models.DateTimeField(),
    implstartdte = models.DateTimeField(),
    implenddte = models.DateTimeField()

    def __str__(self):
        return(self.releaseid)
