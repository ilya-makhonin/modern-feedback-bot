from helpers.sql import get_admins, get_ban_list, user_count
from helpers.log import log


class Cache:
    def __init__(self, is_get_data: bool = True):
        self.admins_list: list = []
        self.users_ban_list: list = []
        self.users_count: int = 0
        self.isClear: bool = True
        self.isUpdate: bool = False
        self.data: dict = {}
        self.logger = log('Cache', 'cache.log', 'INFO')
        if is_get_data:
            self.get_data()

    def get_data(self):
        self.admins_list = get_admins()
        self.users_ban_list = get_ban_list()
        self.users_count = user_count()
        self.isClear = False
        self.data = {
            'admins_list': self.admins_list,
            'users_ban_list': self.users_ban_list,
            'user_count': self.users_count
        }
        self.logger.info('Cache data has been download')

    def user_count(self) -> int:
        if self.isUpdate:
            self.logger.info('Cache is updating now! Return USER COUNT from self.data prop')
            return self.data['user_count']
        if self.isClear:
            self.logger.info('From user_count method. Cache is clear! Download data from DataBase')
            self.get_data()
        self.logger.info('Return USER COUNT from cache')
        return self.users_count

    def get_ban_list(self) -> list:
        if self.isUpdate:
            self.logger.info('Cache is updating now! Return BAN LIST from data prop')
            return self.data['users_ban_list']
        if self.isClear:
            self.logger.info('From get_ban_list method. Cache is clear! Download data from DataBase')
            self.get_data()
        self.logger.info('Return BAN LIST from cache')
        return self.users_ban_list

    def get_admins(self) -> list:
        if self.isUpdate:
            self.logger.info('Cache is updating now! Return ADMINS LIST from data prop')
            return self.data['admins_list']
        if self.isClear:
            self.logger.info('From get_admins method. Cache is clear! Download data from DataBase')
            self.get_data()
        self.logger.info('Return ADMINS LIST from cache')
        return self.admins_list

    def update_user_count(self):
        if self.isUpdate:
            self.logger.info('Cache is updating! Updating USER COUNT prop was canceled')
            return
        if self.isClear:
            self.get_data()
            self.logger.info('From update_user_count method. Cache was cleared! Download data from DataBase')
            return
        self.users_count = user_count()
        self.logger.info('Updating USER COUNT has been success')

    def update_admins_list(self):
        if self.isUpdate:
            self.logger.info('Cache is updating! Updating ADMINS LIST prop was canceled')
            return
        if self.isClear:
            self.get_data()
            self.logger.info('From update_admins_list method. Cache was cleared! Download data from DataBase')
            return
        self.admins_list = get_admins()
        self.logger.info('Updating ADMINS LIST prop has been success')

    def update_user_ban_list(self, new_data: list):
        if self.isUpdate:
            self.logger.info('Cache is updating! Updating BAN LIST prop was canceled')
            return
        if new_data:
            self.users_ban_list = new_data
            self.logger.info('From update_user_ban_list method. New data has been gotten')
            return
        if self.isClear:
            self.get_data()
            self.logger.info('From update_user_ban_list method. Cache was cleared! Download data from DataBase')
            return
        self.users_ban_list = get_ban_list()
        self.logger.info('Updating USERS BAN LIST prop has been success')

    def clear_data(self):
        self.admins_list = []
        self.users_ban_list = []
        self.users_count = 0
        self.isClear = True
        self.logger.info('Cache data has been deleted')

    def update_cache(self):
        self.clear_data()
        self.get_data()
        self.logger.info('Cache has been updated')
