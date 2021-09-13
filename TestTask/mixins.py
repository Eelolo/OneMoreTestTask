from .models import Deal, DealStatus, DealStage, Contact
from django.db.models import Max, Prefetch
from datetime import datetime, timedelta


class IndexPageViewMixin:
    """A class that serves to separate logic and view"""

    @staticmethod
    def get_deals_statuses(date_from, date_to, stages):
        deals = Deal.objects.all().prefetch_related(Prefetch('contact', queryset=Contact.objects.all().prefetch_related('company')))

        deal_statuses = DealStatus.objects\
            .prefetch_related(Prefetch('deal', queryset=deals))\
            .prefetch_related(Prefetch('deal_stage'))\
            .filter(estimated_date__range=[date_from, date_to])\
            .filter(deal_stage__in=stages)\
            .order_by('-created_at', '-deal_stage__probability', '-estimated_date')

        return deal_statuses

    @staticmethod
    def get_deals_info(deal_statuses):
        """Deals info structure: [{}, {}, {}]. Dictionary for each deal"""

        deals_info = []
        for deal_status in deal_statuses:
            deal = deal_status.deal

            # TODO: fix aggregation to avoid deals duplication
            if any([True for info in deals_info if info['deal_id'] == deal.id]):
                continue

            deals_info.append({
                'deal_id': deal.id,
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
        deal_statuses = cls.get_deals_statuses(
            request.POST['date_from'], request.POST['date_to'], request.POST.getlist('deal_stages')
        )
        deals_info = cls.get_deals_info(deal_statuses)
        currencies_info = cls.get_currencies_info(deals_info)

        return deals_info, currencies_info


class FilterFormMixin:
    """A class that serves to separate the form and the logic for its customization"""

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
