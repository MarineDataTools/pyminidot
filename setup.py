from setuptools import setup
import os

ROOT_DIR='pyminidot'
with open(os.path.join(ROOT_DIR, 'VERSION')) as version_file:
    version = version_file.read().strip()

setup(name='pyminidot',
      version=version,
      description='Tool to parse PME minidot textfiles',
      url='https://github.com/MarineDataTools/pyminidot',
      author='Peter Holtermann',
      author_email='peter.holtermann@io-warnemuende.de',
      license='GPLv03',
      packages=['pyminidot'],
      scripts = [],
      entry_points={},
      package_data = {'':['VERSION']},
      zip_safe=False)


