from datetime import date

from django.db import models


class IssueManager(models.Manager):
    def get_today_pending_issues(self):
        today = date.today()
        issues = self.filter(status=self.model.STATUS.pending, created__contains=today)

        return issues

    def import_from_archieml(self, data):
        raise NotImplementedError
