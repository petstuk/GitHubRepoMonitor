# GitHub Repository Monitor

Python script that monitors GitHub repositories and sends email notifications for new commits. Uses GitHub API to track changes across multiple repos, with configurable check intervals and email notifications. Perfect for staying updated on repository changes without manual checking.

## Features

* Real-time monitoring of multiple GitHub repositories
* Email notifications with detailed commit information
* Persistent state tracking to prevent duplicate notifications
* Configurable check intervals
* Support for various email providers

## Requirements

* Python 3.6+
* `requests` library

## Quick Start

1. Install required packages:
   ```bash
   pip install requests
   ```

2. Configure GitHub token and repositories:
   ```python
   GITHUB_TOKEN = "your_github_token_here"
   REPOS_TO_MONITOR = [
       "owner1/repo1",
       "owner2/repo2"
   ]
   ```

3. Set up email configuration:
   ```python
   EMAIL_CONFIG = {
       'smtp_server': 'smtp.gmail.com',
       'smtp_port': '587',
       'sender_email': 'your_email@gmail.com',
       'sender_password': 'your_app_specific_password',
       'recipient_email': 'recipient@example.com'
   }
   ```

4. Run the script:
   ```bash
   python github_monitor.py
   ```

## Detailed Setup

### GitHub Token Setup

1. Navigate to GitHub Settings → Developer Settings → Personal Access Tokens
2. Click "Generate new token" and select the `repo` scope
3. Copy the generated token
4. Replace `your_github_token_here` in the script with your token

### Email Configuration

#### Gmail Setup
1. Enable 2-Step Verification in your Google Account
2. Generate an App Password:
   * Go to Google Account Settings → Security
   * Find "App Passwords" under 2-Step Verification
   * Select "Other" as the app and generate password
   * Use this password in the EMAIL_CONFIG

#### Other Email Providers

Common SMTP configurations:

| Provider | Server | Port |
|----------|--------|------|
| Gmail | smtp.gmail.com | 587 |
| Outlook | smtp-mail.outlook.com | 587 |
| Yahoo | smtp.mail.yahoo.com | 587 |
| AOL | smtp.aol.com | 587 |
| iCloud | smtp.mail.me.com | 587 |

## How It Works

The script:
* Checks repositories at specified intervals
* Compares latest commit with last known state
* Sends email notifications for new commits
* Saves state to prevent duplicate notifications
* Handles errors gracefully

## Error Handling

The script includes robust error handling for:
* Failed GitHub API requests
* Email sending failures
* Network connectivity issues
* Invalid repository names
* Authentication problems

## License

This project is released under the MIT License.

## Contributing

Feel free to:
* Open issues for bugs or suggestions
* Submit pull requests with improvements
* Fork the project for your own use

## Support

If you encounter any issues:
1. Check the error messages in the console
2. Verify your configuration settings
3. Ensure all credentials are correct
4. Check your network connection
