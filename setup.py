from setuptools import setup, find_packages

setup(
    name='k8s-cli',
    version='1.2.3',  # This will be dynamically updated by the GitHub Action
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'kubernetes',
        'prettytable',
    ],
    entry_points='''
        [console_scripts]
        ku=k8s_cli.k8s_cli:ku
        kn=k8s_cli.k8s_cli:kn
        kp=k8s_cli.k8s_cli:kp
        kpf=k8s_cli.k8s_cli:kpf
        kps=k8s_cli.k8s_cli:kps
        kd=k8s_cli.k8s_cli:kd
    ''',
    author='Dejan Gregor',
    author_email='developer@cloudfever.uk',
    description='This Python package provides native Kubernetes CLI aliases, allowing users to manage and query Kubernetes resources directly from Python without using kubectl',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SCGIS-Wales/kalias',  # Replace with your actual URL
    project_urls={
        'Documentation': 'https://github.com/SCGIS-Wales/kalias#readme',
        'Source': 'https://github.com/SCGIS-Wales/kalias',
        'Tracker': 'https://github.com/SCGIS-Wales/kalias/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
)
