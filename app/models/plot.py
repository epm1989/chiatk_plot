from enum import Enum

from tortoise.models import Model
from tortoise import fields


class StatusType(str, Enum):
    OPEN = 'OPEN'
    COMPLETED = 'COMPLETED'
    DELETED = 'DELETED'

class StatusQueueType(str, Enum):
    WAITING = 'WAITING'
    RUNNING = 'RUNNING'
    PROCESSED = 'PROCESSED'


class Queue(Model):
    id = fields.UUIDField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    status = fields.CharEnumField(StatusQueueType, default=StatusQueueType.WAITING)
    command = fields.CharField(max_length=1024)
    plot = fields.OneToOneField('models.Plot', related_name='queue', null=True)

    def __str__(self):
        return self.id


class Plot(Model):

    id = fields.UUIDField(pk=True)
    pid = fields.CharField(max_length=255)
    plot_id = fields.CharField(null=True, max_length=255)
    t = fields.CharField(max_length=255)
    d = fields.CharField(max_length=255)
    r = fields.CharField(max_length=255)
    u = fields.CharField(max_length=255)
    f = fields.CharField(max_length=255)
    p = fields.CharField(max_length=255)
    k = fields.CharField(max_length=255)
    b = fields.CharField(max_length=255)
    log_file = fields.CharField(null=True, max_length=255)
    phase = fields.CharField(null=True, max_length=2)
    progress = fields.CharField(null=True, max_length=10)
    temp_size = fields.CharField(null=True, max_length=10)
    status = fields.CharEnumField(StatusType, default=StatusType.OPEN)
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(null=True)

    def __str__(self):
        return self.id
