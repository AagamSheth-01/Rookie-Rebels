# Rookie Rebels

**Rookie Rebels** is a dynamic web application developed during **DUHacks 4.0**, designed to streamline the management of Marvel movies. Built with Django, this app enables users to easily **add**, **view**, and **delete** movie entries complete with director details, budget info, and poster images.

---

##  Features

-  **Add Movies** – Easily submit new Marvel movie entries with relevant details.
-  **View Movies** – Browse a gallery of your added movies.
-  **Delete Movies** – Remove movies from the collection with ease.
-  **Media Upload Support** – Seamlessly attach poster images to each movie entry.

---

##  Tech Stack

| Component       | Technology             |
|-----------------|------------------------|
| Backend/Framework | Django                 |
| Database        | SQLite (default)       |
| Frontend        | Django Templates       |
| Media Handling  | Django `Media` setup   |

---

##  Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AagamSheth-01/Rookie-Rebels.git
   cd Rookie-Rebels

2.Install required packages:
bash
Copy
Edit
pip install -r requirements.txt

3.Apply database migrations:
bash
Copy
Edit
python manage.py migrate

4.Run the development server:
bash
Copy
Edit
python manage.py runserver
