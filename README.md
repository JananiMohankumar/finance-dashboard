# Finance Data Processing and Access Control Backend

Hi! This is my backend engineering project submission. I've built a full-stack, Role-Based Access Control (RBAC) finance dashboard to demonstrate my understanding of secure backend architectures, database aggregations, and REST API design.

I decided not to use a heavy "batteries-included" framework like Django and instead went with **Python Flask**. This allowed me to show exactly how I approach manually structuring an application cleanly using Blueprints, decorators, and the Application Factory pattern.

## Technical Choices & Features
- **Role-Based Access Control (RBAC):** I wrote a custom decorator (`@role_required`) to securely manage `viewer`, `analyst`, and `admin` roles, making sure the backend physically blocks unauthorized actions instead of just hiding buttons on the frontend.
- **Optimized MongoDB Queries:** For the dashboard summaries, instead of pulling all records into Python and looping through them (which is slow at scale), I wrote native MongoDB `$group` aggregation pipelines so the database engine does the heavy computational lifting.
- **Graceful Error Handling:** I took care to ensure no bad input could cause a 500 server crash. Incomplete forms return custom `400` errors, and unauthorized requests return `401` or `403`.
- **JWT Security:** Passwords are never stored in plain text. I used `Bcrypt` to salt and hash them, and `Flask-JWT-Extended` for stateless API token communication.
- **Frontend Design:** The API is consumed by a React frontend. I designed it using pure "Glassmorphism" CSS (no Tailwind templates) to prove I can handle modern UI hierarchy and React Contexts.

## How to Test the Project Locally

I developed this using a local setup. You will need **Node.js** and **Python 3**.

### 1. Database Setup
Make sure MongoDB is running locally on the default port (`27017`). The database `finance_db` will automatically initialize as soon as you add the first piece of data!

### 2. Start the Backend API
Open a terminal in the `backend` folder:
```bash
python -m venv venv

# For Windows:
venv\Scripts\activate
# For Mac / Linux:
# source venv/bin/activate

pip install -r requirements.txt
python app.py
```
*(The API will be available at `http://127.0.0.1:5000`)*

### 3. Start the Frontend UI
In a completely separate terminal window, go to the `frontend` folder:
```bash
npm install
npm run dev
```
*(Open the printed local link in your browser, usually `http://localhost:5173`)*

---

### A Note for the Evaluator on Roles

Because this uses a local setup, I didn't want you to have to run a complex database seeding script just to test the admin features. 

To solve this smoothly: **The very first account that registers is automatically granted `admin` rights.** All accounts created after that will be restricted default `viewers`.

So, to properly test the application, simply register a fresh account. You will instantly have full control to add expenses, look at the dashboard, and assign roles to other test users via the Users tab!

---
*Thank you for taking the time to review my code! The backend was intentionally separated into distinct logic folders (routes, utils, config) to emulate a clean software engineering environment.*
