# k

**k** is a personal command-line interface (CLI) tool designed to help me automate and streamline tasks like transcribing audio files, assimilating voice memos into notes, prompting AI agents, and more. It leverages a variety of services and integrations (OpenAI, Amazon Transcribe, Discord bots, etc.) to provide a flexible, extensible system for personal productivity and note management.

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

---

## Features

- **Voice Memo Assimilation**: Record daily voice notes and assimilate them into a central note for easy retrieval.  
- **Audio Transcription**: Transcribe audio files using external services (e.g., AWS Transcribe or OpenAI Whisper).  
- **AI Agent Integration**: Prompt AI agents for Q&A, search, scheduling tasks, or more advanced use cases.  
- **Document Indexing**: Index local documents and notes for quick searching.  
- **Discord Bot**: Run a Discord bot that can leverage your AI agents and indexing capabilities.
- **Code Review**: Generate code review feedback by analyzing your project's directory structure and file contents.

---

## Requirements

- **Python 3.8+** (Ensure you have a compatible version installed.)  
- Pipenv or virtualenv (recommended) for Python dependency management

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
     
   - Copy `.env.example` to `.env` and set these variables for local development

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

| Command        | Usage Example                                                  | Description                                                                   |
| -------------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **init**       | `k init`                                                     | Initializes the .k directory with default configuration templates.            |
| **assimilate** | `k assimilate --path /path/to/audio.wav`                       | Assimilates a voice memo into your daily note (requires a local audio file).    |
| **transcribe** | `k transcribe --path /path/to/audio.wav`                       | Transcribes the given audio file.                                             |
| **ask**        | `k ask --agent_name search_agent --prompt "Hello!"`           | Prompts an AI agent with a given text input.                                  |
| **pr**         | `k pr [prompt] [--confirm] [--clipboard] [--paste]`              | Generates a pull request prompt based on your changes. If the --paste flag is used, the prompt is read from the clipboard instead of being provided as an argument or via stdin.                        |
| **review**     | `k review [prompt] [--confirm]`                                | Constructs a code review prompt using the current directory tree and file contents, then prints the LLM's feedback to the console. |
| **run**        | `k run <subcommand> [args...]`                                 | Runs subcommands (e.g., `discord` or `indexer`).                                |

#### Subcommands under `run`

- **discord**  
  Runs the Discord bot, which can respond to user prompts using your AI agents.

- **indexer**  
  Indexes documents in your configured storage for quick searching and retrieval.

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
   Generates a pull request prompt based on your changes. If you use the --paste flag, the prompt will be read from the clipboard instead of being supplied as an argument or via stdin.

5. **Generate a Code Review**  
   `k review [prompt] [--confirm]`  
   Constructs a code review prompt using the current directory tree and file contents, then prints the LLM's feedback to the console.

6. **Initialize .k Directory**  
   `k init`  
   Creates a new .k directory with default templates (excludes.txt, includes.txt, rules.txt). Use this command if the directory does not already exist or to reset its contents.

7. **Run Discord Bot**  
   `k run discord`  
   This starts the Discord bot. Ensure your environment variables contain your bot token.

---

## Configuration

- **K_PATH Environment Variable**  
  Ensure that the `K_PATH` environment variable is set to the absolute path of the project root directory. This variable is critical for proper resolution of configuration files and resources within the application.

- **Application-wide Settings**  
  Configured via the `.env` file, which is read by `application/config` and injected into service constructors through the dependency injection (DI) container in `infrastructure/di`.

- **services.yaml**  
  Declares services like the transcriber, search engine, or any other required integrations.

- **commands.yaml**  
  Defines CLI commands, their help text, the function to execute, and accepted arguments.

---

## Extending k

1. **Add a New Python Dependency**
   - Update `requirements.in` with the python dependency you want to add.
   - Run `pip-compile requirements.in --strip-extras` to compile a new `requirements.txt` file.
   - Run `pip install -r requirements.txt` to install the dependencies.

2. **Add a New Command**  
   - Create or update a use case in the appropriate `application/...` folder.  
   - Reference that use case in `commands.yaml` by specifying a target that points to its DI container name (e.g., `@agency.some_use_case.execute`).

3. **Add a New AI Agent**  
   - Implement the agent logic in `infrastructure/agency/services/agents`.  
   - Register it in the DI container via `services.yaml`.
   - Tag it with `{ name: agent, alias: <alias> }` to include it in the agent registry.

4. **Add a New Service**  
   - Create a service class (e.g., a new search engine or transcriber) in the `infrastructure/` layer.  
   - Update `services.yaml` and the DI container with the new service definition.

---

## Running Tests

This project uses pytest as its testing framework. A basic test scaffold has been set up.

To run the tests:

1. Ensure you have pytest installed in your environment. You can install it using:

   ```
   pip install pytest
   ```

2. From the root directory of the project, run:

   ```
   pytest
   ```

All tests located in the `tests` directory will be automatically discovered and executed.

---

## Additional Information

For more details on the project architecture, dependency injection, and service configuration, please refer to the project documentation and inline comments within the source code.
