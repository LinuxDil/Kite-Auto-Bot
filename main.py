from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from aiohttp import ClientResponseError, ClientSession, ClientTimeout
from aiohttp_socks import ProxyConnector
from fake_useragent import FakeUserAgent
from eth_account import Account
from colorama import *
from datetime import datetime
import asyncio, binascii, random, json, os, pytz
from pyfiglet import Figlet
import shutil

wib = pytz.timezone('Asia/Jakarta')

class KiteAi:
    def __init__(self) -> None:
        self.headers = {
            "Accept-Language": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://testnet.gokite.ai",
            "Referer": "https://testnet.gokite.ai/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": FakeUserAgent().random
        }
        self.NEO_API = "https://neo.prod.gokite.ai/v2"
        self.OZONE_API = "https://ozone-point-system.prod.gokite.ai"
        self.KEY_HEX = "6a1c35292b7c5b769ff47d89a17e7bc4f0adfe1b462981d28e0e9f7ff20b8f8a"
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.auth_tokens = {}
        self.access_tokens = {}
        self.header_cookies = {}
        self.user_interactions = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        figlet = Figlet(font='ansi_shadow')
        banner_lines = figlet.renderText('BG WIN').splitlines()
        term_width = shutil.get_terminal_size().columns

        for line in banner_lines:
            print(Fore.GREEN + Style.BRIGHT + line.center(term_width) + Style.RESET_ALL)

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                    async with session.get("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt") as response:
                        response.raise_for_status()
                        content = await response.text()
                        with open(filename, 'w') as f:
                            f.write(content)
                        self.proxies = content.splitlines()
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = f.read().splitlines()
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, token):
        if token not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[token] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[token]

    def rotate_proxy_for_account(self, token):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[token] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def generate_address(self, private_key: str):
        try:
            account = Account.from_key(private_key)
            address = account.address
            
            return address
        except Exception as e:
            return None
    
    def hex_to_bytes(self, hex_str):
        return bytes.fromhex(hex_str)

    def bytes_to_hex(self, bytes):
        return binascii.hexlify(bytes).decode()

    def encrypt(self, address):
        key = self.hex_to_bytes(self.KEY_HEX)
        iv = os.urandom(12)
        encryptor = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend()).encryptor()

        ciphertext = encryptor.update(address.encode()) + encryptor.finalize()
        auth_tag = encryptor.tag

        result = iv + ciphertext + auth_tag
        return self.bytes_to_hex(result)

    def generate_auth_token(self, address):
        return self.encrypt(address)
    
    def generate_quiz_title(self):
        today = datetime.today().strftime('%Y-%m-%d')
        return f"daily_quiz_{today}"
    
    def extract_cookies(self, raw_cookies: list):
        cookies_dict = {}
        try:
            skip_keys = ['expires', 'path', 'domain', 'samesite', 'secure', 'httponly', 'max-age']

            for cookie_str in raw_cookies:
                cookie_parts = cookie_str.split(';')

                for part in cookie_parts:
                    cookie = part.strip()

                    if '=' in cookie:
                        name, value = cookie.split('=', 1)

                        if name and value and name.lower() not in skip_keys:
                            cookies_dict[name] = value

            cookie_header = "; ".join([f"{key}={value}" for key, value in cookies_dict.items()])
            
            return cookie_header
        except Exception as e:
            return None
        
    def question_lists(self, agent_name: str):
        if agent_name == "Professor":
            return [
                "What is Kite AI's core technology?",
                "How does Kite AI improve developer productivity?",
                "What are the key features of Kite AI's platform?",
                "How does Kite AI handle data security?",
                "What makes Kite AI different from other AI platforms?",
                "How does Kite AI integrate with existing systems?",
                "What programming languages does Kite AI support?",
                "How does Kite AI's API work?",
                "What are Kite AI's scalability features?",
                "How does Kite AI help with code quality?",
                "What is Kite AI's approach to machine learning?",
                "How does Kite AI handle version control?",
                "What are Kite AI's deployment options?",
                "How does Kite AI assist with debugging?",
                "What are Kite AI's code completion capabilities?",
                "How does Kite AI handle multiple projects?",
                "What is Kite AI's pricing structure?",
                "How does Kite AI support team collaboration?",
                "What are Kite AI's documentation features?",
                "How does Kite AI implement code reviews?",
                "What is Kite AI's update frequency?",
                "How does Kite AI handle error detection?",
                "What are Kite AI's testing capabilities?",
                "How does Kite AI support microservices?",
                "What is Kite AI's cloud infrastructure?",
                "How does Kite AI handle API documentation?",
                "What are Kite AI's code analysis features?",
                "How does Kite AI support continuous integration?",
                "What is Kite AI's approach to code optimization?",
                "How does Kite AI handle multilingual support?",
                "What are Kite AI's security protocols?",
                "How does Kite AI manage user permissions?",
                "What is Kite AI's backup system?",
                "How does Kite AI handle code refactoring?",
                "What are Kite AI's monitoring capabilities?",
                "How does Kite AI support remote development?",
                "What is Kite AI's approach to technical debt?",
                "How does Kite AI handle code dependencies?",
                "What are Kite AI's performance metrics?",
                "How does Kite AI support code documentation?",
                "What is Kite AI's approach to API versioning?",
                "How does Kite AI handle load balancing?",
                "What are Kite AI's debugging tools?",
                "How does Kite AI support code generation?",
                "What is Kite AI's approach to data validation?",
                "How does Kite AI handle error logging?",
                "What are Kite AI's testing frameworks?",
                "How does Kite AI support code deployment?",
                "What is Kite AI's approach to code maintenance?",
                "How does Kite AI handle system integration?"
            ]
        elif agent_name == "Crypto Buddy":
            return [
                "What is Bitcoin's current price?",
                "Show me Ethereum price",
                "What's the price of BNB?",
                "Current Solana price?",
                "What's AVAX trading at?",
                "Show me MATIC price",
                "Current price of DOT?",
                "What's the XRP price now?",
                "Show me ATOM price",
                "What's the current LINK price?",
                "Show me ADA price",
                "What's NEAR trading at?",
                "Current price of FTM?",
                "What's the ALGO price?",
                "Show me DOGE price",
                "What's SHIB trading at?",
                "Current price of UNI?",
                "What's the AAVE price?",
                "Show me LTC price",
                "What's ETC trading at?",
                "Show me the price of SAND",
                "What's MANA's current price?",
                "Current price of APE?",
                "What's the GRT price?",
                "Show me BAT price",
                "What's ENJ trading at?",
                "Current price of CHZ?",
                "What's the CAKE price?",
                "Show me VET price",
                "What's ONE trading at?",
                "Show me the price of GALA",
                "What's THETA's current price?",
                "Current price of ICP?",
                "What's the FIL price?",
                "Show me EOS price",
                "What's XTZ trading at?",
                "Show me the price of ZIL",
                "What's WAVES current price?",
                "Current price of KSM?",
                "What's the DASH price?",
                "Show me NEO price",
                "What's XMR trading at?",
                "Show me the price of IOTA",
                "What's EGLD's current price?",
                "Current price of COMP?",
                "What's the SNX price?",
                "Show me MKR price",
                "What's CRV trading at?",
                "Show me the price of RUNE",
                "What's 1INCH current price?"
            ]
        elif agent_name == "Sherlock":
            return [
                "What do you think of this transaction? 0x252c02bded9a24426219248c9c1b065b752d3cf8bedf4902ed62245ab950895b"
            ]
        
    def agent_lists(self, agent_name: str):
        agent_lists = {}
        try:
            if agent_name == "Professor":
                agent_lists["service_id"] = "deployment_KiMLvUiTydioiHm7PWZ12zJU"
                agent_lists["title"] = agent_name
                agent_lists["message"] = random.choice(self.question_lists(agent_name))

            elif agent_name == "Crypto Buddy":
                agent_lists["service_id"] = "deployment_ByVHjMD6eDb9AdekRIbyuz14"
                agent_lists["title"] = agent_name
                agent_lists["message"] = random.choice(self.question_lists(agent_name))

            elif agent_name == "Sherlock":
                agent_lists["service_id"] = "deployment_OX7sn2D0WvxGUGK8CTqsU5VJ"
                agent_lists["title"] = agent_name
                agent_lists["message"] = random.choice(self.question_lists(agent_name))

            return agent_lists
        except Exception as e:
            return None
        
    def generate_inference_payload(self, service_id: str, question: str):
        payload = {
            "service_id":service_id,
            "subnet":"kite_ai_labs",
            "stream":True,
            "body":{
                "stream":True,
                "message":question
            }
        }
        return payload
        
    def generate_receipt_payload(self, address: str, service_id: str, question: str, answer: str):
        payload = {
            "address":address,
            "service_id":service_id,
            "input":[{
                "type":"text/plain",
                "value":question
            }],
            "output":[{
                "type":"text/plain",
                "value":answer
            }]
        }
        return payload
    
    def mask_account(self, account):
        mask_account = account[:6] + '*' * 6 + account[-6:]
        return mask_account 
    
    def print_question(self):
        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Monosans Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run With Private Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Run Without Proxy{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "Run With Monosans Proxy" if choose == 1 else 
                        "Run With Private Proxy" if choose == 2 else 
                        "Run Without Proxy"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}{proxy_type} Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        rotate = False
        if choose in [1, 2]:
            while True:
                rotate = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()

                if rotate in ["y", "n"]:
                    rotate = rotate == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        while True:
            try:
                count = int(input(f"{Fore.YELLOW + Style.BRIGHT}How Many Times Would You Like to Interact With Kite AI Agents? -> {Style.RESET_ALL}").strip())
                if count > 0:
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter a positive number.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

        return count, choose, rotate
        
    async def user_signin(self, address: str, proxy=None, retries=5):
        url = f"{self.NEO_API}/signin"
        data = json.dumps({"eoa":address})
        headers = {
            **self.headers,
            "Authorization": self.auth_tokens[address],
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        result = await response.json()

                        raw_cookies = response.headers.getall('Set-Cookie', [])
                        if raw_cookies:
                            cookie_header = self.extract_cookies(raw_cookies)

                            if cookie_header:
                                return result["data"]["access_token"], cookie_header
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None, None
        
    async def user_data(self, address: str, proxy=None, retries=5):
        url = f"{self.OZONE_API}/me"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[address]}"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
        
    async def create_quiz(self, address: str, proxy=None, retries=5):
        url = f"{self.NEO_API}/quiz/create"
        data = json.dumps({"title":self.generate_quiz_title(), "num":1, "eoa":address})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Cookie": self.header_cookies[address],
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        self.log(await response.text())
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
        
    async def get_quiz(self, address: str, quiz_id: int, proxy=None, retries=5):
        url = f"{self.NEO_API}/quiz/get?id={quiz_id}&eoa={address}"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Cookie": self.header_cookies[address]
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
            
    async def submit_quiz(self, address: str, proxy=None, retries=5):
        url = f"{self.NEO_API}/quiz/submit"
        data = json.dumps({})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Cookie": self.header_cookies[address],
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
            
    async def agent_inference(self, address: str, service_id: str, question: str, proxy=None, retries=5):
        url = f"{self.OZONE_API}/agent/inference"
        data = json.dumps(self.generate_inference_payload(service_id, question))
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        result = ""

                        async for line in response.content:
                            line = line.decode("utf-8").strip()
                            if line.startswith("data:"):
                                try:
                                    json_data = json.loads(line[len("data:"):].strip())
                                    delta = json_data.get("choices", [{}])[0].get("delta", {})
                                    content = delta.get("content")
                                    if content:
                                        result += content
                                except json.JSONDecodeError:
                                    continue

                        return result
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
            
    async def submit_receipt(self, address: str, sa_address: str, service_id: str, question: str, answer: str, proxy=None, retries=5):
        url = f"{self.NEO_API}/submit_receipt"
        data = json.dumps(self.generate_receipt_payload(sa_address, service_id, question, answer))
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Cookie": self.header_cookies[address],
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
            
    async def process_user_signin(self, address: str, use_proxy: bool, rotate_proxy: bool):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.YELLOW + Style.BRIGHT}Try To Login, Wait...{Style.RESET_ALL}",
            end="\r",
            flush=True
        )

        proxy = self.get_next_proxy_for_account(address) if use_proxy else None

        if rotate_proxy:
            access_token = None
            header_cookie = None
            while access_token is None or header_cookie is None:
                access_token, header_cookie = await self.user_signin(address, proxy)
                if not access_token or not header_cookie:
                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Status    :{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Login Failed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Rotating Proxy {Style.RESET_ALL}"
                    )
                    proxy = self.rotate_proxy_for_account(address) if use_proxy else None
                    await asyncio.sleep(5)
                    continue

                self.access_tokens[address] = access_token
                self.header_cookies[address] = header_cookie

                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Status    :{Style.RESET_ALL}"
                    f"{Fore.GREEN+Style.BRIGHT} Login Success {Style.RESET_ALL}                  "
                )
                return True

        access_token, header_cookie = await self.user_signin(address, proxy)
        if not access_token or not header_cookie:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Status    :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Login Failed {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} Skipping This Account {Style.RESET_ALL}"
            )
            return False
        
        self.access_tokens[address] = access_token
        self.header_cookies[address] = header_cookie
        
        self.log(
            f"{Fore.CYAN+Style.BRIGHT}Status    :{Style.RESET_ALL}"
            f"{Fore.GREEN+Style.BRIGHT} Login Success {Style.RESET_ALL}                  "
        )
        return True
        
    async def process_accounts(self, address: str, interact_count: int, use_proxy: bool, rotate_proxy: bool):
        signed = await self.process_user_signin(address, use_proxy, rotate_proxy)
        if signed:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Proxy     :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {proxy} {Style.RESET_ALL}"
            )
        
            user = await self.user_data(address, proxy)
            if not user:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Status    :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} GET User Data Failed {Style.RESET_ALL}"
                )
                return
            
            username = user.get("data", {}).get("profile", {}).get("username", "Unknown")
            sa_address = user.get("data", {}).get("profile", {}).get("smart_account_address", "Undifined").upper()
            balance = user.get("data", {}).get("profile", {}).get("total_xp_points", 0)
            
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Username  :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {username} {Style.RESET_ALL}"
            )
            
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}SA Address:{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {sa_address} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Balance   :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {balance} XP {Style.RESET_ALL}"
            )
            self.log(f"{Fore.CYAN+Style.BRIGHT}AI Agents :{Style.RESET_ALL}")

            self.user_interactions[address] = 0

            while self.user_interactions[address] < interact_count:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}  ● {Style.RESET_ALL}"
                    f"{Fore.BLUE + Style.BRIGHT}Interactions{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {self.user_interactions[address] + 1} of {interact_count} {Style.RESET_ALL}"
                )

                agent_names = ["Professor", "Crypto Buddy", "Sherlock"]
                agents = self.agent_lists(random.choice(agent_names))
                if agents:
                    service_id = agents["service_id"]
                    agent_name = agents["title"]
                    question = agents["message"]

                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}    Agent Name: {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{agent_name}{Style.RESET_ALL}"
                    )
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}    Question  : {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{question}{Style.RESET_ALL}"
                    )

                    answer = await self.agent_inference(address, service_id, question, proxy)
                    if answer:
                        self.user_interactions[address] += 1
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}    Answer    : {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{answer.strip()}{Style.RESET_ALL}"
                        )

                        submit = await self.submit_receipt(address, sa_address, service_id, question, answer, proxy)
                        if submit:
                            self.log(
                                f"{Fore.CYAN + Style.BRIGHT}    Status    : {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}Receipt Submited Successfully{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.CYAN + Style.BRIGHT}    Status    : {Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT}Submit Receipt Failed{Style.RESET_ALL}"
                            )
                    else:
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}    Status    : {Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT}Interaction Failed{Style.RESET_ALL}"
                        )

                    await asyncio.sleep(random.randint(5, 10))

        self.user_interactions[address] = 0

    async def main(self):
        try:
            with open('accounts.txt', 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]
            
            interact_count, use_proxy_choice, rotate_proxy = self.print_question()

            while True:
                use_proxy = False
                if use_proxy_choice in [1, 2]:
                    use_proxy = True

                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
                )

                if use_proxy:
                    await self.load_proxies(use_proxy_choice)
                
                separator = "=" * 25
                for account in accounts:
                    if account:
                        address = self.generate_address(account)

                        if address:
                            auth_token = self.generate_auth_token(address)

                            if auth_token:
                                self.auth_tokens[address] = auth_token
                                self.log(
                                    f"{Fore.CYAN + Style.BRIGHT}{separator}[{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(address)} {Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT}]{separator}{Style.RESET_ALL}"
                                )
                                await self.process_accounts(address, interact_count, use_proxy, rotate_proxy)
                                await asyncio.sleep(3)

                self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*72)
                seconds = 24 * 60 * 60
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE+Style.BRIGHT}All Accounts Have Been Processed.{Style.RESET_ALL}",
                        end="\r"
                    )
                    await asyncio.sleep(1)
                    seconds -= 1

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'accounts.txt' Not Found.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise e

if __name__ == "__main__":
    try:
        bot = KiteAi()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Kite Ai Ozone - BOT{Style.RESET_ALL}                                       "                              
        )
