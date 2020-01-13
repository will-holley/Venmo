from utils import string_to_timestamp

"""
This class will be only the model for User.
All the routes will be defined in the /apis/user_api.py

"""


class User:

    @classmethod
    def init(cls, user_id, username, first_name, last_name, display_name, profile_picture_url,
             about, date_joined, is_group, is_active, crawler_type):
        """
        Initialize a new User
        :param user_id:
        :param username:
        :param first_name:
        :param last_name:
        :param display_name:
        :param profile_picture_url:
        :param about:
        :param date_joined:
        :param is_group:
        :param is_active:
        :param crawler_type: CrawlwerType
        :return:
        """
        self.id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.display_name = display_name
        self.profile_picture_url = profile_picture_url
        self.about = about
        self.date_joined = date_joined
        self.is_group = is_group
        self.is_active = is_active
        self.crawler_type = crawler_type

    @classmethod
    def from_json(cls, json, is_profile=False, crawler_type=CrawlerType.IOS_API):
        """
        Init a new user in DB
        :param json:
        :param is_profile:
        :param crawler_type: CrawlerType
        :return:
        """
        parser = UserJson(json, is_profile=is_profile)
        date_joined_timestamp = string_to_timestamp(parser.get_date_created())

        return cls(user_id=parser.get_user_id(),
                   username=parser.get_username(),
                   first_name=parser.get_first_name(),
                   last_name=parser.get_last_name(),
                   display_name=parser.get_full_name(),
                   profile_picture_url=parser.get_picture_url(),
                   about=parser.get_about(),
                   date_joined=date_joined_timestamp,
                   is_group=parser.get_is_group(),
                   is_active=parser.get_is_active(),
                   crawler_type=crawler_type)

    @classmethod
    def create_or_get_json(cls, json):
        parser = UserJson(json)
        uid = parser.get_user_id()
        try:
            return User.get(User.id == uid)

        except User.DoesNotExist:
            user = cls.from_json(json=json)
            return user

    def __str__(self):
        return f'id: {self.id}, username: {self.username}, firstname: {self.first_name}, lastname: {self.last_name}' +\
            f' display_name: {self.display_name}, picture: {self.profile_picture_url}, about: {self.about},' \
            f' joined: {self.date_joined}, is_group: {self.is_group}, is_active: {self.is_active}'


class UserJson:

    def __init__(self, json, is_profile=False):
        self.json = json
        self.is_profile = is_profile

        if is_profile:
            self.parser = profile_json_format
        else:
            self.parser = user_json_format

    def get_user_id(self):
        return self.json[self.parser.get('user_id')]

    def get_username(self):
        return self.json[self.parser.get('username')]

    def get_first_name(self):
        return self.json[self.parser.get('first_name')]

    def get_last_name(self):
        return self.json[self.parser.get('last_name')]

    def get_full_name(self):
        return self.json[self.parser.get('full_name')]

    def get_picture_url(self):
        return self.json[self.parser.get('picture_url')]

    def get_about(self):
        return self.json[self.parser.get('about')]

    def get_date_created(self):
        return self.json[self.parser.get('date_created')]

    def get_is_group(self):
        if self.is_profile:
            return False
        return self.json[self.parser.get('is_group')]

    def get_is_active(self):
        if self.is_profile:
            return False
        return self.json[self.parser.get('is_active')]


user_json_format = {
    'user_id': 'id',
    'username': 'username',
    'first_name': 'first_name',
    'last_name': 'last_name',
    'full_name': 'display_name',
    'picture_url': 'profile_picture_url',
    'about': 'about',
    'date_created': 'date_joined',
    'is_group': 'is_group',
    'is_active': 'is_active'
}

profile_json_format = {
    'user_id': 'external_id',
    'username': 'username',
    'first_name': 'firstname',
    'last_name': 'lastname',
    'full_name': 'name',
    'picture_url': 'picture',
    'about': 'about',
    'date_created': 'date_created',
    'is_business': 'is_business'
}
