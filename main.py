import asyncio
from depsolve import Dependency, walk


async def perform_importation(dependency: Dependency):
    # osef, on teste juste
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
    async for items in walk(dependencies):
        deps_names = [dep.name for dep in items]
        print(f'dependencies to install: {len(items)} : {", ".join(deps_names)}')
        tasks = asyncio.gather(*[perform_importation(dep) for dep in items])
        await tasks


if __name__ == "__main__":
    asyncio.run(main())
