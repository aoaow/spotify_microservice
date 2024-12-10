# IDS706 - Final Project - Spotify Microservice

## Microservice and Core Development Documentation

### Summary of Completed Work:

**1. Core Microservice Implementation**
- Technology: Python (Flask framework).
- Endpoints:
  1. `/rankings`: Fetch top-ranked tracks by region and date.
  2. `/artist`: Retrieve track data for a specific artist.
- Optimizations:
  - Cached grouped data for faster query performance.
  - Optimized database filtering and ranking logic.
- Tested Functionality:
  - Successfully tested all endpoints locally and within a Docker container.

**2. Logging**
- Integrated structured logging to track:
  - Incoming requests (parameters, endpoints).
  - Errors and debug information.
- Logs are written to both the console and a file (`app.log`).
- Verified correctness during various test scenarios.


**3. Dockerization**
- Created a production-ready Dockerfile:
  - Uses `gunicorn` as a WSGI server for performance.
  - Handles dependency installation (`requirements.txt`).
  - Exposes port 5000 for microservice access.
- Verified the Docker image works as expected locally.

**Note: When to Rebuild the Docker Image?**
- If any of the following files are updated:
    - `app.py` (microservice logic).
    - `requirements.txt` (dependencies).
    - `Dockerfile` (image configuration).
    - Dataset file (e.g., `spotify_top_200.parquet`) if it is embedded within the image.
- Rebuild the Docker image with:
    ```bash
    docker build -t spotify_microservice .
    ```
- After rebuilding, test the new image by running:
    ```bash
    docker run -p 5000:5000 spotify_microservice
    ```

**4. Load Testing**
- Wrote a `locustfile.py` script to simulate concurrent requests:
  - Tested with ~2000 RPS locally (limited by hardware).
  - Achieved <5% failure rate after performance tuning.
  - Identified scaling limitations for 10,000 RPS, which requires cloud deployment.

---

### Pending Work - Scale to 10,000 Requests per Second
- The microservice currently achieves ~2000 RPS locally due to hardware limits.
- Recommended Next Steps:
  - Deploy to AWS or Azure for load balancing and auto-scaling.
  - Use cloud-based tools (e.g., AWS Elastic Beanstalk, Azure App Service) to handle higher RPS.
  - Configure additional caching or database replication if necessary.

---

### Files and Their Purposes
1. `app.py`: The Flask microservice implementation.
2. `locustfile.py`: Load testing script for simulating requests.
3. `Dockerfile`: Defines the Docker image for production deployment.
4. `requirements.txt`: Python dependencies for the microservice.
5. `data.py`: Script for preparing and transforming the dataset.
6. `spotify_top_200.parquet`: Preprocessed dataset for use in the microservice.

---
### How to Test Locally
1. Run the microservice:
   - Open a terminal and run:
     ```bash
     python app.py
     ```
   - This starts the Flask application. Access endpoints at `http://127.0.0.1:5000`.

2. Run load tests:
   - Open a **second terminal** and run:
     ```bash
     locust -f locustfile.py
     ```
   - This starts the Locust load testing framework. Access the monitoring interface at `http://127.0.0.1:8089`.

   **Note**: Make sure to run `app.py` and `locustfile.py` in two separate terminals to avoid interruptions and ensure both processes are running simultaneously!!!

3. Run the Docker container:
   - Alternatively, to test the Dockerized version:
     ```bash
     docker run -p 5000:5000 spotify_microservice
     ```
   - Access the application at `http://127.0.0.1:5000`.

4. Rebuild the Docker Image (if required):
   - If you modify any code or configuration:
     ```bash
     docker build -t spotify_microservice .
     ```
   - Test the updated image using the steps above.

---
### Final Repository Link:
https://github.com/nogibjj/IDS706_Final_Spotify_Microservice