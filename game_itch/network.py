
import requests
import json
import time
import sys
import os
import threading

class LeaderboardClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LeaderboardClient, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
             return
             
        # =================================================================================
        # TODO: USER MUST REPLACE THESE WITH THEIR OWN SUPABASE CREDENTIALS
        # Go to https://supabase.com/dashboard/project/_/settings/api
        # =================================================================================
        self.url = "https://vcqspffrjvokfjpyqoqt.supabase.co"
        self.key = "sb_publishable_fW_PlOUrdlI-wtr3x9gcFQ_QkQVJppG"
        # =================================================================================
        
        self.session = None
        self.user = None
        self.access_token = None
        self.is_offline = True

        # Profanity Filter List (Basic)
        self.banned_words = ["badword", "admin", "null", "fuck", "shit", "bitch", "ass", "cunt"] 
        
        self.init_client()
        self.initialized = True

    def init_client(self):
        if "Replace" in self.url:
            print("[Network] Supabase credentials not configured. Offline mode.")
            self.is_offline = True
            return

        # Simple ping check
        if not self.check_connection():
            print("[Network] No internet connection. Offline mode.")
            self.is_offline = True
        else:
            self.is_offline = False
            print("[Network] Ready (Online)")

    def check_connection(self):
        try:
            requests.get("https://www.google.com", timeout=2)
            return True
        except:
            return False
            
    def contains_profanity(self, text):
        if not text: return False
        text_lower = text.lower()
        for word in self.banned_words:
            if word in text_lower:
                return True
        return False

    def _get_headers(self, authenticated=False):
        headers = {
            "apikey": self.key,
            "Content-Type": "application/json",
            "Prefer": "return=representation"  # Returns created objects
        }
        if authenticated and self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        else:
             headers["Authorization"] = f"Bearer {self.key}"
        return headers

    def _get_session_path(self):
        """Determines the correct path for session.json in both dev and EXE."""
        if getattr(sys, 'frozen', False):
            # Running as EXE
            base_path = os.path.dirname(sys.executable)
        else:
            # Running as Script
            base_path = os.path.abspath(".")
        return os.path.join(base_path, "session.json")

    def signup(self, email, password, data=None):
        if self.is_offline: return {"error": "Offline Mode"}
        
        endpoint = f"{self.url}/auth/v1/signup"
        payload = {
            "email": email,
            "password": password
        }
        if data:
            payload["data"] = data
            
        try:
            response = requests.post(endpoint, json=payload, headers=self._get_headers())
            
            data = response.json()
            if response.status_code == 200:
                self.user = data.get("user")
                self.access_token = data.get("access_token")
                # Store session data if needed
                return {"success": True, "user": self.user}
            else:
                return {"error": data.get("msg", data.get("error_description", "Signup Failed"))}
        except Exception as e:
            return {"error": str(e)}

    def login(self, email, password):
        if self.is_offline: return {"error": "Offline Mode"}
        
        endpoint = f"{self.url}/auth/v1/token?grant_type=password"
        try:
            response = requests.post(endpoint, json={
                "email": email,
                "password": password
            }, headers=self._get_headers())
            
            data = response.json()
            if response.status_code == 200:
                self.access_token = data.get("access_token")
                self.user = data.get("user")
                return {"success": True, "user": self.user}
            else:
                return {"error": data.get("error_description", "Login Failed")}
        except Exception as e:
            return {"error": str(e)}

    def logout(self):
        endpoint = f"{self.url}/auth/v1/logout"
        if self.access_token and not self.is_offline:
            try:
                requests.post(endpoint, headers=self._get_headers(authenticated=True))
            except:
                pass
        self.access_token = None
        self.user = None
        # Clear session file
        try:
            path = self._get_session_path()
            if os.path.exists(path):
                os.remove(path)
        except:
            pass

    def reset_password(self, email):
        """Sends a password reset email via REST API."""
        if self.is_offline:
            print("[Network] Offline. Cannot reset password.")
            return False
            
        endpoint = f"{self.url}/auth/v1/recover"
        try:
            response = requests.post(endpoint, json={
                "email": email
            }, headers=self._get_headers())
            
            if response.status_code == 200:
                print(f"[Network] Password reset email sent to {email}")
                return True
            else:
                print(f"[Network] Reset Failed: {response.text}")
                return False
        except Exception as e:
            print(f"[Network] Reset Error: {e}")
            return False

    def verify_otp(self, email, token):
        """Verifies the recovery token and logs the user in (temporary session)."""
        if self.is_offline: return {"error": "Offline"}
        
        endpoint = f"{self.url}/auth/v1/verify"
        try:
            payload = {
                "type": "recovery",
                "email": email,
                "token": token
            }
            response = requests.post(endpoint, json=payload, headers=self._get_headers())
            data = response.json()
            
            if response.status_code == 200:
                self.access_token = data.get("access_token")
                self.user = data.get("user")
                return {"success": True}
            else:
                return {"error": data.get("error_description", "Invalid Token")}
        except Exception as e:
            return {"error": str(e)}

    def update_password(self, new_password):
        """Updates the password for the currently logged-in user."""
        if self.is_offline or not self.access_token:
             return {"error": "Not logged in"}
             
        endpoint = f"{self.url}/auth/v1/user"
        try:
            payload = {
                "password": new_password
            }
            response = requests.put(endpoint, json=payload, headers=self._get_headers(authenticated=True))
            
            if response.status_code == 200:
                # Password updated!
                # Usually good practice to refresh session, but existing token should still work or might be revoked?
                # Using the data returned to update user
                self.user = response.json()
                self.save_session()
                return {"success": True}
            else:
                error_msg = response.json().get("msg", response.text)
                return {"error": error_msg}
        except Exception as e:
            return {"error": str(e)}

    def update_profile(self, new_username):
        """Updates the user's display name."""
        if self.is_offline or not self.user:
            return False
        
        endpoint = f"{self.url}/auth/v1/user"
        try:
            # Update user_metadata via the /user endpoint
            payload = {
                "data": {"display_name": new_username}
            }
            response = requests.put(endpoint, json=payload, headers=self._get_headers(authenticated=True))
            
            if response.status_code == 200:
                self.user = response.json()
                self.save_session()
                print(f"[Network] Username updated to {new_username}")
                return True
            else:
                 print(f"[Network] Update Profile Failed: {response.text}")
                 return False

        except Exception as e:
             print(f"[Network] Update Profile Error: {e}")
             return False

    def get_user_name(self):
        if self.user and self.user.user_metadata:
             return self.user.user_metadata.get('display_name', 'Player')
        return "Player" # Default

    def save_session(self):
        if not self.user or not self.access_token: return
        try:
            with open(self._get_session_path(), "w") as f:
                json.dump({
                    "access_token": self.access_token,
                    "user": self.user
                }, f)
        except Exception as e:
            print(f"[Network] Session Save Error: {e}")

    def load_session(self):
        if self.is_offline: return False
        try:
            with open(self._get_session_path(), "r") as f:
                data = json.load(f)
                self.access_token = data.get("access_token")
                self.user = data.get("user")
                
                # Verify token is still valid (simple User call)
                endpoint = f"{self.url}/auth/v1/user"
                response = requests.get(endpoint, headers=self._get_headers(authenticated=True))
                if response.status_code == 200:
                    print(f"[Network] Session Restored for {self.user['email']}")
                    return True
                else:
                    print("[Network] Session Expired")
                    self.logout() # Clear bad session
                    return False
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"[Network] Session Load Error: {e}")
            return False

    def get_user_progress(self):
        if self.is_offline or not self.user: return None
        
        endpoint = f"{self.url}/rest/v1/user_progress?user_id=eq.{self.user['id']}&select=max_level_reached,total_deaths"
        try:
            response = requests.get(endpoint, headers=self._get_headers(authenticated=True))
            if response.status_code == 200:
                data = response.json()
                if data: return data[0]
                else:
                    # Create default row
                    return self.init_user_progress()
            return None
        except Exception as e:
            print(f"[Network] Get Progress Error: {e}")
            return None

    def init_user_progress(self):
        # Create initial row
        endpoint = f"{self.url}/rest/v1/user_progress"
        payload = {"user_id": self.user['id'], "max_level_reached": 1, "total_deaths": 0}
        try:
            requests.post(endpoint, json=payload, headers=self._get_headers(authenticated=True))
            return payload
        except:
            return None

    def update_user_progress(self, level_reached, deaths_to_add=0):
        if self.is_offline or not self.user: return
        
        # We need to fetch current first to verify we are upgrading (MAX logic)
        # Or we can do an upsert?
        # Upsert in Supabase via Request is easiest with "Prefer: resolution=merge-duplicates"
        # But we want MAX(level).
        # Simplest: Get, Compare, Update.
        
        current = self.get_user_progress()
        if not current: return
        
        new_max = max(current.get('max_level_reached', 1), level_reached)
        new_deaths = current.get('total_deaths', 0) + deaths_to_add
        
        endpoint = f"{self.url}/rest/v1/user_progress?user_id=eq.{self.user['id']}"
        payload = {
            "max_level_reached": new_max,
            "total_deaths": new_deaths,
            "updated_at": "now()" # Let server handle ts? actually we pass string or let default handle it? 
                                  # Updating row usually updates only specified fields.
        }
        
        try:
            requests.patch(endpoint, json=payload, headers=self._get_headers(authenticated=True))
        except Exception as e:
            print(f"[Network] Update Progress Error: {e}")

    def get_my_score(self, level_id):
        if self.is_offline or not self.user: return None
        
        # We want to find OUR best score for this level.
        # RLS allows us to see our own rows.
        # Sort by deaths, then time.
        endpoint = f"{self.url}/rest/v1/leaderboard?level_id=eq.{level_id}&user_id=eq.{self.user['id']}&order=deaths.asc,time_seconds.asc&limit=1"
        try:
            response = requests.get(endpoint, headers=self._get_headers(authenticated=True))
            if response.status_code == 200:
                data = response.json()
                if data: return data[0]
            return None
        except Exception as e:
            print(f"[Network] Get My Score Error: {e}")
            return None

    def send_feedback(self, message):
        if self.is_offline: return False
        if not message: return False
        
        endpoint = f"{self.url}/rest/v1/feedback"
        # Table needs to exist! We assume user will create it or we fail silently.
        # Structure: id, user_id, message, created_at
        pk_user = self.user['id'] if self.user else None
        
        payload = {
            "user_id": pk_user,
            "message": message
        }
        try:
            requests.post(endpoint, json=payload, headers=self._get_headers(authenticated=True)) # Auth true to allow RLS if needed
            return True
        except:
            return False

    def submit_score(self, level_id, time_seconds, deaths, player_name="Player"):
        if self.is_offline: return False

        # If user is logged in, include user_id
        user_id = self.user['id'] if self.user else None
        
        payload = {
            "level_id": level_id,
            "player_name": player_name,
            "time_seconds": float(f"{time_seconds:.2f}"),
            "deaths": deaths,
            "user_id": user_id
        }
        
        # We need to verify if insertion requires auth in the user's RLS policies.
        # We try to insert using the token if available.
        
        endpoint = f"{self.url}/rest/v1/leaderboard"
        try:
            response = requests.post(
                endpoint, 
                json=payload, 
                headers=self._get_headers(authenticated=bool(self.access_token))
            )
            if response.status_code in [200, 201]:
                # Launch Async Cleanup to keep only PB
                if user_id:
                     threading.Thread(target=self._cleanup_old_scores, args=(level_id, user_id)).start()
                return True
            else:
                print(f"[Network] Submit Error: {response.text}")
                return False
        except Exception as e:
            print(f"[Network] Submit Exception: {e}")
            return False

    def _cleanup_old_scores(self, level_id, user_id):
        """Keeps only the best Time record and best Death record for a user/level."""
        try:
             # 1. Fetch all scores for this Level + User
             endpoint = f"{self.url}/rest/v1/leaderboard?level_id=eq.{level_id}&user_id=eq.{user_id}&select=id,time_seconds,deaths"
             res = requests.get(endpoint, headers=self._get_headers(authenticated=True))
             if res.status_code != 200: return
             
             scores = res.json()
             if len(scores) <= 2: return # Optimization: Nothing to delete
             
             # 2. Find best IDs
             # Best Time: min time, then min deaths
             best_time_entry = min(scores, key=lambda x: (x['time_seconds'], x['deaths']))
             # Best Deaths: min deaths, then min time
             best_death_entry = min(scores, key=lambda x: (x['deaths'], x['time_seconds']))
             
             keep_ids = {best_time_entry['id'], best_death_entry['id']}
             
             # 3. Identify IDs to delete
             delete_ids = [str(s['id']) for s in scores if s['id'] not in keep_ids]
             
             if not delete_ids: return
             
             # 4. Delete
             # Syntax: ?id=in.(1,2,3)
             ids_str = ",".join(delete_ids)
             del_endpoint = f"{self.url}/rest/v1/leaderboard?id=in.({ids_str})"
             requests.delete(del_endpoint, headers=self._get_headers(authenticated=True))
             print(f"[Network] Cleanup: Deleted {len(delete_ids)} redundant scores.")
             
        except Exception as e:
            print(f"[Network] Cleanup Error: {e}")

    def fetch_top_scores(self, level_id):
        if self.is_offline: return []
        
        # Query parameters: level_id=eq.X & order=deaths.asc,time_seconds.asc & limit=10
        query = f"level_id=eq.{level_id}&order=deaths.asc,time_seconds.asc&limit=10&select=player_name,deaths,time_seconds"
        endpoint = f"{self.url}/rest/v1/leaderboard?{query}"
        
        try:
            response = requests.get(endpoint, headers=self._get_headers())
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"[Network] Fetch Error: {e}")
            return []
