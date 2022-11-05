# DepSolve
This is an asyncio agnostic dependency tree solver

The idea is to take out the problem of depencies solving from packages managers or importers

## Usage
```python
import asyncio
from depsolve import Dependency, walk


async def perform_importation(dependency: Dependency):
    # here your package/whatever is supposed to inherit from `Dependency`
    # if any other argument is need for the command line in the package
    # have a look to functools.partial()
    await asyncio.sleep(2)


async def main():
    dependencies = [
        Dependency(name='land'),
        Dependency(name='hen', depends_on=['land']),
        Dependency(name='eggs', depends_on=['hen']),
        Dependency(name='sugar_cane', depends_on=['land']),
        Dependency(name='plain flour', depends_on=['wheat']),
        Dependency(name='sugar', depends_on=['sugar_cane']),
        Dependency(name='genoise', depends_on=['eggs', 'sugar']),
        Dependency(name='strawberry', depends_on=['land']),
        Dependency(name='wheat', depends_on=['land']),
        Dependency(name='sirop', depends_on=['strawberry']),
        Dependency(name='cake', depends_on=['genoise', 'strawberry', 'sirop']),
        Dependency(name='cooking', depends_on=['cake'])
    ]
    for items in walk(dependencies):
        deps_names = [dep.name for dep in items]
        print(f'dependencies to install: {len(items)} : {", ".join(deps_names)}')
        tasks = asyncio.gather(*[perform_importation(dep) for dep in items])
        await tasks


if __name__ == "__main__":
    asyncio.run(main())
```

wich output:
```
dependencies to install: 1 : land
dependencies to install: 4 : hen, sugar_cane, strawberry, wheat
dependencies to install: 4 : eggs, plain flour, sugar, sirop
dependencies to install: 1 : genoise
dependencies to install: 1 : cake
dependencies to install: 1 : cooking
```
