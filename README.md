# Aviate SDE Task - Candidate Management API 🚀

DRF CRUD API to add, delete and search data from api for ats score

Search can be done on splitted words without filtering by python but only orm 

## Setup & Installation 🛠️

First things first, you'll need to get this thing running on your machine. Here's how:

1. Clone this repo (duh!):
```bash
git clone <your-repo-url>
cd aviate-sde-task
```

2. Create a virtual enviornment (trust me, you want this):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install the stuff you need:
```bash
pip install -r requirements.txt
```

4. Run them migrations (database stuff):
```bash
python manage.py migrate
```

5. Start the server:
```bash
python manage.py runserver
```

Now your server should be running at `http://127.0.0.1:8000/` 🎉

## API Endpoints 📡

Here's all the cool stuff you can do with this API:

### 1. Get All Candidates
```bash
curl 'http://127.0.0.1:8000/api/candidates/'
```
This will show you all the candidates in the database. Easy peasy!

### 2. Search Candidates
```bash
curl 'http://127.0.0.1:8000/api/candidates/search/?search=Kumar'
```
This is where the magic happens! You can search for candidates by their name. It's super smart - it'll find partial matches too!

For example, if you search for "Ajay Kumar Yadav", it'll find:
- "Ajay Kumar Yadav" (exact match)
- "Ajay Kumar"
- "Kumar Yadav"
- "Ajay Yadav"
- And any other names containing these words!

### 3. Create a New Candidate
```bash
curl -X POST 'http://127.0.0.1:8000/api/candidates/' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "John Doe",
    "age": 25,
    "gender": "Male",
    "email": "john.doe@example.com",
    "phone_number": "+911234567890"
  }'
```

### 4. Get a Specific Candidate
```bash
curl 'http://127.0.0.1:8000/api/candidates/1/'
```
Just replace '1' with the ID of the candidate you want to see.

### 5. Update a Candidate
```bash
curl -X PUT 'http://127.0.0.1:8000/api/candidates/1/' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "John Updated",
    "age": 26,
    "gender": "Male",
    "email": "john.updated@example.com",
    "phone_number": "+911234567890"
  }'
```

### 6. Delete a Candidate
```bash
curl -X DELETE 'http://127.0.0.1:8000/api/candidates/1/'
```

## Testing the API 


1. First, create a new candidate:
```bash
curl -X POST 'http://127.0.0.1:8000/api/candidates/' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Ajay Kumar Yadav",
    "age": 28,
    "gender": "Male",
    "email": "ajay.kumar@example.com",
    "phone_number": "+911234567890"
  }'
```

2. Then search for them:
```bash
curl 'http://127.0.0.1:8000/api/candidates/search/?search=Ajay%20Kumar'
```

3. Check if you can find them in the full list:
```bash
curl 'http://127.0.0.1:8000/api/candidates/'
```
