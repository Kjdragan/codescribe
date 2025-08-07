#!/usr/bin/env python3
"""
OAuth2 authentication helper for Google Cloud services.
This handles the OAuth flow for accessing Vertex AI with LangExtract.
"""

import os
import json
from pathlib import Path
from typing import Optional

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print("❌ Google auth libraries not installed. Run: uv add google-auth google-auth-oauthlib google-auth-httplib2")
    exit(1)

# Scopes required for Vertex AI access
SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/generative-language'
]

class OAuthHelper:
    """Helper class for managing OAuth2 authentication with Google Cloud."""
    
    def __init__(self, project_root: str = "."):
        """Initialize OAuth helper with project root directory."""
        self.project_root = Path(project_root)
        self.credentials_file = self.project_root / "credentials.json"
        self.token_file = self.project_root / "token.json"
    
    def get_credentials(self) -> Optional[Credentials]:
        """Get valid OAuth2 credentials, refreshing or creating as needed."""
        creds = None
        
        # Load existing token if available
        if self.token_file.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(self.token_file), SCOPES)
                print("✅ Loaded existing OAuth credentials")
            except Exception as e:
                print(f"⚠️  Error loading existing credentials: {e}")
                creds = None
        
        # If there are no valid credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    print("✅ Refreshed OAuth credentials")
                except Exception as e:
                    print(f"⚠️  Error refreshing credentials: {e}")
                    creds = None
            
            if not creds:
                creds = self._run_oauth_flow()
        
        # Save the credentials for the next run
        if creds:
            self._save_credentials(creds)
            return creds
        
        return None
    
    def _run_oauth_flow(self) -> Optional[Credentials]:
        """Run the OAuth2 flow to get new credentials."""
        if not self.credentials_file.exists():
            print(f"❌ Credentials file not found: {self.credentials_file}")
            print("Please download your OAuth2 credentials from Google Cloud Console:")
            print("https://console.cloud.google.com/apis/credentials")
            return None
        
        try:
            print("🔐 Starting OAuth2 flow...")
            print("A browser window will open for authentication.")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(self.credentials_file), SCOPES
            )
            creds = flow.run_local_server(port=0)
            print("✅ OAuth2 authentication completed!")
            return creds
            
        except Exception as e:
            print(f"❌ OAuth2 flow failed: {e}")
            return None
    
    def _save_credentials(self, creds: Credentials) -> None:
        """Save credentials to token file."""
        try:
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
            print(f"✅ Credentials saved to {self.token_file}")
        except Exception as e:
            print(f"⚠️  Error saving credentials: {e}")
    
    def setup_environment(self) -> bool:
        """Set up environment variables for Google Cloud authentication."""
        creds = self.get_credentials()
        if not creds:
            return False
        
        # Set environment variable for Google Cloud authentication
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(self.token_file)
        print("✅ Environment configured for Google Cloud authentication")
        return True
    
    def clear_credentials(self) -> None:
        """Clear stored credentials (for troubleshooting)."""
        if self.token_file.exists():
            self.token_file.unlink()
            print("✅ Cleared stored credentials")
        else:
            print("ℹ️  No stored credentials to clear")

def main():
    """Test the OAuth helper."""
    print("🧪 Testing OAuth2 setup...")
    helper = OAuthHelper()
    
    if helper.setup_environment():
        print("🎉 OAuth2 setup successful!")
        print("You can now use Vertex AI with LangExtract.")
    else:
        print("❌ OAuth2 setup failed.")
        print("Make sure you have downloaded credentials.json from Google Cloud Console.")

if __name__ == "__main__":
    main()
