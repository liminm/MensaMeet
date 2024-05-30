# MensaMeet

Mensa application to find like-minded people to go to the cafeteria with.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

```
certifi==2019.6.16
Django==2.2.3
django-crispy-forms==1.7.2
gunicorn==19.9.0
Pillow==6.0.0
pip==19.0.3
psycopg2==2.8.2
pytz==2019.1
setuptools==40.8.0
sqlparse==0.3.0
wheel==0.33.1
pyOpenSSL==19.0.0
dj-database-url==1.2.0
cloudinary==1.31.0
django-cloudinary-storage==0.3.0
six==1.16.0
```
Also see the [requirements.txt](https://github.com/liminm/MensaMeet/blob/master/requirements.txt).


### Installing

A step by step series of examples that tell you how to get a development env running

1. Download the repository and open it in your code editor of choice.
2. Create a virtual environment by writing in your Bash command shell or the alternative Powershell command.
```
    python -m venv /path/to/new/virtual/environment
```
3. On a Unix system activate the virtual environment by typing in the terminal depending on the directory in which you created the virtual environment:
```
source /path/to/venv/bin/activate
```
Alternatively for Windows use:
```
path\to\venv\Scripts\activate.bat
```
4. Install the required packages from requirements.txt by running the following command in your terminal from the project home directory:
```
pip install -r requirements.txt
```
5. Run manage.py runserver from the project home directory.

```
manage.py runserver
```
6. Click on the link shown to you in the terminal after running the previous step.


## Built With

* [Django](https://www.djangoproject.com/) - Backend Framework
* [Bootstrap](https://getbootstrap.com/) - Frontend CSS framework
* [PostgreSQL](https://www.postgresql.org/) - Database

## Authors

**Mia Szoszkiewicz**  
**Ahmet Kerem Aksoy**  
**Vesela Stefanova**  
**Todor Moskov**  
**Limin Malek**  

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* This work is supported by Alexander Acker and Soeren Becker
