class ConventionViolationError(Exception):
    pass


class SQLError(Exception):
    pass


class CustomSQLBuildError(SQLError):
    pass
