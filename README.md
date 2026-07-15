# Tobii Client-Server

Client-server set-up for Tobii Pro Nano gaze data.

## Server Set-up
The server has only been tested with the Tobii Pro Nano connected to the lab's Dell Inspiron 14 5000 laptop running Windows 10.

1. Plug in the Tobii Pro Nano to the Dell laptop.
2. Clone the repo.
    ```
    git clone https://github.com/mycalize/tobii-client-server.git
    cd tobii-client-server
    ```
3. Update project environment and include dependencies from the server extra.
    ```
    uv sync --extra server
    ```
4. Run the server script.
    ```
    uv run server
    ```

## Client Set-up
The client has only been tested on Ubuntu 24.04 and macOS 15.2. The instructions assume that you are adding the gaze client to a [uv](https://docs.astral.sh/uv/) project.

1. Add library as dependency to your project.
    ```
    uv add git+https://github.com/mycalize/tobii-client-server.git
    ```
2. See example usage in [run_client.py](src/tobii_client_server/scripts/run_client.py).