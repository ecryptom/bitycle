from django.db import models
import json


class indicator(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    interval = models.CharField(max_length=3, choices=(('1m','1m'), ('5m','5m'), ('1h','1h'), ('4h','4h'), ('1d', '1d'), ('1w','1w')))
    setup = models.TextField()
    lines = models.TextField()

    def get_setup(self):
        return json.loads(self.setup)

    def get_lines(self):
        return json.loads(self.lines)


