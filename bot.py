from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from aiohttp_socks import ProxyConnector
from fake_useragent import FakeUserAgent
from colorama import *
from datetime import datetime
import asyncio, random, time, json, os, pytz
from pyfiglet import Figlet
import shutil

wib = pytz.timezone('Asia/Jakarta')

class KiteAi:
    def __init__(self) -> None:
        self.headers = {
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://agents.testnet.gokite.ai",
            "Referer": "https://agents.testnet.gokite.ai/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": FakeUserAgent().random
        }
        self.BASE_API = "https://quests-usage-dev.prod.zettablock.com/api"
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
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
        figlet = Figlet(font='3-d')
        banner_lines = figlet.renderText('Airdrop Seeker').splitlines()
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
    
    def request_text_lists(self, agent_name: str):
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
                agent_lists["agent_url"] = "https://deployment-kazqlqgrjw8hbr8blptnpmtj.staging.gokite.ai/main"
                agent_lists["agent_id"] = "deployment_JtmpnULoMfudGPRhHjTWQlS7"
                agent_lists["name"] = agent_name
                agent_lists["question"] = random.choice(self.request_text_lists(agent_name))

            elif agent_name == "Crypto Buddy":
                agent_lists["agent_url"] = "https://deployment-0ovyzutzgttaydzu6eqn9bxi.staging.gokite.ai/main"
                agent_lists["agent_id"] = "deployment_fseGykIvCLs3m9Nrpe9Zguy9"
                agent_lists["name"] = agent_name
                agent_lists["question"] = random.choice(self.request_text_lists(agent_name))

            elif agent_name == "Sherlock":
                agent_lists["agent_url"] = "https://deployment-tqgv8vboiwipbkgsmzgdmwpm.staging.gokite.ai/main"
                agent_lists["agent_id"] = "deployment_MK9ej2jNz2rFuzuWZjdb1UmR"
                agent_lists["name"] = agent_name
                agent_lists["question"] = random.choice(self.request_text_lists(agent_name))

            return agent_lists
        except Exception as e:
            return None
    
    def generate_payload(self, address: str, agent_id: str, req_text: str, resp_text: str, ttft: int, total_time: int):
        try:
            payload = {
                "wallet_address":address,
                "agent_id":agent_id,
                "request_text":req_text,
                "response_text":resp_text,
                "ttft":ttft,
                "total_time":total_time,
                "request_metadata":{}
            }

            return payload
        except Exception as e:
            return None
    
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

        return choose, rotate
    
    async def check_connection(self, proxy=None):
        connector = ProxyConnector.from_url(proxy) if proxy else None
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=30)) as session:
                async with session.get(url="https://agents.testnet.gokite.ai", headers={}) as response:
                    response.raise_for_status()
                    return True
        except (Exception, ClientResponseError) as e:
            return None
        
    async def user_stats(self, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/user/{address}/stats"
        headers = {
            **self.headers,
            "Accept": "*/*",
        }
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
        
    async def report_usage(self, address: str, agent_id: str, req_text: str, resp_text: str, ttft: int, total_time: int, proxy=None, retries=5):
        url = f"{self.BASE_API}/report_usage"
        data = json.dumps(self.generate_payload(address, agent_id, req_text, resp_text, ttft, total_time))
        headers = {
            **self.headers,
            "Accept": "*/*",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
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
            
    async def perfrom_agent(self, agent_url: str, req_text: str, proxy=None, retries=5, stream_timeout=10):
        data = json.dumps({"message": req_text, "stream": True})
        headers = {
            **self.headers,
            "Accept": "text/event-stream",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }

        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    start_time = time.time()
                    first_token_time = None
                    last_token_time = time.time()
                    resp_text = ""

                    async with session.post(url=agent_url, headers=headers, data=data) as response:
                        response.raise_for_status()

                        async for line in response.content:
                            now = time.time()

                            if now - last_token_time > stream_timeout:
                                return None

                            line = line.decode("utf-8").strip()
                            if line.startswith("data:"):
                                try:
                                    json_data = json.loads(line[len("data:"):].strip())
                                    delta = json_data.get("choices", [{}])[0].get("delta", {})
                                    content = delta.get("content")

                                    if content and first_token_time is None:
                                        first_token_time = now

                                    if content:
                                        resp_text += content
                                        last_token_time = now
                                except json.JSONDecodeError:
                                    continue

                    end_time = time.time()
                    ttft = (first_token_time - start_time) * 1000 if first_token_time else None
                    total_time = (end_time - start_time) * 1000

                    return {
                        "resp_text": resp_text,
                        "ttft": ttft,
                        "total_time": total_time
                    }

            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None
            
    async def process_check_connection(self, address: str, use_proxy: bool, rotate_proxy: bool):
        message = "Checking Connection, Wait..."
        if use_proxy:
            message = "Checking Proxy Connection, Wait..."

        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.YELLOW + Style.BRIGHT}{message}{Style.RESET_ALL}",
            end="\r",
            flush=True
        )

        proxy = self.get_next_proxy_for_account(address) if use_proxy else None

        if rotate_proxy:
            is_valid = None
            while is_valid is None:
                is_valid = await self.check_connection(proxy)
                if not is_valid:
                    self.log(
                        f"{Fore.CYAN+Style.BRIGHT}Proxy   :{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {proxy} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Not 200 OK, {Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT}Rotating Proxy...{Style.RESET_ALL}"
                    )
                    proxy = self.rotate_proxy_for_account(address) if use_proxy else None
                    await asyncio.sleep(5)
                    continue

                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Proxy   :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {proxy} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.GREEN+Style.BRIGHT} 200 OK {Style.RESET_ALL}                  "
                )

                return True

        is_valid = await self.check_connection(proxy)
        if not is_valid:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Proxy   :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {proxy} {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Not 200 OK {Style.RESET_ALL}          "
            )
            return False
        
        self.log(
            f"{Fore.CYAN+Style.BRIGHT}Proxy   :{Style.RESET_ALL}"
            f"{Fore.WHITE+Style.BRIGHT} {proxy} {Style.RESET_ALL}"
            f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.GREEN+Style.BRIGHT} 200 OK {Style.RESET_ALL}                  "
        )

        return True
        
    async def process_accounts(self, address: str, use_proxy: bool, rotate_proxy: bool):
        is_valid = await self.process_check_connection(address, use_proxy, rotate_proxy)
        if is_valid:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            total_interactions = "N/A"
            stats = await self.user_stats(address, proxy)
            if stats:
                total_interactions = stats["total_interactions"]

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Total Interactions With Agents Is{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {total_interactions} {Style.RESET_ALL}"
            )

            self.user_interactions[address] = 0

            while self.user_interactions[address] < 20:

                self.user_interactions[address] += 1
                    
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}●{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Interaction {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{self.user_interactions[address]} of 20{Style.RESET_ALL}"
                )

                agent_names = ["Professor", "Crypto Buddy", "Sherlock"]

                agents = self.agent_lists(random.choice(agent_names))
                if agents:
                    agent_url = agents["agent_url"]
                    agent_id = agents["agent_id"]
                    agent_name = agents["name"]
                    req_text = agents["question"]

                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}    Agent Name: {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{agent_name}{Style.RESET_ALL}"
                    )
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}    Agent Id  : {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{agent_id}{Style.RESET_ALL}"
                    )
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}    Question  : {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{req_text}{Style.RESET_ALL}"
                    )

                    perform_agent = await self.perfrom_agent(agent_url, req_text, proxy)
                    if perform_agent:
                        resp_text = perform_agent["resp_text"]
                        ttft = perform_agent["ttft"]
                        total_time = perform_agent["total_time"]

                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}    Answer    : {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{resp_text.strip()}{Style.RESET_ALL}"
                        )

                        report = await self.report_usage(address, agent_id, req_text, resp_text, ttft, total_time, proxy)
                        if report and report.get("message") == "Usage report successfully recorded":
                            interaction_id = report["interaction_id"]
                            self.log(
                                f"{Fore.CYAN + Style.BRIGHT}    Status    : {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}Usage Report Successfully Recorded{Style.RESET_ALL}"
                            )
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}      >{Style.RESET_ALL}"
                                f"{Fore.BLUE + Style.BRIGHT} Interaction Id: {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}{interaction_id}{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.CYAN + Style.BRIGHT}    Status    : {Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT}Usage Report Failed to Recorded{Style.RESET_ALL}"
                            )
                            self.user_interactions[address] -= 1
                    else:
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}    Status    : {Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT}Interaction With Agent Failed{Style.RESET_ALL}"
                        )
                        self.user_interactions[address] -= 1

                    await asyncio.sleep(random.randint(5, 10))

            self.user_interactions[address] = 0

    async def main(self):
        try:
            with open('accounts.txt', 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]
            
            use_proxy_choice, rotate_proxy = self.print_question()

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
                for address in accounts:
                    if address:
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}{separator}[{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(address)} {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{separator}{Style.RESET_ALL}"
                        )
                        await self.process_accounts(address, use_proxy, rotate_proxy)
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
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Kite Ai Agents - BOT{Style.RESET_ALL}                                       "                              
        )
