from locust import HttpUser, task, between, events
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MicroserviceLoadTest(HttpUser):
    # Configure host
    host = "http://127.0.0.1:3000"

    # Moderate wait time to reduce connection stress
    wait_time = between(0.1, 0.5)

    def on_start(self):
        """
        Setup method to log connection attempts
        """
        logger.info(f"Attempting to connect to {self.host}")

    @task
    def test_endpoint(self):
        """
        Robust endpoint testing with detailed error handling
        """
        try:
            # Increase timeout to prevent premature connection drops
            response = self.client.get("/", timeout=5)
            
            # Log successful requests
            if response.status_code == 200:
                logger.debug("Successful request")
            else:
                logger.error(f"Request failed with status code: {response.status_code}")
        except Exception as e:
            logger.error(f"Connection error: {e}")

# Event listeners for comprehensive logging
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    logger.info("Load test starting...")
    # Reduce initial target to find sustainable load
    environment.target_requests_per_second = 5000

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    logger.info("Load test completed.")
    logger.info(f"Total requests: {environment.stats.total.num_requests}")
    logger.info(f"Failed requests: {environment.stats.total.num_failures}")

# Recommended CLI command with more gradual load
# locust -f locust_test.py --headless -u 50 -r 10 -t 60s

# Debugging and optimization recommendations:
# 1. Check microservice configuration:
#    - Increase worker threads
#    - Configure connection pool
#    - Set appropriate timeout values
# 2. System-level optimizations:
#    - Increase file descriptor limits
#    - Optimize network settings
#    - Use a reverse proxy like Nginx for load balancing
