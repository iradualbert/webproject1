from django.contrib import admin
from .models import Channel, Topic, ProductService, Question, Answer, RateReview, TopicRateReview, Subscriber, ChannelAdmin

admin.site.register(Channel)
admin.site.register(Topic)
admin.site.register(ProductService)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(RateReview)
admin.site.register(TopicRateReview)
admin.site.register(Subscriber)
admin.site.register(ChannelAdmin)
