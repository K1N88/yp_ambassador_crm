from rest_framework import serializers

from ambassadors.models import Ambassadors, Content


class AmbassadorsSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели Амбассадоров'''

    class Meta:
        model = Ambassadors
        fields = ('id', 'reg_date')


class ContentSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели "Контент" запросов POST PUT DEL.'''

    class Meta:
        model = Content
        # fields = ('content_type',)


class ContentListSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели "Контент" запроса GET(list).'''

    class Meta:
        model = Content
        # fields = ('full_name', 'telegram_handle', 'content_types',)


# {
#   [
#     {
#       "full_name": "Пупкин Василий Васильевич",
#       "telegram_handle": "vasya_pupkin",
#       "content_types": [
#         {
#           "title": "Первый отзыв",
#           "status": "Выполнен",
#           "content": [
#               {
#                   "link": "t.me/123"
#               }
#           ]
#         },
#         {
#           "title": "Гайд",
#           "status": "Выполнен",
#           "content": [
#               {
#                   "link": "t.me/123"
#               },
#               {
#                   "link": "t.me/123"
#               },
#               {
#                   "link": "t.me/123"
#               },
#               {
#                   "link": "t.me/123"
#               },
#           ]
#         },
#       ],

#     }
#   ]
# }