import argparse
import os
import random
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from datacenter.models import (Chastisement, Commendation, Lesson, Mark, Schoolkid, Subject)


def get_child(child):
    kid = Schoolkid.objects.get(full_name__contains=child)
    return kid


def find_subject(subject, child):
    subjects = Subject.objects.get(title=subject, year_of_study=child.year_of_study)
    return subjects


def fix_marks(child):
    marks_kid = Mark.objects.filter(schoolkid=child, points__lt=4)
    marks_kid.update(points=5)


def remove_chastisements(child):
    chastisements = Chastisement.objects.filter(schoolkid=child)
    chastisements.delete()


def create_commendation(child, subjects):
    last_lesson = Lesson.objects.filter(year_of_study=child.year_of_study,
                                        group_letter=child.group_letter,
                                        subject=subjects,
                                        ).last()
    Commendation.objects.create(text=random.choice(commendations),
                                created=last_lesson.date,
                                schoolkid=child,
                                subject=subjects,
                                teacher=last_lesson.teacher,
                                )


def parse_user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('schoolkid_surname_name', help='Please type name and surname',)
    parser.add_argument('-s', '--subject', action='store', help='Subject for commendation')
    args = parser.parse_args()
    if args.subject and args.schoolkid_surname_name:
        user_input = dict(schoolkid=args.schoolkid_surname_name, subject=args.subject)
        return user_input
    else:
        user_input = dict(schoolkid=' '.join(args.schoolkid_surname_name))
        return user_input
    return args


if __name__ == '__main__':
    commendations = [' Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
                     'Великолепно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
                     'Сказано здорово – просто и ясно!', 'Прекрасно!', 'Ты, как всегда, точен!',
                     'Очень хороший ответ!', 'Талантливо!Молодец!', 'Ты сегодня прыгнул выше головы!',
                     'Я поражен!', 'Замечательно!']
    input_schoolkid_subject = parse_user_input()
    schoolkid_surname_name = input_schoolkid_subject.schoolkid_surname_name
    try:
        input_schoolkid_subject = parse_user_input()
        schoolkid = input_schoolkid_subject['schoolkid']
    except SystemExit:
        print('Программа завершила работу неправильно, проверьте задаваемые атрибуты')
        exit()
    try:
        fix_marks(get_child(schoolkid))
        schoolkid = get_child(schoolkid_surname_name)
        fix_marks(schoolkid)
        print('Ученик найден')
        print('Оценки исправлены')
        remove_chastisements(get_child(schoolkid))
        remove_chastisements(schoolkid)
        print('Замечания удалены')
        try:
            if input_schoolkid_subject.subject:
                subject = input_schoolkid_subject.subject
                create_commendation(schoolkid, find_subject(subject, schoolkid))
            print('Благодарность присвоена')
        except Subject.DoesNotExist:
            print('Предмет не найден. Пожалуйста проверьте название предмета.'
                  f'Название предмета {subject} некорректно. Для поиска необходимо'
                  'использовать корректное название.'.format(subject=subject))
        except Subject.MultipleObjectsReturned:
            print('Найдено несколько предметов по данному запросу.'
                  'Пожалуйста проверьте название предмета. Название'
                  f'предмета {subject} некорректно. Для поиска необходимо '
                  'использовать корректное название.'.format(subject=subject))
    except Schoolkid.DoesNotExist:
        print('Ученик не найден. '
              f'Пожалуйста проверьте имя ученика. Имя {schoolkid} некорректно. '
              'Для поиска необходимо использовать как имя, '
              'так и фамилию ученика.'.format(schoolkid=schoolkid),
              'так и фамилию ученика.'.format(schoolkid=schoolkid_surname_name))
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько учеников по данному запросу. '
              f'Пожалуйста проверьте имя ученика. Имя {schoolkid} некорректно.'
              'Для поиска необходимо использовать как имя, так и фамилию'
              'ученика.'.format(schoolkid=schoolkid))
    try:
        if input_schoolkid_subject.get('subject'):
            subject = input_schoolkid_subject['subject']
            create_commendation(get_child(schoolkid), find_subject(subject, get_child(schoolkid)))
            print('Благодарность присвоена')
    except Subject.DoesNotExist:
        print('Предмет не найден. Пожалуйста проверьте название предмета.'
              f'Название предмета {subject} некорректно. Для поиска необходимо'
              'использовать корректное название.'.format(subject=subject))
    except Subject.MultipleObjectsReturned:
        print('Найдено несколько предметов по данному запросу.'
              'Пожалуйста проверьте название предмета. Название'
              f'предмета {subject} некорректно. Для поиска необходимо '
              'использовать корректное название.'.format(subject=subject),
              'ученика.'.format(schoolkid=schoolkid_surname_name))
