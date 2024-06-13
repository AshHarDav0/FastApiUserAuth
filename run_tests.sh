#!/bin/bash

# Extract the CONTAINER_NAME from the environment variables
CONTAINER_NAME=${CONTAINER_NAME}

# Run the tests inside the Docker container and redirect output to pytest.log
docker exec $CONTAINER_NAME python -m pytest --color=yes tests 2>&1 | tee tests/pytest.log

# Exit with the exit code of the pytest command
exit ${PIPESTATUS[0]}