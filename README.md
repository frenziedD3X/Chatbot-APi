# Chatbot API

This project is a simple chatbot application that can be used in two ways:
1. By using the hosted API at `https://chatbot-api-1-j5zd.onrender.com/api/chat` (no setup required).
2. By running the chatbot locally using a Flask server (requires Python and Flask).

## Table of Contents
- [Usage Options](#usage-options)
  - [Using the Hosted API](#using-the-hosted-api)
  - [Running Locally with Flask](#running-locally-with-flask)
- [Example HTML Code](#example-html-code)
- [Contributing](#contributing)
- [License](#license)

## Usage Options

### Using the Hosted API

To interact with the chatbot without any local setup, use the hosted API.

#### API Endpoint
The Chatbot API endpoint is:
```plaintext
POST https://chatbot-api-1-j5zd.onrender.com/api/chat
```

#### Request Body
The API expects a JSON payload with the following structure:
```json
{
  "message": "your message here"
}
```

#### Response Body
The API responds with a JSON object:
```json
{
  "response": "Chatbot's response"
}
```

### Running Locally with Flask

If you prefer to run the chatbot locally on your machine, you can use the provided Flask server.

1. Clone the repository:
   ```bash
   git clone https://github.com/frenziedD3X/Chatbot-APi.git
   ```
2. Navigate into the project directory:
   ```bash
   cd Chatbot-APi
   ```
3. Ensure Python and Flask are installed. If Flask is not installed, you can add it via:
   ```bash
   pip install Flask
   ```
4. Start the Flask server:
   ```bash
   python app.py
   ```
5. The Flask server will be available at `http://localhost:10000`. You can now interact with the chatbot by using the local API endpoint.

#### Local API Endpoint
The local API endpoint will be:
```plaintext
POST http://localhost:10000/api/chat
```

## Example HTML Code

Here’s a sample HTML file for interacting with the chatbot API. It can use either the hosted API or the local Flask server.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot Interface</title>
    <style>
        #chat-box { width: 300px; height: 400px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; }
        .message { margin: 5px 0; }
        .user-message { text-align: right; color: blue; }
        .bot-message { text-align: left; color: green; }
    </style>
</head>
<body>

<div id="chat-box"></div>
<input type="text" id="user-input" placeholder="Type your message here...">
<button onclick="sendMessage()">Send</button>

<script>
    // Use either the hosted API URL or the local Flask server URL
    const apiUrl = 'https://chatbot-api-1-j5zd.onrender.com/api/chat';  // Replace with 'http://localhost:10000/api/chat' for local testing

    async function sendMessage() {
        const userInput = document.getElementById("user-input");
        const message = userInput.value.trim();

        if (message === "") {
            return;
        }

        // Display the user's message
        displayMessage(message, "user-message");

        try {
            const response = await fetch(apiUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            displayMessage(data.response, "bot-message");
        } catch (error) {
            console.error("Error communicating with API:", error);
            displayMessage("Error: Could not reach chatbot API.", "bot-message");
        }

        // Clear the input field
        userInput.value = "";
    }

    function displayMessage(message, className) {
        const chatBox = document.getElementById("chat-box");
        const messageElement = document.createElement("div");
        messageElement.className = `message ${className}`;
        messageElement.innerText = message;
        chatBox.appendChild(messageElement);

        // Auto-scroll to the latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    }
</script>

</body>
</html>
```

To switch between the hosted API and the local Flask server, change the `apiUrl` in the script:
- For the hosted API: `const apiUrl = 'https://chatbot-api-1-j5zd.onrender.com/api/chat';`
- For local testing: `const apiUrl = 'http://localhost:10000/api/chat';`

## Contributing
Feel free to open issues or submit pull requests to improve this project.

## License
This project is licensed under the MIT License. See `LICENSE` for more details.
