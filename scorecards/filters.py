import django_filters

from scorecards.models import Scorecard


class ScorecardFilter(django_filters.FilterSet):

    class Meta:
        model = Scorecard
        fields = ['active', 'year', 'approved', 'user__userprofile__position',
                  'user__userprofile__position__department']
