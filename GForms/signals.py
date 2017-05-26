from GForms.models import *
from GForms.serializers import *
from GForms.views import *
from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from pytz import timezone

   
# Signals
@receiver(post_save, sender=form_response_id)
def model_post_save(sender, **kwargs):
	print("Form Response Signal for saving Serializer data",kwargs['instance'].__dict__)
	serializer = FormResponseSerializer(data=kwargs['instance'].__dict__,many=True)
	print(serializer.is_valid())
	if serializer.is_valid():
		serializer.save()
	else:
		print(serializer.errors)
