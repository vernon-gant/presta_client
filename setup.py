from setuptools import setup

setup(
    name='prestashop_orders_client',
    version='0.0.1',
    description='Simple client for PrestaShop Api to extract orders info.',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Aleksandr Zakharov',
    author_email='aleksza.4119@gmail.com',
    url='https://github.com/vernon-gant/prestashop_orders_client',
    project_urls={
        'Source': 'https://github.com/vernon-gant/prestashop_orders_client',
        'Tracker': 'https://github.com/vernon-gant/prestashop_orders_client/issues',
    },
    packages=['prestashop_orders_client'],
    license='Apache License 2.0',
    license_files='LICENSE',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
    ],
    keywords='prestashop orders api client',
    install_requires=["requests>=2.28.1", "xmltodict>=0.13.0"],
    test_require=["pytest"],
    test_suite="pytest",
    python_requires='>=3.10',
)
