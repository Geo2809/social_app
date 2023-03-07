# A social media app developed using  [Django](https://www.djangoproject.com/) and [Semantic UI](https://semantic-ui.com/).
  
## Dependencies
<details>
     <summary> Click to expand </summary>
     
* [python](https://www.python.org/downloads/)
* [django](https://www.djangoproject.com/download/)
* [django-allauth](https://django-allauth.readthedocs.io/en/latest/installation.html)
* [django-countries](https://pypi.org/project/django-countries/)
* [mysqlclient](https://pypi.org/project/mysqlclient/)
* [pillow](https://pypi.org/project/Pillow/)
</details>
  
## Gif

![Animation](https://user-images.githubusercontent.com/106703971/181058635-25cf3ae6-5887-4d77-b6a5-2a817176fb6d.gif)


## Installation Guide
  * Clone repository: `git clone https://github.com/Geo2809/social_app.git`.
  * Install [dependencies](#dependencies).
  * Configure settings.py > DATABASES.
  * You can use default configuration of DATABASES.
   ```    
   DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': BASE_DIR / 'db.sqlite3',
       }
   }
      
  ```
   ## Next
  ```
 
  Run these commands:
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
  ```

## Features

* Profile:
  * A profile is automatically created each time a user registers.
  * Upon registration, a default picture is assigned to the profile. The user can change it with a personal one.
  
* Posts: 
  * A post can be created, updated, or deleted.
  * A user cannot modify or delete another user's post.
  
* Comment: 
  * Add a comment to a post.
  * View all comments in a post.
  
* Likes:
  * Like or unlike a post.
  
* Friends: 
  * Send, accept, or reject a friend request.
  * You can search for a specific friend using the search bar.

