from django.core.management.base import BaseCommand
from random import choice
from app.models import Question, Tag, LikeToQue, LikeToAns, Profile, Answer
from django.contrib.auth.models import User
import time



class Command(BaseCommand):

    def handle(self, *args, **options):
        start_time = time.time()
        tag_create = [Tag(tag_title=f"Tag #{i}") for i in range(15000)]
        Tag.objects.bulk_create(tag_create)
        print('finish tags')

        counter = 0
        for i in range(100):
            profiles_create = []
            for j in range (110):
                user_create = User.objects.create(username=f"username#{counter}",)
                profiles_create.append(Profile(user=user_create))
                counter += 1
            Profile.objects.bulk_create(profiles_create)
        print('finish profiles')
        print("--- %s seconds ---" % (time.time() - start_time))
        profiles = list(Profile.objects.values_list("id", flat=True))

        que_create = [Question(title=f"title #{i}", text_que=f"text for que{i}", author=Profile.objects.get(id=choice(profiles))) for i in range(100000)]
        print('finish que pre')
        Question.objects.bulk_create(que_create)
        questions_ids = Question.objects.values_list("id", flat=True)
        tags_ids = Tag.objects.values_list('id', flat=True)
        tag_questions_rels = []
        for questions_id in questions_ids:
            tag_1_id = choice(tags_ids)
            tag_2_id = choice(tags_ids)
            while tag_2_id == tag_1_id:
                tag_2_id = choice(tags_ids)
            tag_questions_rels.append(Question.tag.through(tag_id=tag_1_id,  question_id=questions_id))
            tag_questions_rels.append(Question.tag.through(tag_id=tag_2_id, question_id=questions_id))
        Question.tag.through.objects.bulk_create(tag_questions_rels)
        print('finish que fin')
        # for i in range(1, 101):
        #     quesi = Question.objects.get(id=i)
        #     quesi.tag.add(Tag.objects.get(id=choice(tags)))
        #     # quesi.save()
        #     if i % 100 == 0:
        #         print(i)


