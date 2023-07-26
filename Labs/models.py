import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import Account
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.


class Lab(models.Model):
    Lab_uuid = models.UUIDField(
        _("Lab's ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        _("Lab name"), blank=True, null=True, max_length=100
    )
    supervisor = models.ForeignKey(
        Account,
        verbose_name=_("Lab's creater"),
        related_name="Lab",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.name

    def get_owner_details(self):
        return Account.objects.get(account_uuid=self.supervisor)

    @staticmethod
    def get_Labs(x):
        """
        get the oganizatioin whose supervisor is x
        x -> customUser instance
        """
        try:
            return Lab.objects.filter(supervisor=x)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_Labs_from_uuid(x):
        try:
            return Lab.objects.get(Lab_uuid=x)
        except ObjectDoesNotExist:
            return None


class Issue(models.Model):
    issueStates = {
        ("Done", "Done"),
        ("Addressing", "Addressing"),
        ("Noted pending address", "Noted pending address"),
        ("Urgent attention", "Urgent attention"),
        ("Medium attention", "Medium attention"),
        ("Low attention", "Low attention"),
    }
    Lab = models.ForeignKey(
        Lab,
        verbose_name=_("Lab"),
        on_delete=models.CASCADE,
    )
    title = models.CharField(_("title of the field"), max_length=100)
    details = models.TextField(verbose_name=_("issue details"), max_length=400)
    reported_on = models.DateTimeField(verbose_name=_("date reported"))
    status = models.CharField(
        verbose_name=_("state"), max_length=50, choices=issueStates
    )
    reported_by = models.ForeignKey(
        Account, verbose_name=_("reported_by"), on_delete=models.CASCADE
    )
    addressed_on = (
        models.DateTimeField(
            verbose_name=_("addressed reported"), null=True, blank=True
        ),
    )
    admin_response = models.TextField(
        _("admins responses "),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Issue")
        verbose_name_plural = _("Issues")
        ordering = ["-reported_on"]

    def __str__(self):
        return f"{self.pk}-{self.reported_on}"

    @staticmethod
    def getList(x):
        # get all Labs issues
        return Issue.objects.filter(Lab=x)

    @staticmethod
    def getUserList(x):
        """
        get list of issues made by user
        x -> account
        """
        reporter = Account.get_account(x)
        return Issue.objects.filter(reported_by=reporter)

    @staticmethod
    def getListbyStatus(x, y):
        return Issue.objects.filter(Lab=x, status=y)

    @staticmethod
    def getIssueByPk(x):
        return Issue.objects.get(pk=x)
