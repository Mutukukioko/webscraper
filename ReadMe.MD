# Django Email Scraper

A Django application that scrapes emails from given URLs and displays the list of scraped emails.

## Features

- Scrape emails from any given website URL.
- Store and display the scraped emails.
- Simple and intuitive UI with a reusable navigation bar.
- CSS styling for a clean and responsive design.
- JavaScript integration for enhanced interactivity.

## Requirements

- Python 3.6+
- Django 3.2+
- BeautifulSoup4
- Requests

## Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/email_scraper.git
    cd email_scraper
    ```

2. **Create a virtual environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run migrations**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run the development server**

    ```bash
    python manage.py runserver
    ```

6. **Access the application**

    Open your web browser and navigate to `http://127.0.0.1:8000/scrape/`.

## Usage

1. **Navigate to the Scrape Page**

    Go to `http://127.0.0.1:8000/scrape/`.

2. **Input a URL**

    Enter the URL of the website you want to scrape for emails.

3. **Submit the Form**

    Click the "Scrape" button to start scraping.

4. **View Scraped Emails**

    Navigate to `http://127.0.0.1:8000/emails/` to view the list of scraped emails.

## Project Structure

email_scraper/
├── email_scraper/
│ ├── init.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── scraper/
│ ├── static/
│ │ ├── scraper/
│ │ │ ├── css/
│ │ │ │ └── styles.css
│ │ │ └── js/
│ │ │ └── main.js
│ ├── templates/
│ │ ├── scraper/
│ │ │ ├── base.html
│ │ │ ├── email_list.html
│ │ │ ├── navbar.html
│ │ │ └── scrape.html
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ ├── utils.py
│ └── views.py
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt


## Dependencies

- Django
- BeautifulSoup4
- Requests

You can install the dependencies using the following command:

```bash
pip install django beautifulsoup4 requests
