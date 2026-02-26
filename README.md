# Athenura FAQ Chatbot

A modern, responsive FAQ chatbot built with Flask and vanilla JavaScript. Features a beautiful teal-themed UI with a friendly robot assistant.

## Features

- 🤖 Intelligent FAQ matching using fuzzy string matching
- 🎨 Modern teal-themed responsive design
- 💬 Real-time chat interface
- 📱 Mobile-friendly responsive layout
- ⚡ Fast and lightweight
- 🔍 Smart question matching with similarity scoring

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Custom CSS with gradients and animations
- **Data**: CSV-based FAQ storage

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/athenura-faq-chatbot.git
cd athenura-faq-chatbot
```

2. Install dependencies:
```bash
pip install flask flask-cors
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and go to `http://127.0.0.1:5000`

## Project Structure

```
├── app.py              # Flask backend server
├── index.html          # Main HTML file
├── style.css           # Styling and animations
├── script.js           # Frontend JavaScript
├── faq_data.csv        # FAQ questions and answers
├── athenura-logo.png   # Company logo
└── README.md           # Project documentation
```

## Usage

1. Click the teal robot icon in the bottom-right corner to open the chat
2. Type your question about Athenura internship
3. Get instant responses based on the FAQ database
4. Use quick reply buttons for common questions

## Customization

- **FAQ Data**: Edit `faq_data.csv` to add/modify questions and answers
- **Styling**: Modify `style.css` to change colors, fonts, or layout
- **Logo**: Replace `athenura-logo.png` with your company logo

## API Endpoints

- `GET /` - Serves the main HTML page
- `POST /chat` - Processes chat messages and returns responses

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.