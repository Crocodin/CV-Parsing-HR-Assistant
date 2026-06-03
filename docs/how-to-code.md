>[!NOTE]
> The location of all the files you need to make is here [Project Plan & Task Split](cv-parser-plan.md)

>[!CAUTION]
> You will NOT commit any of these files, they are all in `.gitignore` and should be created locally by each developer. If you need to change the structure of any of these files, send the modification in private.

## First Time Setup

**1. Clone the repo** <br>
You can do this from GitHub Desktop.

**2. Create your `.env` file** <br>
It's on WhatsApp

**3. Create your `.venv` file** <br>
Even if the app is on docker vsc still need to know what you are doing.
Cristi use vsc it will make your life esier.

**4. Create the database password file** <br>
Create `backend/app/db/password.txt` and write just the password.


**5. Install Ollama and pull the models** <br>
```bash
ollama pull granite4.1:3b
ollama pull embeddinggemma:300m
```

**6. Install Docker Desktop** <br>

**7. Start the project** <br>

```bash
docker compose up --build   # the --build is only needed the first time, or if you change requirements.txt or Dockerfile
```
Docker dosen't always detect changes so if you think the your code is not running close the containers and start them again, and if this dosen't work use the --build flag to force docker to rebuild the images.

```bash
docker compose up           # start everything
docker compose down         # stop everything
docker compose up --build   # use only if you changed requirements.txt or Dockerfile
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev       # development
npm run build     # production build
```

## Git

- **NEVER commit directly to `main`**
- **NEVER confirm your own pull request**
- Always create a branch for your work
- Someone else on the team must review and approve your PR

**Branch naming:**
```bash
git checkout -b feature/your-feature-name
# examples:
# feature/cv-parser
# feature/scoring-logic
# feature/dashboard-screen
```

## Starting to Code
- always be sure your branch is up to date with main before you start coding, to avoid merge conflicts later on
```bash
git checkout main
git pull origin main
git checkout feature/your-feature-name
git merge main
```
- go on the GitHub page and chouse a issue that is not assigned to anyone, assign it to yourself and start working on it. If oyu wan't to work on someting that dosen't have an issue create the issue first and then assign it to yourself.
- when you are done with the issue, create a pull request and ask for a review from one of your teammates. After the review is approved you can merge the PR to main.

> [!TIP]
> You can try the API at `http://localhost:8000/docs` once the project is running, it's a swagger interface that allows you to test all the endpoints without needing a frontend.
> You can view the db via pgAdmin in the app but also in browser at `http://localhost:5050` (username: admin@admin.com, password: admin)

## Docs
- [Architecture Overview](cv-parser-architecture.md)
- [Project Plan & Task Split](cv-parser-plan.md)

> [!NOTE]
> Better less code but written by you then a lot and vibe coded
