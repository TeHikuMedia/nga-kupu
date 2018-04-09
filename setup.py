from distutils.core import setup
import sys

setup(name='taumahi',
      version='1.2',
      data_files=[('lib/python{}/dist-packages/taumahi_tūtira'.\
      		format(sys.version[0:3]), [
      		 'taumahi/taumahi_tūtira/kupu_kino_kūare_tohutō.txt',
      		 'taumahi/taumahi_tūtira/kupu_kino.txt',
      		 'taumahi/taumahi_tūtira/kupu_rangirua_kūare_tohutō.txt',
      		 'taumahi/taumahi_tūtira/kupu_rangirua.txt'])],
      description='Identify Māori words in text',
      url='https://github.com/TeHikuMedia/nga-kupu',
      packages=['taumahi'],
      install_requires=[
          'yelp_uri','beautifulsoup4','pytest'
      ],
      include_package_data=True,
      zip_safe=False)

# Uninstall:
# cd /usr/local/lib/python3.*/dist-packages ; sudo rm -r taumahi*
