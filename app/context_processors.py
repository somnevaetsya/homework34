from app.models import Answer, LikeToAns, LikeToQue, Tag, Question, Profile


def base_content(request):
    base = {'profiles': Profile.objects.best_profiles(),
            'tags': Tag.objects.hot_tags()}
    return base
