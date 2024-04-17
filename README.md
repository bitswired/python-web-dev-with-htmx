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





## Exercises

### Exercise 1: Implement User Login

In this exercise, you will complete the implementation of the user login functionality in the provided code. The login process involves retrieving the user from the database, checking the password, setting a cookie, and redirecting the user to the home page.

Tasks:
1. In the `login` function of `auth_router.py`:
   - Retrieve the user from the database using the provided `app_service.login` method.
   - Set a cookie with the key "python-htmx-workshop" and the value of the user's ID.
   - Set the "HX-Redirect" header to redirect the user to the home page ("/").

2. In the `login` method of `service.py`:
   - Retrieve the user from the database using the provided username.
   - If the user is not found, raise an `HTTPException` with a status code of 404 and the detail "User not found".

3. In `login.html`:
   - Add the appropriate HTMX attribute to the form to trigger the login request.

Note: The password check and other necessary code are already provided.

Good luck!



### Exercise 2: Implement Chat Deletion

In this exercise, you will complete the implementation of the chat deletion functionality in the provided code. The deletion process involves using the application service to delete the chat and returning an appropriate response to HTMX.

Tasks:
1. In the `delete_chat` function of `chat_router.py`:
   - Use the `app_service.delete_chat` method to delete the chat, passing the `chat_id` and `user` as arguments.
   - Return an appropriate response to HTMX to handle the deletion.

2. In the `delete_chat` method of `service.py`:
   - Retrieve the chat from the database using the provided `chat_id` and `user.id`.
   - Delete the chat using the session's `delete` method.

3. In `chat-base.html`:
   - Add the appropriate HTMX attributes to the delete button to trigger the chat deletion request.

Note: The necessary error handling and other code are already provided.

Good luck!

### Exercise 3: Implement Chat Generation with Server-Sent Events (SSE)

In this exercise, you will complete the implementation of the chat generation functionality using Server-Sent Events (SSE) in the provided code. The generation process involves retrieving the chat, building the message list for AI completion, and sending the generated response back to the client using SSE.

Tasks:
1. In the `generate` function of `chat_router.py`:
   - Build the `EventSourceResponse` using the `app_service.generate` method, passing the `chat_id` as an argument.

2. In the `generate` method of `service.py`:
   - Retrieve the chat from the database using the provided `chat_id`.
   - If the chat is not found, raise an `HTTPException` with a status code of 404 and the detail "Chat not found".
   - Build the message list for AI completion by iterating over the chat messages and appending them to the `messages` list.
   - Build the response that will be swapped in the template by HTMX. Use the `markdown` function to render the generated content and wrap it in appropriate HTML tags.
   - Yield the response as a dictionary with the keys "event", "id", and "data".
   - After the generation is complete, send the final response that will be swapped in the template by HTMX. Combine both writing the final message and removing the SSE connection with an out-of-band swap.

3. In `chat-id.html`:
   - Add the appropriate HTMX attributes to the `<div>` element to establish the SSE connection, specify the target for message swapping, and handle the swap behavior.

Note: The necessary AI completion code and other parts are already provided.

Good luck! 


