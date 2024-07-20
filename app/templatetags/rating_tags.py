from django import template

register = template.Library()

@register.filter
def stars(rating):
    emoji = "😠"
    full_stars = rating // 2
    if full_stars >= 3:
        emoji = "🔥"
    elif full_stars > 2:
        emoji = "❤️"
    elif full_stars > 0:
        emoji = "🙂"
    elif full_stars > -2:
        emoji = "😒"
    else:
        emoji = "😠"
    return emoji
