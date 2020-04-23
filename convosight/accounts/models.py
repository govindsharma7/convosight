"""
User model class
"""
import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, Group, Permission,
    _user_has_module_perms, _user_has_perm)


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

'''
Overwriting Django User Manager
'''


class UserManager(BaseUserManager):

    """create user method """

    def _create_user(
            self, email, first_name=None, last_name=None,
            password=None, user_type=None, is_staff=None,
            is_superuser=None, **extra_fields):
        """

        Args:
            email: Unique email
            first_name: First Name
            last_name: Last Name
            password: User defined password which is saved encrypted
            user_type: This fields defines the user_type of the user
            namely Admin and User
            is_staff: This has to true for being super user
            is_superuser: This has to true for being super user
            **extra_fields: These are the extra arguments

        Returns: This returns django user object

        """
        now = timezone.now()
        if not email:
            raise ValueError(_('The given email must be set'))
        email = self.normalize_email(email)

        user = self.model(
            email=email, first_name=first_name,
            last_name=last_name, is_staff=is_staff,
            is_superuser=is_superuser, last_login=now,
            date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
            self, email, first_name=None, last_name=None,
            password=None, user_type=None, **extra_fields):
        if email is None:
            email = ""
        """

        Args:
            email: Unique email
            first_name: First Name
            last_name: Last Name
            password: User defined password which is saved encrypted
            user_type: This fields defines the user_type of the user namely
            Admin and User
            **extra_fields: These are the extra arguments

        Returns: returns values to the create user function, which
        in turn returns the user object

        """
        log.info("Creating user: {0}".format(email))
        return self._create_user(
            email=email.lower(), first_name=first_name, last_name=last_name,
            password=password, user_type=user_type, is_staff=False,
            is_superuser=False, **extra_fields)

    def create_superuser(
            self, email, first_name, last_name, password, **extra_fields):
        """

        Args:
            email: Unique email
            password: User defined password which is saved encrypted
            user_type: This fields defines the user_type of the user namely
            Admin and User
            **extra_fields:These are the extra arguments

        Returns: Returns Super user

        """
        user = self._create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password, is_staff=True,
            is_superuser=True, **extra_fields
        )

        user.is_active = True
        user.save(using=self._db)
        return user

    def update_user_details(self, email, first_name, last_name):
        """

        Args:
            email: Unique email
            first_name: First Name
            last_name: Last Name

        Returns: Updated user object

        """
        user = User.objects.get(email=email)

        if user is not None:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return user
        return None


class User(AbstractBaseUser):
    """ Main User model declaration"""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    groups = models.ManyToManyField(
        Group, verbose_name=_('groups'), blank=True,
        related_name="tmp_user_set", related_query_name="user"
    )
    user_permissions = models.ManyToManyField(
        Permission, verbose_name=_('user permissions'),
        blank=True, related_name="tmp_user_set", related_query_name="user"
    )
    first_name = models.CharField(
        _('first name'), max_length=30, null=True, blank=True)
    last_name = models.CharField(
        _('last name'), max_length=30, null=True, blank=True)
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    contact_number = models.CharField(
        _('contact number'), max_length=20, null=True, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    reset_password_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=timezone.now)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        """This class is used for verbose name defination"""
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def set_password(self, password):
        super(User, self).set_password(password)
        self.save()

    def get_full_name(self):
        """Returns: Full name of user"""
        full_name = ""

        first_name = (self.first_name or '').strip()
        if len(first_name) > 0:
            full_name = first_name

        last_name = (self.last_name or '').strip()
        if len(last_name) > 0:
            if len(full_name) > 0:
                full_name = full_name + ' '

            full_name = full_name + last_name

        return full_name

    def get_short_name(self):
        """Gets the first name of user"""
        return self.first_name

    def is_member(self, group_name):
        "Determine if a user is a member of a group or not."
        return self.groups.filter(name__iexact=group_name).exists()

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        # return "User: [id={0}, email={1}, user_type={2}]".format(
        #     self.id, self.email, self.user_type)
        return "{0} {1} ( {2} )".format(
            self.first_name, self.last_name, self.email)
