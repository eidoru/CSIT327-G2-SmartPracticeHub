<h1 align="center">SmartPracticeHub</h1>

<div align="center">

![Status](https://img.shields.io/badge/Status-In%20development-orange)

</div>

<div align="center">

![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

</div>

## Overview

A collaboration project between students from IT317-G6 Project Management for IT and CSIT327-G2 Information Management 2.

SmartPracticeHub is a web-based problem bank for Mathematics and Science.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Create & Activate Virtual Environment](#create--activate-a-virtual-environment)
  - [Install Dependencies](#install-dependencies)
  - [Go to Project Directory](#go-to-project-directory)
  - [Apply Database Migrations When Necessary](#apply-database-migrations-when-necessary)
  - [Run the Development Server](#run-the-development-server)
- [Team](#team)

## Getting Started

> [!NOTE]
> Contact the developers for access to database credentials

### Prerequisites
- **Python 3.x**
- **Git**

> If you’re on Windows, commands use `py` and PowerShell or Command Prompt.

### Clone the Repository
```bash
  git clone https://github.com/eidoru/smart-practice-hub.git
  cd smart-practice-hub
```

### Create & Activate Virtual Environment
```bash
  py -m venv env
  .\env\Scripts\activate
```

### Install Dependencies
```bash
  (env) pip install -r requirements.txt
```

### Go to Project Directory
```bash
  (env) cd smart_practice_hub
```

### Apply Database Migrations When Necessary
```bash
  (env) py manage.py migrate
```

### Run the Development Server
```bash
  (env) py manage.py runserver
```

> Visit **http://127.0.0.1:8000/** in your browser.
## Team
| Role | Name | GitHub |
|---|---|---|
| Product Owner | Francis Kyle G. Mahinay | [@M0BIUS1](https://www.github.com/M0BIUS1) |
| Business Analyst | John Lloyd Maluto | [@skweks](https://www.github.com/skweks) |
| Scrum Master | Andrei Sam P. Loy | [@Kitanoed](https://www.github.com/Kitanoed) |
| Developer | Adrian Paul D. Gerbise | [@eidoru](https://www.github.com/eidoru) |
| Developer | Xavier A. Fernandez | [@Xavier-XAF](https://github.com/Xavier-XAF) |
| Developer | Chrisalin C. Gemparo | [@ChrisGemps](https://www.github.com/ChrisGemps) |