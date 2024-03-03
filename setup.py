from setuptools import setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt', encoding="utf-8") as f:
    required = f.read().splitlines()

version = '0.1'

setup(name="grifon-api",
      version=version,
      description="grifon shared code",
      long_description=long_description,
      # url="www.our_url.ru",      # todo set our url
      author="grifon",
      # author_email="grifon@mail.com",     # todo set our email
      zip_safe=False,
      packages=['grifon', ],
      package_dir={"": "."},
      package_data={
          "": ["*.html"],
      },
      install_requires=[required],
      )
