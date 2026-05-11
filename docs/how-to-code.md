## First Time Setup

**1. Clone the repo**
You can do this from GitHub Desktop.

**2. Create your `.env` file**
It's on WhatsApp

**3. Create your `.venv` file**
Even if the app is on docker vsc still need to know what you are doing.
Cristi use vsc it will make your life esier.

**4. Create the database password file**
Create `backend/app/db/password.txt` and write just the password.


**5. Install Ollama and pull the models**
For now you  don't need this, but you will.
```bash
ollama pull qwen3.5:4b
ollama pull nomic-embed-text-v2-moe
```

**6. Install Docker Desktop**

**7. Start the project**

```bash
docker compose up           # start everything
docker compose down         # stop everything
docker compose up --build   # use only if you changed requirements.txt or Dockerfile
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

## Docs
- [Architecture Overview](docs/cv-parser-architecture.md)
- [Project Plan & Task Split](docs/cv-parser-plan.md)