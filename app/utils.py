def extract(ancestor, selector=None, attribute=None, multiple=False):
    if selector:
        if multiple:
            return [tag[attribute].strip() if attribute else tag.text.strip()
                    for tag in ancestor.select(selector)]
        if attribute:
            try:
                return ancestor.select_one(selector)[attribute].strip()
            except:
                return None
        try:
            return ancestor.select_one(selector).text.strip()
        except:
            return None
    if attribute:
        return ancestor[attribute].strip()

selectors = {
    "opinion_id": (None, 'data-entry-id'),
    "author": ('span.user-post__author-name',),
    "recommendation": ('span.user-post__author-recomendation > em',),
    "stars": ('span.user-post__score-count',),
    "content": ('div.user-post__text',),
    "pros": ('div.review-feature__item--positive', None, True),
    "cons": ('div.review-feature__item--negative', None, True),
    "useful": ('button.vote-yes', 'data-total-vote'),
    "useless": ('button.vote-no', 'data-total-vote'),
    "post_date": ('span.user-post__published > time:nth-of-type(1)', 'datetime'),
    "purchase_date": ('span.user-post__published > time:nth-of-type(2)', 'datetime'),
}
