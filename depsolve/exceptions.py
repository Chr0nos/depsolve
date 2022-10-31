
class DependencyException(Exception):
    pass


class CirclularDependencyException(DependencyException):
    pass


class UnknowDependencyException(DependencyException):
    pass
