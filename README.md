# Kite AI Auto-Bot

An automated interaction bot for Kite AI platform with multi-wallet and proxy support. go o

## First Step

Join our Telegram channel for more Airdrop:
https://t.me/airdropseeker_official

## 🌟 Features

- Multiple wallet support (manual input or file-based)
- Proxy support (HTTP/HTTPS/SOCKS)
- Rate limiting and retry mechanisms
- Multiple AI agents interaction
- Automatic question selection
- Usage reporting
- Graceful error handling

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/linuxdil/Kite-Auto-Bot.git
cd Kite-Auto-Bot
```

2. Create Environments:
```bash
python3 -m venv myenv
source myenv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```
## 📝 Configuration

1. (Optional) Create a `proxy.txt` file for proxy support:
```
http://user:pass@host:port
socks5://user:pass@host:port
```

2. Create a `accounts.txt` file for multiple wallets:
```
private key
private key 2
```

## 🚀 Usage

Run the bot:
```bash
python3 main.py
```

The bot will prompt you to:
1. Choose connection mode (Direct/Proxy)
2. Choose wallet input mode (Manual/File)
3. Enter wallet address (if manual mode)

## ⚙️ Configuration Options

You can modify the following settings in `main.py`:

## ⚠️ Disclaimer

This bot is for educational purposes only. Use at your own risk and ensure compliance with Kite AI's terms of service.

## 📜 License

MIT License - feel free to use and modify for your own purposes.
