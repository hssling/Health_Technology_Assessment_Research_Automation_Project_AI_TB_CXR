# Contributing to Health Technology Assessment Research Automation Project

Thank you for your interest in contributing to the Health Technology Assessment (HTA) Research Automation Project! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project adheres to a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Help create a positive community

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- PubMed API access (optional, for literature search features)

### Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/Health_Technology_Assessment_Research_Automation_Project.git
   cd Health_Technology_Assessment_Research_Automation_Project
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development dependencies
   ```

5. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Contributing Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write descriptive variable and function names
- Keep functions focused on single responsibilities
- Add docstrings to all public functions and classes

### Commit Messages

Use clear, descriptive commit messages following this format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Branch Naming

Use descriptive branch names:
- `feature/description-of-feature`
- `bugfix/issue-description`
- `docs/update-documentation`

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_specific_module.py
```

### Writing Tests

- Write unit tests for all new functions
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies
- Aim for >80% code coverage

## Documentation

### Code Documentation

- Add docstrings to all public functions and classes
- Use Google-style docstrings
- Document parameters, return values, and exceptions

### Project Documentation

- Update README.md for significant changes
- Add examples for new features
- Keep API documentation current

## Pull Request Process

1. Ensure your code follows the contributing guidelines
2. Update documentation if needed
3. Add or update tests
4. Ensure all tests pass
5. Update CHANGELOG.md if applicable

6. Create a pull request with:
   - Clear title describing the changes
   - Detailed description of what was changed and why
   - Reference to any related issues
   - Screenshots for UI changes (if applicable)

7. Wait for review and address any feedback

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

- Clear title and description
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Python version, etc.)
- Error messages and stack traces
- Screenshots if applicable

### Feature Requests

For feature requests, please include:

- Clear description of the proposed feature
- Use case and benefits
- Any relevant examples or mockups
- Potential implementation approach

## Data Validation and Authenticity

This project emphasizes data authenticity and validation. When contributing:

- Ensure all data sources are properly cited
- Validate data extraction algorithms
- Maintain audit trails for data processing
- Follow the data validation protocols outlined in `DATA_VALIDATION_AND_AUTHENTICATION_DISCLOSURE.md`

## License

By contributing to this project, you agree that your contributions will be licensed under the same MIT License that covers the project.

## Questions?

If you have questions about contributing, please:

1. Check existing issues and documentation
2. Create a new issue with your question
3. Contact the maintainers

Thank you for contributing to the HTA Research Automation Project!
