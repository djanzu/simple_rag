document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatWindow = document.getElementById('chat-window');
    const welcomeMessage = document.querySelector('.welcome-message');

    // Create a typing indicator element
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'typing-indicator';
    typingIndicator.innerText = 'Gemma is thinking...';
    chatWindow.appendChild(typingIndicator);

    function appendMessage(text, type, sources = []) {
        if (welcomeMessage) {
            welcomeMessage.style.display = 'none';
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = `message message-${type}`;

        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'message-bubble';
        bubbleDiv.innerText = text;
        messageDiv.appendChild(bubbleDiv);

        if (sources.length > 0) {
            const sourcesDiv = document.createElement('div');
            sourcesDiv.className = 'sources';
            sourcesDiv.innerText = `Sources: ${sources.join(', ')}`;
            messageDiv.appendChild(sourcesDiv);
        }

        chatWindow.insertBefore(messageDiv, typingIndicator);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = userInput.value.trim();
        if (!query) return;

        // User message
        appendMessage(query, 'user');
        userInput.value = '';

        // Show typing indicator
        typingIndicator.style.display = 'block';
        chatWindow.scrollTop = chatWindow.scrollHeight;

        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Hide typing indicator
            typingIndicator.style.display = 'none';

            if (data.error) {
                appendMessage(`Error: ${data.error}`, 'ai');
            } else {
                appendMessage(data.answer, 'ai', data.sources);
            }
        } catch (error) {
            console.error('Error:', error);
            typingIndicator.style.display = 'none';
            appendMessage('Sorry, something went wrong. Check the console for details.', 'ai');
        }
    });

    // Focus input on page load
    userInput.focus();
});
