from django.forms import ModelForm, DateInput
from .models import Document, Elevator
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget


class DateInput(DateInput):
    input_type = 'date'

class ElevatorForm(ModelForm):
    class Meta:
        model=Elevator
        fields=['id','kind','type','mount_year','load_limit','load_limit_people','velocity',
                 'work_distance','station_count','description']


class DocumentForm(ModelForm):
    class Meta:
        model=Document
        fields=['document_number','elevator','firm','document_type','update_date','expire_date','description']
        widgets = { 'update_date' : DateInput(),
                    'expire_date' : DateInput()}


"""
'venuetypes' : forms.Select(queryset=Venuetypes.objects.all, attrs={'class' : 'venue_type_select'})

class Document(models.Model):
    id=models.CharField(max_length=25, primary_key=True, verbose_name='Döküman Numarası')
    unit=models.ForeignKey(Unit, on_delete=models.PROTECT, verbose_name='Kurum')
    elevator=models.ForeignKey(Elevator, on_delete=models.CASCADE, verbose_name='Asansör')
    document_type=models.ForeignKey(DocumentType, on_delete=models.PROTECT,  verbose_name='Döküman Tipi')
    description=models.CharField(max_length=150, default="", verbose_name='Açıklama')
    update_date=models.DateField(verbose_name='Güncelleme Tarihi')
    expire_date=models.DateField(verbose_name='Sona Erme Tarihi')
    def __str__(self):
        return elevator.unit.__str__()+' '+document_type.__str__()
"""
