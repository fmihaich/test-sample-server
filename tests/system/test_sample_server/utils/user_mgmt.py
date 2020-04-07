from random import randint

DEFAULT_USER_ID = 'DEFAULT'


def get_user_from_context(context, user_id=DEFAULT_USER_ID):
    '''
    This method returns an existent user if user_id exists in context.users map.
    Otherwise, the method:
     - Creates a user with the provided parameters,
     - Stores the recent created user in context.users map, and
     - Returns the recent created user.
    '''

    if user_id in context.users:
        return context.users[user_id]

    context.users[user_id] = _generate_new_user()
    return context.users[user_id]


def _generate_new_user():
    username = 'user_{0}'.format(randint(0, 1000000))
    return {
        'username': username,
        'name': '{0}_name'.format(username),
        'surname': '{0}_surname'.format(username),
        'email': '{0}@somemail.com'.format(username),
        'birthday': '{m}/{d}/{y}'.format(m=randint(1,12), d=randint(1,28), y=randint(1950, 2010)),
        'address': '{0} St'.format(username)
    }
