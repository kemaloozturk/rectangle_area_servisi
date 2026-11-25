from setuptools import find_packages, setup

package_name = 'alan_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kemaloozturk',
    maintainer_email='okemal883@gmail.com',
    description='RectangleArea servisi sunucu ve istemci paketi',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'server = alan_py.server:main',
            'client = alan_py.client:main',
        ],
    },
)
