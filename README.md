# Python Web Applications with GenAI Workshop: ChatGPT Clone

## Getting started

1. Install Docker: https://docs.docker.com/get-docker/
    - Open the application and follow necessary setup instructions.
    - Check installation by running `docker --version` in your Terminal.
2. Clone the repo or download the zip file.
3. Create a `.env` at the project's root containing the following (replace `sk-...` with your OpenAI API key):
```
DB_PATH=.volumes/db/db.local
OPENAI_API_KEY=sk-...
```
4. Run `docker compose up` (from the project's root) to start the server.
5. When you something like `core-1  | Done in XXXms.`, open your browser at [http://localhost:8000](http://localhost:8000).
6. You can edit code and it will automatically rebuild the server. You will see the change when refreshing the page.






