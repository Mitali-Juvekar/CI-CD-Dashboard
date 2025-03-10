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
