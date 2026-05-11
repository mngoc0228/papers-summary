# Papers Summary
This project is a web application that provides summaries of research papers from arXiv. It consists of a backend server built with FastAPI, a frontend application built with Next.js, and a PostgreSQL database to store paper information. The application also includes a crawler worker that continuously fetches new papers from arXiv and updates the database.

## Installation with Docker
- Notice: Make sure you have Docker and Docker Compose installed on your machine before proceeding with the installation.

```bash
bash dev-setup.sh
```

### Backend
- The backend server will be running at `http://localhost:8000`.
- The API documentation will be available at `http://localhost:8000/docs`.
### Frontend
- The frontend server will be running at `http://localhost:3000`.
### Database (PostgreSQL)
- The database will be running at `localhost:5432` with the following credentials:
  - Username: `arxiv_user`
  - Password: `arxiv_password`
  - Database Name: `arxiv_db`
### The Crawler worker:
- The crawler worker will be running in the background and will continuously fetch new papers from arXiv and update the database. Cron jobs are set up to run everyday at 1:00 AM to ensure the database is up-to-date with the latest papers.
