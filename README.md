# Chatbot API

This project is a simple chatbot application that can be used in two ways:
1. By using the hosted API at `https://chatbot-api-1-j5zd.onrender.com/api/chat` (no installation needed).
2. By running the chatbot locally (requires installation).

## Table of Contents
- [Usage Options](#usage-options)
  - [Using the Hosted API](#using-the-hosted-api)
  - [Running Locally (Optional)](#running-locally-optional)
- [Example Code](#example-code)
- [Contributing](#contributing)
- [License](#license)

## Usage Options

### Using the Hosted API

To interact with the chatbot without installation, use the hosted API.

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

### Running Locally (Optional)

If you need to make changes or run the chatbot locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/frenziedD3X/Chatbot-APi.git
   ```
2. Navigate into the project directory:
   ```bash
   cd Chatbot-APi
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Start the local server (you may need to adjust the server script file if specified differently):
   ```bash
   npm start
   ```
5. Open the chatbot front-end HTML file in a browser to interact with the chatbot locally.

## Example Code

Here’s a JavaScript example for interacting with the chatbot, either by using the hosted API or a local server URL if running locally.

```javascript
// Use either the hosted API URL or local server URL
const apiUrl = 'https://chatbot-api-1-j5zd.onrender.com/api/chat';

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
```

## Contributing
Feel free to open issues or submit pull requests to improve this project.

## License
This project is licensed under the MIT License. See `LICENSE` for more details.
