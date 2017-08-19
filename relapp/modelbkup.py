from django.db import models

# Create your models here.
class Release(models.Model):
    releaseid = models.CharField(max_length=20, primary_key=True),
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

class Project(models.Model):
    oppm = models.CharField(max_length=12, primary_key=True)
    release = models.CharField(max_length=7),
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
    adddte = models.DateTimeField()
    status = models.CharField(max_length=20)
    remarks = models.TextField()

    def __str__(self):
        return(self.oppm)

class E0(models.Model):
    e0oppmppid = models.CharField(max_length=13, primary_key=True),
    e0oppm = models.ForeignKey('Project',on_delete=models.CASCADE,)
    e0psgsoe = models.CharField(max_length=7),
    e0pocdte = models.DateTimeField(),
    e0qryopendte = models.DateTimeField(),
    e0qryclosedte = models.DateTimeField(),
    e0providedte = models.DateTimeField(),
    e0partabuild = models.IntegerField(),
    e0partbbuild = models.IntegerField(),
    e0partcbuild = models.IntegerField(),
    e0babuild = models.IntegerField()

    def __str__(self):
        return(self.e0oppmppid)

class E1(models.Model):
    e1oppmppid = models.CharField(max_length=13, primary_key=True),
    e1oppm = models.ForeignKey('Project',on_delete=models.CASCADE,)
    e1psgsoe = models.CharField(max_length=7),
    e1brddte = models.DateTimeField(),
    e1qryopendte = models.DateTimeField(),
    e1qryclosedte = models.DateTimeField(),
    e1providedte = models.DateTimeField(),
    e1partabuild = models.IntegerField(),
    e1partbbuild = models.IntegerField(),
    e1partcbuild = models.IntegerField(),
    e1babuild = models.IntegerField()
    draftfrdte = models.DateTimeField(),
    gate1dte = models.DateTimeField(),
    frdelvdte = models.DateTimeField(),
    gate2dte = models.DateTimeField(),
    gate3dte = models.DateTimeField(),
    frsignoffdte = models.DateTimeField()

    def __str__(self):
        return(self.e1oppmppid)

class PP(models.Model):
    ppid = models.CharField(max_length=20, primary_key=True),
    ppname = models.CharField(max_length=20)

    def __str__(self):
        return(self.ppid)

class Resource(models.Model):
    soeid = models.CharField(max_length=8, primary_key=True),
    fullname = models.CharField(max_length=30),
    onedown = models.CharField(max_length=30),
    manager = models.CharField(max_length=30),
    region = models.CharField(max_length=10),
    billable = models.BooleanField(default=1),
    company = models.CharField(max_length=5),
    location = models.CharField(max_length=10),
    ranking = models.CharField(max_length=10),
    subranking = models.CharField(max_length=10),
    status = models.CharField(max_length=10),
    offphone = models.CharField(max_length=15),
    mobile = models.CharField(max_length=15),
    dob = models.DateTimeField(),
    joindte = models.DateTimeField(),
    enddte = models.DateTimeField(),
    remarks = models.TextField()

    def __str__(self):
        return(self.soeid)

#
