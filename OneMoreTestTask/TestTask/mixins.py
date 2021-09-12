from .models import DealStage


class FilterFormTools:
    """A class that serves as a set of methods for customizing the form"""

    @staticmethod
    def get_deals_stages():
        stages = []
        for stage in DealStage.objects.all().order_by('probability'):
            stages.append((stage.id, f'{stage.name} {str(stage.probability)}%'))

        return stages
