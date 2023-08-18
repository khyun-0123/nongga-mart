from django.contrib.auth.models import AbstractUser, Permission,Group
from django.db import models
from django.utils.translation import gettext_lazy as _  


class UserClass(AbstractUser):


    class Meta:
        permissions = [
            ("user", _("User")),   
            ("manager", _("Manager")), 
            ("admin", _("Admin")), 
            ("test", _("TEst")), 
            
        ]
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_set_userclass", 
        related_query_name="user_userclass",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_set_userclass", 
        related_query_name="user_userclass",
    )
