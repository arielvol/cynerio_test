# This is a solution for the Cynerio home assignment.

## Prerequisites

You will need to have the postgres database installed on your machine.

## Installation Instructions:

1) Create a python virtual environment:

```sh
python3 -m venv venv
```

2) Go into the server folder, activate the virtual env and install the requirements file:

```sh
cd server
source activate
pip install -r requirements.txt
```

3) Run the Flask server by running the "main.py" file:

```sh
python3 main.py
```


4) Go out of the virtual env and go to the client folder and install the packages.json file"

```sh
deactivate
cd ..
cd client
npm install
```

5) Run the client dev server:

```sh
npm run dev
```

6) Open a web browser in the following url:

http://localhost:5173/


## Unit Tests:

All of the server unit tests are located under app/tests/