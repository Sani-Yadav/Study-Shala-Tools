# Media Downloader with Movie Search

A Django-based web application that allows users to search for movies, view details, and stream trailers using the TMDB API.

## Features

- Search for movies with real-time results
- View detailed movie information including cast, ratings, and trailers
- Browse similar movies
- Responsive design that works on all devices
- Integrated with TMDB API for comprehensive movie database

## Setup Instructions

1. **Get a TMDB API Key**
   - Go to [TMDB](https://www.themoviedb.org/settings/api) and sign up for an account
   - Request an API key from the API section
   - Replace `YOUR_TMDB_API_KEY` in `downloader/views.py` with your actual API key

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

5. **Access the Application**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - Click on the "Movies" link in the navigation bar to start searching for movies

## Usage

- **Search for Movies**: Use the search bar to find movies by title
- **View Details**: Click on any movie to see detailed information including cast, plot, and ratings
- **Watch Trailers**: Play the official trailer directly on the movie details page
- **Discover Similar**: Browse through similar movies at the bottom of the details page

## Technologies Used

- Django 4.2
- TMDB API
- Bootstrap 5
- Font Awesome 6
- jQuery

## Note

This application is for educational purposes only. Please respect the terms of service of the TMDB API and other services used.
