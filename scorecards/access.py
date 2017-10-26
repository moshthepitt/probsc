from .models import Scorecard


def can_access_scorecard(this_object, user):
    """
    Determine whether the user has rights to access the
    scorecard
    """
    subordinates = user.userprofile.get_subordinates()
    can_access = False
    if user.userprofile.can_edit():
        can_access = True
    elif (hasattr(this_object, 'user')) and\
         (this_object.user.userprofile in subordinates):
        can_access = True
    else:
        if isinstance(this_object, Scorecard):
            if this_object.user == user:
                can_access = True
        else:
            if (hasattr(this_object, 'scorecard')) and\
               (this_object.scorecard.user == user):
                can_access = True
    return can_access
