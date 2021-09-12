from .models import DealStage
from datetime import datetime, timedelta


class FilterFormTools:
    """A class that serves as a set of methods for customizing the form"""

    @staticmethod
    def get_quarter(date):
        return (date.month - 1) // 3 + 1

    @staticmethod
    def get_default_date_from(date):
        return datetime(date.year, 3 * ((date.month - 1) // 3) + 1, 1)

    @classmethod
    def get_default_date_to(cls, date):
        quarter = cls.get_quarter(date)
        return datetime(
            date.year + 3 * quarter // 12, 3 * quarter % 12 + 1, 1
        ) + timedelta(days=-1)

    @staticmethod
    def get_deals_stages():
        stages = []
        for stage in DealStage.objects.all().order_by('probability'):
            stages.append((stage.id, f'{stage.name} {str(stage.probability)}%'))

        return stages

    @staticmethod
    def get_default_deals_stages():
        return [stage.id for stage in DealStage.objects.all().filter(probability__gte=30)]
