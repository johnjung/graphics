from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='graphics',
    description='Scripts to produce diagrams and graphics',
    version='0.0.1',
    long_description=readme(),
    author='John Jung',
    author_email='john@johnjung.us',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/johnjung/graphics',
    scripts=[
        'graphics/beer_flavor_wheel',
        'graphics/structured_planning_venn',
        'graphics/two_by_two',
        'graphics/venn',
    ]
)
