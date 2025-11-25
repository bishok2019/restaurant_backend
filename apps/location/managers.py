from django.db import models


class LocationManager(models.Manager):
    def get_deliverable_locations(self):
        return self.filter(is_deliverable=True)

    def get_active_locations(self):
        return self.filter(is_active=True)

    def get_active_deliverable_locations(self):
        return self.filter(is_active=True, is_deliverable=True)
