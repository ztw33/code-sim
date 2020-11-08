from setuptools import setup, find_packages

VERSION = "0.1.0"

setup(name="codesim",
      version=VERSION,
      description="A tool for measuring the similarity between two c++ code files.",
      author="Tingwei Zhu",
      author_email="tingweizhu33@smail.nju.edu.cn",
      license="MIT",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          "clang==6.0.0"
      ],
      entry_points={
          "console_scripts": [
              "codesim = codesim.codesim:main"
          ]
      },
)