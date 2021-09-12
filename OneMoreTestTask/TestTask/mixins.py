from .models import Deal, DealStatus, DealStage
from django.db.models import Max
from datetime import datetime, timedelta


class IndexPageViewMixin:
    """A class that serves to separate logic and view"""

    @staticmethod
    def get_deals_by_date_range(date_from, date_to):
        return Deal.objects.filter(status__estimated_date__range=[date_from, date_to])

    @staticmethod
    def filter_deals_by_stages(deals, stages):
        return deals.filter(status__deal_stage__in=stages)

    @staticmethod
    def set_order(deals):
        return deals.order_by('-status__deal_stage__probability', '-status__estimated_date')

    @staticmethod
    def get_deals_info(deals):
        """Deals info structure: [{}, {}, {}]. Dictionary for each deal"""

        deals_info = []

        for deal in deals:
            max_created_at = \
                DealStatus.objects.filter(deal=deal).aggregate(Max('created_at'))['created_at__max']
            deal_status = DealStatus.objects.get(deal=deal, created_at=max_created_at)

            deals_info.append({
                'deal_name': deal.name,
                'company_name': deal.contact.company,
                'contact_fullname': str(deal.contact),
                'amount': deal_status.amount,
                'currency': deal_status.currency,
                'deal_stage': deal_status.deal_stage,
                'estimated_date': deal_status.estimated_date,
                'created_at': deal_status.created_at.strftime("%Y-%m-%d %H:%M"),
            })

        return deals_info

    @staticmethod
    def get_currencies_info(deals_info):
        """
        Currencies info structure:
        {
            'RUB': [{}, {}, {}],
            'USD': [...],
            'EUR': [...]
        }
        Lists of dictionaries for each currency. Each dict in lists for one deal
        """
        currencies_info = {
            'RUB': [],
            'USD': [],
            'EUR': []
        }

        for currency in currencies_info:
            for deal in deals_info:
                if deal['currency'] == currency:
                    currencies_info[currency].append({
                        'deal_stage_name': deal['deal_stage'].name,
                        'deal_stage_probability': deal['deal_stage'].probability,
                        'amount': deal['amount']
                    })

        return currencies_info

    @classmethod
    def get_detailed_info(cls, request):
        deals = cls.get_deals_by_date_range(request.POST['date_from'], request.POST['date_to'])
        deals = cls.filter_deals_by_stages(deals, request.POST.getlist('deal_stages'))
        deals = cls.set_order(deals)
        deals_info = cls.get_deals_info(deals)
        currencies_info = cls.get_currencies_info(deals_info)

        return deals_info, currencies_info


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
