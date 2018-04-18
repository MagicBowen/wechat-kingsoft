try:  
    from setuptools import setup  
except ImportError:  
    from distutils.core import setup  
   
config = {  
   'description': 'dada-qrcode',  
   'author': 'Zhao Yonggang',  
   'url': '',  
   'download_url': 'Where to download it.',  
   'author_email': 'My email.',  
   'version': '0.1',  
   'install_requires': ['qrcode', 'pillow', 'qrtools'],  
   'packages': ['dada-qrcode'],  
   'scripts': [],  
   'name': 'dada-qrcodes'  
}  
   
setup(**config) 