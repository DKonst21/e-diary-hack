import random

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Subject, Commendation


def get_child(schoolkid_name):
    try:
        child = Schoolkid.objects.filter(full_name__contains=schoolkid_name).first()
    except ObjectDoesNotExist:
        print('Does Not Exist!')
    except MultipleObjectsReturned:
        schoolkids = []
        schoolkid_objects = Schoolkid.objects.filter(full_name__contains=schoolkid_name)
        for schoolkid_object in schoolkid_objects:
            schoolkids.append(schoolkid_object.full_name)
        print(f'More then one schoolkid found: {schoolkids}')
        return False
    return child


def fix_marks(schoolkid_name):
    if get_child(schoolkid_name):
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        schoolkid_bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
        for bad_mark in schoolkid_bad_marks:
            bad_mark.points = 5
            bad_mark.save()


def remove_chastisements(schoolkid_name):
    if get_child(schoolkid_name):
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        child_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
        child_chastisements.delete()


def create_commendation(schoolkid_name, subject):
    if get_child(schoolkid_name):
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        commendations = [' Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
                         'Великолепно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
                         'Сказано здорово – просто и ясно!', 'Прекрасно!', 'Ты, как всегда, точен!',
                         'Очень хороший ответ!', 'Талантливо!Молодец!', 'Ты сегодня прыгнул выше головы!',
                         'Я поражен!', 'Замечательно!']
        year_of_study = schoolkid.year_of_study
        group_letter = schoolkid.group_letter
        try:
            subject_object = Subject.objects.filter(title=subject, year_of_study=year_of_study)
            if not subject_object:
                raise ObjectDoesNotExist
            subject = subject_object[0]
            subject_lessons = Lesson.objects.filter(year_of_study=year_of_study, group_letter=group_letter,
                                                    subject=subject)
            last_lesson = subject_lessons.order_by('date').last()
            commendation_text = random.choice(commendations)
            Commendation.objects.create(text=commendation_text, created=last_lesson.date, schoolkid=schoolkid,
                                        subject=subject, teacher=last_lesson.teacher)
        except ObjectDoesNotExist:
            print(f'No subject found')
