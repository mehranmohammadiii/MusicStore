from setuptools import setup, find_packages

setup(
    name='ChinookMusicStore',
    version='1.0.0',
    author='Mehran Mohammadi',
    author_email='mehranmohammaadiii@gmail.com',
    description='A desktop application for managing the Chinook music store.',
    
    #  به صورت خودکار تمام پکیج‌های داخل پروژه را پیدا می‌کند 
    packages=find_packages(),
    
    # این بخش به setuptools  فایل‌های غیر پایتونی (مثل عکس‌ها) را هم شامل شود
    include_package_data=True,
    package_data={
        'MyPackage': ['*.webp', '*.jpg'],
    },

    # لیست کتابخانه‌های مورد نیاز (میشه از requirements.txt هم خواند)
    install_requires=[
        'pyodbc',
        'Pillow',
        'khayyam',
    ],

    #  به پایتون می‌گوید که فایل اجرایی اصلی کجاست
    entry_points={
        'console_scripts': [
            'run-music-store = MyPackage.main:main_function', 
        ],
    },
)