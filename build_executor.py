import docker
import os
import tempfile
import shutil
import git
from models import Build, TestResult
from app import Session
from datetime import datetime

class BuildExecutor:
    def __init__(self, build_id):
        self.build_id = build_id
        self.session = Session()
        self.build = self.session.query(Build).filter(Build.id == build_id).first()
        self.client = docker.from_env()
        self.workspace = tempfile.mkdtemp()
        
    def execute(self):
        """Execute the build process"""
        if not self.build:
            print(f"Build {self.build_id} not found")
            return
        
        self.build.status = 'running'
        self.session.commit()
        
        try:
            # Clone repository
            self._clone_repository()
            
            # Parse build configuration
            config = self._parse_config()
            
            # Run build steps
            self._run_build_steps(config)
            
            # Run tests
            test_results = self._run_tests(config)
            
            # Process results
            success = all(test.get('result') == 'passed' for test in test_results)
            self.build.status = 'success' if success else 'failure'
            
        except Exception as e:
            self.build.status = 'error'
            self.build.test_results = f"Error: {str(e)}"
            print(f"Build error: {e}")
        finally:
            self.build.duration = (datetime.now() - self.build.timestamp).total_seconds()
            self.session.commit()
            self._cleanup()
    
    def _clone_repository(self):
        """Clone the repository to workspace"""
        # In a real system, we'd use actual repository URL
        # git.Repo.clone_from(
        #     f"https://github.com/username/{xyz}.git",
        #     self.workspace,
        #     branch=self.build.branch
        # )
        
        # For demo, just creating some dummy files
        os.makedirs(os.path.join(self.workspace, 'tests'))
        with open(os.path.join(self.workspace, 'requirements.txt'), 'w') as f:
            f.write("pytest==7.0.0\n")
        
        with open(os.path.join(self.workspace, 'tests/test_example.py'), 'w') as f:
            f.write("""
def test_success():
    assert True

def test_failure():
    assert False
""")
    
    def _parse_config(self):
        """Parse build configuration"""
        # In a real system, we'd load from .build-config.yml
        return {
            'build': {
                'image': 'python:3.9',
                'steps': [
                    'pip install -r requirements.txt',
                    'python -m pytest'
                ]
            },
            'test': {
                'unit': {
                    'command': 'pytest tests/ -v',
                    'timeout': 300
                }
            }
        }
    
    def _run_build_steps(self, config):
        """Run build steps in Docker container"""
        image = config['build']['image']
        steps = config['build']['steps']
        
        for step in steps:
            print(f"Running build step: {step}")
            # In a real system, we'd run this in Docker
            # self.client.containers.run(
            #     image,
            #     command=step,
            #     volumes={self.workspace: {'bind': '/workspace', 'mode': 'rw'}},
            #     working_dir='/workspace'
            # )
            
            # For demo, just log it
            print(f"Would run '{step}' in {image}")
    
    def _run_tests(self, config):
        """Run tests and return results"""
        test_results = []
        
        for test_name, test_config in config['test'].items():
            print(f"Running test: {test_name}")
            command = test_config['command']
            
            # In a real system, we'd run this in Docker and parse output
            # For demo, adding some simulated results
            result = 'passed' if test_name != 'failure_test' else 'failed'
            execution_time = 5.2
            
            test_result = TestResult(
                build_id=self.build_id,
                test_name=test_name,
                result=result,
                execution_time=execution_time
            )
            self.session.add(test_result)
            test_results.append({
                'name': test_name,
                'result': result,
                'execution_time': execution_time
            })
        
        self.session.commit()
        return test_results
    
    def _cleanup(self):
        """Clean up resources"""
        shutil.rmtree(self.workspace, ignore_errors=True)