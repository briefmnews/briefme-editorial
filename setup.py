from setuptools import setup

setup(
    name="briefme-editorial",
    version="1.1.0",
    description="Asbtract editorial base for Brief.me projects",
    url="https://github.com/briefmnews/briefme-editorial",
    author="Brief.me",
    author_email="tech@brief.me",
    packages=[
        "briefme_editorial"
    ],
    python_requires=">=3.7",
    install_requires=[
        "Django>=2.2",
        "django-model-utils>=3.2.0",
        "django-tinymce>=2.7.0",
        "django-reactive>=0.1.5"
    ],
    dependency_links=["https://github.com/briefmnews/django-reactive"],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    include_package_data=True,
    zip_safe=False,
)
