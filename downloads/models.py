class AccessFilePermissionMixin(object):
    """
    This mixin is here for all the models that store some files that need to be
    protected. It only defines the interface which each model should reimplement
    itself.
    """

    @classmethod
    def get_by_filepath(cls):
        """
        Returns the Model's instance that owns the file, or None if no such
        instance exists.
        """
        raise NotImplemented("Models inheriting from AccessFilePermissionMixin "
                             "need to reimplement get_by_filepath classmethod.")

    def can_access_files(self, user):
        """
        Implements the Model's custom logic that defines whether user can access
        files belonging to this particular instance.
        """

        raise NotImplemented("Models inheriting from AccessFilePermissionMixin "
                             "need to reimplement can_access_files method.")
