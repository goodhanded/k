# k

**k** is a personal command-line interface (CLI) tool designed to help me automate and streamline tasks such as transcribing audio files, assimilating voice memos into notes, prompting AI agents, generating pull request changesets, and more. It leverages a variety of services and integrations (OpenAI, Amazon Transcribe, Discord bots, etc.) to provide a flexible, extensible system for personal productivity and note management. The tool is built on Clean Architecture principles and utilizes dependency injection to assemble its components.

---

## Table of Contents

- [k](#k)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Commands Overview](#commands-overview)
      - [Subcommands under `run`](#subcommands-under-run)
    - [Examples](#examples)
  - [Configuration](#configuration)
  - [Extending k](#extending-k)
  - [Running Tests](#running-tests)
  - [Additional Information](#additional-information)
  - [Using k to update itself](#using-k-to-update-itself)

---

## Features

- **Voice Memo Assimilation**: Record daily voice notes and assimilate them into a central note for easy retrieval.
- **Audio Transcription**: Transcribe audio files using external services (e.g., Amazon Transcribe).
- **AI Agent Integration**: Prompt various AI agents for Q&A, scheduling, search, or more advanced use cases.
- **Document Indexing**: Index local documents and notes for quick, efficient searching.
- **Discord Bot**: Run a Discord bot that leverages AI agents and indexing capabilities to respond to user prompts.
- **Code Review**: Generate code review feedback by analyzing your project's directory structure and file contents.
- **Code Advice**: Gain detailed insights and suggestions to improve and refactor your codebase.

---

## Requirements

- **Python 3.8+** (Ensure you have a compatible version installed.)
- Pipenv or virtualenv (recommended) for Python dependency management
- Set the `K_PATH` environment variable to the absolute path of the project root for proper resolution of configuration files and templates.

---

## Installation

1. **Clone the Repository:**
   - `git clone https://github.com/goodhanded/k.git`
   - `cd k`

2. **Create and Activate a Virtual Environment:**
   - `python -m venv venv` (from project root)
   - `. ./venv/bin/activate`

3. **Install Dependencies:**
   - `pip install -r requirements.txt`

4. **(Optional) Set Up Environment Variables:**
   - Depending on the integrations you plan to use (OpenAI, AWS, Discord), you may need to set environment variables such as `OPENAI_API_KEY`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `DISCORD_BOT_TOKEN`, etc.
   - **IMPORTANT:** Set the `K_PATH` environment variable to the absolute path of the project root directory. This variable is required for the application to correctly locate configuration files like `.env`, `commands.yaml`, and `services.yaml`. For example, add the following line to your shell configuration file (e.g., `.bashrc` or `.zshrc`):
     
     export K_PATH="/absolute/path/to/k"
     
   - Copy `.env.example` to `.env` and set these variables for local development.

5. **Add Bash/Zsh Alias:**
   - In your shell configuration file (e.g., `.zshrc`), add `alias k='/path/to/k/venv/bin/python /path/to/k/k.py'`
   - Now you can simply call `k` instead of `python k.py`

6. **Initialize the .k Directory (Optional):**
   - Run `k init` to create a fresh `.k` directory with default configuration templates. This is useful if the directory does not already exist or if you want to reset its contents.

7. **Run the CLI:**
   - `k --help`

---

## Usage

All commands are defined in `commands.yaml`. To run a command, use:
`k <command> [args...]`

For subcommands:
`k run <subcommand> [args...]`

### Commands Overview

| Command               | Usage Example                                                | Description                                                                                                           |
|-----------------------|--------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| **init**              | `k init`                                                     | Initializes the .k directory with default configuration templates.                                                  |
| **assimilate**        | `k assimilate --path /path/to/audio.wav`                       | Assimilates a voice memo into your daily note (requires a local audio file).                                          |
| **transcribe**        | `k transcribe --path /path/to/audio.wav`                       | Transcribes the given audio file.                                                                                     |
| **ask**               | `k ask --agent_name search_agent --prompt "Hello!"`           | Prompts an AI agent with a given text input.                                                                          |
| **advise**            | `k advise --prompt "Optimize my database queries."`         | Generates detailed code advice for the project based on your prompt.                                                  |
| **traceback (tb)**    | `k traceback`                                                | Builds a troubleshooting prompt from a traceback present in the clipboard, including related source code excerpts.      |
| **pr**                | `k pr [prompt] [--confirm] [--clipboard] [--paste]`              | Generates a pull request prompt based on your changes. If the --paste flag is used, the prompt is read from the clipboard instead of being supplied as an argument or via stdin. |
| **review**            | `k review [prompt] [--confirm]`                                | Constructs a code review prompt using the current directory tree and file contents, then prints the LLM's feedback.      |
| **run**               | `k run <subcommand> [args...]`                                 | Runs subcommands (e.g., `discord`, `indexer`, `tests`).                                                               |

#### Subcommands under `run`

- **discord**  
  Runs the Discord bot, allowing you to interact with AI agents via Discord.

- **indexer**  
  Indexes documents in your configured storage for quick searching and retrieval.

- **tests**    
  Executes the project test suite using pytest.

---

### Examples

1. **Transcribe an Audio File**  
   `k transcribe --path ~/recordings/todays_notes.wav`  
   This will produce a transcription for the audio file.

2. **Assimilate a Voice Memo**  
   `k assimilate --path ~/recordings/daily_update.wav`  
   This adds the transcribed memo into your daily note (for example, in Obsidian).

3. **Ask an AI Agent**  
   `k ask --agent_name search_agent --prompt "What's the weather like in San Francisco?"`  
   This sends the prompt to the specified agent.

4. **Generate a Pull Request**  
   `k pr [prompt] [--confirm] [--clipboard] [--paste]`  
   Generates a pull request prompt based on your changes. Use the --paste flag to read the prompt from the clipboard if desired.

5. **Generate a Code Review**  
   `k review [prompt] [--confirm]`  
   Constructs a code review prompt using the current directory structure and file contents, then outputs the LLM's feedback.

6. **Generate Code Advice**  
   `k advise --prompt "Refactor my authentication module for better performance."`  
   Generates detailed code advice and suggestions for improving your project based on the provided prompt.

7. **Build Troubleshooting Prompt**  
   Copy a traceback to your clipboard, then run `k traceback`  
   This extracts file references and source code snippets from the traceback to build a comprehensive troubleshooting prompt.

8. **Initialize .k Directory**  
   `k init`  
   Creates a new .k directory with default templates (excludes.txt, includes.txt, rules.txt). Use this command if the directory does not already exist or to reset its contents.

9. **Run Discord Bot**  
   `k run discord`  
   Launches the Discord bot. Ensure your environment variables include your Discord bot token.

---

## Configuration

- **K_PATH Environment Variable**  
  Ensure that the `K_PATH` environment variable is set to the absolute path of the project root directory. This variable is critical for proper resolution of configuration files and resources within the application.

- **Application-wide Settings**  
  Configured via the `.env` file, which is read by `application/config` and injected into service constructors via the dependency injection container in `infrastructure/di`.

- **services.yaml**  
  Declares services like the transcriber, search engine, and other integrations.

- **commands.yaml**  
  Defines CLI commands, their help text, execution targets, and accepted arguments.

---

## Extending k

1. **Add a New Python Dependency**
   - Update `requirements.in` with the new dependency.
   - Run `pip-compile requirements.in --strip-extras` to update `requirements.txt`.
   - Install with `pip install -r requirements.txt`.

2. **Add a New Command**
   - Create or update a use case in the appropriate `application/...` folder.
   - Reference this use case in `commands.yaml` by specifying a target (e.g., `@agency.some_use_case.execute`).

3. **Add a New AI Agent**
   - Implement the agent logic in the `infrastructure/agency/agents` folder.
   - Register the agent in `services.yaml` and tag it appropriately for inclusion in the agent registry.

4. **Add a New Service**
   - Create the service class (e.g., a new transcriber or search engine) in the `infrastructure/` layer.
   - Update `services.yaml` and register the service in the dependency injection container.

---

## Running Tests

This project uses pytest as its testing framework. A basic test scaffold is provided.

1. Ensure pytest is installed:
   ```
   pip install pytest
   ```

2. From the project root, run:
   ```
   pytest
   ```

All tests in the `tests` directory will be automatically discovered and executed.

---

## Additional Information

For more details on the project architecture, dependency injection, and service configuration, please refer to the inline comments in the source code.

---

## Using k to update itself

Occasionally, bugs may occur that prevent followup pull request calls from succeeding. If you encounter such issues while attempting to update k, consider the following process:

1. Create a new work-in-progress (WIP) branch and commit your changes there.
2. Switch back to the main branch.
3. In a separate clone of the repository (for example, in a directory named `k-working`), pull the WIP branch.
4. Use the stable k from the main branch to incrementally update the k-working project.

This approach ensures that you can continue making updates even if k experiences intermittent issues.

---

Happy Coding!
