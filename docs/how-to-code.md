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
For now you  don't need this, but you will.
```bash
ollama pull qwen3.5:4b
ollama pull nomic-embed-text-v2-moe
```

**6. Install Docker Desktop** <br>

**7. Start the project** <br>

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
- [Architecture Overview](cv-parser-architecture.md)
- [Project Plan & Task Split](cv-parser-plan.md)
