import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-form-action",
    version="1.0.3",
    author="Pradish Bijukchhe",
    author_email="pradishbijukchhe@gmail.com",
    description="Django action to add an intermediate page to parse form data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sandbox-pokhara/django-form-action",
    project_urls={
        "Bug Tracker": "https://github.com/sandbox-pokhara/django-form-action/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    include_package_data=True,
    package_dir={"form_action": "form_action"},
    python_requires=">=3",
    install_requires=["django"],
)
