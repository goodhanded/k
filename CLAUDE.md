# CLAUDE.md - Development Guide

## Build/Test Commands
- Run all tests: `pytest`
- Run single test: `pytest tests/path/to/test_file.py::TestClass::test_method`
- Run with verbose output: `pytest -v`
- Install dependencies: `pip install -r requirements.txt`
- Update dependencies: `pip-compile requirements.in --strip-extras`

## Code Style Guidelines
- Follow Clean Architecture principles with clear separation between domain, application, and infrastructure
- Use dependency injection with service registration in services.yaml
- Type annotations required for all functions and methods
- Use Protocol classes for interfaces in application layer
- Module imports ordered: standard library, third-party, then local modules
- Use meaningful variable/function names with snake_case
- Exception handling should be explicit and meaningful (no bare excepts)
- Prefer composition over inheritance
- Workflow nodes should be small, focused, and reusable
- Document public interfaces with docstrings