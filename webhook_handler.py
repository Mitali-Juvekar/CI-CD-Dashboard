from flask import Blueprint, request, jsonify
import hmac
import hashlib
import json
import os
from build_worker import queue_build

webhook_bp = Blueprint('webhooks', __name__)

# Get this from environment variables in production
GITHUB_SECRET = "your_webhook_secret"

@webhook_bp.route('/github', methods=['POST'])
def github_webhook():
    """Handle GitHub push and pull request events"""
    
    # Verify signature
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_signature(request.data, signature):
        return jsonify({'error': 'Invalid signature'}), 403
    
    event = request.headers.get('X-GitHub-Event')
    payload = request.json
    
    if event == 'push':
        branch = payload['ref'].replace('refs/heads/', '')
        commit = payload['after']
        repo_name = payload['repository']['name']
        
        # Queue the build
        build_id = queue_build(branch, commit)
        
        return jsonify({
            'message': f'Build queued for {repo_name} on branch {branch}',
            'build_id': build_id
        })
        
    elif event == 'pull_request':
        action = payload['action']
        if action in ['opened', 'synchronize', 'reopened']:
            branch = payload['pull_request']['head']['ref']
            commit = payload['pull_request']['head']['sha']
            repo_name = payload['repository']['name']
            pr_number = payload['number']
            
            # Queue the build
            build_id = queue_build(branch, commit, f"PR-{pr_number}")
            
            return jsonify({
                'message': f'Build queued for PR #{pr_number} on {repo_name}',
                'build_id': build_id
            })
    
    return jsonify({'message': f'Event {event} ignored'})

def verify_signature(payload, signature):
    """Verify GitHub webhook signature"""
    if not signature:
        return False
    
    # Extract signature algorithm and hash
    algorithm, hash_value = signature.split('=')
    
    # Calculate expected hash
    expected = hmac.new(
        GITHUB_SECRET.encode(),
        payload,
        getattr(hashlib, algorithm.replace('sha', 'sha'))
    ).hexdigest()
    
    return hmac.compare_digest(hash_value, expected)