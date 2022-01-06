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
        counter = 0
        for i in range(1010):
            ans_create = []
            for j in range(1000):
                curr_ans = Answer(text_ans=f"text for ans{counter}", author=Profile.objects.get(id=choice(profiles)),
                                  que=Question.objects.get(id=choice(questions_ids)))
                ans_create.append(curr_ans)
                counter += 1
            Answer.objects.bulk_create(ans_create)
        print('finish answers')
        print("--- %s seconds ---" % (time.time() - start_time))
