# Accuknox_social_media_api
### PostMan Collection Link
Click "Import" in Postman and paste this link

`https://api.postman.com/collections/18603598-37c8bf0e-70ff-4e3e-af35-df8f46d20969?access_key=PMAT-01J6WGWHXR4M9KPYZW3K0Y5Y6K`

### Building the Docker Image
To build the Docker image, run the following command: 

`docker-compose build --no-cache`

### Setting up the Database and Creating a Super User
Run the following commands to set up the database and create a super user: 

```
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
- Email: admin@email.com
- Password: dipanjan
```
### Run the Django App
`docker-compose up`

Now, the app’s admin panel can be accessed at:

`http://127.0.0.1:8000/admin/`

### API Endpoints
1. Sign Up

`POST http://127.0.0.1:8000/api/account/signup/`

2. Login
   
`POST http://127.0.0.1:8000/api/account/login/`

A Token ID will be generated which we will use in further APIs.

3. Log Out
   
```
POST http://127.0.0.1:8000/api/account/logout/

Headers:
Authorization: Token <token_id>
```

4. Search Users
   
Based on Name

```GET http://127.0.0.1:8000/api/account/search/
Query Param:
search=deb
```

Based on Email

```GET http://127.0.0.1:8000/api/account/search/

Query Param:
search=beta@email.com
```

5. Sending Friend Requests
   
To send friend requests (also checking the functionality that no more than 3 requests can be sent in a minute):

```
POST http://127.0.0.1:8000/api/friend-request/send/
Headers:
`Authorization: Token <token_id>
Body 1:
{
    "receiver_id": 1
}
Body 2:
{
    "receiver_id": 3
}
Body 3:
{
    "receiver_id": 4
}
Body 4:
{
    "receiver_id": 5
}
```

6. List Pending Friend Requests
   
`GET http://127.0.0.1:8000/api/friend-request/pending/`

Login to another user:

```
Email: beta@email.com
Password: password
Headers:
Authorization: Token <token_id>
```

7. Accept/Reject Friend Request
   
`PUT http://127.0.0.1:8000/api/friend-request/respond/<int:friendrequest_id>/`

Example:
PUT http://127.0.0.1:8000/api/friend-request/respond/2/

8. Friends List
    
```
GET http://127.0.0.1:8000/api/friends/
Headers:
Authorization: Token <token_id>
```
