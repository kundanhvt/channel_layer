from django.db import models

class Chat(models.Model):
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='group_chat')


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

    @property
    def has_group(self):
        return hasattr(self,'group_chat')

