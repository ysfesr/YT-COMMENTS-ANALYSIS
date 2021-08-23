# Welcome to YT-COMMENTS-ANALYSIS.

sentiment analysis on any youtube video’s comments

### Image from the project

![Image of Yaktocat](https://i.ibb.co/b7w8qbK/1.jpg)

### Seeting up the project

**1. Clone the repository** git clone https://github.com/elasery1999/YT-COMMENTS-ANALYSIS/

**2. Create your own virtual environment** python3 -m venv venv -> source venv/bin/activate

**3. Install your requirements** pip install -r requirements.txt

**7. Make your migrations** python manage.py migrate

**8. Create a new superuser** python manage.py createsuperuser

**5. Generate a new secret API key from Youtube API then add it to** analysis/utlis.py

**9. Start the development server** python manage.py runserver
