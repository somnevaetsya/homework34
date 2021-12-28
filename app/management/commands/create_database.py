from django.core.management.base import BaseCommand
from random import choice
from app.models import Question, Tag, LikeToQue, LikeToAns, Profile, Answer
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        tag_create = [Tag(tag_title=f"Tag #{i}", rating=i) for i in range(12000)]
        Tag.objects.bulk_create(tag_create)
        tags = list(Tag.objects.values_list("id", flat=True))
        user_create = [User.objects.create(username=f"username#{i}",) for i in range(100)]
        profile_create = [Profile(user=user_create[i]) for i in range(100)]
        Profile.objects.bulk_create(profile_create)
        profiles = list(Profile.objects.values_list("id", flat=True))

        # questions_tags_links = []
        # for i in range(120000):
        #     question_tag_rel = Question.tag.through(question_id=i, tag_id=choice(tags))
        #     questions_tags_links.append(question_tag_rel)
        # print(type(question_tag_rel))
        # Question.tag.add(tags)
        que_create = [Question(title=f"title #{i}", text_que=f"text for que{i}", person_que=Profile.objects.get(id=choice(profiles))) for i in range(1000)]
        Question.objects.bulk_create(que_create)
        for i in range(1, 1001):
            quesi = Question.objects.get(id=i)
            quesi.tag.add(Tag.objects.get(id=choice(tags)))
            # quesi.save()
            if i % 100 == 0:
                print(i)

        questions = list(Question.objects.values_list("id", flat=True))

        ans_create = [Answer(text_ans=f"text for ans{i}", person_ans=Profile.objects.get(id=choice(profiles)), que=Question.objects.get(id=choice(questions))) for i in range(10000)]
        Answer.objects.bulk_create(ans_create)
        answers = list(Answer.objects.values_list("id", flat=True))

        like_to_ans = [LikeToAns(like_ans=Answer.objects.get(id=choice(answers)), person_like_ans=Profile.objects.get(id=choice(profiles))) for i in range(10000)]
        LikeToAns.objects.bulk_create(like_to_ans)

        like_to_que = [LikeToQue(like_que=Question.objects.get(id=choice(questions)), person_like_que=Profile.objects.get(id=choice(profiles))) for i in range(10000)]
        LikeToQue.objects.bulk_create(like_to_que)