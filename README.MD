# SoftDesk API

> NOTE : `Python 3.9.9` & `Windows 11 21H2` was used while working on this project.

> NOTE : You will find the API documentation [right here](https://www.postman.com/phonemicrowave/workspace/softdesk-api/api/668c0f9e-dc09-4c2d-a81e-b03077f93630/version/6588de8a-93c1-445c-8d24-bb6c7fa18779)

## Installation

Create a virtual environment

```
python -m venv .venv
```

---

Then activate it

```
[WINDOWS]
./.venv/Scripts/activate

[LINUX]
source .venv/bin/activate
```

---

Once done, Install all the required dependencies using pip:

```
pip install -r requirements.txt
```

## Running the Project

Running django :

```
python ./manage.py runserver
```

you should see something like this :

```
System check identified no issues (0 silenced).
January 23, 2022 - 18:51:44
Django version 3.2.9, using settings 'SoftDesk_API.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Then the API is served on : http://127.0.0.1:8000/

> NOTE : if this isn't what you are seeing, and you are unable to access the website, then its probably because there is a typo somewhere or didn't follow the steps correctly ...
