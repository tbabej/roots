# Based on wiki/core/permissions.py


def wiki_can_read(article, user):
    if not user.is_staff:
        return False
    else:
        # Deny reading access to deleted articles if user has no delete access
        article_is_deleted = (article.current_revision and
                              article.current_revision.deleted)
        if article_is_deleted and not article.can_delete(user):
            return False

        # Check access for other users...
        if user.is_anonymous():
            return False
        elif article.other_read:
            return True
        elif user.is_anonymous():
            return  False

        # Allow access for user owner / group owner
        if user == article.owner:
            return True
        if article.group_read:
            if (article.group and
                user.groups.filter(id=article.group.id).exists()):
                return True
        if article.can_moderate(user):
            return True

        return False