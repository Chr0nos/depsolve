from pydantic import BaseModel, validator
from typing import Literal


class Dependency(BaseModel):
    name: str
    depends_on: set[str] = {}

    def __hash__(self):
        return self.name.__hash__()

    @validator('depends_on', pre=True)
    def convert_depends_to_set(cls, depends_on_raw):
        if isinstance(depends_on_raw, list):
            return set(depends_on_raw)
        return depends_on_raw


class DependencyException(Exception):
    pass


class CirclularDependencyException(DependencyException):
    pass


class UnknowDependencyException(DependencyException):
    pass


Mapping = dict[
    str,
    dict[Literal['deps', 'subs', 'instance'], list[str] | Dependency]
]


def to_flat_mapping(dependencies: list[Dependency]) -> Mapping:
    deps_by_name = dict({
        dep.name: {
            'deps': dep.depends_on.copy() or [],
            'subs': [],
            'instance': dep
        } for dep in dependencies
    })
    for dep in dependencies:
        for other in dep.depends_on:
            try:
                deps_by_name[other]['subs'] += dep.name
            except KeyError as error:
                raise UnknowDependencyException(
                    f'Unknow dependency {other} from "{dep.name}"') from error
    return deps_by_name


def remove_from_mapping(mapping: Mapping, dependency: Dependency) -> Mapping:
    if subdep := mapping[dependency.name]['deps']:
        raise ValueError(
            f'Cannot remove {dependency.name} from the mapping: '
            f'still have unsatisfied dependencies: {subdep}'
        )
    for key, values in mapping.items():
        try:
            values['subs'].remove(dependency.name)
        except (ValueError, KeyError):
            pass
        try:
            values['deps'].remove(dependency.name)
        except (ValueError, KeyError):
            pass
    mapping.pop(dependency.name)
    return mapping


async def walk(dependencies: list[Dependency], max_iterations=100):
    mapping = to_flat_mapping(dependencies)
    iteration = 0
    while mapping:
        iteration += 1
        leafs = list([
            dep['instance']
            for dep in mapping.values()
            if not dep['deps']]
        )
        yield leafs
        for dep in leafs:
            remove_from_mapping(mapping, dep)
        if iteration > max_iterations:
            raise CirclularDependencyException(
                'Too many iterations, something is probably wrong '
                'with the dependency tree'
            )