from django.db import models


class infinido(models.Model):
    title = models.CharField(max_length=90)
    content = models.TextField()
    parent = models.IntegerField(default=-1)
    is_deleted = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return "{} is parent of {} with title {}".format(
            self.parent, self.id, self.title
        )

