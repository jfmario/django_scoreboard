
# Django Scoreboard #

A scoreboard for question/answer competitions.

## Getting Started #

### Prerequisites #

```
pip install django
pip install django-allauth
pip install markdown
```

### Installation #

Clone this repository and run:

```
python manage.py migrate
python manage.py createsuperuser
mkdir .media
```

To set up with the sample challenge set:

```
mkdir .media/files/
touch .media/files/myfile.txt
python manage.py loaddata sample
python manage.py runserver
```

Then go into the admin panel `/admin` and create a Competition,
referencing the sample schema that was created.
Log out and visit the site, creating an account
as another user to see the user experience.

### Usage #

Usage

**Dev**

If you alter files in the `src` dir, you will need to run

```
npm i             # install the node dependencies
npm i -g webpack  # install webpack globally
webpack           # rebuild the frontend JS
```

**Loading Challenges**

You can manage challenges through the admin GUI with the site superuser,
but you can also load "fixtures".

Fixtures should go in `_competitions` dir, and there is a `sample.yaml` file
for reference. All fixtures should go in `.yaml` files.

Note that for data files (example on line 197 (pk: 113)), the file
must exist in the `.media/` directory for the challenge to actually work.
You will have to put it there yourself for the fixture to work.

## Docs #

Docs

## Files #

## Acknowledgements #

### Authors #

* John F Marion

### Built With #

### Other #
