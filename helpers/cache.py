from helpers.sql import get_admins, get_ban_list, user_count
from helpers.log import log


# TODO: Добавить логгирование в методы класса Cache
class Cache:
    def __init__(self, is_get_data=True):
        self.admins_list = []
        self.users_ban_list = []
        self.users_count = 0
        self.isClear = True
        self.isUpdate = False
        self.logger = log('Cache', 'cache.log', 'INFO')
        if is_get_data:
            self.get_data()

    def get_data(self):
        self.admins_list = get_admins()
        self.users_ban_list = get_ban_list()
        self.users_count = user_count()
        self.isClear = False

    def user_count(self):
        if self.isClear and not self.isUpdate:
            self.get_data()
        return self.users_count

    def get_ban_list(self):
        if self.isClear and not self.isUpdate:
            self.get_data()
        return self.users_ban_list

    def get_admins(self):
        if self.isClear and not self.isUpdate:
            self.get_data()
        return self.admins_list

    def update_user_count(self):
        if self.isUpdate:
            return
        if self.isClear:
            self.get_data()
            return
        self.users_count = user_count()

    def update_admins_list(self):
        if self.isUpdate:
            return
        if self.isClear:
            self.get_data()
            return
        self.admins_list = get_admins()

    def update_user_ban_list(self):
        if self.isUpdate:
            return
        if self.isClear:
            self.get_data()
            return
        self.users_ban_list = get_ban_list()

    def clear_data(self):
        self.admins_list = []
        self.users_ban_list = []
        self.users_count = 0
        self.isClear = True

    def update_cache(self):
        self.clear_data()
        self.get_data()
