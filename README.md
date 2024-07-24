# Automated Test Framework

This project is an automated testing framework for web applications using Selenium and Python. It provides a robust structure for creating and running automated tests, with features including:

- Page Object Model (POM) design pattern
- Data-driven testing capabilities
- Cross-browser testing support (Chrome, Firefox, Edge)
- Parallel test execution
- Detailed logging and HTML report generation
- Performance timing measurements

The framework is designed to be easily extendable and maintainable, making it suitable for both small and large-scale web application testing projects.

## Setup

1. Clone the repository :
git clone https://github.com/SIMO12F/automated-test-framework.git
cd automated-test-framework
2. Create a virtual environment:
   python -m venv venv
3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
pip install -r requirements.txt
## Running Tests

To run all tests:
python run_tests.py
To run specific tests:
pytest src/tests/test_search.py
## Project Structure

- `src/`: Source code for the test framework
  - `pages/`: Page object models
  - `tests/`: Test scripts
  - `utils/`: Utility functions and helpers
- `config.py`: Configuration settings
- `run_tests.py`: Script to run all tests

## Contributing

We welcome contributions to improve the Automated Test Framework. Here are some ways you can contribute:

1. **Reporting Bugs**: If you find a bug, please create an issue in the GitHub repository with a detailed description and steps to reproduce.

2. **Suggesting Enhancements**: Have ideas for new features or improvements? Open an issue to discuss your suggestions.

3. **Code Contributions**: 
   - Fork the repository
   - Create a new branch for your feature (`git checkout -b feature/AmazingFeature`)
   - Make your changes
   - Commit your changes (`git commit -m 'Add some AmazingFeature'`)
   - Push to the branch (`git push origin feature/AmazingFeature`)
   - Open a Pull Request

4. **Documentation**: Help improve the documentation, including this README, inline comments, or separate documentation files.

Please ensure that your code adheres to the existing style conventions and includes appropriate tests.

