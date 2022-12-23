from django.contrib import admin
from .models import Document, DocumentType, Unit, Elevator, ElevatorKind, ElevatorType, Firm
# Register your models here.
admin.site.register(Unit)
admin.site.register(ElevatorKind)
admin.site.register(ElevatorType)
admin.site.register(DocumentType)
admin.site.register(Document)
admin.site.register(Elevator)
admin.site.register(Firm)
