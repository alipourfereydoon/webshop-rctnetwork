from django.db import models
from django.utils import timezone

class SiteStatistics(models.Model):
    total= models.IntegerField(default=0)
    last_visit_date = models.DateField(null=True, blank=True)
    daily_visits = models.IntegerField(default=0)
    last_week_start = models.DateField(null=True, blank=True)
    weekly_visits = models.IntegerField(default=0)



    def __str__(self):
        return f" {self.total}"