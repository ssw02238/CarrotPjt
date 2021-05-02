from django import template


register = template.Library()


@register.filter 
def hashtag_link(word):
    content = word.content + ' '
    hashtags = word.hashtags.all()
    
    for hashtag in hashtags:
        content = content.replace(hashtag.content + ' ', f'<a style="color:#3760EF" href="/articles/{hashtag.pk}/hashtag/">{hashtag.content}</a> ')	# 마지막 공백 있음!

    return content