import uuid
import json
from django.db import models

# Create your models here.
class ListenerLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        timestamp = self.created_at.strftime('%m/%d/%y %H:%M:%S')
        if self.webhook_name and self.webhook_id:
            return f'{timestamp} - {self.webhook_name}'
        else:
            return f'{timestamp} - <Non Conforming>'

    @property
    def payload(self):
        try:
            return json.loads(self.data)
        except Exception:
            return {}

    @property
    def webhook_id(self):
        return self.payload.get('webhookId')

    @property
    def webhook_name(self):
        return self.payload.get('webhookName')