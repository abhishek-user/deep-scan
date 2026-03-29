import requests
import urllib3  # <-- NEW: Needed to suppress warnings
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from fpdf import FPDF
import datetime

# Initialize colors
init(autoreset=True)

# Store findings
report_data = []

# Browser headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}

# NEW: Suppress the "InsecureRequestWarning" so our terminal stays clean
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def safe_request(url):
    return requests.get(
        url,
        headers=HEADERS,
        timeout=15,
        allow_redirects=True,
        verify=False  # <-- NEW: Tells the scanner to ignore broken/missing SSL certs
    )


def print_banner():
    print(Fore.CYAN + Style.BRIGHT + """
    =========================================
                 DEEP-SCAN v1.0
       Automated Web Logic & Posture Tester
    =========================================
    """)


def get_target():
    url = input(Fore.YELLOW + "Enter the target URL (e.g., https://example.com): ")
    if not url.startswith("http"):
        url = "https://" + url
    return url


def check_security_headers(url):
    print(Fore.BLUE + "\n[*] Checking Security Headers...")

    try:
        response = safe_request(url)
        headers = response.headers

        security_headers = {
            "Content-Security-Policy": "Helps prevent XSS",
            "X-Frame-Options": "Prevents clickjacking",
            "X-Content-Type-Options": "Stops MIME sniffing",
            "Strict-Transport-Security": "Forces HTTPS",
            "Referrer-Policy": "Controls referrer leakage"
        }

        for header, description in security_headers.items():
            if header in headers:
                print(Fore.GREEN + f"[+] {header} present")
            else:
                print(Fore.RED + f"[-] {header} missing")
                report_data.append([
                    "Missing Header",
                    header,
                    description
                ])

    except Exception as e:
        print(Fore.RED + f"[!] Error checking headers: {e}")


def check_broken_links(url):
    print(Fore.BLUE + "\n[*] Hunting for Broken Links...")

    try:
        response = safe_request(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a', href=True)
        print(f"[*] Found {len(links)} links. Testing first 10...")

        for link in links[:10]:
            href = link.get('href') # Fixed: Safely extract the href

            if href and href.startswith('http'):
                try:
                    link_response = safe_request(href)

                    if link_response.status_code == 404:
                        print(Fore.RED + f"[-] BROKEN LINK: {href}")
                        report_data.append([
                            "Broken Link",
                            href,
                            "404 response detected"
                        ])
                    else:
                        print(Fore.GREEN + f"[+] OK: {href}")

                except:
                    print(Fore.RED + f"[-] Dead Link: {href}")
                    report_data.append([
                        "Dead Link",
                        href,
                        "Unreachable domain"
                    ])

    except Exception as e:
        print(Fore.RED + f"[!] Error analyzing links: {e}")

def check_sensitive_files(url):
    print(Fore.BLUE + "\n[*] Hunting for Exposed Sensitive Files...")

    # A mini-dictionary of common files that hackers look for
    payloads = [
        'robots.txt', 
        '.env', 
        '.git/config', 
        'admin/', 
        'backup.zip'
    ]

    # Make sure the URL has a trailing slash before adding our payloads
    if not url.endswith('/'):
        url += '/'

    for payload in payloads:
        target_url = url + payload
        try:
            response = safe_request(target_url)

            # If the server returns a 200 OK, the file exists and is public!
            if response.status_code == 200:
                print(Fore.RED + f"[-] EXPOSED FILE FOUND: {target_url}")
                report_data.append([
                    "Sensitive File",
                    target_url,
                    "Publicly accessible configuration or backup file"
                ])
            else:
                # 404 Not Found or 403 Forbidden means we are safe
                print(Fore.GREEN + f"[+] Secure: {payload} (Status: {response.status_code})")

        except Exception as e:
            print(Fore.RED + f"[!] Error checking {payload}: {e}")

def generate_pdf_report(target_url):
    print(Fore.MAGENTA + "\n[*] Generating PDF report...")

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Deep-Scan Report", ln=True, align='C')

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Target: {target_url}", ln=True)
    
    # Fixed: Cleaned up the date format
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pdf.cell(0, 10, f"Date: {current_time}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(50, 10, "Type", 1)
    pdf.cell(60, 10, "Location", 1)
    pdf.cell(80, 10, "Details", 1)
    pdf.ln()

    pdf.set_font("Arial", size=10)

    for item in report_data:
        pdf.cell(50, 10, str(item[0])[:25], 1)
        pdf.cell(60, 10, str(item[1])[:35], 1)
        pdf.cell(80, 10, str(item[2])[:45], 1)
        pdf.ln()

    filename = "DeepScan_Report.pdf"
    pdf.output(filename)

    print(Fore.GREEN + Style.BRIGHT + f"[+] Report saved as {filename}")


if __name__ == "__main__":
    print_banner()
    target = get_target()

    check_security_headers(target)
    check_broken_links(target)
    check_sensitive_files(target) # <-- NEW MODULE ADDED HERE

    generate_pdf_report(target)