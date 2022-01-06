from django.db.models import Count

from app.models import Answer, LikeToAns, LikeToQue, Tag, Question, Profile


def base_content(request):
    base = {'profiles': Profile.objects.annotate(count=Count('answer')).order_by("-count")[:10],
            'tags': Tag.objects.annotate(count=Count('question')).order_by("-count")[:10]}
    return base
