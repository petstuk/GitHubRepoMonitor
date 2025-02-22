import requests
import time
import json
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict

class GitHubMonitor:
    def __init__(self, token: str, repos: List[str], email_config: Dict[str, str], check_interval: int = 300):
        """
        Initialize the GitHub repository monitor.
        
        Args:
            token (str): GitHub personal access token
            repos (List[str]): List of repos in format "owner/repo"
            email_config (Dict[str, str]): Email configuration containing:
                - smtp_server: SMTP server address
                - smtp_port: SMTP port
                - sender_email: Email address to send from
                - sender_password: Email password or app-specific password
                - recipient_email: Email address to send notifications to
            check_interval (int): Time between checks in seconds (default: 300)
        """
        self.token = token
        self.repos = repos
        self.check_interval = check_interval
        self.email_config = email_config
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.last_commits: Dict[str, str] = {}
        
        # Load previous commit data if it exists
        self.data_file = 'last_commits.json'
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.last_commits = json.load(f)
    
    def _get_latest_commit(self, repo: str) -> dict:
        """Get the latest commit for a repository."""
        url = f'https://api.github.com/repos/{repo}/commits'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            commits = response.json()
            if commits:
                return commits[0]
        return None
    
    def _send_email_notification(self, repo: str, commit_info: dict, commit_sha: str):
        """Send an email notification about the new commit."""
        subject = f"New Push Detected - {repo}"
        
        body = f"""
        New push detected in {repo}
        
        Author: {commit_info['author']['name']}
        Date: {commit_info['author']['date']}
        Message: {commit_info['message']}
        
        Commit: https://github.com/{repo}/commit/{commit_sha}
        """
        
        msg = MIMEMultipart()
        msg['From'] = self.email_config['sender_email']
        msg['To'] = self.email_config['recipient_email']
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            with smtplib.SMTP(self.email_config['smtp_server'], int(self.email_config['smtp_port'])) as server:
                server.starttls()
                server.login(self.email_config['sender_email'], self.email_config['sender_password'])
                server.send_message(msg)
                print(f"Email notification sent for {repo}")
        except Exception as e:
            print(f"Failed to send email notification: {str(e)}")
    
    def _save_state(self):
        """Save the last known commit states to file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.last_commits, f)
    
    def check_updates(self):
        """Check for updates in all monitored repositories."""
        for repo in self.repos:
            try:
                latest_commit = self._get_latest_commit(repo)
                if not latest_commit:
                    print(f"Could not fetch commits for {repo}")
                    continue
                
                commit_sha = latest_commit['sha']
                last_known_sha = self.last_commits.get(repo)
                
                if last_known_sha != commit_sha:
                    # New commit detected
                    commit_info = latest_commit['commit']
                    author = commit_info['author']['name']
                    message = commit_info['message']
                    date = commit_info['author']['date']
                    
                    print(f"\nNew push detected in {repo}")
                    print(f"Author: {author}")
                    print(f"Date: {date}")
                    print(f"Message: {message}")
                    print(f"Commit: https://github.com/{repo}/commit/{commit_sha}")
                    
                    # Send email notification
                    self._send_email_notification(repo, commit_info, commit_sha)
                    
                    # Update the last known commit
                    self.last_commits[repo] = commit_sha
                    self._save_state()
            
            except Exception as e:
                print(f"Error checking {repo}: {str(e)}")
    
    def start_monitoring(self):
        """Start the continuous monitoring loop."""
        print(f"Starting to monitor repositories: {', '.join(self.repos)}")
        print(f"Checking every {self.check_interval} seconds")
        
        while True:
            self.check_updates()
            time.sleep(self.check_interval)

def main():
    # Configuration
    GITHUB_TOKEN = "your_github_token_here"
    REPOS_TO_MONITOR = [
        "owner1/repo1",
        "owner2/repo2"
    ]
    CHECK_INTERVAL = 300  # 5 minutes
    
    # Email Configuration
    EMAIL_CONFIG = {
        'smtp_server': 'smtp.gmail.com',  # For Gmail
        'smtp_port': '587',
        'sender_email': 'your_email@gmail.com',
        'sender_password': 'your_app_specific_password',  # Use app-specific password for Gmail
        'recipient_email': 'recipient@example.com'
    }
    
    # Create and start the monitor
    monitor = GitHubMonitor(
        token=GITHUB_TOKEN,
        repos=REPOS_TO_MONITOR,
        email_config=EMAIL_CONFIG,
        check_interval=CHECK_INTERVAL
    )
    
    monitor.start_monitoring()

if __name__ == "__main__":
    main()
