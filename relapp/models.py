from django.db import models


class E0(models.Model):
    e0oppm = models.CharField(max_length=12)
    e0module = models.CharField(max_length=20)
    e0efforts = models.DecimalField(max_digits=4, decimal_places=2)
    e0updtdte = models.DateTimeField()

    def __str__(self):
        return(self.e0oppm)


class E1(models.Model):
    e1oppm = models.CharField(max_length=12)
    e1module = models.CharField(max_length=20)
    e1efforts = models.DecimalField(max_digits=4, decimal_places=2)
    e1providedte = models.DateTimeField()

    def __str__(self):
        return(self.e1oppm)


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
    requestchannel = models.CharField(max_length=10)
    bsgleadba = models.CharField(max_length=30)
    bsgba = models.CharField(max_length=7)
    pm = models.CharField(max_length=30)
    adddte = models.DateTimeField()
    status = models.CharField(max_length=20)
    remarks = models.TextField()

    def __str__(self):
        return(self.oppm)


class RelCalendar(models.Model):
    releaseid = models.CharField(max_length=7, primary_key=True)
    planningstartdte = models.DateTimeField()
    planningenddte = models.DateTimeField()
    initstartdte = models.DateTimeField()
    initenddte = models.DateTimeField()
    defnstartdte = models.DateTimeField()
    defnenddte = models.DateTimeField()
    designstartdte = models.DateTimeField()
    designenddte = models.DateTimeField()
    constrstartdte = models.DateTimeField()
    constrenddte = models.DateTimeField()
    valsitstartdte = models.DateTimeField()
    valsitenddte = models.DateTimeField()
    valuatstartdte = models.DateTimeField()
    valuatenddte = models.DateTimeField()
    implstartdte = models.DateTimeField()
    implenddte = models.DateTimeField()

    def __str__(self):
        return(self.releaseid)
