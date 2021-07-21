from setuptools import setup, find_packages

setup(
    name="Libary App",
    description="Application for libary",
    version="1.0.0",
    packages=find_packages(),
    entry_points={"console_scripts": ["start-app = src.app:run"], },
    install_requires=["Flask==1.1.2", "flask_wtf==0.15.1", "autopep8==1.5.7", "requests==2.26.0",
                      "Flask-Testing==0.8.1", "Flask-Cors==3.0.8", "Flask-SQLAlchemy==2.4.3", "SQLAlchemy==1.3.24",
                      "Flask-Migrate==3.0.1", "flask-paginate==0.8.1"],
)
