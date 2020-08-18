from django.db import models

class Counter(models.Model):
    count = models.BigIntegerField(default=0)
    def inc(self):
        self.count = self.count + 1
        self.save()
