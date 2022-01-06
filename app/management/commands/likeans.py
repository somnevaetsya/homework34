from django.core.management.base import BaseCommand
from random import choice
from app.models import Question, Tag, LikeToQue, LikeToAns, Profile, Answer
from django.contrib.auth.models import User
import time



class Command(BaseCommand):

    def handle(self, *args, **options):
        start_time = time.time()
        profiles = list(Profile.objects.values_list("id", flat=True))
        answers = list(Answer.objects.values_list("id", flat=True))
        for i in range(1010):
            like_to_ans_create = []
            for j in range(1000):
                curr_like = LikeToAns(like_ans=Answer.objects.get(id=choice(answers)),
                                      person_like_ans=Profile.objects.get(id=choice(profiles)))
                like_to_ans_create.append(curr_like)
            LikeToAns.objects.bulk_create(like_to_ans_create)
        print('finish like to ans')
        print("--- %s seconds ---" % (time.time() - start_time))
