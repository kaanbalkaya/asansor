from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Unit(models.Model):
    id=models.CharField(max_length=8, primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    has_elevator=models.BooleanField(default=False)
    address=models.CharField(max_length=200)
    def __str__(self):
        return self.name+" - "+self.address

class ElevatorKind(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=25, verbose_name='Cins')
    def __str__(self):
        return self.name.__str__()

class ElevatorType(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=25, verbose_name='Tip')
    def __str__(self):
        return self.name.__str__()

class Firm(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50, verbose_name='Firma İsmi')
    address=models.CharField(max_length=200)
    def __str__(self):
        return self.name.__str__()

class Elevator(models.Model):
    id=models.CharField(max_length=25, primary_key=True, verbose_name='Asansör Kimlik Numarası')
    unit=models.ForeignKey(Unit, on_delete=models.PROTECT, verbose_name='Kurum')
    kind=models.ForeignKey(ElevatorKind, on_delete=models.PROTECT, verbose_name='Cins')  # insan / Yük
    type=models.ForeignKey(ElevatorType, on_delete=models.PROTECT,  verbose_name='Tip')   #elektrik / hidrolik
    mount_year=models.IntegerField(verbose_name='Montaj Yılı')
    load_limit=models.IntegerField(verbose_name='Kapasite(Ağırlık - kg)')
    load_limit_people=models.IntegerField(verbose_name='Kapasite (Kişi - Sayı)')
    velocity=models.IntegerField(verbose_name='Beyan Hız (m/sn)')
    work_distance=models.IntegerField(verbose_name='Seyir Mesafesi (m)')
    station_count=models.IntegerField(verbose_name='Durak Sayısı')
    description=models.CharField(max_length=100, verbose_name='Açıklama')
    def __str__(self):
        return self.id+' - '+self.unit.__str__()


class DocumentType(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    def __str__(self):
        return str(self.id)+" - "+ self.name

class Document(models.Model):
    id=models.CharField(max_length=25, primary_key=True)
    document_number=models.CharField(max_length=50, verbose_name='Döküman Numarası')
    unit=models.ForeignKey(Unit, on_delete=models.PROTECT, verbose_name='Kurum')
    firm=models.ForeignKey(Firm, on_delete=models.PROTECT, verbose_name='Firma')
    elevator=models.ForeignKey(Elevator, on_delete=models.CASCADE, verbose_name='Asansör')
    document_type=models.ForeignKey(DocumentType, on_delete=models.PROTECT,  verbose_name='Döküman Tipi')
    description=models.CharField(max_length=150, default="", verbose_name='Açıklama')
    update_date=models.DateField(verbose_name='Güncelleme Tarihi')
    expire_date=models.DateField(verbose_name='Sona Erme Tarihi')
    def __str__(self):
        return self.document_type.__str__()+' '+self.expire_date.strftime("Bitiş Tarihi: %d/%m/%Y")
    @property
    def is_expired(self):
        return date.today() > self.expire_date
