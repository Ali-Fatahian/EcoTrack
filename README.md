# EcoTrack

**EcoTrack** is a Django-based web application designed to help users track their personal carbon footprint. It allows users to log daily activities (such as transport, food consumption, and energy use), calculates CO₂ emissions automatically, and visualizes progress towards monthly goals.

This project was built using **Django 5.2**, **Python 3.13**, and **Docker**.

## Features

* **Activity Logging:** Users can create, update, delete, and see the list of all the activities. CO₂ emissions are calculated automatically based on the selected co2 factor.
* **Interactive Dashboard:**
    * **Visual Breakdown:** Doughnut/Bar charts (via Chart.js) showing emissions by category.
    * **Goal Tracking:** A progress bar tracking monthly emissions against a user-defined limit.
    * **Recent History:** Quick view of the last 5 activities.
* **Data Export:** Users can download their full activity history as a CSV file.
* **Authentication:** Secure user registration, and login, using `django-allauth`.
* **Admin Interface:** Django Admin Panel with added custom filters, search functionality, and improved list of displayed items for the Activity model.

## Tech Stack

* **Backend:** Python 3.13, Django 5.2
* **Database:** PostgreSQL (via Docker Compose)
* **Frontend:** Bootstrap 5, Chart.js
* **Testing:** Pytest
* **Infrastructure:** Docker, Docker Compose
* **CI/CD:** GitHub Actions
* **Tooling:** Cookiecutter Django, Pre-commit, Ruff

---

## ⚙️ Setup & Installation

**Prerequisites:**
* [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running.

### 1. Build the Project
Build the Docker images for the local development environment:

```bash
docker compose -f docker-compose.local.yml build
