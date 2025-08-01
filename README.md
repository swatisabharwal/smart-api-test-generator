# Smart API Test Case Generator

An AI-powered agent that automatically generates comprehensive API test cases and executable Python test code for any REST API endpoint.

## 🚀 Features

- **AI-Powered Generation**: Uses Google Gemini AI to create intelligent test scenarios
- **Comprehensive Coverage**: Generates positive, negative, boundary, and security test cases
- **Executable Code**: Creates ready-to-run Python test code with pytest
- **Smart Analysis**: Automatically analyzes API endpoints and extracts parameters
- **Graceful Fallback**: Continues working even when AI API limits are reached
- **Domain Agnostic**: Works with any API (users, products, orders, books, etc.)

## 🛠️ Technologies Used

- **Python 3.x**
- **Google Generative AI (Gemini)** - For intelligent test case generation
- **Requests** - For HTTP testing in generated code
- **Pytest** - Testing framework for generated code

## 📋 Prerequisites

- Python 3.7+
- Google AI Studio API key (free tier available)

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/smart-api-test-generator.git
cd smart-api-test-generator
```

2. Install required packages:
```bash
pip install google-generativeai requests pyyaml
```

3. Set up your Google AI API key:
   - Get your free API key from [Google AI Studio](https://aistudio.google.com/)
   - Update `src/config.py` with your API key

## 🏗️ Project Structure

```
smart-api-test-generator/
├── src/
│   ├── main.py                    # Entry point
│   ├── test_generator_agent.py    # Core AI agent
│   └── config.py                  # API configuration
├── tests/                         # Future test files
├── examples/                      # Example outputs
└── README.md
```

## 🎯 Use Cases

- **QE Teams**: Accelerate test case creation and coverage analysis
- **Developers**: Generate comprehensive tests for new API endpoints
- **API Testing**: Create security and boundary tests automatically
- **Learning**: Understand comprehensive API testing strategies

## 🤝 Contributing

This is a learning project, but suggestions and improvements are welcome!

## 📄 License

This project is for educational and portfolio purposes.

## 👨‍💻 About

Created by Swati Sabharwal as a portfolio project demonstrating:
- AI integration in testing tools
- Python development skills
- Understanding of API testing best practices
- Test automation expertise

---

*Built by a QE Automation Engineer exploring the intersection of AI and software testing.*"# smart-api-test-generator" 
