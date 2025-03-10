import time
import subprocess
import os
from models import Build, TestResult
from db import Session
from datetime import datetime

def queue_build(branch, commit_hash):
    """Queue a build for processing"""
    session = Session()
    try:
        # Create a dict of parameters that definitely exist
        build_data = {
            'timestamp': datetime.now(),
            'status': 'queued'
        }
        
        try:
            build_data['branch'] = branch
            build_data['commit_hash'] = commit_hash
        except:
            # If these columns don't exist yet proceed regardless
            pass
            
        new_build = Build(**build_data)
        session.add(new_build)
        session.commit()
        
        # Return the ID
        return new_build.id
    finally:
        session.close()

def process_build(build_id):
    """Process a queued build"""
    session = Session()
    build = session.query(Build).filter(Build.id == build_id).first()
    
    if not build or build.status != 'queued':
        return
    
    # Update build status
    build.status = 'running'
    session.commit()
    
    start_time = time.time()
    
    try:
        # Clone repository (simplified)
        # subprocess.run(['git', 'clone', '--branch', build.branch, REPO_URL, 'workspace'])
        
        # Run build steps (simplified)
        # subprocess.run(['cd', 'workspace', '&&', 'npm', 'install'])
        # subprocess.run(['cd', 'workspace', '&&', 'npm', 'run', 'build'])
        
        # Run tests and collect results
        # test_output = subprocess.run(['cd', 'workspace', '&&', 'npm', 'test', '--json'], capture_output=True)
        # parse_and_store_test_results(build_id, test_output.stdout)
        
        # For demo purposes, we'll simulate this
        time.sleep(3)  # Simulate build time
        
        # Add some test results
        test_names = ['test_functionality', 'test_performance', 'test_security']
        for test_name in test_names:
            result = 'passed' if time.time() % 4 != 0 else 'failed'  # Random pass/fail
            test_time = float(f"{(time.time() % 10) + 5:.2f}")  # Random time between 5-15 seconds
            
            test_result = TestResult(
                build_id=build_id,
                test_name=test_name,
                result=result,
                execution_time=test_time
            )
            session.add(test_result)
        
        # Update build status to success
        build.status = 'success' if time.time() % 5 != 0 else 'failure'  # Occasional failure
        
    except Exception as e:
        build.status = 'error'
        build.test_results = f"Error: {str(e)}"
    finally:
        # Record duration and finish
        build.duration = time.time() - start_time
        session.commit()