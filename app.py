from flask import Flask, request, jsonify
import concurrent.futures
import time
from models import Build, TestResult
from db import Session
from build_worker import queue_build
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# # Set up the connection to your PostgreSQL database
# engine = create_engine('postgresql://mitalijuvekar:MiTuLi26%4002@localhost:5432/ci_metrics')
# Session = sessionmaker(bind=engine)

# Import the webhook blueprint
from webhook_handler import webhook_bp

# Register the blueprint
app.register_blueprint(webhook_bp, url_prefix='/webhooks')

# Add a simple web UI route for viewing builds
@app.route('/')
def home():
    """Render a simple dashboard UI"""
    return """
    <html>
        <head>
            <title>CI/CD Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .card { border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 4px; }
                .success { border-left: 5px solid green; }
                .failure { border-left: 5px solid red; }
                .running { border-left: 5px solid blue; }
                .queued { border-left: 5px solid orange; }
                button { padding: 10px; background: #4CAF50; color: white; border: none; cursor: pointer; }
            </style>
            <script>
                function triggerBuild() {
                    fetch('/api/trigger-build', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            branch: document.getElementById('branch').value
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        alert('Build triggered: ' + data.build_id);
                        location.reload();
                    });
                }
                
                function loadBuilds() {
                    fetch('/api/builds')
                    .then(response => response.json())
                    .then(builds => {
                        const container = document.getElementById('builds');
                        container.innerHTML = '';
                        
                        builds.forEach(build => {
                            const card = document.createElement('div');
                            card.className = `card ${build.status}`;
                            card.innerHTML = `
                                <h3>Build #${build.id}</h3>
                                <p>Status: ${build.status}</p>
                                <p>Duration: ${build.duration ? build.duration.toFixed(2) + 's' : 'N/A'}</p>
                                <p>Time: ${new Date(build.timestamp).toLocaleString()}</p>
                                <a href="/api/builds/${build.id}" target="_blank">View Details</a>
                            `;
                            container.appendChild(card);
                        });
                    });
                }
                
                window.onload = loadBuilds;
                setInterval(loadBuilds, 5000); // Refresh every 5 seconds
            </script>
        </head>
        <body>
            <h1>CI/CD Dashboard</h1>
            <div style="margin-bottom: 20px;">
                <h2>Trigger Build</h2>
                <input id="branch" placeholder="Branch name" value="main" />
                <button onclick="triggerBuild()">Start Build</button>
            </div>
            <h2>Recent Builds</h2>
            <div id="builds">Loading...</div>
        </body>
    </html>
    """

# Simulate the build process
def run_build(build_id):
    print(f"Running build {build_id}...")
    time.sleep(3)  # Simulate build time (e.g., 3 seconds)
    return f"Build {build_id} completed"

# Simulate running tests
def run_test(test_name):
    print(f"Running test {test_name}...")
    time.sleep(2)  # Simulate test execution time (e.g., 2 seconds)
    return f"Test {test_name} passed"

# Concurrent Build and Test Route
@app.route('/trigger-build-and-tests', methods=['POST'])
def trigger_build_and_tests():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Start the build process concurrently
        build_future = executor.submit(run_build, 1)
        
        # Start multiple tests concurrently
        test_futures = [executor.submit(run_test, f"test_{i}") for i in range(1, 4)]
        
        # Wait for the build and tests to complete and collect results
        build_result = build_future.result()  # This will block until the build is done
        test_results = [test.result() for test in test_futures]  # This blocks until all tests are complete

        # Store the build and test results in the database
        session = Session()
        new_build = Build(duration=100, status='success', test_results='pass')
        session.add(new_build)
        session.commit()

        # Return the results as a JSON response
        return jsonify({
            "message": "Build and tests completed successfully",
            "build_result": build_result,
            "test_results": test_results
        })
    
@app.route('/api/builds', methods=['GET'])
def get_builds():
    """Retrieve build history with optional filtering"""
    session = Session()
    try:
        limit = request.args.get('limit', 50, type=int)
        builds = session.query(Build).order_by(Build.timestamp.desc()).limit(limit).all()
        
        result = [{
            'id': build.id,
            'timestamp': build.timestamp,
            'duration': build.duration,
            'status': build.status,
            'test_results': build.test_results
        } for build in builds]
        
        return jsonify(result)
    finally:
        session.close() 

@app.route('/api/builds/<int:build_id>', methods=['GET'])
def get_build(build_id):
    """Get details for a specific build"""
    session = Session()
    try:
        build = session.query(Build).filter(Build.id == build_id).first()
        if not build:
            return jsonify({'error': 'Build not found'}), 404
        
        tests = session.query(TestResult).filter(TestResult.build_id == build_id).all()
        return jsonify({
            'id': build.id,
            'timestamp': build.timestamp,
            'duration': build.duration,
            'status': build.status,
            'test_results': build.test_results,
            'tests': [{
                'name': test.test_name,
                'result': test.result,
                'execution_time': test.execution_time
            } for test in tests]
        })
    finally:
        session.close()

@app.route('/api/trigger-build', methods=['POST'])
@cross_origin() 
def trigger_build():
    """Enhanced build trigger with more options"""
    data = request.json
    branch = data.get('branch', 'main')
    commit_hash = data.get('commit_hash', '')
    
    # Queue the build using a background worker
    build_id = queue_build(branch, commit_hash)
    
    return jsonify({
        "message": "Build queued successfully",
        "build_id": build_id
    })

if __name__ == '__main__':
    app.run(debug=True, port=5050)

