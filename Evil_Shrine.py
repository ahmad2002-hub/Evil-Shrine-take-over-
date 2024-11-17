import subprocess
import os
import argparse

# استخدام argparse لتحليل المعاملات من سطر الأوامر
parser = argparse.ArgumentParser(description="Fetch DNS records and HTTP status codes for subdomains.")
parser.add_argument('-f', '--file', required=True, help="The file containing subdomains list")
args = parser.parse_args()

# اسم الملف المدخل من سطر الأوامر
subdomains_file = args.file

# إنشاء اسم ملف الإخراج بناءً على اسم الملف المدخل
output_file = os.path.splitext(subdomains_file)[0] + "_output.txt"  # إضافة "_output" إلى اسم الملف

# فتح ملف الإخراج لكتابة النتائج فيه
with open(output_file, 'w') as output:
    # كتابة رأس للإخراج
    output.write("Subdomain, DNS Records, HTTP Status Code\n")

    # قراءة النطاقات الفرعية من الملف
    with open(subdomains_file, 'r') as file:
        for subdomain in file:
            subdomain = subdomain.strip()  # إزالة المسافات البيضاء حول النطاق

            # فحص سجلات DNS باستخدام dnsrecon
            print(f"[*] Fetching DNS records for {subdomain}...")
            dnsrecon_command = [
                "dnsrecon",
                "-d", subdomain,
                "-t", "std"
            ]
            dns_output = subprocess.run(dnsrecon_command, capture_output=True, text=True)

            # التحقق من أكواد HTTP باستخدام httpx (البروتوكولين http و https)
            print(f"[*] Checking HTTP status for {subdomain}...")
            httpx_http_command = [
                "httpx",
                "-silent",
                "-status-code",
                "-u", f"http://{subdomain}"
            ]
            httpx_https_command = [
                "httpx",
                "-silent",
                "-status-code",
                "-u", f"https://{subdomain}"
            ]
            
            # تنفيذ الأوامر
            http_output_http = subprocess.run(httpx_http_command, capture_output=True, text=True)
            http_output_https = subprocess.run(httpx_https_command, capture_output=True, text=True)

            # استخراج النتائج من dnsrecon و httpx
            dns_records = dns_output.stdout.strip() if dns_output.stdout else "No DNS records"
            http_status_http = http_output_http.stdout.strip() if http_output_http.stdout else "No HTTP status"
            http_status_https = http_output_https.stdout.strip() if http_output_https.stdout else "No HTTPS status"

            # كتابة النتائج في الملف
            output.write(f"{subdomain}, {dns_records}, HTTP: {http_status_http}, HTTPS: {http_status_https}\n")

print(f"[*] Task completed. Results saved to {output_file}")
