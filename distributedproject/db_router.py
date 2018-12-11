import random


class PrimaryReplicaRouter(object):
    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen replica.
        """
        db = random.choice(['primary', 'replica'])
        print("reading", db)
        return db

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        print("writing")
        return 'primary'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """

        return True
        # db_list = ('primary', 'replica1', 'replica2')
        # if obj1._state.db in db_list and obj2._state.db in db_list:
        #     return True
        # return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return True
