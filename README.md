# EE P 522 A Wi 23: Embedded And Real Time Systems

Final Project

## Objective

These are the codes for the final project of EEP 522, which showcase an API server running on a Raspberry Pi 4. For further details, please refer to the report.

## Rubrics

### Assignment 3
- (2) points for a clear outline of the project and project goals
- (2) points for the final conclusion and references
- (8) points for self-assessment of Assignment 2 characterization
- (2) points for applicability for either limited or mass production
- (3) points for the number of enhancements
- (8) points for difficulty level and engineering implemented
- (10) points for the quality of source code (design, structure, and testing)
- (5) extra points given for stretching beyond the normal project goals

### Presentation
- (3) title and objective
- (7) Characterization focus
- (10) Interesting discovery, observation, or missing features

## Installation

Please note that in order to run the codes, Poetry is required. Kindly refer to the report for guidance on installing Poetry.

Clone the codes and switch to project root, then install the dependencies:

```shell
poetry install
```

### Server Health Check

In order to run this example module, you will need an API key from OpenAI. Please refer to :

[Where do I find my Secret API Key?](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)

Create a `.env` file in the project root if there isn't one and add the following config:

```plaintext
OPENAI_API_KEY="YOUR_API_KEY"
```

#### ./server_health_check/config.py

There are some variables that you can change in the `config.py` file:

- CHECK_INTERVAL: the interval between each health check in seconds
- LOG_LIMIT: the maximum number of logs to keep in the file

### SFTP Operations

In order to run this example module, you will need to grab the SFTP credentials from a server. I recommend using one of the following public SFTP servers or UW SFTP server:

[Free Public SFTP Servers](https://www.sftp.net/public-online-sftp-servers)

Create a `.env` file in the project root if there isn't one and add the following config:

```plaintext
SFTP_HOST="test.rebex.net"
SFTP_USERNAME="demo"
SFTP_PASSWORD="password"
SFTP_PORT=22
```

The username and password here are for a public demo server. However, this server foibids file upload. In the end I used my own account on UW SFTP server (sftp.udrive.uw.edu) to be able to test the full functionality.

#### ./sftp_manager/config.py

There are some variables that you can change in the `config.py` file:

- BACKUP_FILE_PATH: the path to store the backup files
- BACKUP_FILE_SIZE_LIMIT_BYTES: the maximum size of a backup file in bytes; if exceeded, the file will not be backed up

## Running the server

### Commands

Start the server with Python:

```shell
poetry run python main.py
```

Start the server with uvicorn:

```shell
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000  # debug mode
poetry run uvicorn main:app --workers 5 --host 0.0.0.0 --port 8000  # production mode (refer to https://www.uvicorn.org/deployment/)
```

## API Documentation

To see the API documentation, please visit the following link: http://YOUR_SERVER_IP:8000/docs. The server needs to be running in order to access the documentation.
