from django.contrib import admin

from .models import Merchandise, Talk, Comment, Request, Inquiry, Announce, OpenComment, DefaultCard, Report


class MerchandiseAdmin(admin.ModelAdmin):
    search_fields = ('merchandise_name',)
    list_display = ('id', 'merchandise_name', 'user', 'value')
    list_filter = ('merchandise_name', 'user', 'value')


class TalkAdmin(admin.ModelAdmin):
    search_fields = ('merchandise__merchandise_name', 'talk_seller__username')
    list_display = ('id', 'merchandise', 'talk_buyer', 'talk_seller', 'refund_request_status')
    list_filter = ('merchandise', 'talk_buyer', 'talk_seller')


class CommentAdmin(admin.ModelAdmin):
    search_fields = ('talk__id',)
    list_display = ('id', 'talk', 'merchandise', 'user', 'comment', 'created_at')
    list_filter = ('merchandise', 'talk')


class InquiryAdmin(admin.ModelAdmin):
    search_fields = ('name', 'email', 'content')
    list_display = ('id', 'name', 'email', 'content')
    list_filter = ('name', 'email', 'content')


class AnnounceAdmin(admin.ModelAdmin):
    search_fields = ('title', 'content', 'deleted')
    list_display = ('id', 'title', 'content', 'deleted')
    list_filter = ('title', 'content', 'deleted')


class DefaultCardAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'user__email', 'default_card_status')
    list_display = ('id', 'user', 'default_card_status')
    list_filter = ('user', 'default_card_status')


class ReportAdmin(admin.ModelAdmin):
    search_fields = ('reporter__username', 'reporter__email', 'reported_user__username', 'reported_user__email', 'content')
    list_display = ('id', 'reporter', 'reported_user', 'content')
    list_filter = ('reporter', 'reported_user', 'content')


admin.site.register(Merchandise, MerchandiseAdmin)
admin.site.register(Talk, TalkAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Request)
admin.site.register(Inquiry, InquiryAdmin)
admin.site.register(Announce, AnnounceAdmin)
admin.site.register(OpenComment)
admin.site.register(DefaultCard, DefaultCardAdmin)
admin.site.register(Report, ReportAdmin)