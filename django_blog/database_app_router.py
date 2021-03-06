from django.conf import settings


class DatabaseAppsRouter(object):
    def db_for_read(self, model, **hints):
        app_label = model._meta.app_label
        if app_label in settings.DATABASE_APPS_MAPPING:
            return settings.DATABASE_APPS_MAPPING[app_label]
        return None

    def db_for_write(self, model, **hints):
        app_label = model._meta.app_label
        if app_label in settings.DATABASE_APPS_MAPPING:
            return settings.DATABASE_APPS_MAPPING[app_label]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        db_obj1 = settings.DATABASE_APPS_MAPPING.get(obj1._meta.app_label)
        db_obj2 = settings.DATABASE_APPS_MAPPING.get(obj2._meta.app_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            return False
        return None

    def db_for_migrate(self, db, app_label, model_name=None, **hints):
        if db in settings.DATABASE_APPS_MAPPING.values():
            result = db == settings.DATABASE_APPS_MAPPING.get(app_label)
            return result
        elif app_label in settings.DATABASE_APPS_MAPPING:
            return False
        else:
            return None

















