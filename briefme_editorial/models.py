from django.db import models
from django.conf import settings
from django.urls import reverse

from django_reactive.fields import ReactJSONSchemaField, TemplateField
from model_utils.models import StatusModel, TimeStampedModel
from model_utils.fields import MonitorField
from model_utils import Choices
from tinymce.models import HTMLField

from .constants import TEMPLATE_CHOICES
from .utils import apply_func_to_dict, add_target_blank_to_links


class Issue(TimeStampedModel, StatusModel):
    STATUS = Choices("draft", "pending", "published")
    title = models.CharField(max_length=200)
    template = models.CharField(max_length=6, choices=TEMPLATE_CHOICES, default="new")
    intro = HTMLField(blank=True, null=True)
    post_scriptum_intro = HTMLField(null=True, blank=True)
    outro = HTMLField(blank=True, null=True)
    authors = HTMLField(null=True, blank=True)
    post_scriptum_outro = HTMLField(null=True, blank=True)
    published_at = MonitorField(monitor="status", when=["published"])
    pushed = models.BooleanField(default=False)
    pushed_at = MonitorField(monitor="pushed", when=[True])

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def get_email_url(self):
        kwargs = {"pk": self.pk}
        return "%s%s" % (settings.SITE_DOMAIN, reverse("issue_detail_email", kwargs=kwargs))

    def publish(self):
        self.status = self.STATUS.published
        self.save()


class Section(TimeStampedModel):
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class News(TimeStampedModel):
    TEMPLATES = []
    HTML_DATA_FIELDS = {}
    SEARCHABLE_DATA_FIELDS = {}
    TYPOGRAPHIE_DATA_FIELDS = {}

    title = models.CharField(max_length=200, blank=True)
    desc = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=255, blank=True)
    position = models.PositiveSmallIntegerField("Position")
    template = TemplateField(templates=TEMPLATES, max_length=200)
    data = ReactJSONSchemaField(template="template", blank=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        verbose_name_plural = "news"
        ordering = ["position"]

    def __str__(self):
        return self.title or "Sans titre"

    @property
    def published_at(self):
        return self.issue.published_at

    def _add_target_blank(self):
        self.data = apply_func_to_dict(
            self.data, self.get_html_data_fields(), add_target_blank_to_links
        )

    def get_typographie_data_fields(self):
        return self.TYPOGRAPHIE_DATA_FIELDS.get(self.template, [])

    def get_searchable_data_fields(self):
        return self.SEARCHABLE_DATA_FIELDS.get(self.template, [])

    def get_html_data_fields(self):
        return self.HTML_DATA_FIELDS.get(self.template, [])

    def save(self, *args, **kwargs):
        self._add_target_blank()
        super().save(*args, **kwargs)
