from django.core.management.base import BaseCommand
from random import choice
from app.models import Question, Tag, LikeToQue, LikeToAns, Profile, Answer
from django.contrib.auth.models import User
import time



class Command(BaseCommand):

    def handle(self, *args, **options):
        start_time = time.time()
        questions_ids = list(Question.objects.values_list("id", flat=True))
        profiles = list(Profile.objects.values_list("id", flat=True))
        for i in range(1010):
            like_to_que_create = []
            for j in range(1000):
                curr_like = LikeToQue(like_que=Question.objects.get(id=choice(questions_ids)),
                                      person_like_que=Profile.objects.get(id=choice(profiles)))
                like_to_que_create.append(curr_like)
            LikeToQue.objects.bulk_create(like_to_que_create)
        print('finish like to que')
        print("--- %s seconds ---" % (time.time() - start_time))
