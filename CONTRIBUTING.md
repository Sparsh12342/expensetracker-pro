# Contributing to AWS Expense Tracker

Thank you for your interest in contributing to AWS Expense Tracker! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Node.js 16+
- Python 3.8+
- Git

### Setup
1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/AWSExpenseTracker.git`
3. Run the setup script: `./setup.sh`
4. Create a feature branch: `git checkout -b feature/your-feature-name`

## 🏗️ Development Workflow

### Frontend Development
```bash
cd react-app
npm run dev
```

### Backend Development
```bash
cd server
source venv/bin/activate
python app.py
```

### Running Tests
```bash
# Frontend tests (when available)
cd react-app && npm test

# Backend tests (when available)
cd server && python -m pytest
```

## 📝 Code Style

### React/TypeScript
- Use functional components with hooks
- Follow React best practices
- Use TypeScript for type safety
- Prefer CSS-in-JS for styling

### Python
- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for functions and classes
- Use meaningful variable names

## 🐛 Bug Reports

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Browser/OS information

## ✨ Feature Requests

When suggesting features:
- Describe the use case
- Explain the benefit
- Consider implementation complexity
- Check for existing similar requests

## 📋 Pull Request Process

1. **Fork and Clone**: Fork the repo and clone your fork
2. **Create Branch**: Create a feature branch from `main`
3. **Make Changes**: Implement your changes
4. **Test**: Ensure your changes work correctly
5. **Commit**: Write clear commit messages
6. **Push**: Push your branch to your fork
7. **Create PR**: Open a pull request with a clear description

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested locally
- [ ] Added tests
- [ ] All tests pass

## Screenshots (if applicable)
Add screenshots here

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🏷️ Commit Messages

Use clear, descriptive commit messages:
- `feat: add new feature`
- `fix: resolve bug in component`
- `docs: update README`
- `style: format code`
- `refactor: improve code structure`
- `test: add unit tests`

## 📚 Documentation

- Update README.md for significant changes
- Add inline comments for complex logic
- Update API documentation for backend changes
- Include examples for new features

## 🔒 Security

- Never commit sensitive information
- Use environment variables for configuration
- Validate all user inputs
- Follow security best practices

## 🤝 Community Guidelines

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow the code of conduct

## 📞 Getting Help

- Check existing issues and discussions
- Join our community discussions
- Ask questions in GitHub discussions
- Review the documentation

## 🎯 Areas for Contribution

### Frontend
- UI/UX improvements
- New visualization components
- Performance optimizations
- Accessibility enhancements

### Backend
- API improvements
- Machine learning model enhancements
- Performance optimizations
- New analysis features

### Documentation
- Tutorial improvements
- API documentation
- Code examples
- User guides

### Testing
- Unit tests
- Integration tests
- End-to-end tests
- Performance tests

Thank you for contributing to AWS Expense Tracker! 🎉
