# Finance Data Processing and Access Control Backend

Hi! This is my backend engineering project submission. I've built a full-stack, Role-Based Access Control (RBAC) finance dashboard to demonstrate my understanding of secure backend architectures, database aggregations, and REST API design.

I decided not to use a heavy "batteries-included" framework like Django and instead went with **Python Flask**. This allowed me to show exactly how I approach manually structuring an application cleanly using Blueprints, decorators, and the Application Factory pattern.

## Technical Choices & Features
- **Role-Based Access Control (RBAC):** I wrote a custom decorator (`@role_required`) to securely manage `viewer`, `analyst`, and `admin` roles, making sure the backend physically blocks unauthorized actions instead of just hiding buttons on the frontend.
- **Optimized MongoDB Queries:** For the dashboard summaries, instead of pulling all records into Python and looping through them (which is slow at scale), I wrote native MongoDB `$group` aggregation pipelines so the database engine does the heavy computational lifting.
- **Graceful Error Handling:** I took care to ensure no bad input could cause a 500 server crash. Incomplete forms return custom `400` errors, and unauthorized requests return `401` or `403`.
- **JWT Security:** Passwords are never stored in plain text. I used `Bcrypt` to salt and hash them, and `Flask-JWT-Extended` for stateless API token communication.
- **Frontend Design:** The API is consumed by a React frontend. I designed it using pure "Glassmorphism" CSS (no Tailwind templates) to prove I can handle modern UI hierarchy and React Contexts.

## Live Demo
Frontend UI: **[finance-dashboard-lyart-sigma.vercel.app]**
Backend API: **[https://finance-backend-api-vn1t.onrender.com]**

---

### A Note for the Evaluator on Roles

To prove my Role-Based Access Control logic works without you having to seed a database, **the very first account registered into the MongoDB Cloud Database was automatically granted `admin` rights.** All accounts created after that are restricted to default `viewers`.

Because I have already initialized the database, I set up a dedicated testing account for you to use. 

**Admin Testing Credentials:**
- **Email:** `[admin123@gmail.com]`
- **Password:** `[admin123]`

**Analyst testing Credentials:**
- **Email:** `[finance123@gmail.com]`
- **Password:** `[finance123]`

If you use those credentials to Sign In, you can add expenses, view the dashboard, and assign roles to other test users in the Users tab. 
If you click 'Register' and create a brand new personal account, you can verify that the system correctly restricts your new account to 'viewer' status!

---
*Thank you for taking the time to review my code! The backend was intentionally separated into distinct logic folders (routes, utils, config) to emulate a clean software engineering environment.*
