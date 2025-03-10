# CI/CD Metrics Dashboard

A comprehensive CI/CD pipeline monitoring system that tracks build performance, test results, and provides real-time insights for development teams.

## Overview

This project provides a complete CI/CD metrics solution that includes:

- A backend API for managing build and test data
- GitHub webhook integration for automatic build triggering
- Real-time metrics visualization with Grafana
- A simple web UI for manual build triggering and monitoring

The system is designed to help development teams identify bottlenecks in their build and test processes, track build reliability, and make data-driven decisions about their CI/CD infrastructure.

## Key Features

- **Build Tracking**: Monitor the performance and status of all builds
- **Test Result Analysis**: Track test success rates and execution times
- **Metrics Visualization**: View trends and patterns in your build pipeline
- **GitHub Integration**: Automatically trigger builds from code changes
- **Docker-Based Execution**: Run builds in isolated containers

## Technologies Used

- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Visualization**: Grafana
- **Build Execution**: Docker
- **CI/CD Integration**: GitHub webhooks

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL 13+
- Docker
- Grafana

### Database Setup

1. Create a PostgreSQL database:
```bash
createdb ci_metrics
```

2. Update the connection string in db.py with your database credentials

3. Run the database migration:
```bash
python migrate_db.py
```

### Application Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the Flask application:
```bash
python app.py
```

3. Access the web UI at http://localhost:5000

### Grafana Setup

1. Install and start Grafana
2. Add a PostgreSQL data source pointing to your ci_metrics database
3. Set up dashboards to visualize build metrics

### Dashboard Metrics
The Grafana dashboard provides the following key metrics:

- Build Success Rate: Percentage of successful builds over time
- Build Duration Trends: How build times are changing over time
- Test Execution Time: Performance of individual tests
- Top Failing Tests: Tests with the highest failure rates
- Average Build Duration by Day of Week: Identify patterns in build performance

### Architecture
The system consists of the following components:

1. Flask Backend: Provides REST APIs for storing and retrieving build and test data
2. PostgreSQL Database: Stores all build metadata, test results, and performance metrics
3. Build Worker: Executes builds in isolated Docker containers
4. Webhook Handler: Processes GitHub events to trigger builds automatically
5. Grafana Dashboard: Visualizes build metrics and trends
6. Web UI: Provides a simple interface for triggering and monitoring builds

### Future Enhancements
- Build caching for faster execution
- Test parallelization
- Branch and PR-specific metrics
- Failure analysis with machine learning
- Integration with other CI systems (Jenkins, CircleCI)
- Email/Slack notifications for build failures

Grafana dashboard:
<img width="1469" alt="Grafana_ss" src="https://github.com/user-attachments/assets/f4ecceca-a489-4a26-a1aa-28f2ab9f8725" />
