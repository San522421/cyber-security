# PassGuard — Password Integrity Tester

A real-time password strength analyser and secure password generator built with Python and Streamlit.

## Features

- Real-time password strength analysis (score 0–100)
- Password entropy calculation
- Detection of common vulnerabilities (keyboard sequences, repeated chars, year patterns, common passwords)
- 10-point security requirements checklist
- Cryptographically secure password generator (uses Python `secrets` module)
- Beautiful dark-themed UI

## Tech Stack

- Python 3.11
- Streamlit 1.58
- zxcvbn (Dropbox password strength library)

## Run Locally

```bash
pip install streamlit zxcvbn
streamlit run app.py
```

## How It Works

1. Type any password into the input field
2. The app instantly calculates entropy, detects patterns, and gives a score
3. Use the generator section to create a strong password with your preferred options

## Privacy

All analysis runs **locally** — no password is ever sent to any server.
