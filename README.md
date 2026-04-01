# 🕵️‍♂️ Deep-Scan: Automated Web Logic & Posture Tester

Deep-Scan is a lightweight, Python-based Vulnerability Assessment and Penetration Testing (VAPT) orchestration tool. It automates the reconnaissance phase by scanning target domains for security misconfigurations, broken links (potential subdomain takeovers), and exposed sensitive files, instantly compiling the results into a professional PDF report.

## 🚀 Key Features

* **Security Header Analysis:** Evaluates HTTP response headers (CSP, HSTS, X-Frame-Options, etc.) to assess the target's baseline security posture.
* **Broken Link Hijacking Check:** Crawls local links to identify 404/dead endpoints that could lead to subdomain takeover vulnerabilities.
* **Sensitive File Hunting:** Actively probes for commonly exposed directories and files (e.g., `.git/config`, `robots.txt`, `.env`, `backup.zip`).
* **Automated PDF Reporting:** Utilizes `fpdf` to instantly generate a clean, tabular PDF report detailing discovered vulnerabilities, locations, and impact.
* **Resilient Execution:** Features built-in timeouts, custom User-Agents, and SSL-bypass mechanisms to ensure stable scanning against real-world and local CTF environments.

## 🛠️ Prerequisites

* Python 3.x
* Pip (Python package manager)

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/abhishek-user/deep-scan.git](https://github.com/abhishek-user/deep-scan.git)
   cd deep-scan

2. Create and activate a virtual environment (Recommended):
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate

3. Install the required dependencies:
    pip install requests beautifulsoup4 fpdf colorama

4. Run the script from your terminal. When prompted, enter the target URL.
    python scanner.py
    Note: Ensure the target URL includes the protocol (e.g., http:// or https://).

    The tool will execute the scanning modules and save a file named DeepScan_Report.pdf in the same directory upon completion.

## 🤝 Connect with Me

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/abhishek-ganesh07)

⚠️ Disclaimer
This tool is designed for educational purposes and authorized security testing only. Do not run this scanner against any system, network, or application for which you do not have explicit permission. The developer is not responsible for any misuse or damage caused by this program.
