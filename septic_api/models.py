import uuid
from django.db import models
from localflavor.us.models import USStateField, USZipCodeField
#Used localflavor package to make handling address type fields easier. Defaults to USA addresses.
#Decided to use address, city, state, and zipcode as that is what HouseCanary needs, it is easy for a user to enter
# and hopefully if we needed to add other external API interactions they could cover most use-cases

class Home(models.Model):
    # Standard on all models
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    # Unique to home
    owner = models.ForeignKey('auth.User', related_name='home', on_delete=models.CASCADE) #Each home belongs to a user, a user can have multiple homes
    address = models.CharField(max_length=100)
    zipcode = USZipCodeField()
    city = models.CharField(max_length=60, blank=True)
    state = USStateField(blank=True)
    has_septic = models.BooleanField(null=True) #allows null since it is possible for this information to be unknown
    user_septic_info = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f'{self.id}'
