#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MountAlgo Discord Bot
----------------
Bot Discord untuk trading dan analisis pasar keuangan.

Versi: 2.0.0
Author: MountAlgo Team
"""

# ===================== KONFIGURASI KEAMANAN =====================
"""
Konfigurasi untuk keamanan dan moderasi konten
"""

# Daftar kata terlarang (tambahkan sesuai kebutuhan)
BLACKLIST_WORDS = [
    # Indonesian/Malay (Core)
    "anjing", "babi", "tolol", "bangsat", "kontol", "asu", "ngentot", "memek", "jembut", 
    "dancok","dancuk","jancok","jancuk", "goblok", "goblog", "keparat", "bajingan", "titit", "pantat", "bego", "idiot",
    # English
    "fuck", "shit", "asshole", "bitch", "bastard", "dick", "pussy", "cunt", "whore", "slut", 
    "motherfucker", "faggot", "cock", "twat", "wanker", "crap", "douche", "piss", "damn", "nigger",
    # Chinese (Simplified)
    "肏", "傻逼", "妈逼", "草泥马", "他妈的", "屌", "鸡巴", "婊子", "王八蛋", "混蛋", "狗日的", "屎", 
    "屁眼", "阴茎", "阴道", "杂种", "龟头", "妓女", "卖淫", "强奸",
    # Javanese
    "jancuk", "jancok", "celeng", "kontol", "torok", "jembot", "jembut", "pantelo", "bangsat", "tai", "asu", "bejingan", "kemen", "bajingan", "jaran", "keparat", "itil", "modar", "bedhes",
    "becus", "kenthu", "kirik", "koplok", "kodok", "jangkrik", "jembel", "keplek",
    # Sundanese
    "contong", "tai", "kirik", "bajingan", "keparat", "bedog", "monyet", "bangkai", "gembel", 
    "goblog", "gigir", "kacai", "kirey", "kamseupay", "bangor", "gobang", "koplok",
    # Sumatra (Minang/Batak/Aceh)
    "babi", "anjing", "kunyuk", "kirik", "bajingan", "bangkai", "kafir", "setan", "babi", 
    "borot", "begu", "sisol", "sisolak", "babi", "asoe", "bangsat", "pantek", "itik", "kafir",
    # Illegal/NSFW Terms
    "judi", "porn", "bokep", "scam", "phishing", "penipuan", "moneygame", "investasibodong",
    "teroris", "narkoba", "sarang", "madat", "ganja", "sabu", "heroin", "viagra", "escort",
    "prostitusi", "pelacur", "pemerkosaan", "incest", "pedofil", "penganiayaan",
    # Financial Scams
    "investasibodong", "moneygame", "ponzi", "binary", "forexscam", "bodong", "tipu", 
    "penipuonline", "phishing", "scam", "skimming", "carding", "cryptoscam", "ransomware",
    # Hate Speech/Sensitive Topics
    "sara", "rasis", "komunis", "pki", "pembantaian", "genosida", "penistaan", "penghina", 
    "provokator", "penghasut", "penista", "kafir", "murtad", "kristenkafir", "yahudi", "zionis"
]

# Pengaturan sanksi otomatis
WARNING_LIMIT = 2   # Berapa kali warning sebelum mute
MUTE_LIMIT = 3      # Berapa kali warning sebelum kick
KICK_LIMIT = 4      # Berapa kali warning sebelum ban
MUTE_DURATION = 60  # dalam menit
# ===================== IMPORT =====================
"""
Import library yang digunakan dalam aplikasi
"""
# Standard library imports
import os
import re
import io
import csv
import json
import math
import time
import random
import hashlib
import asyncio
import traceback
from datetime import datetime, timedelta, timezone
import datetime as dt
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import List, Dict, Optional, Union
import math
from discord.ext import tasks, commands
import pytz
import aiohttp
import requests
import aiosqlite
from dotenv import load_dotenv
import discord
from discord import Embed, PermissionOverwrite, ButtonStyle
from discord.ext import commands, tasks
from discord.ui import Modal, TextInput, View, Button, Select, button
from typing import Optional, Dict, List
from decimal import Decimal
from typing import Dict, Optional, List
# ===================== LOGGING =====================
"""
Konfigurasi logging untuk aplikasi
"""
import logging

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ===================== KONFIGURASI =====================
"""
Konfigurasi aplikasi dan API keys
"""
# Memuat variabel lingkungan
load_dotenv()

# API Keys
API_KEYS = {
    "DISCORD_TOKEN": os.getenv("DISCORD_TOKEN"),
    "DANA_BULANAN_LINK": os.getenv("DANA_BULANAN_LINK"),
    "DANA_TAHUNAN_LINK": os.getenv("DANA_TAHUNAN_LINK"),
    "USDC_BULANAN_LINK": os.getenv("USDC_BULANAN_LINK"),
    "USDC_TAHUNAN_LINK": os.getenv("USDC_TAHUNAN_LINK"),
    "CARD_BULANAN_LINK": os.getenv("CARD_BULANAN_LINK"),
    "CARD_TAHUNAN_LINK": os.getenv("CARD_TAHUNAN_LINK"),
    "DONATION_LINK": os.getenv("DONATION_LINK"),
    "USDT_WALLET": os.getenv("USDT_WALLET"),
    "BTC_WALLET": os.getenv("BTC_WALLET"),
    "ETH_WALLET": os.getenv("ETH_WALLET"),
    "OPENROUTER_API_KEY": os.getenv("OPENROUTER_API_KEY"),
    "POLYGON_API_KEY": os.getenv("POLYGON_API_KEY"),
    "COIN_MARKET_CAP_API_KEY": os.getenv("COIN_MARKET_CAP_API_KEY"),
    "BINANCE_API_KEY": os.getenv("BINANCE_API_KEY"),
    "ALPHA_VANTAGE_API_KEY": os.getenv("ALPHA_VANTAGE_API_KEY"),
    "TWELVEDATA_API_KEY": os.getenv("TWELVEDATA_API_KEY"),
    "COINAPI_API_KEY1": os.getenv("COINAPI_API_KEY1"),
    "COINAPI_API_KEY2": os.getenv("COINAPI_API_KEY2"),
    "TOKENMETRICS_API_KEY1": os.getenv("TOKENMETRICS_API_KEY1"),
    "TOKENMETRICS_API_KEY2": os.getenv("TOKENMETRICS_API_KEY2"),
    "FCSAPI_API_KEY": os.getenv("FCSAPI_API_KEY"),
    "COINDESK_API_KEY1": os.getenv("COINDESK_API_KEY1"),
    "COINDESK_API_KEY2": os.getenv("COINDESK_API_KEY2"),
    "FINNHUB_API_KEY": os.getenv("FINNHUB_API_KEY")
}

# API Base URLs
API_URLS = {
    "OPENROUTER_BASE_URL": "https://openrouter.ai/api/v1",
    "BINANCE_API_BASE": "https://api.binance.com/api/v3",
    "ALPHA_VANTAGE_BASE": "https://www.alphavantage.co/query",
    "COINAPI_BASE": "https://rest.coinapi.io/v1",
    "FINNHUB_BASE": "https://finnhub.io/api/v1",
    "TRADINGVIEW_QUOTE": "https://scanner.tradingview.com/global/scan",
    "COIN_MARKET_CAP_BASE": "https://pro-api.coinmarketcap.com/v1",
    "POLYGON_BASE": "https://api.polygon.io/v2",
    "FCSAPI_BASE": "https://fcsapi.com/api-v3",
    "COINDESK_BASE": "https://api.coindesk.com/v1"
}

# Konfigurasi lainnya
EXCHANGE_PRIORITY = ["binance", "coinmarketcap", "fcsapi", "alphavantage"]
AI_MODEL = "mistralai/mixtral-8x7b-instruct"  # Model institutional-grade

# Untuk kemudahan akses
DISCORD_TOKEN = API_KEYS["DISCORD_TOKEN"]
DANA_BULANAN_LINK = API_KEYS["DANA_BULANAN_LINK"]
DANA_TAHUNAN_LINK = API_KEYS["DANA_TAHUNAN_LINK"]
USDC_BULANAN_LINK = API_KEYS["USDC_BULANAN_LINK"]
USDC_TAHUNAN_LINK = API_KEYS["USDC_TAHUNAN_LINK"]
CARD_BULANAN_LINK = API_KEYS["CARD_BULANAN_LINK"]
CARD_TAHUNAN_LINK = API_KEYS["CARD_TAHUNAN_LINK"]
DONATION_LINK = API_KEYS["DONATION_LINK"]
DONATION_ACTIVE = False
# Theme Colors (Violet, Green, Slightly Cyan, White, Dark)
COLOR_VIOLET = 0x8B5CF6
COLOR_GREEN = 0x10B981
COLOR_CYAN = 0x06B6D4
COLOR_WHITE = 0xF9FAFB
COLOR_DARK = 0x111827

PAYMENT_DANA_ACTIVE = True
PAYMENT_CRYPTO_ACTIVE = True
PAYMENT_CARD_ACTIVE = True
USDT_WALLET = API_KEYS["USDT_WALLET"]
BTC_WALLET = API_KEYS["BTC_WALLET"]
ETH_WALLET = API_KEYS["ETH_WALLET"]

# ===================== INISIALISASI BOT =====================
"""
Inisialisasi dan konfigurasi bot Discord
"""
# Konfigurasi intents Discord
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Inisialisasi bot
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")  # Menghapus help default untuk diganti dengan custom help
# ===================== FUNGSI UTILITAS =====================



"""
Kumpulan fungsi utilitas yang digunakan di berbagai bagian kode
"""

def safe_field_value(text: str, limit: int = 1024) -> str:
    """
    Memotong teks agar sesuai dengan batas karakter field embed Discord.
    
    Args:
        text (str): Teks yang akan dipotong
        limit (int, optional): Batas maksimum karakter. Default 1024.
        
    Returns:
        str: Teks yang sudah dipotong jika melebihi batas
    """
    if not text:
        return "-"
    return text[:limit-3] + "..." if len(text) > limit else text


# ===================== FUNGSI VALIDASI TRADING =====================
"""
Fungsi-fungsi untuk validasi dan lainya
"""
async def hapus_thread_usang(interaction: discord.Interaction, hari: int = 14):
    """
    Menghapus semua thread di channel 'lounge-chat' atau 'perkenalan'
    yang tidak aktif lebih dari <hari> hari.
    """
    await interaction.response.defer(thinking=True, ephemeral=True)

    guild = interaction.guild
    now = datetime.utcnow()
    total_checked = 0
    total_deleted = 0

    for channel in guild.text_channels:
        if any(k in channel.name.lower() for k in ["lounge-chat", "perkenalan"]):
            # Ambil semua thread aktif + arsip
            threads = channel.threads + [t async for t in channel.archived_threads(limit=None)]
            for thread in threads:
                total_checked += 1
                # Abaikan jika masih aktif
                if thread.last_message_id:
                    try:
                        last_msg = await thread.fetch_message(thread.last_message_id)
                        last_age = (now - last_msg.created_at).days
                        if last_age >= hari:
                            await thread.delete(reason=f"Thread usang (> {hari} hari)")
                            total_deleted += 1
                    except Exception as e:
                        logging.warning(f"Gagal hapus thread {thread.name}: {e}")

    # Buat laporan
    embed = discord.Embed(
        title="🧹 Pembersihan Thread Usang Selesai",
        description=(
            f"📂 **Total diperiksa:** `{total_checked}`\n"
            f"🗑️ **Total dihapus:** `{total_deleted}`\n"
            f"⏰ **Batas umur:** `{hari}` hari"
        ),
        color=discord.Color(COLOR_GREEN),
        timestamp=datetime.now()
    )
    embed.set_footer(text=f"Dijalankan oleh {interaction.user.display_name}")

    # Kirim ke admin & log
    await interaction.followup.send(embed=embed, ephemeral=True)
    log_channel = discord.utils.get(guild.text_channels, name="laporan")
    if log_channel:
        await log_channel.send(embed=embed)

async def safe_parse_position(position_str: str):
    """
    Melakukan parsing string posisi trading dengan aman dan logging.
    
    Args:
        position_str (str): String posisi trading yang akan di-parse
        
    Returns:
        dict: Data posisi trading hasil parsing atau data default jika gagal
    """
    try:
        position_data = await TradingCalculator.parse_position_string(position_str)
        
        # Log parsing result untuk debugging
        if position_data['entry_price'] == 0:
            logging.warning(f"Parsing result - Entry price 0 for: {position_str}")
            logging.warning(f"Parsed data: {position_data}")
            
        return position_data
    except Exception as e:
        logging.error(f"Safe parse failed for '{position_str}': {str(e)}")
        return TradingCalculator.default_position_data()


def validate_position_format(position_str: str) -> bool:
    """
    Validasi cepat untuk format string posisi trading.
    
    Args:
        position_str (str): String posisi trading yang akan divalidasi
        
    Returns:
        bool: True jika format valid, False jika tidak
    """
    if not position_str or '/' not in position_str:
        return False
    
    parts = position_str.split('/')
    if len(parts) < 5:
        return False
        
    if parts[0].upper() not in ['BUY', 'SELL']:
        return False
        
    return True

@bot.command()
async def testparse(ctx, position_str: str):
    """Test parsing position string"""
    position_data = await TradingCalculator.parse_position_string(position_str)
    
    embed = discord.Embed(title="🧪 Position Parsing Test", color=0x0099ff)
    embed.add_field(name="Input", value=f"`{position_str}`", inline=False)
    embed.add_field(name="Parsed Result", value=f"```json\n{json.dumps(position_data, indent=2)}\n```", inline=False)
    
    await ctx.send(embed=embed)

@bot.command()
async def testvalidate(ctx, position_str: str):
    """Test validation position string"""
    is_valid, message = await TradingCalculator.validate_position_string(position_str)
    
    embed = discord.Embed(
        title="🧪 Position Validation Test",
        color=0x00ff00 if is_valid else 0xff0000
    )
    embed.add_field(name="Input", value=f"`{position_str}`", inline=False)
    embed.add_field(name="Is Valid", value=str(is_valid), inline=True)
    embed.add_field(name="Message", value=message, inline=True)
    
    await ctx.send(embed=embed)

# ----REAL-TIME PRICE FETCHER----
class PriceFetcher:
    # API Keys dari environment variables
    COIN_MARKET_CAP_API_KEY = os.getenv('COIN_MARKET_CAP_API_KEY', '')
    ALPHA_VANTAGE_API_KEY    = os.getenv('ALPHA_VANTAGE_API_KEY', '')
    FCSAPI_API_KEY           = os.getenv('FCSAPI_API_KEY', '')

    # Cache untuk harga dengan expiry time (5 detik)
    _price_cache: Dict[str, Dict] = {}
    CACHE_EXPIRY = 5  # detik

    # Mapping asset ke simbol exchange yang komprehensif
    ASSET_MAPPING = {
        # Top 20 Crypto (contoh)
        'BTC': 'BTCUSDT', 'ETH': 'ETHUSDT', 'BNB': 'BNBUSDT',
        'SOL': 'SOLUSDT', 'XRP': 'XRPUSDT', 'ADA': 'ADAUSDT',
        'DOGE': 'DOGEUSDT', 'AVAX': 'AVAXUSDT', 'DOT': 'DOTUSDT',
        'LINK': 'LINKUSDT', 'MATIC': 'MATICUSDT', 'SHIB': 'SHIBUSDT',
        'LTC': 'LTCUSDT', 'BCH': 'BCHUSDT', 'XLM': 'XLMUSDT',
        'ATOM': 'ATOMUSDT', 'ETC': 'ETCUSDT', 'XMR': 'XMRUSDT',
        'ALGO': 'ALGOUSDT', 'FIL': 'FILUSDT',

        # Tambahan crypto token terbaru / populer
        'TON': 'TONUSDT',
        'SUI': 'SUIUSDT',
        'PEPE': 'PEPEUSDT',
        'FLOKI': 'FLOKIUSDT',
        'ARB': 'ARBUSDT',

        # Crypto futures terpanas (contoh)
        # … (sama seperti sebelumnya) …

        # Forex pairs
        'XAU': 'XAUUSD', 'GOLD': 'XAUUSD', 'EUR': 'EURUSD',
        'GBP': 'GBPUSD', 'USDJPY': 'USDJPY', 'AUDUSD': 'AUDUSD',
        'USDCAD': 'USDCAD', 'USDCHF': 'USDCHF', 'NZDUSD': 'NZDUSD',

        # Indices
        'SPX': 'US500', 'NAS100': 'NAS100', 'DOW': 'US30',
        'DAX': 'GER30', 'FTSE': 'UK100', 'NIKKEI': 'JP225',

        # Commodities
        'OIL': 'XTIUSD', 'BRENT': 'XBRUSD', 'NATURALGAS': 'NATGAS',
        'SILVER': 'XAGUSD', 'COPPER': 'COPPER', 'PALLADIUM': 'XPDUSD',
        'PLATINUM': 'XPTUSD',
    }

    @staticmethod
    def _get_symbol(asset: str) -> str:
        """Dapatkan simbol exchange dari asset (membedakan Crypto, Forex, Commodity)."""
        asset_clean = asset.upper().replace("USDT", "").replace("PERP", "").replace("/", "").replace("-", "")

        # Prioritas mapping manual
        if asset_clean in PriceFetcher.ASSET_MAPPING:
            return PriceFetcher.ASSET_MAPPING[asset_clean]

        # Forex pair (misal EURUSD, USDJPY) — 6 huruf
        if len(asset_clean) == 6 and asset_clean.isalpha():
            return asset_clean

        # Commodities atau logam
        commodities = ["XAU", "XAG", "XTI", "XBR", "OIL", "BRENT", "XPD", "XPT", "GOLD", "SILVER", "COPPER", "NATGAS"]
        if any(asset_clean.startswith(c) for c in commodities):
            return asset_clean

        # Default ke crypto USDT
        return f"{asset_clean}USDT"

    @staticmethod
    def _is_cache_valid(symbol: str) -> bool:
        if symbol not in PriceFetcher._price_cache:
            return False
        cache_data = PriceFetcher._price_cache[symbol]
        current_time = asyncio.get_event_loop().time()
        return current_time - cache_data['timestamp'] < PriceFetcher.CACHE_EXPIRY

    @staticmethod
    async def _try_binance(symbol: str) -> Optional[float]:
        try:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        return float(Decimal(data['price']))
        except Exception as e:
            logging.debug(f"Binance API error for {symbol}: {e}")
        return None

    @staticmethod
    async def _try_coinmarketcap(symbol: str) -> Optional[float]:
        if not PriceFetcher.COIN_MARKET_CAP_API_KEY:
            return None
        try:
            cmc_mapping = {
                'BTCUSDT': '1', 'ETHUSDT': '1027', 'BNBUSDT': '1839',
                'SOLUSDT': '5426', 'XRPUSDT': '52', 'ADAUSDT': '2010',
                'DOGEUSDT': '74', 'AVAXUSDT': '5805', 'DOTUSDT': '6636',
                'LINKUSDT': '1975', 'MATICUSDT': '3890', 'LTCUSDT': '2',
                'BCHUSDT': '1831', 'XLMUSDT': '512', 'ATOMUSDT': '3794',
                'ETCUSDT': '1321', 'XMRUSDT': '328', 'ALGOUSDT': '4030',
                'FILUSDT': '2280', 'UNIUSDT': '7083', 'AAVEUSDT': '7278',
                # tambahan token mapping jika mau …
            }
            asset_id = cmc_mapping.get(symbol)
            if not asset_id:
                return None
            url = f"https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?id={asset_id}"
            headers = {'X-CMC_PRO_API_KEY': PriceFetcher.COIN_MARKET_CAP_API_KEY}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        if 'data' in data and asset_id in data['data']:
                            return float(Decimal(str(data['data'][asset_id]['quote']['USD']['price'])))
        except Exception as e:
            logging.debug(f"CoinMarketCap API error for {symbol}: {e}")
        return None

    @staticmethod
    async def _try_alphavantage(symbol: str) -> Optional[float]:
        if not PriceFetcher.ALPHA_VANTAGE_API_KEY:
            return None
        try:
            # Forex pairs
            if len(symbol) == 6 and symbol.isalpha():
                from_curr = symbol[:3]
                to_curr   = symbol[3:]
                url = (f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
                       f"&from_currency={from_curr}&to_currency={to_curr}&apikey={PriceFetcher.ALPHA_VANTAGE_API_KEY}")
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=5) as response:
                        if response.status == 200:
                            data = await response.json()
                            if 'Realtime Currency Exchange Rate' in data:
                                return float(Decimal(data['Realtime Currency Exchange Rate']['5. Exchange Rate']))
            # Crypto via AlphaVantage
            elif 'USD' in symbol:
                crypto_symbol = symbol.replace('USD', '')
                url = (f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
                       f"&from_currency={crypto_symbol}&to_currency=USD&apikey={PriceFetcher.ALPHA_VANTAGE_API_KEY}")
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=5) as response:
                        if response.status == 200:
                            data = await response.json()
                            if 'Realtime Currency Exchange Rate' in data:
                                return float(Decimal(data['Realtime Currency Exchange Rate']['5. Exchange Rate']))
        except Exception as e:
            logging.debug(f"Alpha Vantage API error for {symbol}: {e}")
        return None

    @staticmethod
    async def _try_fcsapi(symbol: str) -> Optional[float]:
        if not PriceFetcher.FCSAPI_API_KEY:
            return None
        try:
            if 'USDT' in symbol or len(symbol) <= 6:
                crypto_symbol = symbol.replace('USDT', '')
                url = "https://fcsapi.com/api-v3/crypto/latest"
                params = {
                    'symbol': crypto_symbol,
                    'access_key': PriceFetcher.FCSAPI_API_KEY
                }
            else:
                # forex dan commodities
                url = "https://fcsapi.com/api-v3/forex/latest"
                params = {
                    'symbol': symbol,
                    'access_key': PriceFetcher.FCSAPI_API_KEY
                }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('status') and 'response' in data:
                            for item in data['response']:
                                if 'c' in item:
                                    return float(Decimal(str(item['c'])))
                        elif 'price' in data:
                            return float(Decimal(str(data['price'])))
        except Exception as e:
            logging.debug(f"FCSAPI API error for {symbol}: {e}")
        return None

    # === FCSAPI Commodity (GOLD, SILVER, OIL, BRENT) ===
    @staticmethod
    async def _try_fcsapi_commodity(symbol: str) -> Optional[float]:
        if not PriceFetcher.FCSAPI_API_KEY:
            return None
        try:
            mapping = {
                "XAUUSD": "XAU/USD", "GOLD": "XAU/USD",
                "XAGUSD": "XAG/USD", "SILVER": "XAG/USD",
                "XTIUSD": "OIL", "OIL": "OIL",
                "XBRUSD": "BRENT", "BRENT": "BRENT",
                "XPDUSD": "PALLADIUM", "XPTUSD": "PLATINUM",
                "COPPER": "COPPER", "NATGAS": "NATGAS"
            }
            mapped = mapping.get(symbol.upper(), symbol)
            url = "https://fcsapi.com/api-v3/commodity/latest"
            params = {"symbol": mapped, "access_key": PriceFetcher.FCSAPI_API_KEY}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("status") and "response" in data:
                            for item in data["response"]:
                                if "c" in item:
                                    return float(Decimal(str(item["c"])))
        except Exception as e:
            logging.debug(f"FCSAPI commodity error for {symbol}: {e}")
        return None

    # === GoldAPI ===
    @staticmethod
    async def _try_goldapi(symbol: str) -> Optional[float]:
        """Ambil harga komoditas (emas, perak, minyak) dari GoldAPI.io"""
        GOLDAPI_KEY = os.getenv("GOLDAPI_KEY", "")
        if not GOLDAPI_KEY:
            return None

        try:
            mapping = {
                "XAUUSD": "XAU/USD", "GOLD": "XAU/USD",
                "XAGUSD": "XAG/USD", "SILVER": "XAG/USD",
                "XPTUSD": "XPT/USD", "PLATINUM": "XPT/USD",
                "XPDUSD": "XPD/USD", "PALLADIUM": "XPD/USD",
                "OIL": "WTIOIL/USD", "BRENT": "BRENTOIL/USD",
            }
            mapped = mapping.get(symbol.upper(), symbol.upper())
            url = f"https://www.goldapi.io/api/{mapped}"
            headers = {"x-access-token": GOLDAPI_KEY, "Content-Type": "application/json"}

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "price" in data:
                            return float(Decimal(str(data["price"])))
        except Exception as e:
            logging.debug(f"GoldAPI error for {symbol}: {e}")
        return None

    # === Yahoo Finance ===
    @staticmethod
    async def _try_yahoo(symbol: str) -> Optional[float]:
        """Fallback umum untuk semua aset via Yahoo Finance."""
        try:
            mapping = {
                "XAUUSD": "GC=F", "XAGUSD": "SI=F",
                "OIL": "CL=F", "BRENT": "BZ=F",
                "EURUSD": "EURUSD=X", "GBPUSD": "GBPUSD=X",
                "USDJPY": "JPY=X", "USDCHF": "CHF=X",
            }
            yahoo_symbol = mapping.get(symbol.upper(), symbol.upper())
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_symbol}?interval=1m"

            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
                        return float(price)
        except Exception as e:
            logging.debug(f"Yahoo Finance error for {symbol}: {e}")
        return None

    @staticmethod
    async def get_real_time_price(asset: str) -> Optional[float]:
        """
        Ambil harga real-time multi-sumber (Binance -> CoinMarketCap -> AlphaVantage -> FCSAPI [+commodity]).
        """
        try:
            symbol = PriceFetcher._get_symbol(asset)

            # cek cache
            if PriceFetcher._is_cache_valid(symbol):
                return PriceFetcher._price_cache[symbol]['price']

            # Urutan prioritas multi-sumber
            exchanges = [
                PriceFetcher._try_binance,
                PriceFetcher._try_coinmarketcap,
                PriceFetcher._try_alphavantage,
                PriceFetcher._try_fcsapi,
                PriceFetcher._try_fcsapi_commodity,
                PriceFetcher._try_goldapi,
                PriceFetcher._try_yahoo
            ]

            # fallback khusus untuk komoditas
            if any(x in symbol for x in ["XAU", "XAG", "XTI", "XBR", "OIL", "BRENT", "XPD", "XPT"]):
                exchanges.append(PriceFetcher._try_fcsapi_commodity)

            price = None
            source = "unknown"

            for exchange_func in exchanges:
                price = await exchange_func(symbol)
                if price is not None:
                    source = exchange_func.__name__
                    break

            if price is not None:
                PriceFetcher._price_cache[symbol] = {
                    'price':     price,
                    'timestamp': asyncio.get_event_loop().time(),
                    'source':    source
                }
                logging.debug(f"Harga {asset} ({symbol}): {price} dari {source}")
            else:
                logging.warning(f"Harga real-time tidak ditemukan untuk {asset} (symbol: {symbol})")

            return price

        except Exception as e:
            logging.error(f"Error fetching real-time price for {asset}: {str(e)}")
            return None

    @staticmethod
    async def get_multiple_prices(assets: List[str]) -> Dict[str, Optional[float]]:
        results: Dict[str, Optional[float]] = {}
        for asset in assets:
            results[asset] = await PriceFetcher.get_real_time_price(asset)
        return results

    @staticmethod
    async def get_price_with_retry(asset: str, retries: int = 3, delay: float = 1.0) -> Optional[float]:
        for attempt in range(retries):
            try:
                price = await PriceFetcher.get_real_time_price(asset)
                if price is not None:
                    return price
                if attempt < retries - 1:
                    await asyncio.sleep(delay)
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1} failed for {asset}: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(delay)
        logging.error(f"Failed to get price for {asset} after {retries} attempts")
        return None

    @staticmethod
    async def get_24h_change(asset: str) -> Optional[float]:
        try:
            symbol = PriceFetcher._get_symbol(asset)
            url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        return float(Decimal(data['priceChangePercent']))
        except Exception as e:
            logging.debug(f"Error getting 24h change for {asset}: {e}")
        return None

    @staticmethod
    async def get_volume_24h(asset: str) -> Optional[float]:
        try:
            symbol = PriceFetcher._get_symbol(asset)
            url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        return float(Decimal(data['volume']))
        except Exception as e:
            logging.debug(f"Error getting 24h volume for {asset}: {e}")
        return None

    @staticmethod
    async def clear_cache():
        PriceFetcher._price_cache.clear()
        logging.info("Price cache cleared")

    @staticmethod
    async def get_cache_info() -> Dict:
        current_time = asyncio.get_event_loop().time()
        cache_info: Dict[str, Dict] = {}
        for symbol, cache_data in PriceFetcher._price_cache.items():
            age = current_time - cache_data['timestamp']
            cache_info[symbol] = {
                'price': cache_data['price'],
                'age_seconds': round(age, 2),
                'source': cache_data['source']
            }
        return cache_info
        
# Utility function untuk format harga
def format_price(price: float) -> str:
    """Format harga dengan presisi tinggi"""
    try:
        if price == 0:
            return "0"
        
        if price >= 1:
            # Untuk harga >= 1, gunakan 2-4 digit desimal
            decimals = min(4, max(2, len(str(price).split('.')[1]) if '.' in str(price) else 0))
            formatted = f"{price:,.{decimals}f}"
        else:
            # Untuk harga < 1, gunakan presisi tinggi
            formatted = f"{price:.8f}".rstrip('0').rstrip('.')
            if formatted == '':
                formatted = '0'
        
        # Ganti decimal point dengan koma untuk format Indonesia
        formatted = formatted.replace('.', ',')
        return formatted
        
    except (ValueError, TypeError):
        return str(price)            
            
async def generate_position_example(asset: str) -> str:
    """Generate contoh format position berdasarkan asset"""
    try:
        current_price = await PriceFetcher.get_real_time_price(asset)
        if current_price is None:
            current_price = 50000  # Default fallback
            
        if "USD" in asset.upper() or "EUR" in asset.upper() or "JPY" in asset.upper():
            # Forex pair
            sl_distance = current_price * 0.01  # 1% SL
            tp1_distance = current_price * 0.02  # 2% TP1
            return f"BUY/{current_price:.2f}/{current_price-sl_distance:.2f}/{current_price+tp1_distance:.2f}//1/LOT"
        else:
            # Crypto
            sl_distance = current_price * 0.05  # 5% SL
            tp1_distance = current_price * 0.08  # 8% TP1
            return f"BUY/{current_price:.2f}/{current_price-sl_distance:.2f}/{current_price+tp1_distance:.2f}//1/USD"
            
    except:
        return "BUY/50000/49000/51000//1/USD"
        
# ----Konversi waktu----
def parse_datetime(dt_str: str) -> datetime:
    """Handle various datetime formats from database"""
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            continue
            
    # Fallback to current time if all parsing fails
    logging.warning(f"Failed to parse datetime: {dt_str}")
    return datetime.utcnow()

def from_utc(utc_dt: datetime) -> datetime:
    """Convert UTC to WIB (UTC+7) with timezone awareness"""
    if not utc_dt.tzinfo:
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)
    return utc_dt.astimezone(timezone(timedelta(hours=7)))

def get_utc_now():
    """Mendapatkan waktu UTC sekarang dengan timezone aware"""
    return datetime.now(timezone.utc)

def to_wib(utc_dt):
    """Konversi waktu UTC ke WIB (UTC+7)"""
    jakarta_tz = pytz.timezone('Asia/Jakarta')
    return utc_dt.astimezone(jakarta_tz)

def format_wib(dt_str):
    """Konversi string datetime UTC ke format WIB"""
    try:
        # Konversi string ke datetime UTC
        dt_utc = datetime.fromisoformat(dt_str).replace(tzinfo=timezone.utc)
        # Konversi ke WIB (UTC+7)
        dt_wib = to_wib(dt_utc)
        # Format ke string
        return dt_wib.strftime('%d %B %Y %H:%M:%S WIB')
    except (ValueError, TypeError):
        # Jika string tidak valid atau null
        return dt_str if dt_str else '-'

# Definisikan timezone Jakarta
jakarta_tz = timezone(timedelta(hours=7))

def to_wib(dt):
    return dt.astimezone(jakarta_tz)


# ===============================================================
# 🔄 TUGAS OTOMATIS: CEK LANGGANAN WizardMember KEDALUWARSA
# ===============================================================
@tasks.loop(hours=12.0)
async def check_Wizard_member_expiry():
    """
    Mengecek semua user WizardMemberBulanan dan WizardMemberTahunan.
    Jika tanggal kedaluwarsa sudah lewat, user otomatis diturunkan
    menjadi member biasa, role diganti, dan notifikasi dikirim.
    """
    await bot.wait_until_ready()
    logging.info("🔍 Memulai pengecekan kedaluwarsa WizardMember (Bulanan & Tahunan)...")

    if not bot.guilds:
        logging.warning("⚠️ Bot belum terhubung ke server manapun.")
        return

    guild = bot.guilds[0]

    try:
        # Ambil semua data user dari database
        users = await Database.get_all_users()
        now_utc = datetime.utcnow()

        expired_count = 0
        soon_expired_count = 0

        # Siapkan channel laporan
        log_channel = discord.utils.get(guild.text_channels, name="laporan")

        for user_id, username, status, sub_type, expiry_str in users:
            if status not in ["WizardMemberBulanan", "WizardMemberTahunan"]:
                continue
            if not expiry_str:
                continue

            try:
                expiry_dt = datetime.fromisoformat(expiry_str)
            except Exception:
                logging.warning(f"⛔ Format tanggal tidak valid untuk user {username}: {expiry_str}")
                continue

            member = guild.get_member(user_id)
            if not member:
                continue

            # Hitung selisih waktu
            time_left = expiry_dt - now_utc
            days_left = time_left.days

            # Jika sudah kedaluwarsa
            if time_left.total_seconds() <= 0:
                expired_count += 1
                status_text = "WizardMemberBulanan" if status == "WizardMemberBulanan" else "WizardMemberTahunan"

                # Hapus role Wizard dan tambah role member
                try:
                    Wizard_role = discord.utils.get(
                        guild.roles, name="WizardMemberBulanan" if status == "WizardMemberBulanan" else "WizardMemberTahunan"
                    )
                    member_role = discord.utils.get(guild.roles, name="Member")

                    if Wizard_role and Wizard_role in member.roles:
                        await member.remove_roles(Wizard_role, reason="Langganan kedaluwarsa")

                    if member_role and member_role not in member.roles:
                        await member.add_roles(member_role, reason="Downgrade otomatis")

                    # Update database
                    await Database.update_user_status(
                        user_id=user_id,
                        status="member",
                        subscription_type=None,
                        expiry_date=None
                    )

                    # DM ke user
                    try:
                        embed = discord.Embed(
                            title="⚠️ Langganan Kedaluwarsa",
                            description=(
                                f"Halo **{member.display_name}**, langganan **{status_text}** Anda telah berakhir.\n\n"
                                "Anda kini kembali ke status **member biasa**.\n\n"
                                "✨ Untuk memperpanjang langganan, silakan hubungi admin "
                                "atau gunakan tombol **Langganan Premium** di channel `#verifikasi`."
                            ),
                            color=discord.Color(COLOR_DARK)
                        )
                        await member.send(embed=embed)
                    except discord.Forbidden:
                        logging.warning(f"Tidak dapat kirim DM ke {member.display_name} (DM tertutup).")

                    # Laporan ke admin
                    if log_channel:
                        await log_channel.send(
                            f"⚠️ {member.mention} ({status_text}) langganannya **kedaluwarsa** dan telah diturunkan menjadi member."
                        )

                    logging.info(f"⏳ Langganan {status_text} kedaluwarsa: {member.display_name}")

                except Exception as role_err:
                    logging.error(f"Gagal menghapus role kedaluwarsa {username}: {role_err}")

            # Jika sisa 3 hari atau kurang → kirim peringatan
            elif 0 < days_left <= 3:
                soon_expired_count += 1
                try:
                    embed_warn = discord.Embed(
                        title="⏰ Pengingat Langganan Hampir Berakhir",
                        description=(
                            f"Halo **{member.display_name}**,\n\n"
                            f"Langganan **{status}** Anda akan berakhir dalam **{days_left} hari** "
                            f"pada **{expiry_dt.strftime('%d %B %Y')}**.\n\n"
                            "Silakan perpanjang agar tidak kehilangan akses ke fitur premium 💎."
                        ),
                        color=discord.Color.gold()
                    )
                    await member.send(embed=embed_warn)
                    logging.info(f"📩 Peringatan kedaluwarsa dikirim ke {member.display_name} ({days_left} hari).")
                except discord.Forbidden:
                    logging.warning(f"Tidak dapat kirim peringatan ke {member.display_name} (DM tertutup).")

        # Kirim laporan rekap
        if log_channel:
            summary = (
                f"📅 **Laporan Otomatis Pengecekan Langganan MountAlgo**\n\n"
                f"🕒 Waktu: {datetime.utcnow().strftime('%d %B %Y %H:%M UTC')}\n"
                f"🔻 Kedaluwarsa: {expired_count} user\n"
                f"⚠️ Akan kedaluwarsa (≤3 hari): {soon_expired_count} user\n"
                f"✅ Selesai diperiksa semua WizardMember"
            )
            await log_channel.send(summary)

        logging.info(f"✅ Pengecekan selesai: {expired_count} expired, {soon_expired_count} warning.")

    except Exception as e:
        logging.error(f"❌ Error di check_Wizard_member_expiry: {e}", exc_info=True)
        
#--user-----
# Mapping status ke role
STATUS_ROLE_MAP = {
    "member": "Member",
    "WizardMemberBulanan": "WizardMemberBulanan",
    "WizardMemberTahunan": "WizardMemberTahunan",
    "Admin": "Admin",
    "PendingVerification": "Unverified"
}

# Update STATUS_ROLES
STATUS_ROLES = list(STATUS_ROLE_MAP.values())

async def ensure_core_roles(guild: discord.Guild):
    """Pastikan semua role inti sudah dibuat"""
    role_configs = {
        "Member": discord.Color(COLOR_CYAN),
        "WizardMemberBulanan": discord.Color(COLOR_GREEN),
        "WizardMemberTahunan": discord.Color(COLOR_VIOLET),
        "Admin": discord.Color(COLOR_VIOLET),
        "Unverified": discord.Color(COLOR_DARK),
        "Muted": discord.Color(COLOR_DARK)
    }
    
    for role_name, color in role_configs.items():
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            perms = discord.Permissions(administrator=True) if role_name == "Admin" else discord.Permissions.none()
            await guild.create_role(
                name=role_name,
                color=color,
                permissions=perms,
                reason="Role otomatis"
            )
        elif role_name == "Admin" and not role.permissions.administrator:
            try:
                await role.edit(permissions=discord.Permissions(administrator=True))
            except Exception as e:
                logging.error(f"Gagal mengedit permissions Admin di ensure_core_roles: {e}")

class VerificationSystem:
    @staticmethod
    async def apply_verification_workflow(guild: discord.Guild):
        """Sistem utama untuk pending verification"""
        channel_verifikasi = discord.utils.get(guild.text_channels, name="verifikasi")
        if channel_verifikasi:
            await VerificationSystem.update_verification_channel(channel_verifikasi)
        
        await VerificationSystem.process_pending_verification(guild)

    @staticmethod
    async def verify_and_update_database(member: discord.Member):
        """
        Verifikasi user dan otomatis update di database
        """
        # Step 1: Verifikasi user di Discord
        unverified_role = discord.utils.get(member.guild.roles, name="Unverified")
        member_role = discord.utils.get(member.guild.roles, name="Member")
        
        # Hapus role Unverified & tambahkan role member
        if unverified_role and unverified_role in member.roles:
            await member.remove_roles(unverified_role)
        if member_role:
            await member.add_roles(member_role)
            
        # Step 2: Otomatis update status di database
        await Database.update_user_status(
            user_id=member.id,
            status="member",
            subscription_type=None,
            expiry_date=None
        )
        
        # Step 3: Kirim konfirmasi ke user
        try:
            await member.send(
                "✅ **Verifikasi Selesai!**\n"
                "Status Anda telah diubah menjadi member di sistem kami.\n"
                "Anda sekarang dapat mengakses semua channel publik server MountAlgo."
            )
        except discord.Forbidden:
            pass  # Skip jika tidak bisa kirim DM
            
        # Step 4: Log perubahan
        logging.info(f"User {member.display_name} ({member.id}) diverifikasi & diupdate database jadi member")
            
        return True

    @staticmethod
    async def update_verification_channel(channel: discord.TextChannel):
        """Perbarui pesan utama di channel verifikasi"""
        # Hapus semua pesan lama
        try:
            await channel.purge(limit=50)
        except:
            pass
            
        # Buat embed baru
        embed = discord.Embed(
            title="🚦 VERIFIKASI ANGGOTA MountAlgo",
            description=(
                "**Selamat datang di komunitas MountAlgo!**\n\n"
                "Untuk mengakses server, Anda harus menyetujui peraturan dan melakukan verifikasi:\n"
                "```diff\n"
                "+ 1. Baca #peraturan dan #disclaimer\n"
                "+ 2. Klik tombol 'Setuju & Verifikasi' di bawah ini\n"
                "+ 3. Jika ingin langganan premium klik 'Langganan Premium'\n"
                "```\n"
                "Hanya anggota terverifikasi yang bisa mengakses channel server."
            ),
            color=COLOR_VIOLET
        )
        embed.add_field(
            name="⚠ PENTING",
            value=(
                "Dengan klik tombol verifikasi, Anda menyetujui:\n"
                "➩ Seluruh peraturan server\n"
                "➩ Kebijakan privasi\n"
                "➩ Persyaratan penggunaan"
            ),
            inline=False
        )
        embed.set_footer(text="MountAlgo Security System (tekan Dismiss Message Untuk menghapus Pesan)")
        
        # Kirim dengan tombol verifikasi utama
        await channel.send(embed=embed, view=VerifView())
    
    @staticmethod
    async def process_pending_verification(guild: discord.Guild):
        """Proses semua anggota tanpa role member yang belum diverifikasi"""
        unverified_role = discord.utils.get(guild.roles, name="Unverified")
        if not unverified_role:
            return
            
        # Cari anggota dengan role Unverified
        unverified_members = [m for m in guild.members if unverified_role in m.roles]
        
        for member in unverified_members:
            # Tambahkan ke database sebagai pending verification
            await Database.add_user(
                user_id=member.id,
                username=member.name,
                status="PendingVerification",
                subscription_type=None,
                expiry_date=None
            )
            
            # Kirim DM instruksi
            try:
                await member.send(
                    "🔐 **PENDAFTARAN MountAlgo**\n"
                    f"Halo {member.mention},\n"
                    "Anda telah bergabung dengan server MountAlgo namun belum melakukan verifikasi.\n\n"
                    "Silakan kunjungi channel #verifikasi di server dan klik tombol "
                    "**Setuju & Verifikasi** untuk mendapatkan akses penuh ke server.\n\n"
                    "Jika mengalami kesulitan, hubungi admin."
                )
            except:
                pass  # Skip jika tidak bisa kirim DM

    @staticmethod
    async def verify_user(member: discord.Member):
        """Lakukan verifikasi user dan berikan role member"""
        try:
            # Role yang perlu diatur
            unverified_role = discord.utils.get(member.guild.roles, name="Unverified")
            member_role = discord.utils.get(member.guild.roles, name="Member")
            
            # Hapus role unverified dan beri role member
            if unverified_role and unverified_role in member.roles:
                await member.remove_roles(unverified_role)
            if member_role:
                await member.add_roles(member_role)
            
            # Update database
            await Database.update_user_status(
                member.id,
                "member",
                subscription_type=None,
                expiry_date=None
            )
            
            # Kirim konfirmasi
            try:
                await member.send(
                    "✅ **VERIFIKASI BERHASIL!**\n"
                    "Anda sekarang memiliki akses penuh ke server MountAlgo!\n\n"
                    "Silakan jelajahi:\n"
                    "➩ 📢 #pengumuman untuk informasi terkini\n"
                    "➩ 💬 #lounge-chat untuk berdiskusi\n"
                    "➩ 📈 #akademi untuk belajar trading"
                )
            except:
                pass
            
            return True
        except Exception as e:
            logging.error(f"Gagal verifikasi user {member.id}: {str(e)}")
            return False

    @staticmethod
    async def upgrade_to_premium(member: discord.Member, sub_type: str, duration_days: int):
        """Upgrade user ke status WizardMemberBulanan atau WizardMemberTahunan"""
        try:
            # Tentukan role berdasarkan jenis
            if sub_type.lower() == "bulanan":
                new_status = "WizardMemberBulanan"
                role_name = "WizardMemberBulanan"
            elif sub_type.lower() == "tahunan":
                new_status = "WizardMemberTahunan"
                role_name = "WizardMemberTahunan"
            else:
                raise ValueError("Jenis langganan tidak dikenal, gunakan 'bulanan' atau 'tahunan'.")

            # Update role
            await apply_user_roles(member, new_status)

            # Simpan tanggal kedaluwarsa
            expiry = (datetime.utcnow() + timedelta(days=duration_days)).isoformat()

            # Update database
            await Database.update_user_status(
                member.id,
                new_status,
                subscription_type=sub_type.lower(),
                expiry_date=expiry
            )

            # Kirim notifikasi ke user
            await member.send(
                f"🎉 **UPGRADE BERHASIL!**\n"
                f"Anda kini menjadi **{new_status}**.\n\n"
                f"🗓️ Berlaku hingga: `{expiry.split('T')[0]}`\n"
                "Terima kasih telah bergabung sebagai anggota premium 💎."
            )
            return True
        except Exception as e:
            logging.error(f"Gagal upgrade user {member.id}: {str(e)}", exc_info=True)
            return False


async def synchronize_admin_added_users(guild: discord.Guild) -> int:
    """Proses upgrade otomatis untuk user yang diadd admin"""
    return 0


# Fungsi Sinkronisasi Harian yang Memperhitungkan Verifikasi
async def sync_verification_system(guild: discord.Guild):
    """Sinkronisasi sistem verifikasi setiap hari"""
    # Logika sinkronisasi utama
    report_lines = ["📅 **LAPORAN HARIAN VERIFIKASI**"]
    
    # Proses semua user dengan status PendingVerification
    pending_users = await Database.get_pending_users()
    pending_count = 0
    notified_count = 0
    
    for user_id, username in pending_users:
        member = guild.get_member(user_id)
        if member:
            # Jika belum diverifikasi dalam 24 jam
            days_since_joined = (datetime.utcnow() - member.joined_at).days
            if days_since_joined >= 1:
                try:
                    # Kirim pengingat verifikasi
                    await member.send(
                        "🔔 **Peringatan Verifikasi**\n"
                        "Anda belum menyelesaikan verifikasi di server MountAlgo!\n"
                        "Silakan kunjungi #verifikasi dan klik tombol 'Setuju & Verifikasi'."
                    )
                    notified_count += 1
                except:
                    pass
            pending_count += 1
    
    report_lines.append(f"✅ Pengguna tertunda: {pending_count} | Diingatkan: {notified_count}")
    
    # Proses upgrade otomatis untuk user yang diadd admin
    updated_users = await synchronize_admin_added_users(guild)
    report_lines.append(f"✅ User ditambah admin: {updated_users}")
    
    # Kirim laporan
    admin_ch = discord.utils.get(guild.text_channels, name="laporan")
    if admin_ch:
        report = "\n".join(report_lines)
        await admin_ch.send(report)
    
    return f"Sinkronisasi harian selesai! {pending_count} user tertunda"

async def apply_user_roles(member: discord.Member, status: str):
    """Terapkan role sesuai status user dengan nama role tepat"""
    try:
        if not member or not member.guild or not member.guild.me.guild_permissions.manage_roles:
            return
            
        # Dapatkan role dengan nama yang konsisten
        member_role = discord.utils.get(member.guild.roles, name="Member")
        Wizard_bulanan_role = discord.utils.get(member.guild.roles, name="WizardMemberBulanan")
        Wizard_tahunan_role = discord.utils.get(member.guild.roles, name="WizardMemberTahunan")
        admin_role = discord.utils.get(member.guild.roles, name="Admin")
        unverified_role = discord.utils.get(member.guild.roles, name="Unverified")
        
        # Buat role jika belum ada
        if not member_role:
            member_role = await member.guild.create_role(
                name="Member",
                reason="Role otomatis",
                color=discord.Color(COLOR_CYAN)
            )
        if not Wizard_bulanan_role:
            Wizard_bulanan_role = await member.guild.create_role(
                name="WizardMemberBulanan",
                reason="Role otomatis",
                color=discord.Color(COLOR_GREEN)
            )
        if not Wizard_tahunan_role:
            Wizard_tahunan_role = await member.guild.create_role(
                name="WizardMemberTahunan",
                reason="Role otomatis",
                color=discord.Color(COLOR_VIOLET)
            )
        if not admin_role:
            admin_role = await member.guild.create_role(
                name="Admin",
                reason="Role otomatis",
                color=discord.Color(COLOR_VIOLET),
                permissions=discord.Permissions(administrator=True)
            )
        elif not admin_role.permissions.administrator:
            try:
                await admin_role.edit(permissions=discord.Permissions(administrator=True))
            except Exception as e:
                logging.error(f"Gagal mengedit permissions Admin di apply_user_roles: {e}")
        if not unverified_role:
            unverified_role = await member.guild.create_role(
                name="Unverified",
                reason="Role otomatis",
                color=discord.Color(COLOR_DARK)
            )
        
        # Hapus semua role level sebelumnya
        roles_to_remove = []
        if status == "WizardMemberBulanan":
            roles_to_remove = [r for r in [member_role, Wizard_tahunan_role, admin_role, unverified_role] if r and r in member.roles]
        elif status == "WizardMemberTahunan":
            roles_to_remove = [r for r in [member_role, Wizard_bulanan_role, admin_role, unverified_role] if r and r in member.roles]
        elif status == "Admin":
            roles_to_remove = [r for r in [member_role, Wizard_bulanan_role, Wizard_tahunan_role, unverified_role] if r and r in member.roles]
        elif status == "PendingVerification":
            roles_to_remove = [r for r in [member_role, Wizard_bulanan_role, Wizard_tahunan_role, admin_role] if r and r in member.roles]
        else:  # member
            roles_to_remove = [r for r in [Wizard_bulanan_role, Wizard_tahunan_role, admin_role, unverified_role] if r and r in member.roles]
            
        if roles_to_remove:
            await member.remove_roles(*roles_to_remove)
        
        # Tambahkan role baru
        if status == "WizardMemberBulanan" and Wizard_bulanan_role:
            await member.add_roles(Wizard_bulanan_role)
        elif status == "WizardMemberTahunan" and Wizard_tahunan_role:
            await member.add_roles(Wizard_tahunan_role)
        elif status == "Admin" and admin_role:
            await member.add_roles(admin_role)
        elif status == "PendingVerification" and unverified_role:
            await member.add_roles(unverified_role)
        elif member_role:  # Default ke member
            await member.add_roles(member_role)
            
    except discord.Forbidden:
        logging.error(f"Bot tidak punya izin untuk mengatur role di server {member.guild.name}")
    except discord.HTTPException as e:
        logging.error(f"Error HTTP saat mengelola role: {e.status} {e.text}")
    except Exception as e:
        logging.error(f"Error tidak terduga di apply_user_roles: {str(e)}")
        
async def synchronize_Wizard_expirations(guild: discord.Guild) -> int:
    """Sinkronisasi otomatis kedaluwarsa WizardMemberBulanan & WizardMemberTahunan"""
    expired_count = 0
    try:
        async with aiosqlite.connect(Database.DB_PATH) as db:
            query = """
                SELECT user_id, expiry_date, status
                FROM users 
                WHERE (status = 'WizardMemberBulanan' OR status = 'WizardMemberTahunan')
                AND expiry_date IS NOT NULL
            """
            async with db.execute(query) as cursor:
                Wizard_members = await cursor.fetchall()

        now = datetime.utcnow()

        for user_id, expiry_date, current_status in Wizard_members:
            try:
                expiry_dt = datetime.fromisoformat(expiry_date)
            except:
                continue

            if expiry_dt < now:
                member = guild.get_member(user_id)
                if not member:
                    continue

                # Downgrade ke member
                await apply_user_roles(member, "member")
                await Database.update_user_status(user_id, "member", None, None)

                # DM user
                try:
                    tipe = "Bulanan" if current_status == "WizardMemberBulanan" else "Tahunan"
                    await member.send(
                        f"⚠️ Langganan WizardMember {tipe} Anda telah **kedaluwarsa**.\n"
                        "Status Anda telah diubah menjadi **member biasa**."
                    )
                except discord.Forbidden:
                    pass

                expired_count += 1
                logging.info(f"✅ Downgrade {member.display_name} ({current_status}) karena kedaluwarsa.")
    except Exception as e:
        logging.error(f"Error sinkronisasi kedaluwarsa: {e}", exc_info=True)

    return expired_count

def get_role_by_status(status: str) -> str:
    """Map status database ke nama role Discord"""
    status_mapping = {
        "member": "Member",
        "WizardMemberBulanan": "WizardMemberBulanan",
        "WizardMemberTahunan": "WizardMemberTahunan",
        "Admin": "Admin"
    }
    return status_mapping.get(status, "Member")

def get_role(guild, role_name):
    """Dapatkan role dengan penanganan error"""
    return discord.utils.get(guild.roles, name=role_name)

# ===============================================================
# ✅ FUNGSI VALIDASI INPUT USER (Versi WizardMember Ganda)
# ===============================================================
def validate_user_input(user_id: str, username: str, status: str, expiry_date: str = ""):
    """
    Memvalidasi input dari admin saat menambah/upgrade user.
    Mendukung status baru: WizardMemberBulanan & WizardMemberTahunan.
    
    Returns:
        dict: hasil validasi berisi field siap simpan ke database.
    Raises:
        ValueError: jika ada input tidak valid.
    """
    from datetime import datetime, timedelta

    # --- Validasi user_id ---
    if not user_id.isdigit():
        raise ValueError("❌ ID Pengguna harus berupa angka!")

    user_id = int(user_id)

    # --- Validasi username ---
    if not username or len(username.strip()) < 2:
        raise ValueError("❌ Nama pengguna tidak boleh kosong atau terlalu pendek!")
    username = username.strip()

    # --- Validasi status ---
    valid_statuses = ["Member", "WizardMemberBulanan", "WizardMemberTahunan", "Admin"]
    if status not in valid_statuses:
        raise ValueError(f"❌ Status tidak valid! Pilih salah satu dari: {', '.join(valid_statuses)}")

    # --- Tentukan subscription_type & expiry_date ---
    subscription_type = None
    expiry_result = None

    if status in ["WizardMemberBulanan", "WizardMemberTahunan"]:
        subscription_type = "bulanan" if status == "WizardMemberBulanan" else "tahunan"

        # Jika expiry_date kosong → hitung otomatis
        if not expiry_date.strip():
            days = 30 if subscription_type == "bulanan" else 365
            expiry_result = (datetime.utcnow().date() + timedelta(days=days)).isoformat()
        else:
            # Pastikan format valid (YYYY-MM-DD)
            try:
                expiry_result = datetime.strptime(expiry_date.strip(), "%Y-%m-%d").date().isoformat()
            except ValueError:
                raise ValueError("❌ Format tanggal tidak valid! Gunakan format YYYY-MM-DD.")
    else:
        # Untuk Member & Admin tidak perlu expiry_date
        expiry_result = None
        subscription_type = None

    # --- Return hasil validasi ---
    return {
        "user_id": user_id,
        "username": username,
        "status": status,
        "subscription_type": subscription_type,
        "expiry_date": expiry_result,
    }

async def find_invalid_status_users(guild: discord.Guild):
    """
    Temukan dan perbaiki user dengan status/role tidak valid di database.
    Validasi penuh mendukung: member, WizardMemberBulanan, WizardMemberTahunan, Admin, PendingVerification.
    """
    try:
        users = await Database.get_all_users()
        log_channel = discord.utils.get(guild.text_channels, name="laporan")

        fixed_users = []
        invalid_users = []

        for user in users:
            user_id, username, status, sub_type, expiry = user
            member = guild.get_member(user_id)
            if not member:
                continue  # Skip jika user tidak ada di server

            valid = True
            fix_note = ""

            # --- VALIDASI STATUS ---
            if status not in STATUS_ROLE_MAP:
                valid = False
                fix_note = "Status tidak dikenal, diset ulang jadi member"
                await Database.update_user_status(user_id, "member", None, None)
                await apply_user_roles(member, "member")

            # --- VALIDASI Wizard BULANAN ---
            elif status == "WizardMemberBulanan":
                if sub_type != "bulanan" or not expiry:
                    valid = False
                    fix_note = "Sub-type atau expiry hilang (WizardBulanan diperbaiki)"
                    expiry = (datetime.utcnow() + timedelta(days=30)).isoformat()
                    await Database.update_user_status(user_id, "WizardMemberBulanan", "bulanan", expiry)
                    await apply_user_roles(member, "WizardMemberBulanan")
                else:
                    try:
                        datetime.fromisoformat(expiry)
                    except Exception:
                        valid = False
                        fix_note = "Format expiry salah, diperbaiki otomatis (30 hari dari sekarang)"
                        expiry = (datetime.utcnow() + timedelta(days=30)).isoformat()
                        await Database.update_user_status(user_id, "WizardMemberBulanan", "bulanan", expiry)
                        await apply_user_roles(member, "WizardMemberBulanan")

            # --- VALIDASI Wizard TAHUNAN ---
            elif status == "WizardMemberTahunan":
                if sub_type != "tahunan" or not expiry:
                    valid = False
                    fix_note = "Sub-type atau expiry hilang (WizardTahunan diperbaiki)"
                    expiry = (datetime.utcnow() + timedelta(days=365)).isoformat()
                    await Database.update_user_status(user_id, "WizardMemberTahunan", "tahunan", expiry)
                    await apply_user_roles(member, "WizardMemberTahunan")
                else:
                    try:
                        datetime.fromisoformat(expiry)
                    except Exception:
                        valid = False
                        fix_note = "Format expiry salah, diperbaiki otomatis (365 hari dari sekarang)"
                        expiry = (datetime.utcnow() + timedelta(days=365)).isoformat()
                        await Database.update_user_status(user_id, "WizardMemberTahunan", "tahunan", expiry)
                        await apply_user_roles(member, "WizardMemberTahunan")

            # --- VALIDASI MEMBER / ADMIN / PENDING ---
            elif status in ["member", "Admin", "PendingVerification"]:
                if sub_type or expiry:
                    valid = False
                    fix_note = "Sub-type/expiry tidak seharusnya ada, dihapus"
                    await Database.update_user_status(user_id, status, None, None)
                    await apply_user_roles(member, status)

            # --- REKAP ---
            if valid:
                continue
            else:
                invalid_users.append((username, fix_note))
                fixed_users.append(member.display_name)
                logging.info(f"🔧 Perbaiki {username}: {fix_note}")

        # --- LAPORAN ---
        if log_channel:
            if fixed_users:
                fixed_list = "\n".join([f"✅ {u}" for u in fixed_users])
                await log_channel.send(
                    f"🧩 **Laporan Validasi & Perbaikan User MountAlgo**\n\n"
                    f"Total Diperbaiki: {len(fixed_users)} user\n\n{fixed_list}"
                )
            else:
                await log_channel.send("✅ Semua data user valid. Tidak ada perbaikan diperlukan.")

        return fixed_users

    except Exception as e:
        logging.error(f"Error di find_invalid_status_users (Auto-Fix): {e}", exc_info=True)
        return []

#---(sinkronasi db dengan role user-----
async def synchronize_users_and_roles(guild: discord.Guild):
    """
    Sinkronisasi database ↔ role Discord
    Versi penuh mendukung: WizardMemberBulanan & WizardMemberTahunan
    """
    report = [
        "🔁 **PROSES SINKRONISASI PENGGUNA MountAlgo**",
        f"📅 {datetime.now(timezone.utc).strftime('%d/%m %H:%M UTC')}"
    ]

    db_users = {str(u[0]): u for u in await Database.get_all_users()}
    members = {str(m.id): m for m in guild.members if not m.bot}

    stats = {"added": 0, "updated": 0, "fixed_roles": 0, "expired": 0}

    for user_id, user_data in db_users.items():
        user_id_num = int(user_id)
        _, username, db_status, sub_type, expiry = user_data
        member = members.get(user_id)
        if not member:
            continue

        # Perbarui username jika berubah
        if member.name != username:
            await Database.update_username(user_id_num, member.name)

        # Cek kedaluwarsa
        if db_status in ["WizardMemberBulanan", "WizardMemberTahunan"] and expiry:
            try:
                expiry_dt = datetime.fromisoformat(expiry)
                if expiry_dt < datetime.utcnow():
                    db_status = "member"
                    sub_type = None
                    expiry = None
                    await Database.update_user_status(user_id_num, "member", None, None)
                    stats["expired"] += 1
                    report.append(f"⏳ {member.display_name}: langganan berakhir → Member")
            except Exception:
                pass

        # Cari status berdasarkan role Discord saat ini
        current_roles = [r.name for r in member.roles]
        role_status = "PendingVerification"
        if "Admin" in current_roles:
            role_status = "Admin"
        elif "WizardMemberTahunan" in current_roles:
            role_status = "WizardMemberTahunan"
        elif "WizardMemberBulanan" in current_roles:
            role_status = "WizardMemberBulanan"
        elif "Member" in current_roles:
            role_status = "member"

        # Tentukan status akhir berdasarkan prioritas
        resolved_status = "PendingVerification"
        if db_status == "Admin" or role_status == "Admin":
            resolved_status = "Admin"
        elif db_status == "WizardMemberTahunan" or role_status == "WizardMemberTahunan":
            resolved_status = "WizardMemberTahunan"
        elif db_status == "WizardMemberBulanan" or role_status == "WizardMemberBulanan":
            resolved_status = "WizardMemberBulanan"
        elif db_status == "member" or role_status == "member":
            resolved_status = "member"

        # Jika resolved status berubah dari DB status
        if resolved_status != db_status:
            new_sub_type = None
            new_expiry = None
            if resolved_status == "WizardMemberBulanan":
                new_sub_type = "bulanan"
                new_expiry = expiry if (db_status == "WizardMemberBulanan" and expiry) else (datetime.utcnow() + timedelta(days=30)).isoformat()
            elif resolved_status == "WizardMemberTahunan":
                new_sub_type = "tahunan"
                new_expiry = expiry if (db_status == "WizardMemberTahunan" and expiry) else (datetime.utcnow() + timedelta(days=365)).isoformat()

            await Database.update_user_status(user_id_num, resolved_status, new_sub_type, new_expiry)
            stats["updated"] += 1
            report.append(f"🔄 DB Update {member.display_name}: {db_status} -> {resolved_status}")
            db_status = resolved_status
            sub_type = new_sub_type
            expiry = new_expiry

        # Pastikan role di Discord sinkron dengan resolved status
        target_role_name = None
        if resolved_status == "Admin":
            target_role_name = "Admin"
        elif resolved_status == "WizardMemberTahunan":
            target_role_name = "WizardMemberTahunan"
        elif resolved_status == "WizardMemberBulanan":
            target_role_name = "WizardMemberBulanan"
        elif resolved_status == "member":
            target_role_name = "Member"
        elif resolved_status == "PendingVerification":
            target_role_name = "Unverified"

        if target_role_name and target_role_name not in current_roles:
            await apply_user_roles(member, resolved_status)
            stats["fixed_roles"] += 1
            report.append(f"🎭 Role Update {member.display_name} -> {target_role_name}")
        else:
            stats["updated"] += 1

    # Tambahkan user baru ke database
    existing_ids = set(db_users.keys())
    for mid, member in members.items():
        if mid not in existing_ids:
            roles = [r.name for r in member.roles]
            status = "PendingVerification"
            sub_type = None
            expiry = None

            if "Admin" in roles:
                status = "Admin"
            elif "WizardMemberTahunan" in roles:
                status, sub_type = "WizardMemberTahunan", "tahunan"
                expiry = (datetime.utcnow() + timedelta(days=365)).isoformat()
            elif "WizardMemberBulanan" in roles:
                status, sub_type = "WizardMemberBulanan", "bulanan"
                expiry = (datetime.utcnow() + timedelta(days=30)).isoformat()
            elif "Member" in roles:
                status = "member"

            await Database.add_user(member.id, member.name, status, sub_type, expiry)
            stats["added"] += 1
            report.append(f"➕ Tambah user baru ke DB: {member.display_name} ({status})")

    # Laporan
    final_report = (
        f"✅ **Sinkronisasi Selesai**\n"
        f"Total DB: {len(db_users)} | Total Member: {len(members)}\n"
        f"📈 Diperbarui: {stats['updated']} | Role Diperbaiki: {stats['fixed_roles']} | "
        f"Ditambah: {stats['added']} | Kedaluwarsa: {stats['expired']}"
    )

    log_channel = discord.utils.get(guild.text_channels, name="laporan")
    if log_channel:
        await log_channel.send(final_report)
    logging.info(final_report)
    return final_report

# ===================== STRUKTUR SERVER =====================
SERVER_STRUCTURE = [
    ("🌏|HALAMAN UTAMA|", ["@everyone"], [
        ("welcome", "Selamat datang untuk semua anggota baru.", ["@everyone"]),
        ("peraturan", "Aturan dasar server yang wajib dipatuhi.", ["@everyone"]),
        ("disclaimer", "Informasi hukum dan tanggung jawab penggunaan konten.", ["@everyone"]),
        ("verifikasi", "Proses verifikasi pengguna (2 tombol: Setuju & Langganan).", ["@everyone"]),
    ]),
    ("🔥|MEMBER|", ["@Member", "@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"], [
        ("bantuan", "Panduan cepat untuk pengguna baru (FAQ & verifikasi langganan).", ["@Member","@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"]),
        ("pengumuman", "Update resmi tentang server atau layanan.", ["@Member", "@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"]),
        ("all-news", "Kanal berita dan analisis finansial global.", ["@Member", "@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"]),
        ("lounge-chat", "Ruang diskusi umum antar anggota.", ["@Member", "@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"]),
        ("roadmap_trader", "perjalanan seorang trader yang berkelanjutan.", ["@Member", "@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"]),
        ("akademi", "Materi edukasi trading.", ["@Member", "@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"]),
        ("free-indikator", "Indikator gratis yang dikembangkan MountAlgo.", ["@Member", "@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"]),
        ("share-your-profits", "Bagikan profit kamu dengan Semua member.", ["@Member","@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"]),
        ("member-voice", "Ruang obrolan suara antar anggota.", ["@Member", "@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"], "voice"),
        ("member-stage", "Panggung utama diskusi panel & event komunitas.", ["@Member", "@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"], "stage"),
    ]),
    ("🧬|WIZARD|🚀🚀", ["@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"], [
        ("wizard-lounge-chat", "Ruang diskusi khusus anggota premium Wizard.", ["@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"]),
        ("wizard-toolkits", "Tools bantu strategi trading personal.", ["@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"]),
        ("wizard-strategy", "Kumpulan strategi trading  yang sudah di packing.", ["@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"]),
        ("wizard-crypto", "Analisis harian aset Crypto premium.", ["@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"]),
        ("wizard-forex", "Analisis harian Forex premium.", ["@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"]),
        ("wizard-gold", "Analisis harian Emas & Komoditas premium.", ["@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"]),
        ("relaxation-games", "Game santai untuk melepas penat setelah trading.", ["@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"]),
        ("music-videos", "Musik & Video santai untuk relaksasi.", ["@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"]),
        ("wizard-voice", "Ruang obrolan suara eksklusif Wizard Member.", ["@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"], "voice"),
        ("wizard-stage", "Panggung live sesi analisis & edukasi premium.", ["@WizardMemberBulanan", "@WizardMemberTahunan", "@Admin"], "stage"),
    ]),
    ("🧩|CYPHER|", ["@Admin"], [
        ("kontrol-admin", "Pengaturan admin, hak akses, dan kontrol server.", ["@Admin"]),
        ("kontrol-pengguna", "Kelola pengguna, izin, dan status langganan.", ["@Admin"]),
        ("laporan", "Rekap aktivitas, pelanggaran, dan data pengguna.", ["@Admin"]),
        ("bot3", "bot pihak ketiga.", ["@Admin"]),
    ]),
]

# ===================== DATABASE HANDLER =====================
class Database:
    DB_PATH = "/storage/303F-13EA/Download/MountAlgo_bot/MountAlgo.db"
# --- setup db ---
    @classmethod
    async def setup(cls):
        try:
            db_dir = os.path.dirname(cls.DB_PATH)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
                
            async with aiosqlite.connect(cls.DB_PATH) as db:
                # Buat tabel users jika belum ada
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        status TEXT,
                        subscription_type TEXT,
                        expiry_date TEXT
                    )
                """)
                
                # Buat tabel spam jika belum ada
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS spam (
                        user_id INTEGER,
                        last_msg TEXT,
                        count INTEGER
                    )
                """)
                
                # Buat tabel violations jika belum ada
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS violations (
                        user_id INTEGER PRIMARY KEY,
                        count INTEGER DEFAULT 0,
                        last_violation TEXT
                    )
                """)

                # Buat tabel settings jika belum ada
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS settings (
                        key TEXT PRIMARY KEY,
                        value TEXT
                    )
                """)
                
                # Perbaiki: Tambahkan mekanisme untuk menambahkan kolom secara kondisional
                column_changes = [
                    # (nama_kolom, tipe_data, perintah_sql)
                    ("subscription_type", "TEXT", "ALTER TABLE users ADD COLUMN subscription_type TEXT"),
                    ("expiry_date", "TEXT", "ALTER TABLE users ADD COLUMN expiry_date TEXT")
                ]
                
                # Cek kolom yang sudah ada untuk users
                cursor = await db.execute("PRAGMA table_info(users)")
                existing_columns_users = [row[1] for row in await cursor.fetchall()]
                
                # Tambahkan kolom yang belum ada untuk users
                for column_name, col_type, sql_command in column_changes[:2]:  # Only users columns
                    if column_name not in existing_columns_users and "users" in sql_command:
                        try:
                            await db.execute(sql_command)
                            logging.info(f"[Database] Kolom {column_name} ditambahkan ke tabel users")
                        except aiosqlite.OperationalError as e:
                            if "duplicate column name" not in str(e).lower():
                                logging.warning(f"Failed to add column {column_name} to users: {e}")
                
                await db.commit()
                logging.info("[Database] Setup selesai. Semua tabel dan kolom dipastikan ada.")
                
        except Exception as e:
            logging.error(f"[Database.setup] Critical error: {e}")
            raise



    # --- settings db ---
    @classmethod
    async def get_setting(cls, key: str, default: str = None) -> str | None:
        try:
            async with aiosqlite.connect(cls.DB_PATH) as db:
                async with db.execute("SELECT value FROM settings WHERE key = ?", (key,)) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        return row[0]
                    return default
        except Exception as e:
            logging.error(f"get_setting error: {e}")
            return default

    @classmethod
    async def set_setting(cls, key: str, value: str):
        try:
            async with aiosqlite.connect(cls.DB_PATH) as db:
                await db.execute(
                    "INSERT INTO settings (key, value) VALUES (?, ?) "
                    "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                    (key, str(value))
                )
                await db.commit()
                return True
        except Exception as e:
            logging.error(f"set_setting error: {e}")
            return False

    # --- user db ---
    @classmethod
    async def add_user(
        cls, 
        user_id: int, 
        username: str, 
        status: str,
        subscription_type: str | None = None,
        expiry_date: str | None = None
    ):
        """Tambah user baru ke database"""
        try:
            async with aiosqlite.connect(cls.DB_PATH) as db:
                await db.execute(
                    "INSERT INTO users (user_id, username, status, subscription_type, expiry_date) "
                    "VALUES (?, ?, ?, ?, ?) "
                    "ON CONFLICT(user_id) DO UPDATE SET "
                    "username = excluded.username, "
                    "status = excluded.status, "
                    "subscription_type = excluded.subscription_type, "
                    "expiry_date = excluded.expiry_date",
                    (user_id, username, status, subscription_type, expiry_date)
                )
                await db.commit()
                return True
        except Exception as e:
            logging.error(f"add_user error: {str(e)}")
            return False

    @staticmethod
    async def check_expiry():
        """
        Mengecek dan memperbarui status user WizardMemberBulanan & WizardMemberTahunan yang sudah kedaluwarsa.
        Mengembalikan daftar user_id yang statusnya diubah menjadi member.
        """
        try:
            async with aiosqlite.connect(Database.DB_PATH) as db:
                # Ambil semua user premium dengan expiry
                query = """
                    SELECT user_id, username, status, expiry_date 
                    FROM users 
                    WHERE status IN ('WizardMemberBulanan', 'WizardMemberTahunan')
                    AND expiry_date IS NOT NULL
                """
                async with db.execute(query) as cursor:
                    results = await cursor.fetchall()

            if not results:
                logging.info("Tidak ada user WizardMember untuk dicek kadaluwarsa.")
                return []

            now = datetime.utcnow()
            expired_users = []

            async with aiosqlite.connect(Database.DB_PATH) as db:
                for user_id, username, status, expiry_str in results:
                    try:
                        expiry_dt = datetime.fromisoformat(expiry_str)
                    except Exception:
                        logging.warning(f"⛔ Format expiry tidak valid untuk {username}: {expiry_str}")
                        continue

                    # Jika tanggal kedaluwarsa sudah lewat
                    if expiry_dt < now:
                        expired_users.append((user_id, username, status))
                        await db.execute(
                            "UPDATE users SET status='member', subscription_type=NULL, expiry_date=NULL WHERE user_id=?",
                            (user_id,)
                        )
                await db.commit()

            if expired_users:
                for uid, uname, stat in expired_users:
                    logging.info(f"🕓 Langganan {stat} kedaluwarsa: {uname} ({uid})")
            else:
                logging.info("✅ Tidak ada langganan yang kedaluwarsa.")

            return expired_users

        except Exception as e:
            logging.error(f"Error di Database.check_expiry(): {e}", exc_info=True)
            return []

    @classmethod
    async def update_user_status(
        cls, 
        user_id: int, 
        status: str,
        subscription_type: Optional[str] = None,
        expiry_date: Optional[str] = None
    ):
        """Update status user dengan opsi langganan"""
        try:
            async with aiosqlite.connect(cls.DB_PATH) as db:
                if subscription_type and expiry_date:
                    await db.execute(
                        "UPDATE users SET status=?, subscription_type=?, expiry_date=? WHERE user_id=?",
                        (status, subscription_type, expiry_date, user_id)
                    )
                else:
                    await db.execute(
                        "UPDATE users SET status=?, subscription_type=NULL, expiry_date=NULL WHERE user_id=?",
                        (status, user_id)
                    )
                await db.commit()
        except Exception as e:
            logging.error(f"[Database.update_user_status] Error: {e}")

    @classmethod
    async def remove_user(cls, user_id) -> bool:
        try:
            async with aiosqlite.connect(cls.DB_PATH) as db:
                await db.execute(
                    "DELETE FROM users WHERE user_id=?",
                    (user_id,)
                )
                await db.commit()  # ✅ TAMBAHKAN INI!
                return True
        except Exception as e:
            logging.error(f"[Database.remove_user] Error: {e}")
            return False

    @classmethod
    async def update_username(cls, user_id: int, new_username: str):
        """Update username di database"""
        try:
            async with aiosqlite.connect(cls.DB_PATH) as db:
                await db.execute(
                    "UPDATE users SET username = ? WHERE user_id = ?",
                    (new_username, user_id)
                )
                await db.commit()
        except Exception as e:
            logging.error(f"[Database.update_username] Error: {e}")
    
    @classmethod
    async def get_all_users(cls):
        """Dapatkan semua data user"""
        try:
            async with aiosqlite.connect(cls.DB_PATH) as db:
                query = """
                    SELECT user_id, username, status, subscription_type, expiry_date 
                    FROM users
                    ORDER BY status, user_id
                """
                async with db.execute(query) as cursor:
                    return await cursor.fetchall()
        except Exception as e:
            logging.error(f"[Database.get_all_users] Error: {e}")
            return []
            
    @classmethod
    async def get_user_subscription(cls, user_id: int):
        """Dapatkan informasi langganan user"""
        try:
            async with aiosqlite.connect(cls.DB_PATH) as db:
                async with db.execute(
                    "SELECT subscription_type, expiry_date FROM users WHERE user_id = ?",
                    (user_id,)
                ) as cursor:
                    return await cursor.fetchone()
        except Exception as e:
            logging.error(f"[Database.get_user_subscription] Error: {e}")
            return None

    @classmethod
    async def get_user_data(cls, user_id: int) -> tuple | None:
        """Ambil semua data user berdasarkan ID, return None jika tidak ditemukan"""
        try:
            async with aiosqlite.connect(cls.DB_PATH) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    "SELECT user_id, username, status, subscription_type, expiry_date FROM users WHERE user_id = ?",
                    (user_id,)
                ) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        return tuple(row)  # Convert ke tuple untuk konsistensi
                    return None
        except Exception as e:
            logging.error(f"get_user_data error: {str(e)}")
            return None

    @classmethod
    async def update_user_status(
        cls, 
        user_id: int, 
        status: str,
        subscription_type: Optional[str] = None,
        expiry_date: Optional[str] = None
    ):
        """Update status user dengan options"""
        try:
            async with aiosqlite.connect(cls.DB_PATH) as db:
                await db.execute(
                    "UPDATE users SET status = ?, subscription_type = ?, expiry_date = ? "
                    "WHERE user_id = ?",
                    (status, subscription_type, expiry_date, user_id)
                )
                await db.commit()
        except Exception as e:
            logging.error(f"Database.update_user_status error: {str(e)}")

    @classmethod
    async def get_pending_users(cls):
        """Dapatkan user dengan status PendingVerification"""
        try:
            async with aiosqlite.connect(cls.DB_PATH) as db:
                async with db.execute(
                    "SELECT user_id, username FROM users WHERE status = 'PendingVerification'"
                ) as cursor:
                    return await cursor.fetchall()
        except Exception as e:
            logging.error(f"Database.get_pending_users error: {str(e)}")
            return []
            
    # --- spam db ---
    @classmethod
    async def update_spam(cls, user_id, last_msg, count):
        try:
            async with aiosqlite.connect(cls.DB_PATH) as db:
                await db.execute(
                    "REPLACE INTO spam (user_id, last_msg, count) VALUES (?, ?, ?)",
                    (user_id, last_msg, count)
                )
                await db.commit()
        except Exception as e:
            logging.error(f"[Database.update_spam] Error: {e}")

    @classmethod
    async def get_spam(cls, user_id):
        try:
            async with aiosqlite.connect(cls.DB_PATH) as db:
                async with db.execute(
                    "SELECT last_msg, count FROM spam WHERE user_id=?",
                    (user_id,)
                ) as cursor:
                    return await cursor.fetchone()
        except Exception as e:
            logging.error(f"[Database.get_spam] Error: {e}")
            return None
            
    # --- violations db ---
    @classmethod
    async def add_violation(cls, user_id):
        try:
            async with aiosqlite.connect(cls.DB_PATH) as db:
                async with db.execute("SELECT count FROM violations WHERE user_id=?", (user_id,)) as cursor:
                    row = await cursor.fetchone()
                now = datetime.utcnow().isoformat()
                if row:
                    count = row[0] + 1
                    await db.execute(
                        "UPDATE violations SET count=?, last_violation=? WHERE user_id=?",
                        (count, now, user_id)
                    )
                else:
                    count = 1
                    await db.execute(
                        "INSERT INTO violations (user_id, count, last_violation) VALUES (?, ?, ?)",
                        (user_id, count, now)
                    )
                await db.commit()
                return count
        except Exception as e:
            logging.error(f"[Database.add_violation] Error: {e}")
            return 0

    @classmethod
    async def reset_violations(cls, user_id):
        try:
            async with aiosqlite.connect(cls.DB_PATH) as db:
                await db.execute("DELETE FROM violations WHERE user_id=?", (user_id,))
                await db.commit()
        except Exception as e:
            logging.error(f"[Database.reset_violations] Error: {e}")
#---obrolanview
    @staticmethod
    def get_role(guild, role_name):
        """Dapatkan role dengan penanganan error"""
        try:
            return discord.utils.get(guild.roles, name=role_name.replace("@", ""))
        except Exception:
            return None

# ===================== ATUR IZIN OTOMATIS =====================
CHANNEL_PERMISSIONS = {
    "welcome": {
        "@everyone": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        }
    },
    "peraturan": {
        "@everyone": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        }
    },
    "disclaimer": {
        "@everyone": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        }
    },
    "verifikasi": {
        "@everyone": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        }
    },
    "bantuan": {
        "@Member": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberTahunan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberBulanan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@Admin": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        }
    },
    "pengumuman": {
        "@Member": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberTahunan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberBulanan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@Admin": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        }
    },
    "all-news": {
        "@Member": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberTahunan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberBulanan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@Admin": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": True,
            "add_reactions": True,
            "embed_links": True,
            "attach_files": True,
            "mention_everyone": True,
            "manage_messages": True,
            "manage_channels": True,
            "manage_permissions": True,
        }
    },
    "lounge-chat": {
        "@Member": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": True,
            "attach_files": True,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": True,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberTahunan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": True,
            "attach_files": True,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": True,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberBulanan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": True,
            "attach_files": True,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": True,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@Admin": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": True,
            "attach_files": True,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": True,
            "use_external_emojis": False,
            "manage_messages": False,
        }
    },
    "roadmap_trader": {
        "@Member": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": False,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberTahunan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberBulanan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@Admin": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        }
    },
    "akademi": {
        "@Member": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberTahunan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberBulanan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@Admin": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        }
    },
    "free-indikator": {
        "@Member": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberTahunan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberBulanan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@Admin": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        }
    },
    "share-your-profits": {
        "@Member": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberTahunan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": True,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": True,
            "mention_everyone": True,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberBulanan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": True,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": True,
            "mention_everyone": True,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@Admin": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": True,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": True,
            "mention_everyone": True,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        }
    },
    "wizard-lounge-chat": {
        "@WizardMemberTahunan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": True,
            "attach_files": True,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": True,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberBulanan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": True,
            "attach_files": True,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": True,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@Admin": {
            "view_channel": True,
            "send_messages": True,
            "add_reactions": True,
            "embed_links": True,
            "mention_everyone": True,
            "manage_messages": True,
            "manage_channels": True,
            "manage_permissions": True,
        }
    },
    "wizard-crypto": {
        "@WizardMemberTahunan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberBulanan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@Admin": {
            "view_channel": True,
            "send_messages": True,
            "add_reactions": True,
            "embed_links": True,
            "mention_everyone": True,
            "manage_messages": True,
            "manage_channels": True,
            "manage_permissions": True,
        }
    },
    "wizard-forex": {
        "@WizardMemberTahunan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberBulanan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@Admin": {
            "view_channel": True,
            "send_messages": True,
            "add_reactions": True,
            "embed_links": True,
            "mention_everyone": True,
            "manage_messages": True,
            "manage_channels": True,
            "manage_permissions": True,
        }
    },
    "wizard-gold": {
        "@WizardMemberTahunan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberBulanan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@Admin": {
            "view_channel": True,
            "send_messages": True,
            "add_reactions": True,
            "embed_links": True,
            "mention_everyone": True,
            "manage_messages": True,
            "manage_channels": True,
            "manage_permissions": True,
        }
    },
    "wizard-strategy": {
        "@WizardMemberTahunan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberBulanan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@Admin": {
            "view_channel": True,
            "send_messages": True,
            "add_reactions": True,
            "embed_links": True,
            "mention_everyone": True,
            "manage_messages": True,
            "manage_channels": True,
            "manage_permissions": True,
        }
    },
    "wizard-toolkits": {
        "@WizardMemberTahunan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberBulanan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@Admin": {
            "view_channel": True,
            "send_messages": True,
            "add_reactions": True,
            "embed_links": True,
            "mention_everyone": True,
            "manage_messages": True,
            "manage_channels": True,
            "manage_permissions": True,
        }
    },
    "kontrol-pengguna": {
        "@Admin": {
            "view_channel": True,
            "send_messages": True,
            "add_reactions": True,
            "embed_links": True,
            "attach_files": True,
            "mention_everyone": True,
            "manage_messages": True,
            "manage_channels": True,
            "manage_permissions": True,
        }
    },
    "kontrol-admin": {
        "@Admin": {
            "view_channel": True,
            "send_messages": True,
            "add_reactions": True,
            "embed_links": True,
            "attach_files": True,
            "mention_everyone": True,
            "manage_messages": True,
            "manage_channels": True,
            "manage_permissions": True,
        }
    },
    "bot3": {
        "@Admin": {
            "view_channel": True,
            "send_messages": True,
            "add_reactions": True,
            "embed_links": True,
            "attach_files": True,
            "mention_everyone": True,
            "manage_messages": True,
            "manage_channels": True,
            "manage_permissions": True,
        }
    },
    "laporan": {
        "@Admin": {
            "view_channel": True,
            "send_messages": True,
            "add_reactions": True,
            "embed_links": True,
            "attach_files": True,
            "mention_everyone": True,
            "manage_messages": True,
            "manage_channels": True,
            "manage_permissions": True,
        }
    },
    "relaxation-games": {
        "@WizardMemberTahunan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberBulanan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@Admin": {
            "view_channel": True,
            "send_messages": True,
            "add_reactions": True,
            "embed_links": True,
            "mention_everyone": True,
            "manage_messages": True,
            "manage_channels": True,
            "manage_permissions": True,
        }
    },
    "music-videos": {
        "@WizardMemberTahunan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@WizardMemberBulanan": {
            "view_channel": True,
            "read_message_history": True,
            "send_messages": False,
            "add_reactions": True,
            "embed_links": False,
            "attach_files": False,
            "mention_everyone": False,
            "create_public_threads": False,
            "create_private_threads": False,
            "send_messages_in_threads": False,
            "use_external_emojis": False,
            "manage_messages": False,
        },
        "@Admin": {
            "view_channel": True,
            "send_messages": True,
            "add_reactions": True,
            "embed_links": True,
            "mention_everyone": True,
            "manage_messages": True,
            "manage_channels": True,
            "manage_permissions": True,
        }
    },
}

async def apply_channel_permissions(guild: discord.Guild):
    success_count = 0
    error_count = 0
    error_details = []
    
    for channel_name, role_perms in CHANNEL_PERMISSIONS.items():
        channel = discord.utils.get(guild.text_channels, name=channel_name)
        if not channel:
            error_count += 1
            error_details.append(f"Channel `{channel_name}` tidak ditemukan")
            continue
            
        for role_name, perms in role_perms.items():
            if role_name == "@everyone":
                role = guild.default_role
            else:
                role = discord.utils.get(guild.roles, name=role_name.replace("@", ""))
                
            if not role:
                error_count += 1
                error_details.append(f"Role `{role_name}` tidak ditemukan di `{channel_name}`")
                continue
                
            try:
                overwrite = PermissionOverwrite()
                for perm, value in perms.items():
                    setattr(overwrite, perm, value)
                    
                await channel.set_permissions(role, overwrite=overwrite)
                success_count += 1
            except Exception as e:
                error_count += 1
                error_details.append(f"Gagal atur {role_name} di {channel_name}: {str(e)}")
    
    return success_count, error_count, error_details
#---thread--
async def create_analysis_threads(channel: discord.TextChannel):
    """Membuat thread otomatis untuk Wizard Analisis"""
    thread_names = [
        "1.analisa fundamental",
        "2.analisa teknikal"
    ]
    
    created_threads = []
    
    for name in thread_names:
        try:
            # Cek apakah thread sudah ada
            existing_thread = discord.utils.get(channel.threads, name=name)
            
            if not existing_thread:
                # Buat thread baru
                thread = await channel.create_thread(
                    name=name,
                    auto_archive_duration=1440,  # 1 hari
                    reason="Thread analisis otomatis"
                )
                created_threads.append(thread.name)
                
                # Tambahkan pesan pembuka di thread
                if "fundamental" in name.lower():
                    await thread.send("**Thread Analisis Fundamental**\nDiskusikan analisis fundamental harian di sini.")
                elif "teknikal" in name.lower():
                    await thread.send("**Thread Analisis Teknikal**\nDiskusikan analisis teknikal dan pola grafik harian di sini.")
                
        except Exception as e:
            logging.error(f"Gagal membuat thread {name}: {str(e)}")
    
    return created_threads

# ===================== KONTEN EMBED =====================
# --- Atur Izin embed ---
async def send_permission_update_embed(interaction: Optional[discord.Interaction], success_count: int, error_count: int, error_details: list):
    """Mengirim embed laporan hasil pengaturan izin channel"""
    # Waktu dalam WIB
    wib_now = to_wib(get_utc_now())
    
    # Tentukan warna berdasarkan hasil
    if error_count == 0:
        title = "⦿ PERMISSION CONFIGURATION SUCCESS"
        color = COLOR_GREEN  # Positive green
        description = "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n✔ Semua izin channel telah diatur ulang dengan sukses!\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
    else:
        title = "⚠ PERMISSION CONFIGURATION WARNING"
        color = COLOR_VIOLET  # Notice blue (changed from orange for better visibility)
        description = (
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            f"Pengaturan izin selesai dengan {success_count} berhasil,\n"
            f"tetapi ada {error_count} error yang perlu diperiksa.\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        )
    
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=wib_now
    )
    
    # Statistik channel
    embed.add_field(
        name="⬈ CONFIGURATION SUMMARY",
        value=(
            f"▹ Total channels: `{len(CHANNEL_PERMISSIONS)}`\n"
            f"▹ Success: `{success_count}`\n"
            f"▹ Errors: `{error_count}`\n"
            f"▹ Timestamp: <t:{int(wib_now.timestamp())}:R>"
        ),
        inline=False
    )
    
    # Tampilkan error jika ada
    if error_count > 0:
        # Batasi maksimal 5 error yang ditampilkan
        error_list = "\n".join([f"✘ {e}" for e in error_details[:5]])
        if error_count > 5:
            error_list += f"\n➩ Dan {error_count - 5} error lainnya..."
            
        embed.add_field(
            name="⬊ ERROR DETAILS",
            value=f"```diff\n{error_list}\n```",
            inline=False
        )
        
        embed.add_field(
            name="⬈ TROUBLESHOOTING GUIDE",
            value=(
                "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                "① Pastikan semua role sudah dibuat\n"
                "② Verifikasi nama channel sesuai\n"
                "③ Cek permission bot (Manage Roles & Channels)\n"
                "④ Ulangi proses atau hubungi developer\n"
                "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
            ),
            inline=False
        )
    
    # Footer dengan avatar admin atau bot
    if interaction:
        embed.set_footer(
            text=f"▰ Executed by {interaction.user.display_name} ▰",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else None
        )
    else:
        embed.set_footer(
            text=f"▰ MountAlgo BOT SYSTEM ▰",
            icon_url=bot.user.avatar.url if bot.user.avatar else None
        )
    
    embed.set_thumbnail(url=interaction.guild.me.display_avatar.url)
    
    return embed
 
# --- Welcome ---
async def send_welcome_embed(channel: discord.TextChannel):
    """Mengirim embed welcome dengan desain khusus dan tombol ke channel peraturan"""
    # Buat objek embed
    embed = discord.Embed(color=COLOR_VIOLET)  # Gunakan warna #5134ff

    # Teks besar di tengah vertikal (format: tebal, italic)
    large_text ="|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n\n" "***▰▰▰▰▰ KNOWING THEN RUNNING / LEAVING***" "\n"
    small_text = "Trader terbaik berjalan berdasarkan riset ▰▰▰▰\n lalu komitmen dan konsisten ▰▰▰▰" "\n\n|\n|\n|\n|\n|\n|\n|\n|\n|\n" # Teks kecil biasa

    # Gabungkan teks dengan format
    embed.description = (
        f"\n\n{large_text}\n"  # \n\n untuk pusat vertikal
        f"{small_text}\n\n"    # Teks kecil di bawah
    )

    # Buat tombol yang mengarah ke channel peraturan
    class WelcomeButtonView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            # Cari channel peraturan di server
            rules_channel = discord.utils.get(channel.guild.text_channels, name="peraturan")
            # Buat tombol jika channel ditemukan
            if rules_channel:
                self.add_item(discord.ui.Button(
                    label="Arungi Lautan Pasar 🌊🛳️ ",
                    style=discord.ButtonStyle.success,
                    url=f"https://discord.com/channels/{channel.guild.id}/{rules_channel.id}"
                ))

    # Kirim embed beserta tombol
    await channel.send(embed=embed, view=WelcomeButtonView())

# --- Peraturan Server ---
async def send_peraturan_embed(channel: discord.TextChannel):
    embed = discord.Embed(
        title="\n" "》》 PERATURAN SERVER MountAlgo 》》",
        description=(
            "\n✇ Selamat datang di komunitas **MountAlgo**!\n"
            "✇ Agar server tetap nyaman, aman, dan bermanfaat untuk semua,\n"
            "✇ harap baca dan patuhi peraturan berikut:"
        ),
        color=COLOR_GREEN
    )
    embed.add_field(
        name="➮ ➊ Saling Menghormati",
        value="```diff\n❑ Hormati semua anggota tanpa memandang latar belakang.\n❑ Tidak diperbolehkan SARA, bullying, atau provokasi.```",
        inline=False
    )
    embed.add_field(
        name="➮ ➋ Dilarang Spam & Iklan",
        value="```diff\n❑ Spam pesan, promosi, atau link tanpa izin admin\n❑ **dilarang keras**.```",
        inline=False
    )
    embed.add_field(
        name="➮ ➌ Jaga Privasi",
        value="```diff\n❑ Dilarang menyebarkan data pribadi milik sendiri\n❑ atau orang lain tanpa izin.```",
        inline=False
    )
    embed.add_field(
        name="➮ ➍ Konten & Bahasa",
        value="```diff\n❑ Gunakan bahasa yang sopan.\n❑ Tidak diperbolehkan konten NSFW, judi, atau ilegal.```",
        inline=False
    )
    embed.add_field(
        name="➮ ➎ Topik Diskusi",
        value="```diff\n❑ Fokus pada trading, edukasi, dan diskusi finansial.\n❑ Hindari OOT (off-topic) di channel utama.```",
        inline=False
    )
    embed.add_field(
        name="➮ ➏ Ikuti Arahan Admin/Moderator",
        value="```diff\n❑ Keputusan admin/moderator bersifat final\n❑ demi kenyamanan bersama.```",
        inline=False
    )
    embed.add_field(
        name="➮ ➐ Sanksi",
        value="```diff\n❑ Pelanggaran akan diberikan peringatan\n❑ hingga banned permanen sesuai tingkat pelanggaran.```",
        inline=False
    )
    embed.set_footer(text="▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\nDengan tetap berada di server ini, Anda dianggap setuju dengan seluruh peraturan di atas.\n✇ Selamat berdiskusi & belajar bersama!")
    embed.set_thumbnail(url=channel.guild.me.display_avatar.url)
    # Buat tombol yang mengarah ke channel peraturan
    class PeraturanButtonView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            # Cari channel peraturan di server
            rules_channel = discord.utils.get(channel.guild.text_channels, name="disclaimer")
            # Buat tombol jika channel ditemukan
            if rules_channel:
                self.add_item(discord.ui.Button(
                    label="Melanjutkan baca Disclaimer ⚠️ ",
                    style=discord.ButtonStyle.success,
                    url=f"https://discord.com/channels/{channel.guild.id}/{rules_channel.id}"
                ))

    # Kirim embed beserta tombol
    await channel.send(embed=embed, view=PeraturanButtonView())

# --- Disclaimer ---
async def send_disclaimer_embed(channel: discord.TextChannel):
    embed = discord.Embed(
        title="🌟 Selamat Datang di Komunitas MountAlgo! 🌟",
        description=(
            "Sebelum menjelajah lebih jauh, mari bersama-sama memahami prinsip komunitas kita\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "**Komunitas ini adalah ruang edukasi mandiri, bukan platform investasi berizin**\n"
            "Silakan baca pernyataan berikut dengan saksama ⚠️"
        ),
        color=COLOR_CYAN  # Warna biru yang lebih ramah
    )
    
    # Header hukum dengan penyampaian lebih positif
    embed.add_field(
        name="📋 Status Komunitas Edukasi",
        value=(
            "```diff\n"
            "+ MountAlgo adalah komunitas edukasi trading\n"
            "+ Fokus utama: pembelajaran mandiri\n"
            "+ Semua konten bersifat edukasional\n"
            "- Bukan penyedia jasa investasi/penasihat keuangan\n"
            "- Tidak terafiliasi dengan broker manapun\n"
            "```"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🤝 Tanggung Jawab Bersama",
        value=(
            "```diff\n"
            "▸ Dengan bergabung, kita sepakat:\n"
            "+ Berbagi pengetahuan trading\n"
            "+ Mengedepankan pembelajaran mandiri\n"
            "+ Verifikasi broker melalui situs resmi:\n"
            "  • https://bappebti.go.id\n"
            "  • https://ojk.go.id\n"
            "```"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⚠️ Penting: Manajemen Risiko",
        value=(
            "```diff\n"
            "▸ Trading mengandung risiko tinggi:\n"
            "! Hanya gunakan dana 'siap rugi'\n"
            "! Hindari dana kebutuhan pokok/utang\n"
            "! Fluktuasi pasar tak terduga\n"
            "+ Komunitas siap bantu edukasi manajemen risiko\n"
            "```"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🛡️ Keamanan & Regulasi",
        value=(
            "```diff\n"
            "▸ Mari bersama patuhi:\n"
            "+ UU Pasar Modal & Peraturan BAPPEBTI\n"
            "+ Prinsip anti pencucian uang\n"
            "+ Kewajiban perpajakan\n"
            "! Laporkan aktivitas mencurigakan ke moderator\n"
            "```"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔒 Proteksi Diri",
        value=(
            "```diff\n"
            "▸ Ingat selalu:\n"
            "! MountAlgo tidak pernah meminta dana/transfer\n"
            "! Tidak menjanjikan keuntungan pasti\n"
            "! Waspada penawaran via DM/pribadi\n"
            "+ Moderator siap bantu verifikasi informasi\n"
            "```"
        ),
        inline=False
    )
    
    embed.set_footer(
        text="Dengan melanjutkan, Anda menyatakan telah memahami semangat komunitas edukasi ini 🤗"
    )
    embed.set_thumbnail(url=channel.guild.me.display_avatar.url)
    
    class DisclaimerButtonView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            rules_channel = discord.utils.get(channel.guild.text_channels, name="verifikasi")
            if rules_channel:
                self.add_item(discord.ui.Button(
                    label="🚀 Lanjutkan & Verifikasi Sekarang",
                    style=discord.ButtonStyle.primary,
                    emoji="✅",
                    url=f"https://discord.com/channels/{channel.guild.id}/{rules_channel.id}"
                ))

    await channel.send(
        content="Halo para calon trader! 👋 Mari mulai perjalanan edukasi bersama...",
        embed=embed,
        view=DisclaimerButtonView()
    )
# --- Verifikasi ---
async def send_verifikasi_embed(channel: discord.TextChannel):
    embed = discord.Embed(
        title="⦿ MountAlgo » Verifikasi Anggota",
        description=(
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "✚ Selamat datang di komunitas **MountAlgo**!\n\n"
            "➩ Untuk mengakses seluruh fitur server, silakan lakukan verifikasi terlebih dahulu.\n"
            "➩ Jika ingin menjadi member premium (Wizard Member), klik tombol langganan di bawah.\n\n"
            "☛ Pastikan sudah membaca [Peraturan](#peraturan) dan [Disclaimer](#disclaimer) sebelum melanjutkan.\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        color=COLOR_CYAN
    )
    embed.add_field(
        name="❑ Privasi & Keamanan",
        value=(
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "✔ Data dan aktivitas Anda di server ini dijaga kerahasiaannya\n"
            "✘ Jangan bagikan password atau data pribadi ke siapapun\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        inline=False
    )
    embed.set_footer(text="∎ MountAlgo » Komunitas Trading Profesional Indonesia(tekan Dismiss Message Untuk menghapus Pesan")
    embed.set_thumbnail(url=channel.guild.me.display_avatar.url)
    await channel.send(embed=embed, view=VerifView())

# --- Verifikasi Sukses ---
async def send_verifikasi_sukses_embed(user, channel):
    """Mengirim embed notifikasi verifikasi berhasil"""
    wib_now = to_wib(get_utc_now())
    
    embed = discord.Embed(
        title="⦿ VERIFIKASI BERHASIL » [✓]",
        description=(
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            f"➮ {user.mention}, Anda telah **terverifikasi** di MountAlgo\n"
            f"⌚ Pada: {format_wib(wib_now)}\n\n"
            "✇ Akses penuh ke channel edukasi, diskusi,\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        color=COLOR_GREEN
    )
    
    embed.set_thumbnail(url=channel.guild.me.display_avatar.url)
    
    embed.add_field(
        name="❑ PANDUAN MEMBAR BARU » [➤]",
        value=(
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "◈ Baca peraturan & disclaimer server\n"
            "◈ Aktif berdiskusi, jangan ragu bertanya\n"
            "◈ Jaga etika & privasi\n"
            "◈ Upgrade ke **Wizard Member** untuk fitur premium!\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        inline=False
    )
    
    embed.set_footer(text="∎ MountAlgo » Komunitas Trading Profesional Indonesia")
    
    await channel.send(embed=embed)
# --- Langganan premium ---
async def send_premium_sukses_embed(user, channel, expired_date):
    """Mengirim embed notifikasi langganan premium berhasil"""
    expired_wib = to_wib(expired_date)
    
    embed = discord.Embed(
        title="⦿ Wizard Member ACTIVATED ⦿",
        description=(
            f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            f"✇ Terima kasih {user.mention} telah berlangganan **Wizard Member MountAlgo**!\n\n"
            "➮ Akses premium telah aktif. Nikmati fitur eksklusif:\n"
            "‣ **Wizard Toolkits**: Kalkulator & analisis risiko trading presisi harian.\n"
            "‣ **Wizard Analisis**: Analisis teknikal/fundamental mendalam untuk Crypto, Forex & Emas.\n"
            "‣ **Wizard Strategi**: Strategi trading siap pakai yang dipacking profesional.\n"
            "‣ **Relaxation Space**: Ruang santai bermain game di `#relaxation-games`.\n"
            "‣ **Music & Videos**: Berbagi & nikmati musik santai di `#music-videos`.\n\n"
            f"▹ Langganan aktif hingga: **{format_wib(expired_wib)}**\n"
            f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        color=COLOR_VIOLET  # Positive color
    )
    
    embed.set_thumbnail(url=channel.guild.me.display_avatar.url)
    
    embed.add_field(
        name="⬈ KEUNTUNGAN Wizard Member",
        value=(
            "▹ Sinyal premium harian dengan tingkat akurasi tinggi\n"
            "▹ Akses penuh alat bantu trading canggih multi-sumber\n"
            "▹ Ruang diskusi premium bebas spam & interaktif\n"
            "▹ Prioritas konsultasi personal langsung dengan Admin\n"
            "▹ Ruang santai pengusir stres setelah trading"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⬊ PENTING UNTUK DIPERHATIKAN",
        value=(
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "⚠ Jangan bagikan akses atau konten premium ke luar server.\n"
            "⚠ Hormati privasi & hak cipta komunitas.\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        inline=False
    )
    
    embed.set_footer(
        text="▰ MountAlgo Wizard Member SYSTEM ▰",
        icon_url=channel.guild.me.display_avatar.url
    )
    
    await channel.send(embed=embed)

async def send_hubungi_admin_embed(guild: discord.Guild, interaction: discord.Interaction):
    admin_role = discord.utils.get(guild.roles, name="Admin")

    # === Embed untuk USER ===
    user_embed = discord.Embed(
        title="✉ SUPPORT REQUEST RECEIVED",
        description=(
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            f"➩ Terima kasih telah menghubungi tim Admin {admin_role.mention}, {interaction.user.mention}.\n\n"
            "✔ Permintaan bantuanmu sudah diteruskan ke tim admin.\n"
            "✔ Admin akan segera menghubungimu melalui DM.\n\n"
            "⚠ Mohon tunggu beberapa saat dan pastikan DM kamu terbuka untuk admin.\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        color=COLOR_VIOLET
    )

    user_embed.add_field(
        name="⬈ PRIVACY & SECURITY NOTICE",
        value=(
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "✘ Jangan pernah membagikan:\n"
            "‣ Password akun\n"
            "‣ Data pribadi\n"
            "‣ Informasi sensitif\n\n"
            "✔ Admin tidak akan meminta informasi tersebut.\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        inline=False
    )

    user_embed.set_footer(
        text="▰ MountAlgo SUPPORT SYSTEM ▰ (tekan Dismiss Message untuk menutup pesan ini)"
    )

    # Kirim pesan konfirmasi ke user
    await interaction.response.send_message(embed=user_embed, ephemeral=True)

    # === DM ke Admin ===
    if not admin_role:
        return  # Tidak ada role admin

    report_embed = discord.Embed(
        title="🚨 PERMINTAAN BANTUAN DARI USER",
        description=(
            f"**👤 User:** {interaction.user.mention} (`{interaction.user.id}`)\n"
            f"**🌐 Server:** {guild.name}\n"
            f"**🕒 Waktu:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
            "Pesan ini dikirim otomatis oleh sistem MountAlgo Support."
        ),
        color=0xff0000
    )

    report_embed.set_footer(text="▰ MountAlgo SUPPORT NOTIFICATION ▰")

    # Coba kirim DM ke semua admin
    admin_members = [m for m in guild.members if admin_role in m.roles]

    for admin in admin_members:
        try:
            await admin.send(embed=report_embed)
        except Exception as e:
            print(f"Gagal mengirim DM ke admin {admin}: {e}")
            
            
async def send_laporan_admin_embed(guild: discord.Guild, user: discord.Member, alasan: str = None):
    admin_role = discord.utils.get(guild.roles, name="Admin")
    laporan_channel = discord.utils.get(guild.text_channels, name="laporan")
    if not laporan_channel or not admin_role:
        return

    embed = discord.Embed(
        title="⚠ ADMIN SUPPORT REQUEST ⚠",
        description=(
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            f"▸ **User:** {user.mention}\n"
            f"▸ **ID:** `{user.id}`\n"
            f"▸ **Waktu:** <t:{int(datetime.utcnow().timestamp())}:R>\n"
            f"▸ **Status:** {'Online' if user.status == discord.Status.online else 'Offline'}\n\n"
            f"**Alasan Permintaan:**\n"
            f"```\n{alasan or 'Tidak ada keterangan'}\n```\n"
            f"{admin_role.mention}, mohon segera tindak lanjuti.\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        color=0xFF0000  # Urgent red color
    )
    
    # Add user details
    embed.add_field(
        name="⬈ USER DETAILS",
        value=(
            f"▹ Akun dibuat: <t:{int(user.created_at.timestamp())}:R>\n"
            f"▹ Bergabung server: <t:{int(user.joined_at.timestamp())}:R>\n"
            f"▹ Roles: {len(user.roles)-1}"
        ),
        inline=True
    )
    
    embed.add_field(
        name="⬊ ACTION REQUIRED",
        value=(
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "① Berikan respon dalam 15 menit\n"
            "② Hubungi via DM jika diperlukan\n"
            "③ Update status ticket setelah selesai\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        inline=True
    )
    
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.set_author(name=f"Report from: {user.display_name}", icon_url=user.display_avatar.url)
    embed.set_footer(
        text="▰ MountAlgo ADMIN NOTIFICATION SYSTEM ▰"
    )
    
    await laporan_channel.send(content=admin_role.mention, embed=embed)

def send_faq_embed():
    embed = discord.Embed(
        title="⦿ MountAlgo FREQUENTLY ASKED QUESTIONS",
        description=(
            "▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "Kumpulan pertanyaan dan jawaban paling sering ditanyakan di komunitas MountAlgo.\n"
            "**Baca baik-baik sebelum bertanya ke admin!**\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        color=COLOR_VIOLET
    )
    
    # Section 1: Basic Information
    embed.add_field(
        name="▸ 01. APA ITU MountAlgo?",
        value="➤ MountAlgo adalah komunitas trading online untuk:\n‣ Edukasi trading profesional\n‣ Diskusi pasar finansial\n‣ Berbagi sinyal trading (forex/crypto/Komoditas)\n➤ Semua level trader dipersilakan bergabung\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰",
        inline=False
    )
    
    # Section 2: Important Disclaimers
    embed.add_field(
        name="▸ 02. INVESTASI & PENGELOLAAN DANA",
        value=
              "✘ MountAlgo **BUKAN** perusahaan investasi\n"
              "✘ **TIDAK** menerima dana anggota\n"
              "✘ **TIDAK** menawarkan jasa pengelolaan dana\n"
              "✔ Semua konten hanya untuk tujuan edukasi\n"
              "▰▰▰▰▰▰▰▰▰▰▰▰▰▰",
        inline=False
    )
    
    # Section 3: Membership Process
    embed.add_field(
        name="▸ 03. PROSES BERGABUNG",
        value=(
            "① Baca peraturan di #peraturan\n"
            "② Lakukan verifikasi di #verifikasi\n"
            "③ Perkenalkan diri di #lounge-chat\n"
            "④ Akses channel edukasi dasar\n"
            "⑤ Untuk fitur premium → langganan WizardMember\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        inline=False
    )
    
    # Section 4: Free Membership Features (Member Biasa)
    embed.add_field(
        name="▸ 04. FITUR MEMBER BIASA (FREE TIER)",
        value=(
            "```diff\n"
            "+ 📢 #pengumuman: Akses informasi, berita, dan pengumuman resmi server.\n"
            "+ 📰 #all-news: Berita finansial global & update pasar real-time.\n"
            "+ 💬 #lounge-chat: Ruang diskusi umum & obrolan santai antar member.\n"
            "+ 🗺️ #roadmap_trader: Alur perjalanan terstruktur karir seorang trader.\n"
            "+ 📚 #akademi: Gudang materi edukasi & dasar-dasar trading multi-level.\n"
            "+ ⚙️ #free-indikator: Akses gratis indikator buatan tim MountAlgo.\n"
            "+ 📈 #share-your-profits: Ruang berbagi profit trading & jurnal Anda.\n"
            "+ 🔊 #member-voice & #member-stage: Ruang obrolan suara & panggung event.\n"
            "```\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        inline=False
    )
    
    # Section 5: Premium Membership Features (Wizard Member)
    embed.add_field(
        name="▸ 05. FITUR WIZARD MEMBER (PREMIUM TIER)",
        value=(
            "```diff\n"
            "+ 💎 #wizard-lounge-chat: Diskusi eksklusif & konsultasi premium bebas spam.\n"
            "+ 🛠️ #wizard-toolkits: Alat bantu canggih & Kalkulator Risiko Trading presisi.\n"
            "+ 📐 #wizard-strategy: Strategi trading premium yang dipacking siap pakai (SMC, dll).\n"
            "+ 🪙 #wizard-crypto: Analisis harian premium mendalam untuk aset Crypto.\n"
            "+ 💱 #wizard-forex: Analisis harian premium mendalam untuk pasangan Forex.\n"
            "+ 🔱 #wizard-gold: Analisis harian premium mendalam untuk Emas & Komoditas.\n"
            "+ 🎮 #relaxation-games: Kanal khusus berbagi & bermain game santai favorit Anda.\n"
            "+ 🎵 #music-videos: Kanal khusus untuk berbagi playlist, musik, & video santai.\n"
            "+ 🔊 #wizard-voice & #wizard-stage: Live analisis, webinar privat & voice eksklusif.\n"
            "```\n"
            "➤ **Cara Berlangganan:**\n"
            "① Klik tombol **Langganan Premium** di `#verifikasi`\n"
            "② Pilih paket langganan Anda (Bulanan / Tahunan)\n"
            "③ Bayar via DANA, USDC (Crypto - Base/Solana), atau Bank/Kartu Transfer\n"
            "④ Kirim bukti transfer di `#bantuan` ke Admin untuk aktivasi kilat!\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        inline=False
    )
    embed.add_field(
        name="▸ 06. PERATURAN & SANKSI",
        value=(
            "Sistem peringatan bertahap:\n"
            "① Warning → ② Mute → ③ Kick → ④ Ban\n\n"
            "Pelanggaran dicatat di #laporan\n"
            "Semua keputusan admin bersifat final\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        inline=False
    )
    
    # Section 8: Support
    embed.add_field(
        name="▸ 07. BANTUAN ADMIN",
        value=(
            "➤ Cara menghubungi admin:\n"
            "① Gunakan tombol di Hubungi Admin #bantuan\n"
            "⏱ Waktu respon: 1-24 jam\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        inline=False
    )
    
    # Section 9: Privacy & Security
    embed.add_field(
        name="▸ 08. KEAMANAN DATA",
        value=(
            "✔ Data anggota dilindungi\n"
            "✘ Jangan bagikan credential apapun\n"
            "✘ Admin tidak akan meminta password\n"
            "✘ Waspada terhadap phishing/scam\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        inline=False
    )
    
    embed.set_footer(
        text="▰ MountAlgo KNOWLEDGE BASE ▰ |  (tekan Dismiss Message Untuk menghapus Pesan",
        icon_url="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
    )
    
    return embed

async def send_bantuan_embed(channel: discord.TextChannel):
    embed = discord.Embed(
        title="⦿ MountAlgo SUPPORT CENTER",
        description=(
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "Selamat datang di pusat bantuan MountAlgo!\n"
            "Gunakan menu interaktif di bawah untuk:\n"
            "‣ Akses informasi cepat\n"
            "‣ Panduan verifikasi\n"
            "‣ Bantuan admin langsung\n\n"
            "**Pertanyaan kompleks?** Hubungi admin via tombol khusus.\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        color=COLOR_VIOLET
    )
    
    embed.add_field(
        name="⬈ FAQ & KNOWLEDGE BASE",
        value=(
            "▸ Kumpulan pertanyaan umum\n"
            "▸ Panduan penggunaan server\n"
            "▸ Informasi fitur premium\n"
            "▸ Kebijakan & peraturan\n\n"
            "➤ Tekan tombol **FAQ** untuk membuka"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⬈ VERIFICATION GUIDE",
        value=(
            "▸ Proses verifikasi anggota\n"
            "▸ Panduan langganan premium\n"
            "▸ Metode pembayaran\n"
            "▸ Troubleshooting\n\n"
            "➤ Tekan tombol **Verifikasi** untuk panduannya juga" 
        ),
        inline=False
    )
    
    embed.add_field(
        name="⬈ ADMIN SUPPORT",
        value=(
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "Untuk bantuan langsung:\n"
            "① Tekan tombol **Hubungi Admin**\n"
            "② Jelaskan masalah secara detail\n"
            "③ Tunggu respon (biasanya <24 jam)\n\n"
            "⚠ **Penting:** Pastikan DM terbuka\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        inline=False
    )
    
    embed.set_footer(
        text="▰ MountAlgo SUPPORT SYSTEM ▰ | Respon dalam 1x24 jam"
    )
    embed.set_thumbnail(url=channel.guild.me.display_avatar.url)
    await channel.send(embed=embed, view=BantuanView())  

# ---send Pengumuman ---
async def send_reset_pengumuman_embed(channel: discord.TextChannel, admin: discord.Member = None):
    wib_now = to_wib(get_utc_now())
    
    embed = discord.Embed(
        title="📢 》》 Pengumuman Telah Direset",
        description=(
            "Seluruh pesan pengumuman sebelumnya telah **dihapus/reset** untuk menjaga kerapihan dan relevansi informasi.\n\n"
            "Pengumuman baru akan segera diinformasikan pada channel ini.\n"
            "Pastikan kamu selalu cek #pengumuman untuk update terbaru terkait event, sinyal, edukasi, dan info penting komunitas MountAlgo."
        ),
        color=0x00b894,
        timestamp=wib_now
    )
    
    embed.set_thumbnail(url="https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif")
    
    embed.add_field(
        name="⏰ 》》 Kapan Pengumuman Baru?",
        value="Pengumuman baru akan diposting secara berkala oleh tim admin. Aktifkan notifikasi channel ini agar tidak ketinggalan info penting!",
        inline=False
    )
    
    embed.add_field(
        name="🔔 》》 Tips",
        value="● Jangan lewatkan info event dan update server\n● Jika ada pertanyaan, gunakan channel #bantuan",
        inline=False
    )
    
    if admin:
        embed.set_footer(text=f"Reset oleh: {admin.display_name} | MountAlgo Announcement System")
    else:
        embed.set_footer(text="MountAlgo Announcement System")
    await channel.send(embed=embed)
    
# --- Obrolan ---
async def send_obrolan_embed(channel: discord.TextChannel):
    embed = discord.Embed(
        title="⦿ WELCOME TO MountAlgo DISCUSSION HUB",
        description=(
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "**Channel diskusi utama komunitas trading profesional**\n\n"
            "➤ Cocok untuk:\n"
            "‣ Perkenalan anggota baru\n"
            "‣ Diskusi trading & analisis pasar\n"
            "‣ Berbagi insight finansial\n"
            "‣ Tanya jawab seputar trading\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        color=COLOR_VIOLET
    )
    
    embed.add_field(
        name="⬈ COMMUNITY GUIDELINES",
        value=(
            "① Saling menghormati & menjaga sopan santun\n"
            "② Hindari spam/off-topic berlebihan\n"
            "③ Gunakan channel yang sesuai untuk topik khusus\n"
            "④ Diskusi harus relevan dengan finansial/trading\n"
            "⑤ Dilarang promosi tanpa izin admin"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⬈ GETTING STARTED",
        value=(
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "➤ Anggota baru:\n"
            "‣ Tekan tombol **Perkenalan** di bawah\n"
            "‣ Ceritakan pengalaman trading Anda\n"
            "‣ Tanyakan apa yang ingin diketahui\n\n"
            "➤ Anggota lama:\n"
            "‣ Bantu jawab pertanyaan baru\n"
            "‣ Berbagi analisis terbaru\n"
            "‣ Diskusikan peluang pasar\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        inline=False
    )
    
    # UPDATED: Added note about new discussion threads
    embed.add_field(
        name="💬 FITUR DISKUSI BARU",
        value=(
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "Kini Anda dapat membuat ruang diskusi khusus:\n"
            "‣ Klik **Mulai Diskusi Baru** di bawah\n"
            "‣ Masukkan topik dan deskripsi\n"
            "‣ Atur thread sesuai kebutuhan\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        inline=False
    )
    
    embed.set_footer(
        text="▰ MountAlgo COMMUNITY CHAT ▰ | Keep discussions professional and constructive",
        icon_url="https://cdn-icons-png.flaticon.com/512/219/219983.png"
    )
    embed.set_thumbnail(url=channel.guild.me.display_avatar.url)
    
    # UPDATED: Added new button to ObrolanView
    await channel.send(embed=embed, view=ObrolanView())

async def send_wizard_lounge_embed(channel: discord.TextChannel):
    embed = discord.Embed(
        title="⦿ WELCOME TO WIZARD LOUNGE CHAT 🚀",
        description=(
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "**Kanal diskusi khusus untuk anggota premium Wizard Member MountAlgo.**\n\n"
            "➤ Fitur eksklusif:\n"
            "‣ Diskusi strategi trading mendalam\n"
            "‣ Kolaborasi analisis teknikal & fundamental\n"
            "‣ Berbagi pandangan pasar real-time\n"
            "‣ Ruang diskusi bebas dengan sesama trader premium\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        color=COLOR_VIOLET
    )
    embed.add_field(
        name="💬 MULAI DISKUSI KHUSUS WIZARD",
        value=(
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "Gunakan tombol di bawah untuk membuat ruang diskusi/analisis baru:\n"
            "‣ Klik **Mulai Diskusi Baru** di bawah\n"
            "‣ Tulis topik strategi atau pair yang ingin dibahas\n"
            "‣ Diskusikan bersama rekan Wizard lainnya\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        inline=False
    )
    embed.set_footer(
        text="▰ MountAlgo WIZARD CHAT ▰ | Keep premium insights constructive",
        icon_url="https://cdn-icons-png.flaticon.com/512/219/219983.png"
    )
    embed.set_thumbnail(url=channel.guild.me.display_avatar.url)
    await channel.send(embed=embed, view=WizardLoungeView())

async def send_wizard_toolkits_embed(channel: discord.TextChannel):
    """Mengirim embed alat trading dengan tombol kalkulator"""
    embed = discord.Embed(
        title="✇ ALAT TRADING MountAlgo",
        description=(
            "☛ Pusat Alat Trading Canggih untuk Strategi Anda\n"
            "Manfaatkan alat berikut untuk meningkatkan akurasi perdagangan:\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "● ❑ **Kalkulator Trading** - Hitung margin, risiko/profit, dan analisis posisi\n"
            "● ❑ **Penganalisis Risiko/Imbalan** - Tentukan rasio risiko optimal\n"
            "● ❑ **Penentu Ukuran Posisi** - Atur ukuran posisi dengan presisi\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "```yaml\n"
            "Alat ini mendukung semua instrumen:\n"
            "➩ Forex: EURUSD, GBPJPY, dll.\n"
            "➩ Kripto: BTC/USD, ETH/USDT, XRP\n"
            "➩ Komoditas: Emas, XAUUSD, Perak\n"
            "➩ Derivatif: Indeks, Minyak, Gas Alam\n"
            "```"
        ),
        color=COLOR_VIOLET  # Biru positif
    )
    embed.set_thumbnail(url=channel.guild.me.display_avatar.url)
    await channel.send(embed=embed, view=WizardToolkitsView())

async def send_panduan_calculator_embed():
    embed = discord.Embed(
        title="✔ PANDUAN KALKULATOR TRADING MountAlgo",
        description=(
            "☛ Selamat Datang di Kalkulator Trading MountAlgo v6.6.0\n"
            "Kalkulator ini dirancang untuk memberikan **Analisis Lebih Mendalam** untuk hasil trading Lebih maksimal. Berikut panduan lengkap:\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        color=COLOR_VIOLET  # Biru positif
    )

    embed.add_field(
        name="❑ FUNGSI UTAMA KALKULATOR",
        value=(
            "```yaml\n"
            "● Ukuran Posisi: Menghitung volume optimal berdasarkan modal dan risiko.\n"
            "● Stop Loss (SL) & Take Profit (TP): Analisis risiko dan profit potensial.\n"
            "● Margin & Fee: Estimasi margin dan dampak fee broker.\n"
            "● Analisis Mendalam:\n"
            "  - Probabilitas keberhasilan dan expected return.\n"
            "  - Value at Risk (VaR) untuk estimasi kerugian maksimal.\n"
            "  - Optimalisasi posisi dengan Modified Kelly Criterion.\n"
            "  - Skenario hasil (best, base, worst case).\n"
            "  - Strategi mitigasi risiko (trailing stop, hedging).\n"
            "  - Konteks waktu trading dan indikator pendukung.\n"
            "  - Psikologi trading dan checklist pra-trading.\n"
            "```"
        ),
        inline=False
    )

    embed.add_field(
        name="❑ INPUT YANG DIPERLUKAN",
        value=(
            "```yaml\n"
            "1. Pasangan Perdagangan\n"
            "   Contoh: `BTCUSD`, `EURUSD`, `XAUUSD`.\n"
            "   Menentukan aset (crypto, forex, komoditas).\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "2. Posisi/Harga Entry\n"
            "   Format: `BUY/62000` atau `SELL/1.0850`.\n"
            "   Tentukan arah (BUY/SELL) dan harga masuk.\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "3. Modal Akun\n"
            "   Masukkan modal dalam USD, contoh: `10000`.\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "4. Parameter Risiko\n"
            "   Format: `Volume/Leverage/SL/TP`.\n"
            "   Contoh: `500/50/60000/64000` (crypto) atau `0.1/500/1.0800/1.1000` (forex).\n"
            "   Volume: USD untuk crypto, lot untuk forex/komoditas.\n"
            "```"
        ),
        inline=False
    )

    embed.add_field(
        name="⬈ OUTPUT YANG DIHASILKAN",
        value=(
            "```yaml\n"
            "1. Profil Akun\n"
            "   Total modal, margin digunakan, dan total fee.\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "2. Posisi Trading\n"
            "   Detail pair, arah, volume, leverage, dan risiko per pip.\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "3. Analisis Risiko Utama\n"
            "   Peringatan risiko (terkendali, tinggi, kritis) dan leverage.\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "4. Manajemen Risiko\n"
            "   SL/TP, kerugian/profit potensial, dan rasio risk/reward.\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "5. Analisis Mendalam\n"
            "   - Ringkasan Eksekutif: Risiko, probabilitas, Pilihan utama.\n"
            "   - Skenario Hasil: Best, base, worst case.\n"
            "   - Optimalisasi Posisi: Volume dan leverage ideal.\n"
            "   - Mitigasi Risiko: Strategi pengamanan posisi.\n"
            "   - Konteks Waktu: Sesi trading dan indikator.\n"
            "   - Psikologi & Checklist: Disiplin dan persiapan.\n"
            "   - Dampak Fee: Analisis biaya broker.\n"
            "```"
        ),
        inline=False
    )

    embed.add_field(
        name="✚ VISUALISASI HASIL ANALISIS",
        value=(
            "```yaml\n"
            "1. Grafik Batang\n"
            "   Visualisasi margin, leverage, dan risiko (% modal).\n"
            "   Format: [▰▰▱▱▱] (persentase).\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "2. Peringatan Warna\n"
            "   ● Hijau: Risiko rendah (<30% modal).\n"
            "   ● Kuning: Risiko tinggi (30-50% modal).\n"
            "   ● Merah: Risiko kritis (>50% modal).\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "3. Format Embed\n"
            "   Pemisah tematik (`yaml`, `prolog`, `diff`, `python`) untuk kejelasan.\n"
            "   Emoji (🪙, 🌐, 🔥) untuk jenis aset.\n"
            "```"
        ),
        inline=False
    )

    timestamp = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    embed.set_footer(
        text=f"Komunitas Trading MountAlgo v6.6.0 © • Edukasi dan Profit Bersama • {timestamp}"
    )
    return embed

async def send_risk_template_embed():
    embed = discord.Embed(
        title="✔ TEMPLAT RISIKO PERDAGANGAN BERDASARKAN ASET",
        description=(
            "Contoh Template risiko untuk crypto, forex, dan komoditas dengan Contoh modal akun $100. "
            "Dirancang untuk mendukung **Analisis Mendalam**, "
            "dengan mempertimbangkan fee broker, volatilitas, dan optimalisasi posisi:\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        ),
        color=COLOR_VIOLET  # Biru positif
    )

    # Risiko Rendah
    embed.add_field(
        name="❑ RISIKO RENDAH",
        value=(
            "```yaml\n"
            "Modal Akun: $100\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "🪙 Kripto (contoh: BTCUSD):\n"
            "  ➩ Ukuran Posisi: $10 (10% modal)\n"
            "  ➩ Leverage: 1:10\n"
            "  ➩ Stop Loss: 10 pips\n"
            "  ➩ Take Profit: 20 pips\n"
            "  ➩ Fee (0.1%): $0.02\n"
            "  ➩ Potensi Rugi: $1.02 (1.02% modal)\n"
            "  ➩ Potensi Untung: $1.98 (1.98% modal)\n"
            "  ➩ RR: 1:2 | Probabilitas: 60%\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "🌐 Forex (contoh: EURUSD):\n"
            "  ➩ Ukuran Posisi: 0.01 lot\n"
            "  ➩ Leverage: 1:500\n"
            "  ➩ Stop Loss: 20 pips\n"
            "  ➩ Take Profit: 40 pips\n"
            "  ➩ Fee (2 pip + $0.14): $0.34\n"
            "  ➩ Potensi Rugi: $2.34 (2.34% modal)\n"
            "  ➩ Potensi Untung: $3.66 (3.66% modal)\n"
            "  ➩ RR: 1:2 | Probabilitas: 65%\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "🔥 Emas (XAUUSD):\n"
            "  ➩ Ukuran Posisi: 0.01 lot\n"
            "  ➩ Leverage: 1:500\n"
            "  ➩ Stop Loss: 50 pips\n"
            "  ➩ Take Profit: 100 pips\n"
            "  ➩ Fee (0.5 pip + $0.2): $0.25\n"
            "  ➩ Potensi Rugi: $0.75 (0.75% modal)\n"
            "  ➩ Potensi Untung: $1.75 (1.75% modal)\n"
            "  ➩ RR: 1:2 | Probabilitas: 62%\n"
            "```"
        ),
        inline=False
    )

    # Risiko Standar
    embed.add_field(
        name="❑ RISIKO STANDAR",
        value=(
            "```yaml\n"
            "Modal Akun: $100\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "🪙 Kripto (contoh: BTCUSD):\n"
            "  ➩ Ukuran Posisi: $30 (30% modal)\n"
            "  ➩ Leverage: 1:20\n"
            "  ➩ Stop Loss: 30 pips\n"
            "  ➩ Take Profit: 60 pips\n"
            "  ➩ Fee (0.1%): $0.06\n"
            "  ➩ Potensi Rugi: $3.06 (3.06% modal)\n"
            "  ➩ Potensi Untung: $5.94 (5.94% modal)\n"
            "  ➩ RR: 1:2 | Probabilitas: 55%\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "🌐 Forex (contoh: EURUSD):\n"
            "  ➩ Ukuran Posisi: 0.05 lot\n"
            "  ➩ Leverage: 1:500\n"
            "  ➩ Stop Loss: 40 pips\n"
            "  ➩ Take Profit: 80 pips\n"
            "  ➩ Fee (2 pip + $0.7): $1.70\n"
            "  ➩ Potensi Rugi: $5.70 (5.70% modal)\n"
            "  ➩ Potensi Untung: $7.30 (7.30% modal)\n"
            "  ➩ RR: 1:2 | Probabilitas: 60%\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "🔥 Emas (XAUUSD):\n"
            "  ➩ Ukuran Posisi: 0.05 lot\n"
            "  ➩ Leverage: 1:500\n"
            "  ➩ Stop Loss: 100 pips\n"
            "  ➩ Take Profit: 200 pips\n"
            "  ➩ Fee (0.5 pip + $1): $1.25\n"
            "  ➩ Potensi Rugi: $2.25 (2.25% modal)\n"
            "  ➩ Potensi Untung: $3.75 (3.75% modal)\n"
            "  ➩ RR: 1:2 | Probabilitas: 58%\n"
            "```"
        ),
        inline=False
    )

    # Risiko Tinggi
    embed.add_field(
        name="❑ RISIKO TINGGI",
        value=(
            "```yaml\n"
            "Modal Akun: $100\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "🪙 Kripto (contoh: BTCUSD):\n"
            "  ➩ Ukuran Posisi: $50 (50% modal)\n"
            "  ➩ Leverage: 1:50\n"
            "  ➩ Stop Loss: 50 pips\n"
            "  ➩ Take Profit: 100 pips\n"
            "  ➩ Fee (0.1%): $0.10\n"
            "  ➩ Potensi Rugi: $5.10 (5.10% modal)\n"
            "  ➩ Potensi Untung: $9.90 (9.90% modal)\n"
            "  ➩ RR: 1:2 | Probabilitas: 50%\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "🌐 Forex (contoh: EURUSD):\n"
            "  ➩ Ukuran Posisi: 0.1 lot\n"
            "  ➩ Leverage: 1:500\n"
            "  ➩ Stop Loss: 50 pips\n"
            "  ➩ Take Profit: 100 pips\n"
            "  ➩ Fee (2 pip + $1.4): $3.40\n"
            "  ➩ Potensi Rugi: $8.40 (8.40% modal)\n"
            "  ➩ Potensi Untung: $11.60 (11.60% modal)\n"
            "  ➩ RR: 1:2 | Probabilitas: 55%\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "🔥 Emas (XAUUSD):\n"
            "  ➩ Ukuran Posisi: 0.1 lot\n"
            "  ➩ Leverage: 1:500\n"
            "  ➩ Stop Loss: 150 pips\n"
            "  ➩ Take Profit: 300 pips\n"
            "  ➩ Fee (0.5 pip + $2): $2.50\n"
            "  ➩ Potensi Rugi: $4.50 (4.50% modal)\n"
            "  ➩ Potensi Untung: $7.50 (7.50% modal)\n"
            "  ➩ RR: 1:2 | Probabilitas: 52%\n"
            "```"
        ),
        inline=False
    )

    # Catatan Tambahan
    embed.add_field(
        name="❑ CATATAN PENTING",
        value=(
            "```yaml\n"
            "● Fee Broker: Termasuk dalam potensi rugi/untung.\n"
            "  - Crypto: 0.1% per sisi.\n"
            "  - Forex: 2 pip + $7/lot/sisi.\n"
            "  - Emas: 0.5 pip + $10/lot/sisi.\n"
            "● Leverage: Min 500x (forex/komoditas), maks 400x (crypto).\n"
            "● Mitigasi Risiko:\n"
            "  - Gunakan trailing stop setelah 50% jarak TP.\n"
            "  - Diversifikasi: Maks 30% modal per aset.\n"
            "  - Jurnal trading untuk disiplin.\n"
            "● Optimalisasi: Gunakan Modified Kelly Criterion untuk volume ideal.\n"
            "● Volatilitas:\n"
            "  - Crypto: Tinggi (5%).\n"
            "  - Forex: Rendah (1%).\n"
            "  - Emas: Sedang (2%).\n"
            "```"
        ),
        inline=False
    )

    timestamp = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    embed.set_footer(
        text=f"Komunitas Trading MountAlgo v6.6.0 © • Edukasi dan Profit Bersama • {timestamp}"
    )
    return embed

# --- Kontrol Pengguna ---
async def send_kontrol_pengguna_embed(channel: discord.TextChannel):
    embed = discord.Embed(
        title="✔ PANEL KONTROL PENGGUNA",
        description=(
            "☛ Kelola Anggota Server dengan Mudah\n"
            "Gunakan tombol di bawah untuk mengelola pengguna server:\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "● ❑ **Tambah Pengguna**: Daftarkan pengguna baru secara manual\n"
            "● ❑ **Hapus Pengguna**: Hapus pengguna dari basis data\n"
            "● ❑ **Tingkatkan Pengguna**: Jadikan pengguna WizardMember\n"
            "● ❑ **Sinkronkan User**: Sinkronkan database dengan role Discord\n"
            "● ❑ **Lihat Status**: Periksa daftar pengguna dan statusnya\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "➮ Hanya admin yang dapat mengakses panel ini"
        ),
        color=COLOR_VIOLET  # Biru positif
    )
    embed.set_footer(
        text="Komunitas Trading MountAlgo ● Panel Kontrol Pengguna",
        icon_url=channel.guild.me.display_avatar.url
    )
    embed.set_thumbnail(url=channel.guild.me.display_avatar.url)
    await channel.send(embed=embed, view=KontrolPenggunaView())

async def send_kontrol_admin_embed(channel: discord.TextChannel):
    embed = discord.Embed(
        title="✇ PANEL KONTROL ADMIN MountAlgo",
        description=(
            "☛ Pusat Kendali Utama Server MountAlgo\n"
            "Kelola semua aspek server dengan tombol di bawah:\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            "➩ Setiap tindakan dicatat otomatis di #laporan"
        ),
        color=COLOR_VIOLET  # Biru positif
    )
    embed.add_field(
        name="❑ MANAJEMEN KONTEN",
        value=(
            "```yaml\n"
            "● Atur ulang kanal peraturan, disclaimer, pengumuman\n"
            "● Perbarui konten penting server\n"
            "```"
        ),
        inline=False
    )
    embed.add_field(
        name="❑ MANAJEMEN SINYAL",
        value=(
            "```yaml\n"
            "● Buat sinyal perdagangan baru\n"
            "● Kelola atau tutup sinyal aktif\n"
            "● Pantau dasbor sinyal\n"
            "● Akses arsip semua sinyal\n"
            "```"
        ),
        inline=False
    )
    embed.add_field(
        name="❑ MANAJEMEN DATA",
        value=(
            "```yaml\n"
            "● Hapus sinyal tertentu (berdasarkan ID)\n"
            "● Atur ulang seluruh basis data\n"
            "● Ekspor data sinyal (format CSV)\n"
            "```"
        ),
        inline=False
    )
    embed.add_field(
        name="❑ MANAJEMEN AKSES",
        value=(
            "```yaml\n"
            "● Promosikan atau turunkan admin\n"
            "● Atur izin pengguna\n"
            "● Atur ulang setup server lengkap\n"
            "```"
        ),
        inline=False
    )
    embed.add_field(
        name="❑ MANAJEMEN PEMBAYARAN & DONASI",
        value=(
            "```yaml\n"
            "● Aktif/nonaktifkan tombol DANA\n"
            "● Aktif/nonaktifkan tombol Crypto (USDC)\n"
            "● Aktif/nonaktifkan tombol Bank/Kartu\n"
            "● Aktif/nonaktifkan tombol Donasi\n"
            "```"
        ),
        inline=False
    )
    embed.add_field(
        name="⬈ PERHATIAN",
        value=(
            "```yaml\n"
            "● Tindakan bersifat permanen dan tidak dapat dibatalkan\n"
            "● Periksa ulang sebelum melakukan operasi kritis\n"
            "● Aktivitas admin terekam lengkap di #laporan\n"
            "```"
        ),
        inline=False
    )
    wib_now = to_wib(get_utc_now())
    embed.set_footer(
        text=f"Komunitas Trading MountAlgo ● {format_wib(wib_now)}"
    )
    embed.set_thumbnail(url=channel.guild.me.display_avatar.url)
    await channel.send(embed=embed, view=KontrolAdminView())

async def send_laporan_embed(
    bot: commands.Bot,
    judul: str,
    deskripsi: str,
    fields: list = None,
    warna: int = COLOR_GREEN,  # Hijau negatif
    thumbnail: str = "https://cdn-icons-png.flaticon.com/512/595/595067.png"
):
    wib_now = to_wib(get_utc_now())
    laporan_channel = discord.utils.get(bot.get_all_channels(), name="laporan")
    if not laporan_channel:
        logging.warning("Kanal #laporan tidak ditemukan.")
        return

    embed = discord.Embed(
        title=f"➮ {judul}",
        description=deskripsi,
        color=warna,
        timestamp=wib_now
    )

    if fields:
        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

    embed.set_footer(
        text="Komunitas Trading MountAlgo ● Notifikasi Otomatis"
    )
    await laporan_channel.send(embed=embed)
    
#---send embed wizard-analisis---
async def send_analysis_embed(
    interaction: discord.Interaction,
    thread_name: str,
    title: str,
    description: str,
    file_url: Optional[str] = None,
    diff_code: Optional[str] = None
):
    analysis_channel = discord.utils.get(interaction.guild.text_channels, name='wizard-analisis')
    if not analysis_channel:
        await interaction.followup.send('❌ Channel "wizard-analisis" tidak ditemukan.', ephemeral=True)
        return

    # Cari thread yang sudah ada atau buat baru
    thread = discord.utils.get(analysis_channel.threads, name=thread_name)
    if not thread:
        thread = await analysis_channel.create_thread(
            name=thread_name,
            type=discord.ChannelType.public_thread,
            auto_archive_duration=1440
        )

    # Buat embed untuk analisis
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color(COLOR_CYAN)
    )
    
    # Tambahkan URL file jika ada
    if file_url:
        embed.add_field(
            name="🔗 Link File",
            value=f"[Klik di sini untuk mengunduh]({file_url})",
            inline=False
        )

    # Tambahkan blok kode jika tersedia
    if diff_code:
        embed.add_field(
            name="📄 Diff / Kode",
            value=f"```{diff_code}```",
            inline=False
        )

    # Kirim embed ke thread
    await thread.send(embed=embed)


# ===================== VIEW =====================
# --- Pilihan Pembayaran ---
class PaymentSelect(discord.ui.Select):
    def __init__(self):
        options = []
        if PAYMENT_DANA_ACTIVE:
            options.append(discord.SelectOption(
                label="📱 Bayar via DANA",
                value="dana",
                description="Tampilkan opsi pembayaran DANA"
            ))
        if PAYMENT_CRYPTO_ACTIVE:
            options.append(discord.SelectOption(
                label="🪙 Bayar via USDC (Crypto)",
                value="crypto",
                description="Tampilkan opsi pembayaran USDC (Crypto)"
            ))
        if PAYMENT_CARD_ACTIVE:
            options.append(discord.SelectOption(
                label="💳 Transfer Bank / Kartu",
                value="card",
                description="Tampilkan opsi pembayaran via Transfer Bank / Kartu"
            ))

        if not options:
            options.append(discord.SelectOption(
                label="❌ Tidak Ada Metode Pembayaran",
                value="none",
                description="Silakan hubungi Admin untuk informasi pembayaran"
            ))

        super().__init__(
            placeholder="💳 Pilih Metode Pembayaran...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="select_pembayaran"
        )

    async def callback(self, interaction: discord.Interaction):
        # Update embed dengan informasi pembayaran
        embed = interaction.message.embeds[0]
        new_embed = embed.copy()

        # Dapatkan nilai terbaru dari environment / API_KEYS
        dana_bulanan = DANA_BULANAN_LINK or "https://link.dana.id/qr/your_monthly_qr_id"
        dana_tahunan = DANA_TAHUNAN_LINK or "https://link.dana.id/qr/your_yearly_qr_id"
        usdc_bulanan = USDC_BULANAN_LINK or "https://link.usdc.id/qr/your_monthly_usdc_id"
        usdc_tahunan = USDC_TAHUNAN_LINK or "https://link.usdc.id/qr/your_yearly_usdc_id"
        card_bulanan = CARD_BULANAN_LINK or "https://link.card.id/your_monthly_card_id"
        card_tahunan = CARD_TAHUNAN_LINK or "https://link.card.id/your_yearly_card_id"

        # Bersihkan field pembayaran sebelumnya jika ada
        for i in range(len(new_embed.fields) - 1, -1, -1):
            if new_embed.fields[i].name in [
                "📱 DETAIL PEMBAYARAN DANA",
                "🪙 DETAIL PEMBAYARAN CRYPTO",
                "💳 DETAIL PEMBAYARAN BANK/KARTU",
                "❌ METODE PEMBAYARAN TIDAK TERSEDIA"
            ]:
                new_embed.remove_field(i)

        # Buat view baru yang melestarikan Select dropdown ini
        view = discord.ui.View(timeout=None)
        view.add_item(PaymentSelect())

        if self.values[0] == "none":
            new_embed.add_field(
                name="❌ METODE PEMBAYARAN TIDAK TERSEDIA",
                value=(
                    f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                    f"Saat ini seluruh metode pembayaran otomatis sedang dinonaktifkan oleh Admin.\n\n"
                    f"Silakan hubungi **Admin** secara langsung untuk detail info pembayaran manual.\n"
                    f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
                ),
                inline=False
            )
        elif self.values[0] == "dana":
            new_embed.add_field(
                name="📱 DETAIL PEMBAYARAN DANA",
                value=(
                    f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                    f"➩ **Paket Wizard Bulanan:**\nSilakan bayar menggunakan tombol **Bayar Wizard Bulanan** di bawah.\n\n"
                    f"➩ **Paket Wizard Tahunan:**\nSilakan bayar menggunakan tombol **Bayar Wizard Tahunan** di bawah.\n\n"
                    f"💡 *Setelah melakukan pembayaran, silakan kirim bukti transfer ke Admin untuk konfirmasi.*\n"
                    f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
                ),
                inline=False
            )
            # Tambahkan tombol Link DANA untuk Bulanan dan Tahunan
            view.add_item(discord.ui.Button(
                label="⬈ Bayar Wizard Bulanan",
                url=dana_bulanan,
                style=discord.ButtonStyle.link
            ))
            view.add_item(discord.ui.Button(
                label="⬈ Bayar Wizard Tahunan",
                url=dana_tahunan,
                style=discord.ButtonStyle.link
            ))
        elif self.values[0] == "crypto":
            new_embed.add_field(
                name="🪙 DETAIL PEMBAYARAN CRYPTO",
                value=(
                    f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                    f"➩ **Pembayaran hanya menggunakan USDC (USDC ONLY).**\n\n"
                    f"🌐 **Jaringan yang Didukung (Supported Networks):**\n"
                    f"• **Base**\n"
                    f"• **Solana**\n\n"
                    f"💡 *Silakan klik tombol di bawah untuk membayar paket bulanan atau tahunan.*\n"
                    f"💡 *Setelah pembayaran berhasil, kirim bukti transfer ke Admin untuk konfirmasi.*\n"
                    f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
                ),
                inline=False
            )
            # Tambahkan tombol Link USDC untuk Bulanan dan Tahunan
            view.add_item(discord.ui.Button(
                label="⬈ Bayar USDC Bulanan",
                url=usdc_bulanan,
                style=discord.ButtonStyle.link
            ))
            view.add_item(discord.ui.Button(
                label="⬈ Bayar USDC Tahunan",
                url=usdc_tahunan,
                style=discord.ButtonStyle.link
            ))
        elif self.values[0] == "card":
            new_embed.add_field(
                name="💳 DETAIL PEMBAYARAN BANK/KARTU",
                value=(
                    f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                    f"➩ **Paket Wizard Bulanan:**\nSilakan bayar menggunakan tombol **Bayar Card Bulanan** di bawah.\n\n"
                    f"➩ **Paket Wizard Tahunan:**\nSilakan bayar menggunakan tombol **Bayar Card Tahunan** di bawah.\n\n"
                    f"💡 *Pembayaran mendukung kartu kredit, kartu debit, dan transfer bank otomatis.*\n"
                    f"💡 *Setelah pembayaran berhasil, kirim bukti transfer ke Admin untuk konfirmasi.*\n"
                    f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
                ),
                inline=False
            )
            # Tambahkan tombol Link Card untuk Bulanan dan Tahunan
            view.add_item(discord.ui.Button(
                label="⬈ Bayar Card Bulanan",
                url=card_bulanan,
                style=discord.ButtonStyle.link
            ))
            view.add_item(discord.ui.Button(
                label="⬈ Bayar Card Tahunan",
                url=card_tahunan,
                style=discord.ButtonStyle.link
            ))

        await interaction.response.edit_message(embed=new_embed, view=view)


# --- Verifikasi ---
class VerifView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        if not DONATION_ACTIVE:
            for child in self.children.copy():
                if child.custom_id == "verif_donation":
                    self.remove_item(child)

    @discord.ui.button(
        label="✔ Setuju & Verifikasi",
        style=discord.ButtonStyle.success,
        custom_id="verif_setuju"
    )
    async def cek_status(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        roles = [r.name for r in user.roles]
        channel = interaction.channel

        # Jika sudah Admin
        if "Admin" in roles:
            embed = discord.Embed(
                title="🛡️ STATUS ADMIN",
                description="Kamu adalah **Admin** di server MountAlgo.\nAkses penuh ke seluruh fitur, kontrol pengguna, dan panel admin.\n\nTerima kasih atas kontribusimu menjaga komunitas!",
                color=0xffc300
            )
            embed.add_field(
                name="Hak Khusus Admin",
                value=(
                    "• Mengelola pengguna & channel\n"
                    "• Membuat/menutup sinyal\n"
                    "• Reset konten penting\n"
                    "• Akses penuh panel kontrol"
                ),
                inline=False
            )
            embed.set_footer(text="MountAlgo Admin System")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Jika sudah WizardMember
        if "WizardMemberBulanan" in roles:
            embed = discord.Embed(
                title="💎 STATUS Wizard Member Bulanan",
                description="Kamu sudah **terverifikasi** dan **berlangganan WizardMember bulanan**.\nAkses premium aktif, nikmati seluruh fitur eksklusif MountAlgo!",
                color=COLOR_VIOLET
            )
            embed.add_field(
                name="Fitur Premium",
                value=(
                    "• Wizard Toolkits: Alat Serbaguna\n"
                    "• Wizard Analisis: Analisis Dari aset crypto forex dan komoditas yang mendalam \n"
                    "• Wizard Setrategi : Strategi khusus yang dipacking sebaik mungkin untuk Strategi perdagangan di pasar crypto forex dan komoditas\n\n"
                    "• Konsultasi prioritas\n"
                    "• event eksklusif"
                ),
                inline=False
            )
            embed.set_footer(text="MountAlgo WizardMember System")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if "WizardMemberTahunan" in roles:
            embed = discord.Embed(
                title="🏆 STATUS Wizard Member Tahunan",
                description="Kamu sudah **terverifikasi** dan **berlangganan WizardMember Tahunan**.\nAkses premium aktif, nikmati seluruh fitur eksklusif MountAlgo!",
                color=COLOR_VIOLET
            )
            embed.add_field(
                name="Fitur Premium",
                value=(
                    "• Wizard Toolkits: Alat Serbaguna\n"
                    "• Wizard Analisis: Analisis Dari aset crypto forex dan komoditas yang mendalam \n"
                    "• Wizard Setrategi : Strategi khusus yang dipacking sebaik mungkin untuk Strategi perdagangan di pasar crypto forex dan komoditas\n\n"
                    "• Konsultasi prioritas\n"
                    "• event eksklusif"
                ),
                inline=False
            )
            embed.set_footer(text="MountAlgo WizardMember System")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        # Jika sudah member
        if "Member" in roles:
            embed = discord.Embed(
                title="✅ STATUS MEMBER TERVERIFIKASI",
                description="Kamu sudah **terverifikasi** sebagai member MountAlgo.\nTidak perlu verifikasi lagi, akses channel publik sudah terbuka.",
                color=COLOR_GREEN
            )
            embed.add_field(
                name="Tips Member",
                value=(
                    "• Aktif diskusi di #lounge-chat\n"
                    "• Baca materi di #akademi\n"
                    "• Upgrade ke WizardMember untuk fitur premium"
                ),
                inline=False
            )
            embed.set_footer(text="MountAlgo Member System")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Jika belum punya role utama (auto verifikasi)
        guild = interaction.guild
        unverified_role = discord.utils.get(guild.roles, name="Unverified")
        member_role = discord.utils.get(guild.roles, name="Member")

        # Hapus Unverified, tambahkan member
        if unverified_role and unverified_role in user.roles:
            await user.remove_roles(unverified_role)
        if member_role and member_role not in user.roles:
            await user.add_roles(member_role)

        # Update database (panggil fungsi dari VerificationSystem)
        try:
            from bot import VerificationSystem  # pastikan import sesuai struktur project kamu
            await VerificationSystem.verify_and_update_database(user)
        except Exception as e:
            print(f"Gagal update database: {e}")

        # Kirim embed sangat menarik
        embed = discord.Embed(
            title="🎉 Selamat! Kamu Sudah Diverifikasi 🎉",
            description=(
                "✨ **Akses Penuh Telah Dibuka!** ✨\n\n"
                "Kamu kini resmi menjadi bagian dari keluarga **MountAlgo**!\n"
                "Jelajahi berbagai fitur, diskusi, dan peluang trading bersama komunitas terbaik. 🚀\n\n"
                "Berikut beberapa langkah awal yang bisa kamu lakukan:"
            ),
            color=discord.Color.from_rgb(41, 128, 185)
        )
        embed.set_thumbnail(url=channel.guild.me.display_avatar.url)
        embed.add_field(
            name="📢 Channel Penting",
            value=(
                "• **#pengumuman** — Info terbaru & event\n"
                "• **#akademi** — Belajar trading dari nol\n"
                "• **#lounge-chat** — Diskusi bebas & sharing"
            ),
            inline=False
        )
        embed.add_field(
            name="🔰 Tips Awal",
            value=(
                "✅ Lengkapi profil Discord kamu\n"
                "✅ Perkenalkan diri di #perkenalan\n"
                "✅ Baca peraturan server di #peraturan\n"
                "✅ Jangan ragu bertanya, semua ramah!"
            ),
            inline=False
        )
        embed.add_field(
            name="💡 Upgrade ke WizardMember?",
            value=(
                "Nikmati tools eksklusif, dan konsultasi langsung dengan mentor!\n"
                "Segera Explore Room Wizard nya."
            ),
            inline=False
        )
        embed.set_image(url="https://media.giphy.com/media/26ufnwz3wDUli7GU0/giphy.gif")
        embed.set_footer(
            text="MountAlgo | Komunitas Trader Indonesia",
            icon_url=channel.guild.me.display_avatar.url
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        label="➮ Langganan Premium",
        style=discord.ButtonStyle.primary,
        custom_id="verif_langganan"
    )
    async def premium_subscribe(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        roles = [r.name for r in user.roles]

        if "WizardMemberBulanan" in roles or "WizardMemberTahunan" in roles:
            # Embed super menarik untuk WizardMember yang sudah langganan
            embed = discord.Embed(
                title="💎 Kamu Sudah Wizardmember premium (Wizard Member)!",
                description=(
                    "Terima kasih telah menjadi bagian dari **WizardMember MountAlgo**!\n\n"
                    "🌟 **Langganan premium kamu masih aktif.**\n"
                    "Nikmati seluruh fitur eksklusif dan akses premium tanpa batas!\n\n"
                    "Jika masa langganan habis, kamu bisa memperpanjang kembali melalui tombol ini."
                ),
                color=discord.Color.gold()
            )
            embed.set_thumbnail(url=interaction.guild.me.display_avatar.url)
            embed.add_field(
                name="🚀 Fitur Premium yang Kamu Nikmati",
                value=(
                    "• Wizard Toolkits: Alat Serbaguna\n"                     
                    "• Wizard Analisis: Analisis Dari aset crypto forex dan komoditas yang mendalam \n"                     
                    "• Wizard Setrategi : Strategi khusus yang dipacking sebaik mungkin untuk Strategi perdagangan di pasar crypto forex dan komoditas\n\n"                     
                    "• Konsultasi prioritas\n"                     
                    "• event eksklusif"
                ),
                inline=False
            )
            embed.add_field(
                name="⏳ Perpanjang Langganan?",
                value=(
                    "Kamu bisa memperpanjang langganan setelah masa aktifmu berakhir.\n"
                    "Pantau tanggal kadaluwarsa di DM atau hubungi admin jika butuh bantuan."
                ),
                inline=False
            )
            embed.set_image(url="https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif")
            embed.set_footer(
                text="MountAlgo Premium System | Terima kasih telah menjadi WizardMember!",
                icon_url=interaction.guild.me.display_avatar.url
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title="✚ KEANGGOTAAN Wizard MountAlgo",
            description=(
                "☛ Tingkatkan ke WizardMember untuk Akses Penuh\n"
                "Buka semua fitur premium MountAlgo dan maksimalkan potensi perdagangan Anda.\n"
                "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                "➩ Pilih paket langganan di bawah ini:"
            ),
            color=COLOR_GREEN  # Hijau negatif
        )
        
        # Fungsi untuk membuat bar fitur
        def feature_bar(enabled=True, length=15):
            bar = "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰" if enabled else "▰▰▰▰▰▰▱▱▱▱▱▱▱▱▱"
            return f"{'✔' if enabled else '✘'}  ●{bar}\n"

        # Fitur untuk WizardMember
        embed.add_field(
            name="❑ FITUR WizardMember",
            value=(
                "```yaml\n"
                f"{feature_bar(True)} Analisis Pasar QuantumFlow™\n"
                f"{feature_bar(True)} Wizard Toolkits: Alat Serbaguna\n"                     
                f"{feature_bar(True)} Wizard Analisis: Analisis Dari aset crypto forex dan komoditas yang mendalam \n"                     
                f"{feature_bar(True)} Wizard Setrategi : Strategi khusus yang dipacking sebaik mungkin untuk Strategi perdagangan di pasar crypto forex dan komoditas\n\n"                     
                f"{feature_bar(True)} Konsultasi prioritas\n"                     
                f"{feature_bar(True)} event eksklusif"
                "```"
            ),
            inline=False
        )
        
        # Fitur untuk Anggota Biasa
        embed.add_field(
            name="❑ FITUR ANGGOTA BIASA",
            value=(
                "```yaml\n"
                f"{feature_bar(False)} Akses terbatas\n"
                f"{feature_bar(False)} Tanpa strategi khusus\n"
                f"{feature_bar(False)} Tanpa alat cang\n"
                f"{feature_bar(True)} Edukasi dasar hingga profesional\n"
                f"{feature_bar(True)} Komunitas publik\n"
                "```"
            ),
            inline=False
        )
        
        # Paket Harga
        embed.add_field(
            name="⬈ BIAYA LANGGANAN",
            value=(
                "```yaml\n"
                "┌───────────────┬───────────────┐\n"
                "│ Paket         │ Harga         │\n"
                "├───────────────┼───────────────┤\n"
                "│ Wizard Bulanan │ Rp 596.000/bln│\n"
                "│ Wizard Tahunan │ Rp 5.803.000  │\n"
                "│ (Hemat 15%)   │               │\n"
                "└───────────────┴───────────────┘\n"
                "```\n"
                "➩ Catatan: Setelah pembayaran, lakukan verifikasi Pembayaran di kanal [#bantuan](https://discord.com/channels/SERVER_ID/1385294197497532426) / langsung Kirim bukti Pembayaran pada [Admin](https://discord.com/users/1210393702032347158)"
            ),
            inline=False
        )
        embed.add_field(
            name="❑ STATUS HUKUM PEMBAYARAN",
            value=(
                "```diff\n"
                "➤ Transaksi merupakan pembayaran jasa Alat serta apa yang ada pada fitur Wizard\n"
                "➤ BUKAN investasi atau pengelolaan dana\n"
                "➤ Tidak ada jaminan hasil trading\n"
                "➤ Tidak termasuk layanan finansial berizin\n"
                "➤ Keputusan trading sepenuhnya mandiri\n"
                "```"
            ),
            inline=False
        )
        embed.set_footer(
            text="Komunitas Trading MountAlgo ● Fitur Premium Diperbarui oktobrr 2025 (tekan Dismiss Message Untuk menghapus Pesan"
        )
        
        # Dropdown Opsi Pembayaran
        view = discord.ui.View(timeout=None)
        view.add_item(PaymentSelect())

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(
        label="🫂 Donasi & Free Wizard",
        style=discord.ButtonStyle.danger,
        custom_id="verif_donation"
    )
    async def donation_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        guild = interaction.guild

        # Send confirmation and donation link
        donation_link = DONATION_LINK or "https://saweria.co/mountalgo"
        embed = discord.Embed(
            title="🫂 DUKUNGAN SERVER & WIZARD MEMBER GRATIS",
            description=(
                f"Terima kasih telah mendukung server **𝙈𝙤𝙪𝙣𝙩𝘼𝙡𝙜𝙤**! ❤️\n\n"
                f"Sesuai dengan ketentuan kami, Anda berhak mendapatkan status **Wizard Member Bulanan** secara **GRATIS**! 🎉\n\n"
                f"🔗 **Link Pembayaran/Donasi (Saweria/Payment Link):**\n"
                f"[Klik di sini untuk melakukan Donasi]({donation_link})\n\n"
                f"⚠️ **PENTING:** Setelah melakukan donasi, silakan kirim bukti transfer/pembayaran Anda ke **Admin** "
                f"secara manual untuk mendapatkan peran/role **Wizard Member** gratis Anda!\n\n"
                f"Terima kasih atas kontribusi Anda dalam membantu menjaga kelangsungan komunitas kami!"
            ),
            color=discord.Color.gold()
        )
        embed.set_footer(text="MountAlgo Donation System")
        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Log to laporan channel
        log_channel = discord.utils.get(guild.text_channels, name="laporan")
        if log_channel:
            await log_channel.send(
                f"🫂 {user.mention} telah mengklik tombol donasi untuk mengklaim **Wizard Member Gratis** (Menunggu Verifikasi Manual Admin)."
            )

# --- Bantuan ---
class BantuanView(View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="💎 Cek Langganan Saya", style=discord.ButtonStyle.primary, custom_id="cek_langganan_saya")
    async def cek_langganan(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Menampilkan status langganan user (member / Wizard / admin)"""
        try:
            user_id = interaction.user.id
            guild = interaction.guild

            # Ambil data user dari database
            user_data = await Database.get_user_data(user_id)
            if not user_data:
                await interaction.response.send_message(
                    "❌ Data Anda belum terdaftar di sistem. Silakan klik **Verifikasi** dulu di channel `#verifikasi`.",
                    ephemeral=True
                )
                return

            user_id, username, status, sub_type, expiry = user_data
            role_display = "👤 Member Biasa"
            color = discord.Color(COLOR_CYAN)
            expiry_text = "-"
            subscription_label = "Tidak Aktif"

            # --- Tentukan status dan role ---
            if status == "WizardMemberBulanan":
                role_display = "💎 **Wizard Member Bulanan**"
                color = discord.Color.gold()
                subscription_label = "Bulanan (30 Hari)"
                if expiry:
                    expiry_text = format_wib(expiry)
            elif status == "WizardMemberTahunan":
                role_display = "👑 **Wizard Member Tahunan**"
                color = discord.Color(COLOR_VIOLET)
                subscription_label = "Tahunan (365 Hari)"
                if expiry:
                    expiry_text = format_wib(expiry)
            elif status == "Admin":
                role_display = "⚙️ **Admin MountAlgo**"
                color = discord.Color.red()
                subscription_label = "Tidak Terbatas"
                expiry_text = "-"
            else:
                role_display = "👤 **Member Biasa**"
                color = discord.Color(COLOR_VIOLET)

            # --- Cek Role Discord Langsung ---
            member = guild.get_member(user_id)
            active_roles = ", ".join([r.name for r in member.roles if r.name != "@everyone"])

            # --- Buat Embed ---
            embed = discord.Embed(
                title="📋 STATUS LANGGANAN ANDA",
                description=f"Informasi terkini status akun MountAlgo Anda.",
                color=color
            )
            embed.add_field(name="👤 Nama Pengguna", value=f"`{interaction.user.display_name}`", inline=True)
            embed.add_field(name="🆔 ID", value=f"`{user_id}`", inline=True)
            embed.add_field(name="📜 Status", value=role_display, inline=False)
            embed.add_field(name="🕒 Jenis Langganan", value=subscription_label, inline=True)
            embed.add_field(name="⏳ Berlaku Sampai", value=expiry_text or "-", inline=True)
            embed.add_field(name="🎭 Role Discord Aktif", value=active_roles or "-", inline=False)
            embed.set_footer(text="MountAlgo Premium System — Cek status langganan Anda kapan pun.")

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            logging.error(f"Error di tombol cek_langganan: {e}", exc_info=True)
            await interaction.response.send_message(
                "❌ Terjadi kesalahan saat memeriksa status langganan Anda.",
                ephemeral=True
            )

    @discord.ui.button(label="❑ FAQ", style=discord.ButtonStyle.secondary, custom_id="bantuan_faq")
    async def faq(self, interaction: discord.Interaction, button: Button):
        embed = send_faq_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="✔ Verifikasi Langganan", style=discord.ButtonStyle.primary, custom_id="bantuan_langganan")
    async def verif_langganan(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="➮ PANDUAN VERIFIKASI KEANGGOTAAN Wizard",
            color=COLOR_GREEN,  # Hijau negatif
            description=(
                "☛ Langkah-langkah untuk Mengaktifkan Keanggotaan Wizard\n"
                "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                "1. Transfer biaya langganan melalui pilihan DANA / CRYPTO di menu verifikasi.\n"
                "2. Kirim bukti pembayaran beserta Id discord anda ke admin dengan menekan tombol hubungi admin di kanal #bantuan.\n"
                "3. Tunggu konfirmasi dan peningkatan peran ke WizardMember.\n"
                "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                "➩ Jika mengalami kendala, gunakan  juga tombol Hubungi Admin Untuk permasalahan tersebut."
            )
        )
        embed.set_footer(
            text="Komunitas Trading MountAlgo ● Panduan Keanggotaan Wizard (tekan Dismiss Message Untuk menghapus Pesan"
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="● Hubungi Admin", style=discord.ButtonStyle.success, custom_id="bantuan_admin")
    async def hubungi_admin(self, interaction: discord.Interaction, button: Button):
        await send_hubungi_admin_embed(interaction.guild,interaction)
        await send_laporan_admin_embed(
            guild=interaction.guild,
            user=interaction.user,
            alasan="Permintaan bantuan melalui tombol Hubungi Admin"
        )
        
async def get_thread_creator_id(thread: discord.Thread) -> int | None:
    """Mendapatkan ID pembuat thread asli dari embed pembuka"""
    if not thread or not thread.guild:
        return None
    if thread.owner_id and thread.owner_id != thread.guild.me.id:
        return thread.owner_id

    try:
        async for msg in thread.history(limit=5, oldest_first=True):
            if msg.embeds:
                for embed in msg.embeds:
                    for field in embed.fields:
                        if "Diprakarsai oleh" in field.name:
                            match = re.search(r"<@!?(\d+)>", field.value)
                            if match:
                                return int(match.group(1))
    except Exception as e:
        logging.error(f"Error get_thread_creator_id: {e}")

    return None


class ThreadManagementView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Cek akses berdasarkan role"""
        # Cek apakah channel adalah thread
        if not isinstance(interaction.channel, discord.Thread):
            await interaction.response.send_message("❌ Ini hanya bisa digunakan di thread!", ephemeral=True)
            return False
            
        return True  # Biarkan semua user berinteraksi

    async def is_owner_or_admin(self, interaction: discord.Interaction) -> bool:
        """Mengecek apakah user adalah pembuat thread atau Admin"""
        creator_id = await get_thread_creator_id(interaction.channel)
        is_creator = (creator_id == interaction.user.id)
        admin_role = discord.utils.get(interaction.guild.roles, name="Admin")
        is_admin = (admin_role in interaction.user.roles) or interaction.user.guild_permissions.administrator
        return is_creator or is_admin
    
    @discord.ui.button(
        label="Hapus Thread",
        style=discord.ButtonStyle.red,
        custom_id="delete_thread"
    )
    async def delete_thread(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.is_owner_or_admin(interaction):
            await interaction.response.send_message(
                "❌ Hanya pembuat thread atau Admin yang bisa menghapus thread!",
                ephemeral=True
            )
            return
            
        await interaction.response.send_message(
            "Thread akan dihapus dalam 5 detik...",
            ephemeral=True
        )
        await asyncio.sleep(5)
        await interaction.channel.delete()
    
    @discord.ui.button(
        label="🔔 Tag Anggota",
        style=discord.ButtonStyle.primary,
        custom_id="tag_members"
    )
    async def tag_members(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.is_owner_or_admin(interaction):
            await interaction.response.send_message(
                "❌ Hanya pembuat thread atau Admin yang bisa menggunakan fitur tag anggota!",
                ephemeral=True
            )
            return

        await interaction.response.send_modal(ThreadTaggingModal())

class ObrolanView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="🫂 Perkenalan Diri", style=discord.ButtonStyle.primary, custom_id="perkenalan_baru")
    async def perkenalan(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(PerkenalanModal())
    
    @button(label="💬 Mulai Diskusi Baru", style=discord.ButtonStyle.success, custom_id="mulai_diskusi")
    async def mulai_diskusi(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(DiskusiModal())

class WizardLoungeView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="💬 Mulai Diskusi Baru", style=discord.ButtonStyle.success, custom_id="wizard_mulai_diskusi")
    async def mulai_diskusi(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(DiskusiModal())

# --- wizard-toolkits view ---
class WizardToolkitsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="❑ Lihat harga aset",
        style=discord.ButtonStyle.primary,
        custom_id="toolkit:harga_aset",
        row=0
    )
    async def harga_aset(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AssetPriceModal())

    @discord.ui.button(
        label="❑ Kalkulator Perdagangan",
        style=discord.ButtonStyle.primary,
        custom_id="toolkit:calculator",
        row=0
    )
    async def calculate_trade(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TradingCalculatorModal())

    @discord.ui.button(
        label="✇ Panduan Kalkulator",
        style=discord.ButtonStyle.secondary,
        custom_id="panduan_calculator",
        row=0
    )
    async def panduan_calculator(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = await send_panduan_calculator_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        label="✔ Templat Risiko",
        style=discord.ButtonStyle.success,
        custom_id="risk_template",
        row=0
    )
    async def risk_template(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = await send_risk_template_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)

# --- wizard-journal view ---
from typing import Optional, Tuple

def format_price(price: float, precision: int = 8) -> str:
    """Format harga dengan presisi tinggi untuk crypto"""
    try:
        if price == 0:
            return "0"
        
        # Tentukan jumlah digit desimal berdasarkan besaran angka
        if price >= 1:
            # Untuk angka >= 1, gunakan 2-4 digit desimal
            decimals = min(4, max(2, len(str(price).split('.')[1]) if '.' in str(price) else 0))
        elif price >= 0.1:
            decimals = 4
        elif price >= 0.01:
            decimals = 5
        elif price >= 0.001:
            decimals = 6
        elif price >= 0.0001:
            decimals = 7
        elif price >= 0.00001:
            decimals = 8
        else:
            decimals = 9
        
        # Format dengan pemisah ribuan dan desimal
        formatted = f"{price:,.{decimals}f}"
        
        # Hapus trailing zeros dan koma yang tidak perlu
        if '.' in formatted:
            formatted = formatted.rstrip('0').rstrip('.')
        
        return formatted
        
    except (ValueError, TypeError):
        return str(price)

def format_number(value, is_price=False):
    """Format angka umum dengan handling khusus untuk harga"""
    if value is None or str(value).strip() in ("", "-"):
        return "-"
    
    try:
        if is_price:
            return format_price(float(value))
        
        val = float(value)
        if val == 0:
            return "0"
        
        # Format berdasarkan besaran angka
        if abs(val) >= 1000:
            return f"{val:,.0f}"
        elif abs(val) >= 1:
            return f"{val:,.2f}".rstrip('0').rstrip('.')
        elif abs(val) >= 0.001:
            return f"{val:.6f}".rstrip('0').rstrip('.')
        else:
            return f"{val:.8f}".rstrip('0').rstrip('.')
            
    except (ValueError, TypeError):
        return str(value)


class TradingCalculator:
    """Kalkulator trading dengan format 8 parts: DIRECTION/ENTRY/SL/TP1/TP2/TP3/LEVERAGE/VALUE_TYPE"""
    
    @staticmethod
    def default_position_data():
        """Return default position data untuk error handling"""
        return {
            'direction': "BUY",
            'entry_price': 0.0,
            'current_price': 0.0,
            'sl_price': 0.0,
            'tp1_price': 0.0,
            'tp2_price': None,
            'tp3_price': None,
            'leverage': 1.0,
            'value_type': "USD",
            '_precision': {
                'entry': 8,
                'sl': 8,
                'tp1': 8,
                'tp2': 8,
                'tp3': 8,
                'leverage': 1
            }
        }

    @staticmethod
    async def validate_position_string(position_str: str) -> Tuple[bool, str]:
        """
        Validasi format position string dengan format 8 parts (7 slash)
        DIRECTION/ENTRY/SL/TP1/TP2/TP3/LEVERAGE/VALUE_TYPE
        """
        try:
            parts = [part.strip() for part in position_str.split('/')]
            
            # Debug info
            logging.info(f"VALIDATION: Parts={parts}, Count={len(parts)}")
            
            # Format harus tepat 7 slash untuk 8 parts
            expected_slashes = 7  # 8 parts = 7 slash
            actual_slashes = position_str.count('/')
            if actual_slashes != expected_slashes:
                return False, f"Format harus memiliki tepat 7 slash (/). Contoh: BUY/ENTRY/SL/TP1/TP2/TP3/LEVERAGE/VALUE_TYPE"
            
            # Pastikan ada 8 parts
            if len(parts) != 8:
                return False, f"Format harus memiliki 8 bagian. Ditemukan: {len(parts)} bagian"
            
            # Validasi direction
            direction = parts[0].upper()
            if direction not in ["BUY", "SELL"]:
                return False, "Direction harus BUY atau SELL"
            
            # Validasi angka utama (entry, sl, tp1) - WAJIB ADA
            required_indices = [1, 2, 3]  # ENTRY, SL, TP1
            required_names = ["ENTRY", "SL", "TP1"]
            
            for i, idx in enumerate(required_indices):
                if not parts[idx] or parts[idx] in ['', ' ']:
                    return False, f"{required_names[i]} harus diisi"
                
                try:
                    clean_value = parts[idx].replace(',', '.')
                    clean_value = re.sub(r'[^\d.]', '', clean_value)
                    if not clean_value:
                        return False, f"{required_names[i]} tidak valid"
                        
                    val = float(clean_value)
                    if val <= 0:
                        return False, f"{required_names[i]} harus > 0"
                except ValueError:
                    return False, f"Format {required_names[i]} tidak valid: '{parts[idx]}'"
            
            # Validasi TP2 dan TP3 (opsional, bisa kosong)
            for i in [4, 5]:  # Index untuk TP2 dan TP3
                if parts[i] and parts[i] not in ['', ' ']:
                    try:
                        clean_value = parts[i].replace(',', '.')
                        clean_value = re.sub(r'[^\d.]', '', clean_value)
                        if clean_value:
                            val = float(clean_value)
                            if val <= 0:
                                return False, f"TP{i-2} harus > 0 jika diisi"
                    except ValueError:
                        return False, f"Format TP{i-2} tidak valid: '{parts[i]}'"
            
            # Validasi leverage - WAJIB di posisi 6
            if not parts[6] or parts[6] in ['', ' ']:
                return False, "Leverage harus diisi"
            
            try:
                leverage_str = parts[6]
                clean_leverage = leverage_str.replace(',', '.')
                clean_leverage = re.sub(r'[^\d.]', '', clean_leverage)
                leverage = float(clean_leverage)
                
                if leverage <= 0:
                    return False, "Leverage harus > 0"
                if leverage > 1000:
                    return False, "Leverage terlalu tinggi (max 1000x)"
                    
            except ValueError:
                return False, f"Leverage tidak valid: '{parts[6]}'"
            
            # Validasi value type - WAJIB di posisi 7
            if not parts[7] or parts[7] in ['', ' ']:
                return False, "Value type harus diisi"
            
            value_type = parts[7].upper()
            if value_type not in ["USD", "LOT", "USDT"]:
                return False, "Value type harus USD, LOT, atau USDT"
            
            return True, "Valid"
            
        except Exception as e:
            logging.error(f"Validation error: {str(e)}")
            return False, f"Error validasi: {str(e)}"

    @staticmethod
    async def parse_position_string(position_str: str) -> dict:
        """
        Parse position string dengan format 8 parts (7 slash)
        DIRECTION/ENTRY/SL/TP1/TP2/TP3/LEVERAGE/VALUE_TYPE
        """
        try:
            parts = [part.strip() for part in position_str.split('/')]
            
            # Pastikan selalu ada 8 parts
            if len(parts) != 8:
                return TradingCalculator.default_position_data()
            
            logging.info(f"PARSING: Parts={parts}")
            
            def safe_float(value, default=None):
                if not value or value in ['', ' ', 'None', 'null', 'undefined']:
                    return default
                try:
                    clean_value = value.replace(',', '.')
                    clean_value = re.sub(r'[^\d.]', '', clean_value)
                    if not clean_value:
                        return default
                    return float(clean_value)
                except (ValueError, TypeError):
                    return default
            
            # Parse dengan format tetap
            result = {
                'direction': parts[0].upper(),
                'entry_price': safe_float(parts[1], 0.0),
                'current_price': safe_float(parts[1], 0.0),
                'sl_price': safe_float(parts[2], 0.0),
                'tp1_price': safe_float(parts[3], 0.0),
                'tp2_price': safe_float(parts[4]),
                'tp3_price': safe_float(parts[5]),
                'leverage': safe_float(parts[6], 1.0),
                'value_type': parts[7].upper() if parts[7] else "USD",
                '_precision': {
                    'entry': TradingCalculator._determine_precision(parts[1]),
                    'sl': TradingCalculator._determine_precision(parts[2]),
                    'tp1': TradingCalculator._determine_precision(parts[3]),
                    'tp2': TradingCalculator._determine_precision(parts[4]) if parts[4] else 8,
                    'tp3': TradingCalculator._determine_precision(parts[5]) if parts[5] else 8,
                    'leverage': TradingCalculator._determine_precision(parts[6]) if parts[6] else 1
                }
            }
            
            logging.info(f"PARSED: {result}")
            return result
            
        except Exception as e:
            logging.error(f"Parsing error: {str(e)}")
            return TradingCalculator.default_position_data()

    @staticmethod
    def _determine_precision(value: str) -> int:
        """
        Tentukan presisi berdasarkan nilai string
        """
        try:
            if not value or value in ['', ' ']:
                return 8
                
            if '.' not in value:
                return 2
            
            decimal_part = value.split('.')[1]
            
            # Untuk angka sangat kecil
            if value.startswith('0.0'):
                return min(8, len(decimal_part))
            
            # Untuk angka normal
            return min(6, len(decimal_part.rstrip('0')))
            
        except:
            return 6

    @staticmethod
    def format_price_extended(price: float, original_str: str = None) -> str:
        """
        Format harga dengan presisi adaptif
        """
        try:
            if price == 0:
                return "0"
            
            if original_str:
                precision = TradingCalculator._determine_precision(original_str)
            else:
                if price >= 1000:
                    precision = 2
                elif price >= 1:
                    precision = 4
                elif price >= 0.1:
                    precision = 5
                elif price >= 0.01:
                    precision = 6
                elif price >= 0.001:
                    precision = 7
                elif price >= 0.0001:
                    precision = 8
                else:
                    precision = 10
            
            formatted = f"{price:,.{precision}f}"
            
            if '.' in formatted:
                formatted = formatted.rstrip('0').rstrip('.')
            
            formatted = formatted.replace('.', ',')
            return formatted
            
        except:
            return str(price)

    @staticmethod
    def format_position_display(position_data: dict) -> str:
        """
        Format position untuk display
        """
        try:
            precision_info = position_data.get('_precision', {})
            
            def format_with_precision(value, precision_type, default_precision=6):
                if value is None:
                    return "-"
                precision = precision_info.get(precision_type, default_precision)
                return TradingCalculator.format_price_extended(value, str(value))
            
            lines = [
                f"**Direction**: {position_data['direction']}",
                f"**Entry**: {format_with_precision(position_data['entry_price'], 'entry')}",
                f"**Current**: {format_with_precision(position_data['current_price'], 'current')}",
                f"**SL**: {format_with_precision(position_data['sl_price'], 'sl')}",
                f"**TP1**: {format_with_precision(position_data['tp1_price'], 'tp1')}",
            ]
            
            if position_data['tp2_price'] is not None:
                lines.append(f"**TP2**: {format_with_precision(position_data['tp2_price'], 'tp2')}")
            else:
                lines.append(f"**TP2**: -")
                
            if position_data['tp3_price'] is not None:
                lines.append(f"**TP3**: {format_with_precision(position_data['tp3_price'], 'tp3')}")
            else:
                lines.append(f"**TP3**: -")
            
            lines.append(f"**Leverage**: {format_with_precision(position_data['leverage'], 'leverage', 1)}x")
            lines.append(f"**Type**: {position_data['value_type']}")
            
            return "\n".join(lines)
            
        except Exception as e:
            return f"Error formatting: {str(e)}"

    @staticmethod
    async def calculate_pnl_high_precision(direction: str, entry: float, exit: float, 
                                        value: float, leverage: float, value_type: str) -> Tuple[float, str]:
        """
        Hitung PnL dengan presisi tinggi
        """
        try:
            entry_dec = Decimal(str(entry))
            exit_dec = Decimal(str(exit))
            value_dec = Decimal(str(value))
            leverage_dec = Decimal(str(leverage))
            
            if value_type.upper() == "LOT":
                multiplier = Decimal('100000')
            else:
                multiplier = Decimal('1')
            
            if direction.upper() == "BUY":
                raw_pnl = (exit_dec - entry_dec) * value_dec * multiplier * leverage_dec
            else:
                raw_pnl = (entry_dec - exit_dec) * value_dec * multiplier * leverage_dec
            
            pnl_value = float(raw_pnl)
            
            # Format PnL
            if abs(pnl_value) >= 1000:
                formatted_pnl = f"${pnl_value:,.2f}"
            elif abs(pnl_value) >= 1:
                formatted_pnl = f"${pnl_value:,.4f}"
            elif abs(pnl_value) >= 0.01:
                formatted_pnl = f"${pnl_value:,.6f}"
            else:
                formatted_pnl = f"${pnl_value:.8f}"
            
            formatted_pnl = formatted_pnl.rstrip('0').rstrip('.')
            return pnl_value, formatted_pnl
            
        except Exception as e:
            return 0.0, "$0"

    @staticmethod
    async def determine_trade_result(direction: str, entry: float, sl: float, 
                                   tp1: float, current_price: float,
                                   tp2: Optional[float] = None, 
                                   tp3: Optional[float] = None) -> Tuple[str, str]:
        """
        Tentukan hasil trade - RETURN TUPLE (result, status)
        """
        try:
            direction = direction.upper()
            entry_dec = Decimal(str(entry))
            sl_dec = Decimal(str(sl))
            tp1_dec = Decimal(str(tp1))
            current_dec = Decimal(str(current_price))
            
            tp2_dec = Decimal(str(tp2)) if tp2 is not None else None
            tp3_dec = Decimal(str(tp3)) if tp3 is not None else None
            
            if direction == "BUY":
                if current_dec <= sl_dec:
                    return "SL", "❌ Stop Loss"
                elif tp3_dec and current_dec >= tp3_dec:
                    return "TP3", "✅ Take Profit 3"
                elif tp2_dec and current_dec >= tp2_dec:
                    return "TP2", "✅ Take Profit 2"
                elif current_dec >= tp1_dec:
                    return "TP1", "✅ Take Profit 1"
                else:
                    return "OPEN", "⏳ Masih Berjalan"
            else:
                if current_dec >= sl_dec:
                    return "SL", "❌ Stop Loss"
                elif tp3_dec and current_dec <= tp3_dec:
                    return "TP3", "✅ Take Profit 3"
                elif tp2_dec and current_dec <= tp2_dec:
                    return "TP2", "✅ Take Profit 2"
                elif current_dec <= tp1_dec:
                    return "TP1", "✅ Take Profit 1"
                else:
                    return "OPEN", "⏳ Masih Berjalan"
                    
        except Exception as e:
            return "ERROR", "⚠️ Error"

    @staticmethod
    async def format_position_string(position_data: dict) -> str:
        """
        Format dictionary ke string position dengan format tetap
        """
        try:
            tp2 = position_data.get('tp2_price', '')
            tp3 = position_data.get('tp3_price', '')
            
            # Handle None values
            tp2 = '' if tp2 is None else tp2
            tp3 = '' if tp3 is None else tp3
            
            return f"{position_data['direction']}/" \
                   f"{position_data['entry_price']}/" \
                   f"{position_data['sl_price']}/" \
                   f"{position_data['tp1_price']}/" \
                   f"{tp2}/" \
                   f"{tp3}/" \
                   f"{position_data['leverage']}/" \
                   f"{position_data['value_type']}"
        except Exception as e:
            return "BUY/0/0/0///1/USD"

    @staticmethod
    async def calculate_pnl(direction: str, open_price: float, close_price: float, 
                          value: float, leverage: float, value_type: str) -> float:
        """
        Hitung Profit/Loss berdasarkan tipe trading dengan leverage
        """
        try:
            # Hitung persentase perubahan harga
            if direction.upper() == "BUY":
                pct_change = (close_price - open_price) / open_price if open_price != 0 else 0
            else:  # SELL
                pct_change = (open_price - close_price) / open_price if open_price != 0 else 0
            
            # Hitung PnL berdasarkan tipe nilai
            if value_type.upper() == "LOT":
                # Untuk forex/komoditas: 1 LOT = 100,000 unit
                contract_size = 100000
                # PnL tanpa leverage
                base_pnl = pct_change * value * contract_size
                # Terapkan leverage
                leveraged_pnl = base_pnl * leverage
            elif value_type.upper() in ["USD", "USDT"]:
                # Untuk crypto dan direct USD value
                # PnL tanpa leverage
                base_pnl = pct_change * value
                # Terapkan leverage
                leveraged_pnl = base_pnl * leverage
            else:
                # Default fallback
                leveraged_pnl = pct_change * value * leverage
                
            return leveraged_pnl
        except Exception as e:
            logging.error(f"Error calculating PnL: {e}")
            return 0.0







# Utility functions untuk formatting
def format_price(price: float, precision: int = 8) -> str:
    """Format harga dengan presisi tinggi untuk crypto"""
    try:
        if price == 0:
            return "0"
        
        # Tentukan jumlah digit desimal berdasarkan besaran angka
        if price >= 1:
            decimals = min(4, max(2, len(str(price).split('.')[1]) if '.' in str(price) else 0))
        elif price >= 0.1:
            decimals = 4
        elif price >= 0.01:
            decimals = 5
        elif price >= 0.001:
            decimals = 6
        elif price >= 0.0001:
            decimals = 7
        elif price >= 0.00001:
            decimals = 8
        else:
            decimals = 9
        
        # Format dengan pemisah ribuan dan desimal
        formatted = f"{price:,.{decimals}f}"
        
        # Hapus trailing zeros dan koma yang tidak perlu
        if '.' in formatted:
            formatted = formatted.rstrip('0').rstrip('.')
            # Ganti decimal point dengan koma untuk format Indonesia
            formatted = formatted.replace('.', ',')
        
        return formatted
        
    except (ValueError, TypeError):
        return str(price)

def format_number(value, is_price=False):
    """Format angka umum dengan handling khusus untuk harga"""
    if value is None or str(value).strip() in ("", "-"):
        return "-"
    
    try:
        if is_price:
            return format_price(float(value))
        
        val = float(value)
        if val == 0:
            return "0"
        
        # Format berdasarkan besaran angka
        if abs(val) >= 1000:
            return f"{val:,.0f}".replace(',', '.')
        elif abs(val) >= 1:
            return f"{val:,.2f}".rstrip('0').rstrip('.').replace(',', '.')
        elif abs(val) >= 0.001:
            return f"{val:.6f}".rstrip('0').rstrip('.').replace('.', ',')
        else:
            return f"{val:.8f}".rstrip('0').rstrip('.').replace('.', ',')
            
    except (ValueError, TypeError):
        return str(value)

class KontrolPenggunaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    async def interaction_check(self, interaction: discord.Interaction):
        admin_role = discord.utils.get(interaction.guild.roles, name="Admin")
        if admin_role not in interaction.user.roles and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "✘ Hanya admin yang dapat mengakses panel ini.",
                ephemeral=True
            )
            return False
        return True

    @discord.ui.button(
        label="Tambah Pengguna",
        style=discord.ButtonStyle.success,
        custom_id="user_add",
        emoji=None
    )
    async def tambah_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AddUserModal())

    @discord.ui.button(
        label="Hapus Pengguna",
        style=discord.ButtonStyle.danger,
        custom_id="user_remove",
        emoji=None
    )
    async def hapus_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RemoveUserModal())

    @discord.ui.button(
        label="Tingkatkan Pengguna",
        style=discord.ButtonStyle.primary,
        custom_id="user_upgrade",
        emoji=None
    )
    async def upgrade_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(UpgradeUserModal())

    @discord.ui.button(
        label="Sinkronkan User sesuai Roles",
        style=discord.ButtonStyle.secondary,
        custom_id="user_sync_roles",
        emoji="🔄"
    )
    async def sinkronkan_user_roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True, thinking=True)
        try:
            result = await synchronize_users_and_roles(interaction.guild)
            await interaction.followup.send(f"✅ {result}", ephemeral=True)
        except Exception as e:
            logging.error(f"Error sinkronkan user roles: {e}", exc_info=True)
            await interaction.followup.send(f"❌ Terjadi kesalahan saat sinkronisasi:\n`{e}`", ephemeral=True)

    @discord.ui.button(
        label="Lihat Status",
        style=discord.ButtonStyle.primary,
        emoji="📋",
        custom_id="lihat_status_btn"
    )
    async def lihat_status(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        try:
            users = await Database.get_all_users()
            if not users:
                embed = discord.Embed(
                    title="📊 DATA PENGGUNA",
                    description="Tidak ada data pengguna ditemukan di database.",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            user_list = []
            now_utc = datetime.utcnow()

            for user_id, username, status, sub_type, expiry_str in users:
                emoji = "👤"
                color = discord.Color(COLOR_VIOLET)
                extra = ""

                # Penentuan warna & ikon per status
                if status == "WizardMemberBulanan":
                    emoji = "💎"
                    color = discord.Color.gold()
                    extra = "▸ **Tipe:** Bulanan"
                elif status == "WizardMemberTahunan":
                    emoji = "🏆"
                    color = discord.Color(COLOR_VIOLET)
                    extra = "▸ **Tipe:** Tahunan"
                elif status == "Admin":
                    emoji = "🛡️"
                    color = discord.Color.red()
                elif status == "member":
                    emoji = "🔹"
                    color = discord.Color(COLOR_CYAN)
                elif status == "PendingVerification":
                    emoji = "⏳"
                    color = discord.Color.greyple()
                else:
                    emoji = "⚪"
                    color = discord.Color.light_grey()

                # Format tanggal kedaluwarsa (jika ada)
                expiry_info = ""
                if expiry_str:
                    try:
                        expiry_dt = datetime.fromisoformat(expiry_str)
                        expiry_wib = format_wib(expiry_str)
                        days_left = math.ceil((expiry_dt - now_utc).total_seconds() / 86400)
                        if days_left > 0:
                            expiry_info = f"\n▸ **Berakhir:** `{expiry_wib}` ({days_left} hari lagi)"
                        else:
                            expiry_info = f"\n▸ **Berakhir:** `Kedaluwarsa`"
                    except Exception:
                        expiry_info = f"\n▸ **Berakhir:** `{expiry_str}`"

                # Susun teks status
                line = (
                    f"{emoji} **{username}** (`{user_id}`)\n"
                    f"▸ **Status:** `{status}`"
                )
                if extra:
                    line += f"\n{extra}"
                if expiry_info:
                    line += expiry_info

                user_list.append((line, color))

            # Buat halaman (maks 5 user per halaman)
            per_page = 5
            pages = [user_list[i:i + per_page] for i in range(0, len(user_list), per_page)]

            # Fungsi buat embed per halaman
            def make_embed(page_index: int):
                page_users = pages[page_index]
                desc = "\n\n".join(u[0] for u in page_users)
                # Ambil warna dominan
                colors = [u[1] for u in page_users]
                color = colors[0] if len(set(colors)) == 1 else discord.Color(COLOR_VIOLET)

                embed = discord.Embed(
                    title="📋 DAFTAR PENGGUNA TERDAFTAR",
                    description=desc,
                    color=color
                )
                embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
                embed.set_footer(text=f"Halaman {page_index + 1}/{len(pages)} • Total {len(user_list)} pengguna")
                return embed

            # Tampilkan halaman pertama
            current_page = 0
            embed = make_embed(current_page)

            if len(pages) == 1:
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            # View Pagination
            class UserStatusPaginator(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=120)
                    self.page = 0

                async def interaction_check(self, inter: discord.Interaction) -> bool:
                    is_admin = any(r.name == "Admin" for r in inter.user.roles) or inter.user.guild_permissions.administrator
                    if not is_admin:
                        await inter.response.send_message("✘ Akses Ditolak!", ephemeral=True)
                        return False
                    return True

                @discord.ui.button(label="⬅️", style=discord.ButtonStyle.secondary)
                async def prev_page(self, inter: discord.Interaction, btn: discord.ui.Button):
                    self.page = (self.page - 1) % len(pages)
                    await inter.response.edit_message(embed=make_embed(self.page), view=self)

                @discord.ui.button(label="➡️", style=discord.ButtonStyle.secondary)
                async def next_page(self, inter: discord.Interaction, btn: discord.ui.Button):
                    self.page = (self.page + 1) % len(pages)
                    await inter.response.edit_message(embed=make_embed(self.page), view=self)

            await interaction.followup.send(embed=embed, view=UserStatusPaginator(), ephemeral=True)

        except Exception as e:
            logging.error(f"Error tombol Lihat Status: {e}", exc_info=True)
            await interaction.followup.send(
                f"⚠️ Terjadi kesalahan saat memuat data pengguna.\n`{e}`",
                ephemeral=True
            )
            
class UserListPaginationView(discord.ui.View):
    def __init__(self, pages: list):
        super().__init__(timeout=60)
        self.pages = pages
        self.current_page = 0
        
    @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.secondary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_embed(interaction)
            
    @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.secondary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            await self.update_embed(interaction)
            
    async def update_embed(self, interaction: discord.Interaction):
        embed = interaction.message.embeds[0]
        embed.description = (
            "```diff\n"
            "+ DAFTAR PENGGUNA AKTIF MountAlgo\n"
            "```\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n" +
            "\n\n".join(self.pages[self.current_page])
        )
        embed.set_footer(
            text=f"MountAlgo Trading Community • Halaman {self.current_page + 1}/{len(self.pages)} • Total {sum(len(page) for page in self.pages)} pengguna"
        )
        await interaction.response.edit_message(embed=embed)
        
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

# ==========================================================
# ⚙️ PANEL KONTROL ADMIN VIEW
# ==========================================================

class WizardChannelSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.button(label="🪙 Wizard Crypto", style=discord.ButtonStyle.primary, custom_id="select_wizard_crypto")
    async def crypto_selected(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(
            AnalysisModal(title="Analisis Crypto Pasar", thread_name="wizard-crypto")
        )

    @discord.ui.button(label="🌐 Wizard Forex", style=discord.ButtonStyle.primary, custom_id="select_wizard_forex")
    async def forex_selected(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(
            AnalysisModal(title="Analisis Forex Pasar", thread_name="wizard-forex")
        )

    @discord.ui.button(label="🏆 Wizard Gold", style=discord.ButtonStyle.primary, custom_id="select_wizard_gold")
    async def gold_selected(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(
            AnalysisModal(title="Analisis Gold/Komoditas Pasar", thread_name="wizard-gold")
        )

class KontrolAdminView(discord.ui.View):
    """Panel kontrol utama untuk Admin MountAlgo"""
    def __init__(self):
        super().__init__(timeout=None)

    # ------------------------------------------------------
    # 🔐 Validasi Akses Admin
    # ------------------------------------------------------
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        admin_role = discord.utils.get(interaction.guild.roles, name="Admin")
        if admin_role not in interaction.user.roles and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "✘ Akses Ditolak! Hanya admin yang dapat mengakses panel ini.",
                ephemeral=True
            )
            return False
        return True

    # ------------------------------------------------------
    # 🗣️ Tombol: Atur Ulang Pengumuman
    # ------------------------------------------------------
    @discord.ui.button(
        label="⬈ Atur Ulang Pengumuman",
        style=discord.ButtonStyle.primary,
        custom_id="admin_reset_announce",
        row=0
    )
    async def reset_announce(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ResetChannelModal("pengumuman"))

    # ------------------------------------------------------
    # 🧹 Tombol: Hapus Thread Usang
    # ------------------------------------------------------
    @discord.ui.button(
        label="🧹 Hapus Thread Usang",
        style=discord.ButtonStyle.danger,
        custom_id="admin_delete_threads",
        row=1
    )
    async def hapus_thread_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Tombol untuk menghapus thread perkenalan & obrolan yang sudah usang"""
        view = ConfirmHapusThreadView()
        await interaction.response.send_message(
            "⚠️ Apakah kamu yakin ingin menghapus thread **obrolan & perkenalan** yang sudah tidak aktif?",
            view=view,
            ephemeral=True
        )

    # ------------------------------------------------------
    # 📱 Tombol: Toggle DANA
    # ------------------------------------------------------
    @discord.ui.button(
        label="📱 Toggle DANA",
        style=discord.ButtonStyle.success,
        custom_id="admin_toggle_dana",
        row=1
    )
    async def toggle_dana(self, interaction: discord.Interaction, button: discord.ui.Button):
        global PAYMENT_DANA_ACTIVE
        PAYMENT_DANA_ACTIVE = not PAYMENT_DANA_ACTIVE
        await Database.set_setting("payment_dana_active", str(PAYMENT_DANA_ACTIVE))

        status_str = "AKTIF" if PAYMENT_DANA_ACTIVE else "NONAKTIF"
        await interaction.response.send_message(
            f"✅ Pembayaran via **DANA** sekarang **{status_str}**!",
            ephemeral=True
        )

    # ------------------------------------------------------
    # 🪙 Tombol: Toggle Crypto
    # ------------------------------------------------------
    @discord.ui.button(
        label="🪙 Toggle Crypto",
        style=discord.ButtonStyle.success,
        custom_id="admin_toggle_crypto",
        row=1
    )
    async def toggle_crypto(self, interaction: discord.Interaction, button: discord.ui.Button):
        global PAYMENT_CRYPTO_ACTIVE
        PAYMENT_CRYPTO_ACTIVE = not PAYMENT_CRYPTO_ACTIVE
        await Database.set_setting("payment_crypto_active", str(PAYMENT_CRYPTO_ACTIVE))

        status_str = "AKTIF" if PAYMENT_CRYPTO_ACTIVE else "NONAKTIF"
        await interaction.response.send_message(
            f"✅ Pembayaran via **Crypto (USDC)** sekarang **{status_str}**!",
            ephemeral=True
        )

    # ------------------------------------------------------
    # 💳 Tombol: Toggle Card / Bank
    # ------------------------------------------------------
    @discord.ui.button(
        label="💳 Toggle Bank/Kartu",
        style=discord.ButtonStyle.success,
        custom_id="admin_toggle_card",
        row=1
    )
    async def toggle_card(self, interaction: discord.Interaction, button: discord.ui.Button):
        global PAYMENT_CARD_ACTIVE
        PAYMENT_CARD_ACTIVE = not PAYMENT_CARD_ACTIVE
        await Database.set_setting("payment_card_active", str(PAYMENT_CARD_ACTIVE))

        status_str = "AKTIF" if PAYMENT_CARD_ACTIVE else "NONAKTIF"
        await interaction.response.send_message(
            f"✅ Pembayaran via **Bank/Kartu** sekarang **{status_str}**!",
            ephemeral=True
        )

    # ------------------------------------------------------
    # 💾 Tombol: Hapus Basis Data
    # ------------------------------------------------------
    @discord.ui.button(
        label="✘ Hapus Basis Data",
        style=discord.ButtonStyle.danger,
        custom_id="admin_delete_data",
        row=2
    )
    async def delete_data(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = DeleteDatabaseView()
        await interaction.response.send_message(
            "⚠️ PILIH DATA YANG AKAN DIHAPUS\nPilih salah satu opsi di bawah ini:",
            view=view,
            ephemeral=True
        )

    # ------------------------------------------------------
    # 📤 Tombol: Ekspor Data
    # ------------------------------------------------------
    @discord.ui.button(
        label="⬈ Ekspor Data",
        style=discord.ButtonStyle.secondary,
        custom_id="admin_export",
        row=2
    )
    async def export_signals(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📂 Silakan pilih tabel yang ingin diekspor ke file CSV:",view=ExportDataSelectView(),ephemeral=True)
    # ------------------------------------------------------
    # 👑 Tombol: Kelola Admin
    # ------------------------------------------------------
    @discord.ui.button(
        label="➮ Kelola Admin",
        style=discord.ButtonStyle.secondary,
        custom_id="admin_control_access",
        row=3
    )
    async def admin_control_access(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AdminAccessModal())

    # ------------------------------------------------------
    # 🔧 Tombol: Atur Izin Channel
    # ------------------------------------------------------
    @discord.ui.button(
        label="✇ Atur Izin",
        style=discord.ButtonStyle.secondary,
        custom_id="admin_permissions",
        row=3
    )
    async def atur_izin(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True, thinking=True)
        success_count, error_count, error_details = await apply_channel_permissions(interaction.guild)
        embed = await send_permission_update_embed(interaction, success_count, error_count, error_details)
        await interaction.followup.send(embed=embed, ephemeral=True)

    # ------------------------------------------------------
    # 📊 Tombol: Kirim Analisis Pasar
    # ------------------------------------------------------
    @discord.ui.button(
        label="Kirim Analisis Pasar",
        style=discord.ButtonStyle.secondary,
        custom_id="admin:send_market_analysis",
        row=3
    )
    async def send_market_analysis(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "📊 **Pilih Channel Analisis Pasar:**\nSilakan pilih channel tujuan pengiriman analisis pasar di bawah ini:",
            view=WizardChannelSelectView(),
            ephemeral=True
        )

    # ------------------------------------------------------
    # 🧠 Tombol: Kirim Strategi ke Wizard
    # ------------------------------------------------------
    @discord.ui.button(
        label="➩ Kirim Strategi ke Wizard",
        style=discord.ButtonStyle.blurple,
        custom_id="kirim_wizard_embed",
        row=4
    )
    async def kirim_wizard_embed(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(WizardEmbedModal())

    # ------------------------------------------------------
    # 🔄 Tombol: Setting Up Ulang
    # ------------------------------------------------------
    @discord.ui.button(
        label="🔄 Setting Up Ulang",
        style=discord.ButtonStyle.danger,
        custom_id="admin_setup_ulang",
        row=4
    )
    async def setup_ulang_server(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ConfirmSetupUlangView()
        await interaction.response.send_message(
            "⚠️ **PERINGATAN KRITIS:** Apakah Anda yakin ingin melakukan Setting Up Ulang?\n"
            "Tindakan ini akan menghapus dan membuat ulang seluruh kategori, channel, dan izin di server ini! "
            "Proses ini **tidak dapat dibatalkan** setelah dimulai.",
            view=view,
            ephemeral=True
        )

    # ------------------------------------------------------
    # 🫂 Tombol: Toggle Donasi
    # ------------------------------------------------------
    @discord.ui.button(
        label="🫂 Toggle Tombol Donasi",
        style=discord.ButtonStyle.success,
        custom_id="admin_toggle_donation",
        row=4
    )
    async def toggle_donation(self, interaction: discord.Interaction, button: discord.ui.Button):
        global DONATION_ACTIVE
        DONATION_ACTIVE = not DONATION_ACTIVE
        await Database.set_setting("donation_button_active", str(DONATION_ACTIVE))

        status_str = "AKTIF" if DONATION_ACTIVE else "NONAKTIF"
        await interaction.response.send_message(
            f"✅ Tombol Donasi di channel verifikasi sekarang **{status_str}**!\n"
            f"Memulai proses pembaruan channel verifikasi...",
            ephemeral=True
        )

        # Otomatis perbarui channel verifikasi
        verif_channel = discord.utils.get(interaction.guild.text_channels, name="verifikasi")
        if verif_channel:
            try:
                await VerificationSystem.update_verification_channel(verif_channel)
            except Exception as e:
                logging.error(f"Gagal update channel verifikasi saat toggle donasi: {e}")

# ==========================================================
# 💾 EXPORT DATA VIEW (DENGAN FITUR ZIP SEMUA DATA)
# ==========================================================
import csv, os, zipfile
from datetime import datetime

class ExportDataSelectView(discord.ui.View):
    """View interaktif untuk mengekspor data dari tabel database ke file CSV"""

    def __init__(self):
        super().__init__(timeout=90)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        is_admin = any(r.name == "Admin" for r in interaction.user.roles) or interaction.user.guild_permissions.administrator
        if not is_admin:
            await interaction.response.send_message("✘ Akses Ditolak!", ephemeral=True)
            return False
        return True

    # ------------------------------------------------------
    # 📂 PILIHAN TABEL UNTUK DIEKSPOR
    # ------------------------------------------------------
    @discord.ui.select(
        placeholder="📂 Pilih tabel yang ingin diekspor ke file CSV...",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="users", description="Data pengguna terdaftar"),
            discord.SelectOption(label="spam", description="Riwayat pelanggaran spam"),
            discord.SelectOption(label="violations", description="Catatan pelanggaran pengguna"),
            discord.SelectOption(label="threads", description="Data thread diskusi (jika ada)"),
            discord.SelectOption(label="introductions", description="Data perkenalan diri (jika ada)"),
            discord.SelectOption(label="📦 Ekspor Semua", description="Ekspor semua tabel ke dalam satu file ZIP")
        ]
    )
    async def pilih_tabel(self, interaction: discord.Interaction, select: discord.ui.Select):
        table = select.values[0]
        await interaction.response.defer(ephemeral=True, thinking=True)

        if table == "📦 Ekspor Semua":
            await self.export_all_tables(interaction)
        else:
            await self.export_single_table(interaction, table)

    # ------------------------------------------------------
    # 📑 EKSPOR SATU TABEL KE CSV
    # ------------------------------------------------------
    async def export_single_table(self, interaction: discord.Interaction, table: str):
        try:
            async with aiosqlite.connect(Database.DB_PATH) as db:
                cursor = await db.execute(f"SELECT * FROM {table}")
                rows = await cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

            if not rows:
                await interaction.followup.send(f"⚠️ Tidak ada data di tabel `{table}` untuk diekspor.", ephemeral=True)
                return

            # Buat folder exports jika belum ada
            os.makedirs("exports", exist_ok=True)
            file_path = os.path.join("exports", f"{table}_export.csv")

            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(columns)
                writer.writerows(rows)

            embed = discord.Embed(
                title="⬈ Ekspor Data Berhasil",
                description=f"📁 Tabel `{table}` telah berhasil diekspor ke file CSV.",
                color=discord.Color(COLOR_GREEN),
                timestamp=datetime.now()
            )
            embed.set_footer(text=f"Dieksekusi oleh {interaction.user.display_name}")

            await interaction.followup.send(
                embed=embed,
                file=discord.File(file_path),
                ephemeral=True
            )

            logging.info(f"[EXPORT] {interaction.user} mengekspor tabel '{table}'")

        except aiosqlite.Error as e:
            await interaction.followup.send(
                f"❌ Kesalahan database saat mengekspor `{table}`:\n```{str(e)}```",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"🚨 Gagal mengekspor tabel `{table}`:\n```{str(e)}```",
                ephemeral=True
            )
            logging.error(f"Kesalahan export_single_table: {e}", exc_info=True)

    # ------------------------------------------------------
    # 🗃️ EKSPOR SEMUA TABEL KE ZIP
    # ------------------------------------------------------
    async def export_all_tables(self, interaction: discord.Interaction):
        tables = ["users", "spam", "violations", "threads", "introductions"]
        export_dir = "exports"
        os.makedirs(export_dir, exist_ok=True)

        csv_files = []
        exported_count = 0

        for table in tables:
            try:
                async with aiosqlite.connect(Database.DB_PATH) as db:
                    cursor = await db.execute(f"SELECT * FROM {table}")
                    rows = await cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]

                if not rows:
                    continue

                csv_path = os.path.join(export_dir, f"{table}_export.csv")
                with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(columns)
                    writer.writerows(rows)
                csv_files.append(csv_path)
                exported_count += 1
            except Exception as e:
                logging.warning(f"Gagal ekspor tabel {table}: {e}")

        if not csv_files:
            await interaction.followup.send("⚠️ Tidak ada data dari tabel apa pun untuk diekspor.", ephemeral=True)
            return

        # Buat file ZIP dari semua CSV
        zip_path = os.path.join(export_dir, f"database_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for csv_file in csv_files:
                zipf.write(csv_file, os.path.basename(csv_file))

        embed = discord.Embed(
            title="📦 Ekspor Semua Data Berhasil",
            description=f"✅ {exported_count} tabel berhasil diekspor ke dalam satu file ZIP.",
            color=discord.Color(COLOR_CYAN),
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"Dieksekusi oleh {interaction.user.display_name}")

        await interaction.followup.send(embed=embed, file=discord.File(zip_path), ephemeral=True)

        logging.info(f"[EXPORT ALL] {interaction.user} mengekspor seluruh data ke ZIP")
        

class ConfirmHapusThreadView(View):
    def __init__(self):
        super().__init__(timeout=30)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        is_admin = any(r.name == "Admin" for r in interaction.user.roles) or interaction.user.guild_permissions.administrator
        if not is_admin:
            await interaction.response.send_message("✘ Akses Ditolak!", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="✅ Ya, Hapus Thread Usang", style=discord.ButtonStyle.danger)
    async def konfirmasi_hapus(self, interaction: discord.Interaction, button: discord.ui.Button):
        await hapus_thread_usang(interaction, hari=7)

    @discord.ui.button(label="❌ Batal", style=discord.ButtonStyle.secondary)
    async def batal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Dibatalkan ❎", ephemeral=True)
        await interaction.message.delete()

class ConfirmSetupUlangView(View):
    def __init__(self):
        super().__init__(timeout=60)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        is_admin = any(r.name == "Admin" for r in interaction.user.roles) or interaction.user.guild_permissions.administrator
        if not is_admin:
            await interaction.response.send_message("✘ Akses Ditolak!", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="✅ Ya, Setting Up Ulang Server", style=discord.ButtonStyle.danger)
    async def konfirmasi_setup(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True, thinking=True)

        admin = interaction.user
        guild = interaction.guild
        start_time = datetime.now(jakarta_tz)
        errors = []

        async def safe_update(content: str, critical=False):
            sent = False
            try:
                msg = f"🚨 {content}" if critical else f"ℹ️ {content}"
                await interaction.followup.send(msg, ephemeral=True)
                sent = True
            except Exception:
                pass

            try:
                msg = f"🚨 {content}" if critical else f"ℹ️ {content}"
                await admin.send(msg)
                sent = True
            except Exception:
                pass

            try:
                laporan_ch = discord.utils.get(guild.text_channels, name="laporan")
                if laporan_ch:
                    msg = f"🚨 {content}" if critical else f"ℹ️ {content}"
                    await laporan_ch.send(msg)
                    sent = True
            except Exception:
                pass

            return sent

        await safe_update("🏗️ **Memulai setup server...** (`Proses bisa memakan waktu ±3 menit`)")

        current_step = ""
        try:
            # Step 1: Inisialisasi server
            current_step = "Setup struktur server"
            await safe_update("🛠️ Memulai inisialisasi struktur server...")
            try:
                server_result = await asyncio.wait_for(
                    ServerBuilder.setup_server(guild),
                    timeout=300
                )
                await safe_update(f"✅ Struktur server selesai!")
            except asyncio.TimeoutError:
                await safe_update("⚠️ Waktu setup server habis! Lanjut ke penerapan izin...", True)

            # Step 2: Terapkan izin channel
            current_step = "Penerapan izin channel"
            await safe_update("🔐 Menerapkan izin channel...")
            success_count, error_count, permission_errors = await apply_channel_permissions(guild)
            if permission_errors:
                errors.extend(permission_errors)

            # Step 3: Sinkronisasi database
            current_step = "Sinkronisasi user & role"
            await safe_update("🔄 Memulai sinkronisasi user dan role...")
            sync_report = await synchronize_users_and_roles(guild)

            # Step 4: Kirim konten ke roadmap_trader
            current_step = "Pengiriman roadmap trader"
            await safe_update("📝 Mengirim konten ke channel roadmap_trader...")
            roadmap_channel = discord.utils.get(guild.text_channels, name="roadmap_trader")
            if not roadmap_channel:
                await safe_update("⚠️ Channel #roadmap_trader tidak ditemukan, membuat secara manual...", True)
                nexus_category = discord.utils.get(guild.categories, name="🔥|NEXUS HUB|") or await guild.create_category("🔥|NEXUS HUB|")
                roadmap_channel = await guild.create_text_channel(
                    name="roadmap_trader",
                    category=nexus_category,
                    topic="Perjalanan seorang trader yang berkelanjutan",
                    position=3,
                    overwrites={
                        guild.default_role: discord.PermissionOverwrite(read_messages=True)
                    }
                )

            try:
                await send_roadmap_trader(roadmap_channel)
                await safe_update("✅ Konten roadmap trader berhasil dikirim!")
            except Exception as e:
                errors.append(f"Gagal kirim roadmap: {str(e)}")
                await safe_update(f"⚠️ Gagal kirim roadmap: {str(e)}", True)

            # Step 5: Setup thread analisis (opsional)
            try:
                current_step = "Setup thread analisis"
                channel = discord.utils.get(guild.text_channels, name="wizard-analisis")
                if channel:
                    created_threads = await create_analysis_threads(channel)
                    if created_threads:
                        await safe_update(f"✅ Thread Wizard Analisis dibuat: {', '.join(created_threads)}")
                        await sync_members_to_threads(guild)
            except Exception as e:
                errors.append(f"Gagal setup thread: {str(e)}")
                await safe_update(f"⚠️ Gagal setup thread: {str(e)}", True)

            duration = (datetime.now(jakarta_tz) - start_time).total_seconds()
            await safe_update(f"🟢 Semua proses setup selesai! Durasi: {duration:.1f} detik")

        except Exception as step_error:
            error_msg = f"🔥 **GAGAL** pada langkah `{current_step}`: {str(step_error)}"
            errors.append(error_msg)
            await safe_update(error_msg, True)

    @discord.ui.button(label="❌ Batal", style=discord.ButtonStyle.secondary)
    async def batal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("❌ Aksi setup ulang dibatalkan. Struktur server tetap aman.", ephemeral=True)
        try:
            await interaction.message.delete()
        except Exception:
            pass


class DeleteDatabaseView(discord.ui.View):
    """View untuk menghapus tabel database dengan konfirmasi"""
    def __init__(self):
        super().__init__(timeout=120)
        self.selected_table = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        is_admin = any(r.name == "Admin" for r in interaction.user.roles) or interaction.user.guild_permissions.administrator
        if not is_admin:
            await interaction.response.send_message("✘ Akses Ditolak!", ephemeral=True)
            return False
        return True

    @discord.ui.select(
        placeholder="✘ Pilih Data untuk Dihapus",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Data Pengguna",
                value="users",
                description="Hapus semua data pengguna"
            ),
            discord.SelectOption(
                label="Data Spam",
                value="spam",
                description="Hapus semua rekaman spam"
            ),
            discord.SelectOption(
                label="Data Pelanggaran",
                value="violations",
                description="Hapus semua pelanggaran"
            ),
            discord.SelectOption(
                label="Threads Diskusi",
                value="threads",
                description="Hapus semua data thread diskusi"
            ),
            discord.SelectOption(
                label="Perkenalan Diri",
                value="introductions",
                description="Hapus semua data perkenalan diri"
            )
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        # Cek role admin
        if not any(role.name.lower() == "admin" for role in interaction.user.roles):
            await interaction.response.send_message("🚫 Hanya Admin yang dapat menghapus data.", ephemeral=True)
            return

        self.selected_table = select.values[0]
        await interaction.response.send_modal(DeleteConfirmModal(self.selected_table))
        
# ===================== MODAL =====================
#---obrolanview
class ThreadTaggingModal(Modal, title="🔔 Tag Anggota dalam Thread"):
    targets = TextInput(
        label="Role/User yang Ditag (pisahkan koma)",
        placeholder="Contoh: @Admin, @WizardMemberTahunan,@WizardMemberTahunan, @Username",
        required=True
    )
    
    message = TextInput(
        label="Pesan Notifikasi",
        placeholder="Pesan untuk anggota yang ditag",
        style=discord.TextStyle.paragraph,
        required=True
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        thread = interaction.channel
        if not isinstance(thread, discord.Thread):
            await interaction.response.send_message("❌ Hanya bisa di thread!", ephemeral=True)
            return
            
        creator_id = await get_thread_creator_id(thread)
        is_creator = (creator_id == interaction.user.id)
        admin_role = discord.utils.get(interaction.guild.roles, name="Admin")
        is_admin = (admin_role in interaction.user.roles) if admin_role else False
        is_admin = is_admin or interaction.user.guild_permissions.administrator
        if not (is_creator or is_admin):
            await interaction.response.send_message("❌ Hanya pembuat thread atau Admin yang bisa menggunakan fitur tag anggota!", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        
        # Daftar role yang diizinkan
        ALLOWED_ROLES = {"Member", "WizardMemberBulanan","WizardMemberTahunan", "Admin"}
        
        target_names = [t.strip() for t in self.targets.value.split(",")]
        tagged_mentions = []
        valid_targets = []
        
        for target in target_names:
            # Cek role
            role_obj = discord.utils.get(interaction.guild.roles, name=target.replace('@', ''))
            if role_obj and role_obj.name in ALLOWED_ROLES:
                tagged_mentions.append(role_obj.mention)
                valid_targets.append(f"Role: {role_obj.name}")
                continue
                
            # Cek user
            user_obj = None
            if target.startswith('@'):
                user_obj = discord.utils.get(interaction.guild.members, name=target[1:])
            else:
                parts = target.split('#')
                if len(parts) == 2 and parts[1].isdigit():
                    user_obj = discord.utils.get(interaction.guild.members, name=parts[0], discriminator=parts[1])
                else:
                    user_obj = discord.utils.get(interaction.guild.members, display_name=target) or \
                             discord.utils.get(interaction.guild.members, name=target)
            
            # Verifikasi user memiliki role yang diizinkan
            if user_obj:
                user_roles = {role.name for role in user_obj.roles}
                if user_roles & ALLOWED_ROLES:  # Cek apakah user memiliki minimal 1 role yang diizinkan
                    tagged_mentions.append(user_obj.mention)
                    valid_targets.append(f"User: {user_obj.display_name} (Role: {', '.join(user_roles & ALLOWED_ROLES)})")
                else:
                    continue  # Skip user yang tidak memiliki role yang diizinkan
        
        if not tagged_mentions:
            await interaction.followup.send("❌ Tidak ada role/user yang valid! Pastikan target memiliki role Member, WizardMember, atau Admin.", ephemeral=True)
            return
            
        # Buat embed notifikasi
        embed = discord.Embed(
            title="🔔 NOTIFIKASI THREAD",
            description=self.message.value,
            color=0xffd700
        )
        embed.add_field(
            name="Thread",
            value=f"[{thread.name}]({thread.jump_url})",
            inline=False
        )
        embed.set_author(
            name=f"Tag oleh {interaction.user.display_name}",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else None
        )
        
        # Kirim tag di thread
        tag_message = await thread.send(
            content=" ".join(tagged_mentions),
            embed=embed
        )
        
        await interaction.followup.send(
            f"✅ Anggota berhasil ditag!",
            ephemeral=True
        )
        
        # Catat action
        await send_laporan_embed(
            bot,
            judul="🔔 PENGGUNAAN TAG THREAD",
            deskripsi=f"Thread #{thread.name} ditag oleh {interaction.user.mention}",
            fields=[
                ("Target Ditag", "\n".join(valid_targets)),
                ("Pesan", self.message.value[:200] + "..." if len(self.message.value) > 200 else self.message.value),
                ("Thread", f"[Link Thread]({thread.jump_url})")
            ],
            warna=0xffd700
        )

class PerkenalanModal(Modal, title="🏆 PERKENALAN DIRI MountAlgo 🚀"):
    nama = TextInput(
        label="Nama Lengkap/Panggilan",
        placeholder="Contoh: Andre Wijaya",
        max_length=50,
        required=True
    )
    alamat = TextInput(
        label="📍 Domisili",
        placeholder="Kota & Negara (Contoh: Jakarta, Indonesia)",
        max_length=100,
        required=True
    )
    pengalaman_tahun = TextInput(
        label="📈 Pengalaman Trading",
        placeholder="Angka tahun (Contoh: 2)",
        max_length=2,
        required=True
    )
    trading_style = TextInput(
        label="🔄 Trading Style",
        placeholder="Scalping/Swing/Intraday/Position Trading",
        max_length=50,
        required=False
    )
    tujuan = TextInput(
        label="🎯 Tujuan Bergabung",
        placeholder="Jelaskan secara singkat (maks 300 karakter)",
        style=discord.TextStyle.paragraph,
        max_length=300,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            # ================ BUAT THREAD ================
            general_channel = discord.utils.get(interaction.guild.text_channels, name="lounge-chat")
            if not general_channel:
                return await interaction.followup.send("❌ Channel #lounge-chat tidak ditemukan!", ephemeral=True)

            timestamp = datetime.now().strftime("%d %b %Y")
            thread = await general_channel.create_thread(
                name=f"📢  | {self.nama.value} │ {timestamp}",
                auto_archive_duration=1440,
                reason=f"Perkenalan: {self.nama.value}"
            )

            # ================ AUTO-JOIN ================
            await thread.add_user(interaction.user)
            target_roles = ["Member", "WizardMemberBulanan","WizardMemberTahunan", "Admin"]
            for role_name in target_roles:
                role = discord.utils.get(interaction.guild.roles, name=role_name)
                if role:
                    for member in role.members:
                        try:
                            await thread.add_user(member)
                        except:
                            continue

            # ================ FORMAT PENGALAMAN ================
            pengalaman = self.pengalaman_tahun.value.strip()
            if not pengalaman.isdigit():
                pengalaman_text = "🔹 Pemula"
            else:
                years = int(pengalaman)
                if years == 0:
                    pengalaman_text = "🔹 Pemula"
                elif years < 3:
                    pengalaman_text = f"🔸 {years} tahun (Intermediate)"
                else:
                    pengalaman_text = f"💎 {years}+ tahun (Expert)"

            # ================ EMBED YANG SUDAH DIPERBAIKI ================
            embed = discord.Embed(
                title=f"🌟 SELAMAT DATANG DI MountAlgo! 🌟",
                description=f"**{self.nama.value.upper()}** telah bergabung dengan komunitas kami!",
                color=discord.Color.gold(),
                timestamp=interaction.created_at
            )
            
            # Header Section
            embed.set_author(
                name="MountAlgo TRADING COMMUNITY",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            
            # Profile Section - Fixed f-string formatting
            embed.add_field(
                name="📌 **PROFIL ANGGOTA**",
                value=(
                    f"• **Nama**: {self.nama.value}\n"
                    f"• **Domisili**: {self.alamat.value}\n"
                    f"• **Pengalaman Trading**: {pengalaman_text}\n"
                    f"• **Trading Style**: {self.trading_style.value if self.trading_style.value else 'Belum ditentukan'}\n"
                ),
                inline=False
            )
            
            # Goals Section
            embed.add_field(
                name="🎯 **TUJUAN BERGANUNG**",
                value=self.tujuan.value,
                inline=False
            )
            
            # Guide Section
            guide_items = [
                "Perkenalkan diri lebih detail di thread ini",
                "Jelaskan pair/instrumen favorit Anda",
                "Bagikan pengalaman trading Anda",
                "Tanyakan apa yang ingin Anda ketahui",
                "Jangan lupa baca rules di setiap channel"
            ]
            
            embed.add_field(
                name="📚 **PANDUAN UNTUK ANDA**",
                value="\n".join(f"{i+1}. {item}" for i, item in enumerate(guide_items)),
                inline=False
            )
            
            # Footer
            embed.set_footer(
                text=f"MountAlgo Community • Bergabung pada {timestamp}"
            )

            # ================ KIRIM EMBED ================
            welcome_msg = await thread.send(
                content=f"👋 **Halo Member MountAlgo!** Sambut hangat {interaction.user.mention} yuk! 🎉",
                embed=embed
            )
            await welcome_msg.pin()

            # ================ TAMBAH REAKSI ================
            for emoji in ["👋", "🎉", "📈", "❤️", "🤝"]:
                await welcome_msg.add_reaction(emoji)

            # ================ KONFIRMASI KE USER ================
            await interaction.followup.send(
                embed=discord.Embed(
                    title="✅ PERKENALAN BERHASIL DIBUAT",
                    description=f"Thread perkenalan Anda sudah aktif!\n{thread.mention}\n\n"
                                 "**Tips:** \n"
                                 "- Gunakan thread untuk berinteraksi\n"
                                 "- Jelaskan trading style Anda\n"
                                 "- Jangan lupa baca rules!\n",
                    color=discord.Color(COLOR_GREEN)
                ),
                ephemeral=True
            )

        except Exception as e:
            logging.error(f"Error: {str(e)}", exc_info=True)
            await interaction.followup.send(
                embed=discord.Embed(
                    title="❌ GAGAL MEMBUAT PERKENALAN",
                    description=f"```{str(e)[:200]}```\n\nSilakan coba lagi atau hubungi Admin.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )

async def safe_respond(interaction: discord.Interaction, 
                       content: str, 
                       ephemeral: bool = False,
                       **kwargs) -> bool:
    """
    Handle response safely with fallback to DM.
    Returns True if succeeded, False if failed.
    """
    try:
        if interaction.response.is_done():
            await interaction.followup.send(content, ephemeral=ephemeral, **kwargs)
        else:
            await interaction.response.send_message(content, ephemeral=ephemeral, **kwargs)
        return True
    except discord.NotFound:
        try:
            await interaction.user.send(content)
            return True
        except discord.Forbidden:
            logging.warning(f"Tidak bisa mengirim DM ke {interaction.user.id}")
            return False
    except discord.Forbidden:
        logging.error(f"Dilarang mengirim respon di channel {interaction.channel.id}")
        return False
    except Exception as e:
        logging.error(f"Error di safe_respond: {str(e)}")
        return False

# ===================== MODAL DENGAN INPUT SIMBOL =====================
class DiskusiModal(Modal, title="📝 Buat Diskusi Baru"):
    topic = TextInput(
        label="Topik Diskusi",
        placeholder="Masukkan topik diskusi utama...",
        max_length=100,
        required=True
    )
    
    symbol = TextInput(
        label="Simbol (Opsional)",
        placeholder="Contoh: ⭐, 🔥, 💬",
        max_length=5,
        required=False
    )
    
    description = TextInput(
        label="Detail Diskusi",
        placeholder="Jelaskan poin utama yang ingin didiskusikan...",
        style=discord.TextStyle.paragraph,
        max_length=500,
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Format nama thread dengan emoji
            emoji = self.symbol.value.strip()[:1] if self.symbol.value.strip() else "💬"
            thread_name = f"{emoji}｜{self.topic.value[:95]}"
            
            # Buat thread baru
            channel = interaction.channel
            thread = await channel.create_thread(
                name=thread_name,
                auto_archive_duration=1440,
                reason=f"Diskusi baru oleh {interaction.user.display_name}"
            )
            
            # Auto-join pembuat thread
            await thread.add_user(interaction.user)
            
            # Buat embed untuk pesan pembuka
            embed = discord.Embed(
                title=f"🚀 DISKUSI BARU: {self.topic.value}",
                color=discord.Color(COLOR_CYAN)
            )
            
            embed.add_field(
                name="Diprakarsai oleh",
                value=interaction.user.mention,
                inline=False
            )
            
            if self.description.value:
                embed.add_field(
                    name="Deskripsi Diskusi",
                    value=self.description.value,
                    inline=False
                )
                
            embed.add_field(
                name="💡 Panduan Diskusi",
                value=(
                    "• Berargumen dengan data/faktual\n"
                    "• Hormati pendapat berbeda\n"
                    "• Tetap on-topik\n"
                    "• Gunakan reaksi untuk mengekspresikan pendapat"
                ),
                inline=False
            )
            
            embed.set_footer(text="Gunakan tombol di bawah untuk mengelola thread")
            
            # Kirim pesan embed dengan view management
            msg = await thread.send(
                embed=embed,
                view=ThreadManagementView()
            )
            
            # Tambahkan 21 reaksi berbeda
            reaction_emojis = [
                "👍", "👎", "❤️", "🔥", "🎉", "🤔", "😄",
                "😲", "😢", "😠", "👀", "🧠", "💬", "📌",
                "❓", "✅", "❌", "⭐", "🔄", "📢", "💡"
            ]
            
            for emoji in reaction_emojis:
                try:
                    await msg.add_reaction(emoji)
                except Exception as e:
                    logging.warning(f"Gagal menambahkan reaksi {emoji}: {str(e)}")
                    continue
            
            # Konfirmasi ke user
            await interaction.followup.send(
                f"✅ Thread berhasil dibuat: {thread.mention}\n"
                f"Anda telah otomatis bergabung ke thread ini.",
                ephemeral=True
            )
            
            # Pin thread jika mengandung kata "penting"
            if "penting" in self.topic.value.lower():
                await thread.edit(pinned=True)
            
        except Exception as e:
            await interaction.followup.send(
                f"❌ Gagal membuat thread: {str(e)}",
                ephemeral=True
            )
            logging.error(f"Error buat diskusi: {str(e)}")


# --- Tambah User ---
class AddUserModal(discord.ui.Modal, title="⬈ Tambah Pengguna"):
    user_id = discord.ui.TextInput(
        label="ID Pengguna",
        placeholder="Masukkan ID pengguna (angka)",
        required=True,
        max_length=20
    )
    username = discord.ui.TextInput(
        label="Nama Pengguna",
        placeholder="Nama pengguna Discord",
        required=True,
        max_length=32
    )
    status = discord.ui.TextInput(
        label="Status",
        placeholder="Member / WizardMemberBulanan / WizardMemberTahunan / Admin",
        required=True,
        max_length=25
    )
    expiry_date = discord.ui.TextInput(
        label="Tanggal Kedaluwarsa",
        placeholder="YYYY-MM-DD (kosongkan untuk otomatis)",
        required=False,
        max_length=10
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            user_id = int(self.user_id.value)
            username = self.username.value.strip()
            status_val = self.status.value.strip()
            expiry = self.expiry_date.value.strip() if self.expiry_date.value else ""

            valid_statuses = ["Member", "WizardMemberBulanan", "WizardMemberTahunan", "Admin"]
            if status_val not in valid_statuses:
                await interaction.response.send_message(
                    f"✘ Status tidak valid! Pilih salah satu dari: {', '.join(valid_statuses)}",
                    ephemeral=True
                )
                return

            # 🔍 Cek apakah user sudah terdaftar di database
            existing_user = await Database.get_user_data(user_id)
            if existing_user:
                existing_status = existing_user[2]
                # Jika user sudah punya status aktif, tolak pendaftaran baru
                if existing_status in ["Member", "Admin", "WizardMemberBulanan", "WizardMemberTahunan"]:
                    await interaction.response.send_message(
                        f"⚠️ **Pengguna sudah terdaftar!**\n"
                        f"👤 **Nama:** {existing_user[1]}\n"
                        f"🏷️ **Status Sekarang:** {existing_status}\n\n"
                        f"Anda tidak bisa menambahkan ulang pengguna yang sudah memiliki status aktif.",
                        ephemeral=True
                    )
                    return

            # 🕒 Hitung tanggal kedaluwarsa otomatis jika tidak diisi
            if status_val in ["WizardMemberBulanan", "WizardMemberTahunan"]:
                today = datetime.utcnow().date()
                days = 30 if status_val == "WizardMemberBulanan" else 365
                expiry = expiry or (today + timedelta(days=days)).isoformat()

            # 💾 Tambahkan ke database
            await Database.add_user(
                user_id=user_id,
                username=username,
                status=status_val,
                subscription_type=(
                    "Bulanan" if "Bulanan" in status_val
                    else "Tahunan" if "Tahunan" in status_val
                    else None
                ),
                expiry_date=expiry
            )

            # 🎭 Terapkan role ke member di server (jika ada) secara paksa
            member = interaction.guild.get_member(user_id)
            if member:
                await apply_user_roles(member, status_val)

            # ✅ Kirim notifikasi sukses ke admin
            message = (
                f"✅ **Pengguna berhasil ditambahkan!**\n"
                f"👤 **Nama:** {username}\n"
                f"🆔 **ID:** `{user_id}`\n"
                f"🏷️ **Status:** {status_val}\n"
            )
            if expiry:
                message += f"⏳ **Kedaluwarsa:** {expiry}\n"

            await interaction.response.send_message(message, ephemeral=True)

            # 📩 Kirim DM ke user jika memungkinkan
            if member:
                try:
                    dm_msg = (
                        f"👋 Hai {member.display_name},\n"
                        f"Akun Anda telah didaftarkan sebagai **{status_val}** di {interaction.guild.name}."
                    )
                    if expiry:
                        dm_msg += f"\nLangganan berlaku hingga **{expiry}**."
                    await member.send(dm_msg)
                except discord.Forbidden:
                    logging.warning(f"Tidak bisa kirim DM ke {member.display_name}")

        except ValueError:
            await interaction.response.send_message("✘ ID Pengguna harus berupa angka!", ephemeral=True)
        except Exception as e:
            logging.error(f"Kesalahan AddUserModal: {e}", exc_info=True)
            await interaction.response.send_message(
                f"⚠️ Terjadi kesalahan sistem: {e}",
                ephemeral=True
            )

# --- Hapus User dengan Verifikasi ---
class RemoveUserModal(Modal, title="🗑️ Hapus User (Verifikasi Diperlukan)"):
    user_id = TextInput(
        label="User ID",
        placeholder="Masukkan User ID (angka)",
        required=True,
        max_length=20
    )
    confirm_text = TextInput(
        label="Ketik 'HAPUS SEKARANG' untuk konfirmasi",
        placeholder="Ketik persis: HAPUS SEKARANG",
        required=True,
        max_length=20
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            # 🔒 Verifikasi input teks konfirmasi
            if self.confirm_text.value.strip().upper() != "HAPUS SEKARANG":
                await interaction.response.send_message(
                    "❌ Aksi dibatalkan — Anda harus mengetik **HAPUS SEKARANG** untuk mengonfirmasi.",
                    ephemeral=True
                )
                return

            user_id = int(self.user_id.value)

            # 🔍 Ambil data user dari database
            async with aiosqlite.connect(Database.DB_PATH) as db:
                async with db.execute("SELECT username FROM users WHERE user_id = ?", (user_id,)) as cursor:
                    user_data = await cursor.fetchone()
            
            if not user_data:
                await interaction.response.send_message("🚫 User tidak ditemukan dalam database.", ephemeral=True)
                return

            guild = interaction.guild
            member = guild.get_member(user_id)

            # 🔎 Jika user tidak ditemukan di server
            if not member:
                await Database.remove_user(user_id)
                await interaction.response.send_message(
                    "ℹ️ User tidak ditemukan di server, tetapi telah dihapus dari database.",
                    ephemeral=True
                )
                return

            # 📋 Simpan roles sebelum dihapus
            role_names = [role.name for role in member.roles if role.name != "@everyone"]

            try:
                # 🔧 Hapus role & kick dari server
                await member.remove_roles(*member.roles[1:])
                await member.kick(reason=f"Dihapus oleh admin {interaction.user.name}")
                await Database.remove_user(user_id)

                success_message = (
                    f"✅ **User berhasil dihapus!**\n"
                    f"👤 **Nama:** {member.display_name} (`{member.id}`)\n"
                    f"🎭 **Roles Dicabut:** {', '.join(role_names) or '-'}"
                )
                await interaction.response.send_message(success_message, ephemeral=True)

                # 🧾 Kirim laporan ke channel admin
                await send_laporan_embed(
                    bot,
                    judul="🗑️ USER DIHAPUS",
                    deskripsi=f"User dihapus oleh {interaction.user.mention}",
                    fields=[
                        ("User", f"{member.display_name} ({member.id})"),
                        ("Admin", interaction.user.display_name),
                        ("Roles Dicabut", ', '.join(role_names) or "Tidak ada"),
                        ("Waktu", format_wib(to_wib(get_utc_now())))
                    ],
                    warna=0xe74c3c,
                    thumbnail=interaction.guild.me.display_avatar.url
                )

            except discord.Forbidden:
                await interaction.response.send_message("🚫 Bot tidak memiliki izin untuk menghapus user!", ephemeral=True)
            except Exception as e:
                logging.error(f"Error deleting user: {str(e)}")
                await interaction.response.send_message(f"❌ Terjadi kesalahan saat menghapus user: {str(e)}", ephemeral=True)

        except ValueError:
            await interaction.response.send_message("🚫 ID harus berupa angka!", ephemeral=True)
        except Exception as e:
            logging.error(f"Error in RemoveUserModal: {str(e)}", exc_info=True)
            await interaction.response.send_message(f"❌ Terjadi kesalahan sistem: {str(e)}", ephemeral=True)
            
            
# --- Upgrade User ke WizardMember (Bulanan/Tahunan) ---
class UpgradeUserModal(discord.ui.Modal, title="⤴️ Upgrade Pengguna ke WizardMember"):
    user_id = discord.ui.TextInput(
        label="ID Pengguna",
        placeholder="Masukkan ID Discord pengguna (angka)",
        required=True,
        max_length=20
    )
    subscription_type = discord.ui.TextInput(
        label="Tipe Langganan",
        placeholder="Bulanan / Tahunan",
        required=True,
        max_length=15
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            user_id = int(self.user_id.value)
            sub_type = self.subscription_type.value.strip().capitalize()

            if sub_type not in ["Bulanan", "Tahunan"]:
                await interaction.response.send_message(
                    "❌ Tipe langganan tidak valid! Pilih: `Bulanan` atau `Tahunan`.",
                    ephemeral=True
                )
                return

            member = interaction.guild.get_member(user_id)
            if not member:
                await interaction.response.send_message(
                    "⚠️ Pengguna tidak ditemukan di server!",
                    ephemeral=True
                )
                return

            # Tentukan role & masa berlaku berdasarkan tipe langganan
            if sub_type == "Bulanan":
                role_name = "WizardMemberBulanan"
                days = 30
                status = "WizardMemberBulanan"
            else:
                role_name = "WizardMemberTahunan"
                days = 365
                status = "WizardMemberTahunan"

            # Terapkan role secara paksa sesuai dengan pilihan tombol
            await apply_user_roles(member, status)

            # Hitung expiry date otomatis
            expiry = (datetime.utcnow() + timedelta(days=days)).isoformat()

            # Update database status
            await Database.update_user_status(
                user_id=user_id,
                status=status,
                subscription_type=sub_type.lower(),
                expiry_date=expiry
            )

            # Kirim notifikasi ke admin (via embed)
            embed = discord.Embed(
                title="✅ Upgrade Pengguna Berhasil",
                description=(
                    f"👤 **User:** {member.mention}\n"
                    f"🆔 **ID:** `{user_id}`\n"
                    f"🏷️ **Status Baru:** {status}\n"
                    f"📅 **Masa Berlaku:** {expiry.split('T')[0]}\n"
                ),
                color=discord.Color.gold() if sub_type == "Bulanan" else discord.Color(COLOR_VIOLET)
            )
            embed.set_footer(text="MountAlgo Membership System")
            await interaction.response.send_message(embed=embed, ephemeral=True)

            # Kirim DM ke user
            try:
                dm_embed = discord.Embed(
                    title="🎉 Upgrade Berhasil!",
                    description=(
                        f"Halo {member.display_name},\n\n"
                        f"Selamat! Anda telah diupgrade menjadi **{role_name}** di server **{interaction.guild.name}**.\n\n"
                        f"🗓️ Berlaku hingga: **{expiry.split('T')[0]}**\n"
                        f"🔑 Nikmati akses penuh ke:\n"
                        f"• 💎 Sinyal Premium\n"
                        f"• 📊 Dashboard Sinyal\n"
                        f"• 🧠 Wizard Analisis\n\n"
                        f"Terima kasih telah menjadi bagian dari **MountAlgo Premium Member**!"
                    ),
                    color=discord.Color.gold() if sub_type == "Bulanan" else discord.Color(COLOR_VIOLET)
                )
                await member.send(embed=dm_embed)
            except discord.Forbidden:
                logging.warning(f"Tidak dapat mengirim DM ke {member.display_name} (DM tertutup).")
            except Exception as e:
                logging.error(f"Gagal mengirim DM upgrade ke {member.display_name}: {e}")

            logging.info(
                f"User {member.display_name} (ID: {user_id}) berhasil diupgrade ke {status} sampai {expiry}"
            )

        except ValueError:
            await interaction.response.send_message(
                "⚠️ ID pengguna harus berupa angka!",
                ephemeral=True
            )
        except Exception as e:
            logging.error(f"Kesalahan UpgradeUserModal: {e}", exc_info=True)
            await interaction.response.send_message(
                f"❌ Terjadi kesalahan sistem: {e}",
                ephemeral=True
            )
            
class DeleteConfirmModal(Modal, title="🧨 KONFIRMASI PENGHAPUSAN DATA"):
    def __init__(self, table_name: str):
        super().__init__()
        self.table_name = table_name
        self.konfirmasi = TextInput(
            label=f"Ketik 'HAPUS {table_name.upper()}' untuk konfirmasi",
            placeholder=f"HAPUS {table_name.upper()}",
            required=True,
            max_length=25
        )
        self.add_item(self.konfirmasi)

    async def on_submit(self, interaction: discord.Interaction):
        confirm_text = f"HAPUS {self.table_name.upper()}"
        if self.konfirmasi.value.strip().upper() != confirm_text:
            await interaction.response.send_message(
                f"🚫 Konfirmasi gagal! Ketik persis: `{confirm_text}`.",
                ephemeral=True
            )
            return

        allowed_tables = {"users", "spam", "violations", "threads", "introductions"}
        if self.table_name not in allowed_tables:
            await interaction.response.send_message(
                f"⚠️ Tabel `{self.table_name}` tidak diizinkan untuk dihapus.",
                ephemeral=True
            )
            return

        try:
            async with aiosqlite.connect(Database.DB_PATH) as db:
                await db.execute(f"DELETE FROM {self.table_name}")
                await db.commit()

            embed = discord.Embed(
                title=f"✅ DATA {self.table_name.upper()} DIHAPUS",
                description=f"Semua data pada tabel `{self.table_name}` telah dihapus oleh {interaction.user.mention}.",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            embed.set_footer(text="MountAlgo System • Reset Database")
            await interaction.response.send_message(embed=embed, ephemeral=True)

            # Kirim laporan ke log admin
            wib_now = format_wib(to_wib(get_utc_now()))
            await send_laporan_embed(
                bot,
                judul=f"🧨 RESET DATA {self.table_name.upper()}",
                deskripsi=f"Tabel `{self.table_name}` dihapus oleh {interaction.user.mention}",
                fields=[
                    ("🗂️ Tabel", self.table_name),
                    ("👤 Admin", interaction.user.display_name),
                    ("⏰ Waktu", wib_now),
                    ("Konfirmasi", confirm_text)
                ],
                warna=0xe74c3c,
                thumbnail="https://cdn-icons-png.flaticon.com/512/542/542638.png"
            )

            logging.info(f"[DELETE] {interaction.user} menghapus seluruh data di tabel '{self.table_name}'")

        except aiosqlite.Error as e:
            await interaction.response.send_message(
                f"❌ Kesalahan database:\n```{str(e)}```", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"🚨 Kesalahan sistem:\n```{str(e)}```", ephemeral=True
            )
            logging.error(f"Kesalahan DeleteConfirmModal: {e}", exc_info=True)

#---- wizard-toolkits ----

class TradingCalculatorModal(Modal, title="🧠 Kalkulator Trading Premium"):
    pair_symbol = TextInput(
        label="🔤 Pair Trading",
        placeholder="Contoh: BTCUSD, EURUSD, XAUUSD",
        required=True
    )
    position_entry = TextInput(
        label="📈 Posisi/Harga Entry",
        placeholder="Format: Arah/Harga\nContoh: BUY/62000",
        required=True
    )
    account_balance = TextInput(
        label="💰 Modal Akun (USD)",
        placeholder="Jumlah modal akun trading Anda\nContoh: 10000",
        required=True
    )
    risk_params = TextInput(
        label="⚖️ Parameter Risiko",
        placeholder="Volume/Leverage/SL/TP\nCrypto(USD)|Lainnya(Lot)\nContoh: 500/50/60000/64000",
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            # 1. Daftar aset crypto populer
            CRYPTO_SYMBOLS = {
                "BTC", "ETH", "BNB", "XRP", "ADA", "SOL", "DOGE", "DOT", "AVAX",
                "SHIB", "MATIC", "TRX", "LINK", "LTC", "BCH", "UNI", "ATOM", "ETC",
                "XMR", "XLM", "ALGO", "VET", "FIL", "ICP", "APE", "FLOW", "QNT",
                "AAVE", "MANA", "SAND", "FRAX", "HBAR", "XTZ", "EGLD", "THETA",
                "AXS", "KLAY", "BSV", "EOS", "NEAR", "STX", "IMX", "GRT", "RPL",
                "FXS", "BAT", "KSM", "NEO", "USDC", "USDT", "DAI", "TUSD", "USDP",
                "UST", "BUSD", "LDO", "WAVES", "KAVA", "ENJ", "COMP", "ZEC", "SNX",
                "CRV", "RUNE", "MKR", "FTM", "GALA", "OP", "APT", "GMX", "INJ"
            }

            # 2. Validasi modal akun
            try:
                account_balance = float(self.account_balance.value)
                if account_balance <= 0:
                    return await interaction.response.send_message("❌ Modal akun harus lebih besar dari 0!", ephemeral=True)
            except ValueError:
                return await interaction.response.send_message("❌ Format modal akun salah! Harus angka\nContoh: 5000", ephemeral=True)

            # 3. Validasi pair trading
            pair = self.pair_symbol.value.upper().replace(" ", "")
            if not re.match(r"^[A-Z0-9]+(USD|EUR|JPY|GBP|CAD|AUD|CHF|NZD|XAU|XAG)$", pair):
                return await interaction.response.send_message("❌ Pair trading tidak valid! Contoh: BTCUSD, EURUSD, XAUUSD", ephemeral=True)

            # 4. Deteksi tipe aset dan konfigurasi fee
            if any(c in pair for c in ["XAU", "XAG", "GOLD", "SILVER"]):
                asset_type = "komoditas"
                prefix = "🔥"
                contract_size = 100
                pip_value = 0.01
                max_leverage = float('inf')
                min_leverage = 500
                spread_fee = 0.5 * pip_value * contract_size  # Spread 0.5 pip
                commission_per_lot = 10  # $10 per lot per sisi
                volatility_factor = 0.02  # Volatilitas sedang
            elif any(symbol in pair for symbol in CRYPTO_SYMBOLS):
                asset_type = "crypto"
                prefix = "🪙"
                contract_size = 1
                pip_value = 1
                max_leverage = 400
                min_leverage = 1
                spread_fee = 0  # Tidak ada spread, hanya fee persentase
                commission_per_lot = 0.001  # 0.1% per sisi
                volatility_factor = 0.05  # Volatilitas tinggi
            else:
                asset_type = "forex"
                prefix = "🌐"
                contract_size = 100000
                pip_value = 0.0001
                max_leverage = float('inf')
                min_leverage = 500
                spread_fee = 2 * pip_value * contract_size  # Spread 2 pip
                commission_per_lot = 7  # $7 per lot per sisi
                volatility_factor = 0.01  # Volatilitas rendah

            # 5. Parsing posisi dan entry
            pos_data = self.position_entry.value.upper().split("/")
            if len(pos_data) != 2:
                return await interaction.response.send_message("❌ Format posisi salah! Gunakan: BUY/62000", ephemeral=True)

            position = pos_data[0].strip()
            if position not in ["BUY", "SELL"]:
                return await interaction.response.send_message("❌ Arah harus BUY atau SELL!", ephemeral=True)

            try:
                entry = float(pos_data[1].strip())
                if entry <= 0:
                    return await interaction.response.send_message("❌ Harga entry harus lebih besar dari 0!", ephemeral=True)
            except ValueError:
                return await interaction.response.send_message("❌ Harga entry harus angka! Contoh: 62000", ephemeral=True)

            # 6. Parsing parameter risiko
            input_value, leverage, sl, tp = None, None, None, None
            if self.risk_params.value:
                risk_data = [x.strip() for x in self.risk_params.value.split("/")]
                try:
                    if len(risk_data) > 0 and risk_data[0]:
                        input_value = float(risk_data[0])
                    if len(risk_data) > 1 and risk_data[1]:
                        leverage = float(risk_data[1])
                    if len(risk_data) > 2 and risk_data[2]:
                        sl = float(risk_data[2])
                        if sl == entry:
                            return await interaction.response.send_message("❌ Stop Loss tidak boleh sama dengan harga entry!", ephemeral=True)
                    if len(risk_data) > 3 and risk_data[3]:
                        tp = float(risk_data[3])
                        if tp == entry:
                            return await interaction.response.send_message("❌ Take Profit tidak boleh sama dengan harga entry!", ephemeral=True)
                except ValueError:
                    return await interaction.response.send_message("❌ Format parameter risiko salah! Contoh: 500/50/60000/64000", ephemeral=True)

            # 7. Default values
            if input_value is None:
                input_value = min(account_balance * 0.02, 500) if asset_type == "crypto" else 0.1  # 2% modal atau 0.1 lot
            if leverage is None:
                leverage = min_leverage if asset_type != "crypto" else 50

            # 8. Validasi leverage
            if leverage < min_leverage:
                return await interaction.response.send_message(f"❌ Leverage terlalu rendah! Minimal {min_leverage}x untuk {asset_type}.", ephemeral=True)
            if asset_type == "crypto" and leverage > max_leverage:
                return await interaction.response.send_message(f"❌ Leverage terlalu tinggi! Maksimal {max_leverage}x untuk crypto.", ephemeral=True)

            # 9. Perhitungan volume, margin, dan fee
            if asset_type == "crypto":
                input_value = min(input_value, account_balance * 0.02)  # Batas 2% modal
                volume_coins = input_value / entry
                volume_usd = input_value
                volume_lots = 0  # Tidak digunakan untuk crypto
                required_margin = volume_usd / leverage
                commission_fee = volume_usd * commission_per_lot * 2  # Fee beli + jual
            else:
                volume_lots = min(input_value, account_balance * 0.02 / (contract_size * entry / leverage))
                volume_units = volume_lots * contract_size
                volume_usd = 0  # Tidak digunakan untuk forex/komoditas
                required_margin = (volume_units * entry) / leverage
                commission_fee = volume_lots * commission_per_lot * 2  # Fee beli + jual
                spread_fee = volume_lots * spread_fee  # Spread fee

            total_fee = commission_fee + spread_fee
            pip_value_per_unit = pip_value * contract_size
            risk_per_pip = volume_coins * pip_value_per_unit if asset_type == "crypto" else volume_lots * pip_value_per_unit

            # 10. Validasi margin
            if required_margin + total_fee > account_balance * 0.8:
                return await interaction.response.send_message("❌ Margin + fee melebihi 80% modal! Kurangi volume atau tambah modal.", ephemeral=True)

            # 11. Deteksi mata uang
            currency = "USD" if "USD" in pair else "EUR" if "EUR" in pair else "JPY" if "JPY" in pair else "GBP" if "GBP" in pair else pair[-3:]

            # 12. Fungsi grafik batang
            def create_bar_chart(value, max_value, size=10, color_ok=0x00ff00, color_warn=0xffff00, color_danger=0xff0000):
                ratio = min(1.0, value / max_value)
                filled = int(ratio * size)
                empty = size - filled
                chart = "▰" * filled + "▱" * empty
                color = color_danger if ratio > 0.7 else color_warn if ratio > 0.3 else color_ok
                return chart, color, f"{ratio*100:.1f}%"

            # 13. Fungsi untuk memotong field jika terlalu panjang
            def split_field_content(content, max_length=1000, header=""):
                fields = []
                current_content = header
                content_lines = content.split("\n")
                for line in content_lines:
                    if len(current_content) + len(line) + 1 <= max_length:
                        current_content += line + "\n"
                    else:
                        fields.append(current_content.strip())
                        current_content = header + line + "\n"
                if current_content.strip():
                    fields.append(current_content.strip())
                return fields

            # 14. Buat embed utama
            trade_color = 0x00ff00 if position == "BUY" else 0xff0000
            embed = discord.Embed(
                title="🚀 KALKULATOR TRADING PREMIUM",
                description="Analisis risiko terintegrasi dengan modal dan fee broker",
                color=trade_color
            )

            # 15. Info akun dan modal
            balance_chart, balance_color, balance_percent = create_bar_chart(required_margin, account_balance, 15)
            account_info = (
                f"```scss\n"
                f"● Total Modal: ${account_balance:,.2f}\n"
                f"● Margin Digunakan: ${required_margin:,.2f}\n"
                f"● Total Fee (Beli/Jual): ${total_fee:,.2f}\n"
                f"  [{balance_chart}]\n"
                f"  {balance_percent} Modal Tertahan```"
            )
            embed.add_field(
                name="▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n💼 PROFIL AKUN\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰",
                value=account_info,
                inline=False
            )

            # 16. Info posisi trading
            position_str = f"**{prefix} Pair:** {pair} ({asset_type.capitalize()})\n"
            position_str += f"**{'🟢 BUY' if position == 'BUY' else '🔴 SELL'} Arah:** @ `{entry:,.5f} {currency}`\n"
            if asset_type == "crypto":
                position_str += f"**● Investasi:** ${volume_usd:,.2f} ({volume_coins:.6f} koin)\n"
            else:
                position_str += f"**● Volume:** {volume_lots:.2f} lot ({volume_units:,.0f} unit)\n"
            position_str += f"**● Leverage:** 1:`{leverage:.0f}`\n"
            position_str += f"**● Risk/PIP:** ${risk_per_pip:,.2f}"
            embed.add_field(
                name="▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n📊 POSISI TRADING\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰",
                value=position_str,
                inline=False
            )

            # 17. Analisis risiko kritis
            warning_level = ""
            leverage_ratio = leverage / (1000 if asset_type != "crypto" else 200)
            leverage_chart, leverage_color, leverage_percent = create_bar_chart(leverage_ratio, 1.5, 10)

            if required_margin + total_fee > account_balance:
                warning_level = "🚨 **RISIKO MARGIN CALL!**"
                risk_color = 0xff0000
            elif required_margin + total_fee > account_balance * 0.5:
                warning_level = "🔥 **RISIKO TINGGI!** - >50% modal tertahan"
                risk_color = 0xff3300
            elif required_margin + total_fee > account_balance * 0.3:
                warning_level = "⚠️ **CAUTION** - >30% modal tertahan"
                risk_color = 0xff9900
            else:
                warning_level = "✅ **RISIKO TERKENDALI**"
                risk_color = 0x00cc00

            risk_analysis = (
                f"{warning_level}\n"
                f"```prolog\n"
                f"➩ Margin + Fee: ${(required_margin + total_fee):,.2f} / ${account_balance:,.2f}\n"
                f"➩ Risk/PIP: ${risk_per_pip:,.2f}\n"
                f"➩ Leverage: [{leverage_chart}]\n"
                f"            {leverage_percent} Tingkat Bahaya\n"
                f"```"
            )
            embed.add_field(
                name="▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n⚠️ ANALISIS RISIKO UTAMA\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰",
                value=risk_analysis,
                inline=False
            )

            # 18. Analisis SL/TP
            risk_details = ""
            rr_ratio = 0
            risk_amount = 0
            profit_potential = 0
            if sl or tp:
                if sl:
                    sl_distance = abs(entry - sl)
                    pip_distance_sl = sl_distance / pip_value
                    risk_amount = pip_distance_sl * risk_per_pip + total_fee
                    risk_percent = min(100, risk_amount / account_balance * 100)
                    risk_chart, risk_chart_color, risk_percent_str = create_bar_chart(risk_percent, 100, 12)
                    risk_level = (
                        "⁉️ RISIKO FATAL (>10%)" if risk_percent > 10 else
                        "⚠️ RISIKO TINGGI (>5%)" if risk_percent > 5 else
                        "ℹ️ RISIKO MODERAT" if risk_percent > 2 else
                        "✅ RISIKO AMAN"
                    )
                    risk_details += (
                        f"🔴 **Stop Loss:** `{sl:,.5f} {currency}`\n"
                        f"```diff\n- Jarak: {pip_distance_sl:,.1f} pip\n"
                        f"➩ Kerugian Potensial: ${risk_amount:,.2f} ({risk_percent:.2f}% modal)\n"
                        f"  [{risk_chart}]\n"
                        f"  {risk_level}```\n"
                    )

                if tp:
                    tp_distance = abs(entry - tp if position == "BUY" else tp - entry)
                    pip_distance_tp = tp_distance / pip_value
                    profit_potential = pip_distance_tp * risk_per_pip - total_fee
                    profit_percent = min(100, max(0, profit_potential / account_balance * 100))
                    profit_chart, profit_color, profit_percent_str = create_bar_chart(profit_percent, 50, 12)
                    profit_level = (
                        "🚀 PROFIT BESAR (>20%)" if profit_percent > 20 else
                        "📈 PROFIT WAJAR (5-20%)" if profit_percent > 5 else
                        "📊 PROFIT KECIL (<5%)"
                    )
                    risk_details += (
                        f"🟢 **Take Profit:** `{tp:,.5f} {currency}`\n"
                        f"```yaml\n+ Jarak: {pip_distance_tp:,.1f} pip\n"
                        f"+ Profit Potensial: ${profit_potential:,.2f} ({profit_percent:.2f}% modal)\n"
                        f"  [{profit_chart}]\n"
                        f"  {profit_level}```\n"
                    )

                if sl and tp:
                    rr_ratio = pip_distance_tp / pip_distance_sl if pip_distance_sl > 0 else float('inf')
                    rr_quality = (
                        "🌟 **IDEAL** (≥3:1)" if rr_ratio >= 3 else
                        "✅ BAIK (2-3:1)" if rr_ratio >= 2 else
                        "⚠️ CUKUP (1-2:1)" if rr_ratio >= 1 else
                        "❌ BURUK (<1:1)"
                    )
                    risk_details += (
                        f"📐 **Risk/Reward Ratio:** {rr_ratio:.2f}:1\n"
                        f"```diff\n+ Kualitas Rasio: {rr_quality}```"
                    )

                embed.add_field(
                    name="▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n🎯 MANAJEMEN RISIKO\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰",
                    value=risk_details,
                    inline=False
                )

            # 19. Analisis Mendalam (Super Akurat, Kompleks, Totalitas)
            risk_ratio = (required_margin + total_fee) / account_balance * 100
            prob_success = min(0.9, max(0.3, 0.5 + (rr_ratio - 1) * 0.1)) if sl and tp else 0.5
            expected_return = (prob_success * profit_potential - (1 - prob_success) * risk_amount) if sl and tp else 0
            var_95 = risk_amount * 1.65 * volatility_factor if sl else account_balance * 0.05
            kelly_fraction = (prob_success * (rr_ratio + 1) - 1) / rr_ratio if sl and tp and rr_ratio > 0 else 0.01
            optimal_volume = account_balance * min(0.05, max(0.005, kelly_fraction)) / (entry / leverage)
            optimal_volume = optimal_volume if asset_type == "crypto" else optimal_volume / contract_size

            # Ringkasan Eksekutif
            executive_summary = (
                f"```yaml\n"
                f"● Risiko Total: {risk_ratio:.1f}% modal\n"
                f"● Probabilitas Sukses: {prob_success*100:.1f}%\n"
                f"● Expected Return: ${expected_return:,.2f}\n"
                f"● Volume Optimal: {optimal_volume:,.4f} {'USD' if asset_type == 'crypto' else 'lot'}\n"
                f"● Lebih Tepat: {'Kurangi volume 70-80%' if risk_ratio > 50 else 'Kurangi volume 30-50%' if risk_ratio > 30 else 'Pertahankan posisi'}\n"
                f"```"
            )
            embed.add_field(
                name="▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n📜 RINGKASAN EKSEKUTIF\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰",
                value=executive_summary,
                inline=False
            )

            # Skenario Hasil
            scenario_content = (
                f"```yaml\n"
                f"● Best Case (TP Tercapai): Profit ${profit_potential:,.2f} ({profit_potential/account_balance*100:.2f}%)\n"
                f"● Base Case (50% Jarak TP): Profit ${(profit_potential*0.5):,.2f}\n"
                f"● Worst Case (SL Tercapai): Rugi ${risk_amount:,.2f} ({risk_amount/account_balance*100:.2f}%)\n"
                f"```"
            )
            embed.add_field(
                name="▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n📊 SKENARIO HASIL\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰",
                value=scenario_content,
                inline=False
            )

            # Optimalisasi Posisi
            optimal_position = (
                f"```prolog\n"
                f"● Volume Optimal: {optimal_volume:,.4f} {'USD' if asset_type == 'crypto' else 'lot'}\n"
                f"● Leverage Lebih Tepat: 1:{min(max(50, leverage * (1 - volatility_factor)), 1000 if asset_type != 'crypto' else 200)}\n"
                f"● Risiko Maks per Trade: 1-1.5% modal (${account_balance*0.015:,.2f})\n"
                f"```"
            )
            embed.add_field(
                name="▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n📈 OPTIMALISASI POSISI\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰",
                value=optimal_position,
                inline=False
            )

            # Mitigasi Risiko
            mitigation_content = (
                f"```diff\n"
                f"+ Trailing Stop: Aktifkan setelah {pip_distance_tp*0.5:,.1f} pip profit\n"
                f"+ Hedging Parsial: Posisi lawan 20% volume jika mendekati SL\n"
                f"+ Diversifikasi: Maks 30% modal untuk {asset_type}\n"
                f"- Hindari Overtrading: Maks 2-3 posisi aktif\n"
                f"```"
            )
            embed.add_field(
                name="▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n🛡️ MITIGASI RISIKO\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰",
                value=mitigation_content,
                inline=False
            )

            # Konteks Waktu Trading
            trading_time = (
                "Sesi Asia (rendah volatilitas)" if asset_type == "forex" and risk_ratio < 30 else
                "Sesi London/New York (volatilitas optimal)" if asset_type == "forex" else
                "24/7, hindari jam news besar (FOMC, NFP)" if asset_type == "crypto" else
                "Sesi London (likuiditas tinggi untuk XAU/XAG)"
            )
            time_content = (
                f"```yaml\n"
                f"● Waktu Ideal: {trading_time}\n"
                f"● Perhatikan: Cek kalender ekonomi ({pair})\n"
                f"● Indikator: RSI, MA50/200, Bollinger Bands\n"
                f"```"
            )
            embed.add_field(
                name="▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n⏰ KONTEKS WAKTU TRADING\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰",
                value=time_content,
                inline=False
            )

            # Psikologi & Checklist
            psikologi_content = (
                f"```prolog\n"
                f"● Psikologi: Hindari FOMO, disiplin\nplanning trading\n"
                f"● Jurnal: Catat alasan entry dan emosi\n"
                f"● Checklist:\n"
                f"  - Analisis selesai\n"
                f"  - SL/TP diatur\n"
                f"  - Modal cukup\n"
                f"  - Tidak ada event makro besar\n"
                f"```"
                
            )
            embed.add_field(
                name="▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n PSIKOLOGI\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰",
                value=psikologi_content,
                inline=False
            )

            # Dampak Fee Broker
            fee_content = (
                f"```python\n"
                f"● Fee: ${total_fee:,.2f} ({(total_fee / profit_potential * 100 if profit_potential > 0 else 0):,.1f}% profit)\n"
                f"● Lebih Presisi: Cari broker dengan spread rendah\n"
                f"```"
                
            )
            embed.add_field(
                name="▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n DAMPAK FEE \n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰",
                value=fee_content,
                inline=False
            )

            # 20. Footer dengan disclaimer
            timestamp = datetime.now().strftime("%d/%m/%Y %I:%M %p")
            embed.set_footer(
                text=f"MountAlgo Risk Master v6.6.0 © • Perdagangan berisiko\n{timestamp}"
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except ValueError as e:
            error_embed = discord.Embed(
                title="❌ KESALAHAN INPUT",
                description=(
                    f"Format input tidak valid. Periksa:\n"
                    f"1. Gunakan titik (.) untuk desimal\n"
                    "2. Pisahkan nilai dengan tanda /\n"
                    f"3. Masukkan hanya angka numerik\n\n"
                    f"Error detail: {str(e)}\n\n"
                    "**Contoh untuk Crypto:**\n"
                    f"`BTCUSD` + `BUY/50000` + `10000` + `500/50/48000/55000`\n\n"
                    "**Contoh untuk Forex:**\n"
                    f"`EURUSD` + `BUY/1.0850` + `5000` + `0.5/500/1.0800/1.1000`"
                ),
                color=0xe74c3c
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
        except Exception as e:
            error_msg = (
                f"🚨 Maaf terjadi kesalahan sistem.\n"
                f"Error: {str(e)}"
                
            )
            await interaction.response.send_message(error_msg, ephemeral=True)
            logging.error(f"Kalkulator trading error: {str(e)}", exc_info=True)

class ResetChannelModal(Modal):
    def __init__(self, channel_name):
        super().__init__(title=f"Reset Channel {channel_name.capitalize()}")
        self.channel_name = channel_name
        self.new_content = TextInput(label="Konten Baru", style=discord.TextStyle.paragraph, required=True)
        self.add_item(self.new_content)

    async def on_submit(self, interaction: discord.Interaction):
        channel = discord.utils.get(interaction.guild.text_channels, name=self.channel_name)
        if channel:
            try:
                await channel.purge(limit=None)
            except Exception as e:
                print(f"Gagal hapus pesan di {channel.name}: {e}")
            await channel.send(self.new_content.value)
            await interaction.response.send_message(f"Channel #{self.channel_name} berhasil direset.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Channel #{self.channel_name} tidak ditemukan.", ephemeral=True)

class AdminAccessModal(Modal, title="Kontrol Hak Access Admin"):
    user_id = TextInput(label="User ID", placeholder="Masukkan User ID", required=True)
    action = TextInput(label="Aksi (promote/demote)", placeholder="promote/demote", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            user_id = int(self.user_id.value)
            member = interaction.guild.get_member(user_id)
            admin_role = discord.utils.get(interaction.guild.roles, name="Admin")
            if not member or not admin_role:
                await interaction.response.send_message("User/Role tidak ditemukan.", ephemeral=True)
                return
            if self.action.value.lower() == "promote":
                # Daftarkan ke database sebagai Admin
                await Database.update_user_status(user_id, "Admin", None, None)
                await apply_user_roles(member, "Admin")
                await interaction.response.send_message(f"User {member.mention} dipromosikan jadi Admin.", ephemeral=True)
            elif self.action.value.lower() == "demote":
                # Cabut semua dari database dan roles agar menjadi Member biasa
                await Database.update_user_status(user_id, "member", None, None)
                await apply_user_roles(member, "member")
                await interaction.response.send_message(f"User {member.mention} didegradasi (demote) menjadi Member biasa di database dan roles.", ephemeral=True)
            else:
                await interaction.response.send_message("Aksi tidak valid. Gunakan promote/demote.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

# ==============================================================
# 📊 AnalysisModal — Kirim Analisis (Fix Unknown Webhook & Safe Field)
# ==============================================================

class AnalysisModal(Modal, title="Kirim Analisis"):
    def __init__(self, title: str, thread_name: str):
        super().__init__(title=title)
        self.thread_name = thread_name

        self.input_title = TextInput(
            label="Judul Analisis",
            style=discord.TextStyle.short,
            placeholder="Contoh: Analisis BTC/USD - Breakout Area",
            max_length=100
        )
        self.input_description = TextInput(
            label="Deskripsi",
            style=discord.TextStyle.paragraph,
            placeholder="Tuliskan insight atau sentimen analisis Anda...",
            max_length=1500
        )
        self.input_image_url = TextInput(
            label="URL Gambar Chart (Opsional)",
            style=discord.TextStyle.short,
            required=False,
            placeholder="https://www.tradingview.com/x/abcd1234/"
        )
        self.input_file_url = TextInput(
            label="URL File / Dokumen (Opsional)",
            style=discord.TextStyle.short,
            required=False,
            placeholder="https://example.com/file.pdf"
        )
        self.input_diff_code = TextInput(
            label="Kode / Catatan Teknis (Opsional)",
            style=discord.TextStyle.paragraph,
            required=False,
            placeholder="Tuliskan ringkasan kode atau analisa teknikal..."
        )

        self.add_item(self.input_title)
        self.add_item(self.input_description)
        self.add_item(self.input_image_url)
        self.add_item(self.input_file_url)
        self.add_item(self.input_diff_code)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        title = self.input_title.value.strip()
        description = self.input_description.value.strip()
        image_url = self.input_image_url.value.strip()
        file_url = self.input_file_url.value.strip()
        diff_code = self.input_diff_code.value.strip()

        if not title or not description:
            await interaction.followup.send("❌ Judul dan deskripsi tidak boleh kosong!", ephemeral=True)
            return

        for url in [image_url, file_url]:
            if url and not url.lower().startswith(("http://", "https://")):
                await interaction.followup.send(f"⚠️ URL tidak valid: `{url}`", ephemeral=True)
                return

        target = discord.utils.get(interaction.guild.threads, name=self.thread_name)
        if not target:
            target = discord.utils.get(interaction.guild.text_channels, name=self.thread_name)

        if not target:
            await interaction.followup.send(f"❌ Thread atau Channel `{self.thread_name}` tidak ditemukan.", ephemeral=True)
            return

        if image_url and "tradingview.com/x/" in image_url:
            try:
                snapshot_id = image_url.split("/x/")[1].strip("/ ")
                image_url = f"https://s3.tradingview.com/snapshots/{snapshot_id}.png"
            except Exception:
                pass

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color(COLOR_CYAN),
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"Dikirim oleh {interaction.user.display_name}")
        if image_url:
            embed.set_image(url=image_url)

        if file_url:
            safe_file = file_url[:1000] + "..." if len(file_url) > 1000 else file_url
            embed.add_field(name="🔗 File Terkait", value=f"[Klik di sini untuk membuka file]({safe_file})", inline=False)
        if diff_code:
            safe_diff = diff_code[:1000] + "..." if len(diff_code) > 1000 else diff_code
            embed.add_field(name="📘 Catatan Teknis", value=f"```{safe_diff}```", inline=False)

        files_to_send = []
        async for msg in interaction.channel.history(limit=10):
            if msg.author == interaction.user and msg.attachments:
                for attach in msg.attachments:
                    if not attach.filename.lower().endswith(('.exe', '.bat', '.sh', '.js')):
                        files_to_send.append(await attach.to_file())
                break

        try:
            if files_to_send:
                await target.send(embed=embed, files=files_to_send)
            else:
                await target.send(embed=embed)

            target_type = "thread" if isinstance(target, discord.Thread) else "channel"
            await interaction.followup.send(f"✅ Analisis berhasil dikirim ke {target_type} `{self.thread_name}`.", ephemeral=True)
        except discord.errors.NotFound:
            print("[WARNING] Follow-up webhook sudah tidak aktif.")
        except Exception as e:
            try:
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="❌ Gagal Mengirim Analisis",
                        description=f"Terjadi kesalahan: `{e}`",
                        color=discord.Color.red()
                    ),
                    ephemeral=True
                )
            except discord.errors.NotFound:
                print(f"[ERROR] Tidak bisa follow-up: {e}")

# ==============================================================
# 🧙 WizardEmbedModal — Kirim Embed ke #wizard-strategy (FINAL)
# ==============================================================

class WizardEmbedModal(Modal, title="Kirim Embed ke #wizard-strategy"):
    def __init__(self):
        super().__init__()

        self.judul = TextInput(
            label="Judul Embed",
            placeholder="Contoh: Strategi SMC Breaker Block",
            max_length=100
        )
        self.add_item(self.judul)

        self.isi = TextInput(
            label="Isi Penjelasan",
            style=discord.TextStyle.paragraph,
            placeholder="Tuliskan deskripsi strategi atau penjelasan indikator...",
            required=True,
            max_length=1500
        )
        self.add_item(self.isi)

        self.hasil_diff = TextInput(
            label="Hasil Diff / Contoh Kode (opsional)",
            style=discord.TextStyle.paragraph,
            required=False,
            placeholder="Akan dibungkus otomatis dalam blok ```...```"
        )
        self.add_item(self.hasil_diff)

        self.link = TextInput(
            label="Link Indikator / Sumber (opsional)",
            required=False,
            placeholder="https://tradingview.com/script/..."
        )
        self.add_item(self.link)

        self.image_url = TextInput(
            label="URL Gambar (Opsional)",
            required=False,
            placeholder="https://www.tradingview.com/x/abcd1234/"
        )
        self.add_item(self.image_url)

    async def on_submit(self, interaction: discord.Interaction):
        # --- Aktifkan webhook follow-up ---
        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild
        channel = discord.utils.get(guild.text_channels, name="wizard-strategy")

        if not channel:
            await interaction.followup.send("❌ Channel #wizard-strategy tidak ditemukan!", ephemeral=True)
            return

        title = self.judul.value.strip()
        description = self.isi.value.strip()
        diff_code = self.hasil_diff.value.strip()
        link = self.link.value.strip()
        image_url = self.image_url.value.strip()

        # --- Validasi gambar ---
        if image_url:
            if not image_url.lower().startswith(("http://", "https://")):
                await interaction.followup.send("⚠️ URL gambar tidak valid.", ephemeral=True)
                return
            if not image_url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                await interaction.followup.send("⚠️ Hanya URL gambar langsung (.png/.jpg/.gif).", ephemeral=True)
                return
            if "tradingview.com/x/" in image_url:
                try:
                    snapshot_id = image_url.split("/x/")[1].strip("/ ")
                    image_url = f"https://s3.tradingview.com/snapshots/{snapshot_id}.png"
                except Exception:
                    pass

        # --- Buat embed ---
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color(COLOR_CYAN),
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"Dikirim oleh {interaction.user.display_name}")
        if image_url:
            embed.set_image(url=image_url)

        # Batasi panjang teks (maks 1024 per field)
        if diff_code:
            safe_diff = diff_code[:1000] + "..." if len(diff_code) > 1000 else diff_code
            embed.add_field(name="📄 Hasil Diff / Kode", value=f"```{safe_diff}```", inline=False)
        if link:
            safe_link = link[:1000] + "..." if len(link) > 1000 else link
            embed.add_field(name="🔗 Link Indikator / Sumber", value=f"[Klik di sini]({safe_link})", inline=False)

        # --- Cek upload user ---
        files_to_send = []
        async for msg in interaction.channel.history(limit=10):
            if msg.author == interaction.user and msg.attachments:
                for attach in msg.attachments:
                    if not attach.filename.lower().endswith(('.exe', '.bat', '.sh', '.js')):
                        files_to_send.append(await attach.to_file())
                break

        try:
            if files_to_send:
                await channel.send(embed=embed, files=files_to_send)
            else:
                await channel.send(embed=embed)
            await interaction.followup.send("✅ Embed berhasil dikirim ke #wizard-strategy!", ephemeral=True)
        except discord.errors.NotFound:
            print("[WARNING] Webhook follow-up sudah tidak aktif (10015).")
        except Exception as e:
            try:
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="❌ Gagal Mengirim Embed",
                        description=f"Terjadi kesalahan: `{e}`",
                        color=discord.Color.red()
                    ),
                    ephemeral=True
                )
            except discord.errors.NotFound:
                print(f"[ERROR] Tidak bisa follow-up: {e}")
            
def calculate_pnl(direction, open_price, close_price, value, value_type, leverage=1):
    """Hitung Profit/Loss berdasarkan tipe trading dengan leverage"""
    try:
        # Hitung persentase perubahan harga
        if direction == "BUY" or "Buy" or "buy":
            pct_change = (close_price - open_price) / open_price if open_price != 0 else 0
        else:  # SELL
            pct_change = (open_price - close_price) / open_price if open_price != 0 else 0
        
        # Hitung PnL berdasarkan tipe nilai
        if value_type == "LOT":
            # Untuk forex/komoditas: 1 LOT = 100,000 unit
            contract_size = 100000
            # PnL tanpa leverage
            base_pnl = pct_change * value * contract_size
            # Terapkan leverage
            leveraged_pnl = base_pnl * leverage
        elif value_type == "USD":
            # Untuk crypto dan direct USD value
            # PnL tanpa leverage
            base_pnl = pct_change * value
            # Terapkan leverage
            leveraged_pnl = base_pnl * leverage
        else:
            # Default fallback
            leveraged_pnl = pct_change * value * leverage
            
        return leveraged_pnl
    except Exception as e:
        logging.error(f"Error calculating PnL: {e}")
        return 0.0

def calculate_duration():
    """Hitung durasi posisi (implementasi sederhana)"""
    # Dalam implementasi nyata, ini akan dihitung dari waktu open ke close
    return "2h 30m"  # Contoh statis
            
# ---chart---
class AssetPriceModal(Modal, title="📊 Analisis Institusional Aset"):
    symbol = TextInput(
        label="💱 Pair/Symbol Trading",
        placeholder="Contoh: BTC-USD, EUR/USD, XAU/USD, OIL",
        required=True,
        max_length=20
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)

        # Normalisasi simbol
        raw_symbol = self.symbol.value.strip().upper()
        clean_symbol = raw_symbol.replace("/", "").replace("-", "").replace(" ", "")

        try:
            # === Ambil harga multi-sumber (prioritas otomatis) ===
            price = await PriceFetcher.get_real_time_price(clean_symbol)
            change_24h = await PriceFetcher.get_24h_change(clean_symbol)
            volume_24h = await PriceFetcher.get_volume_24h(clean_symbol)

            # === Jika semua sumber gagal ===
            if price is None:
                await interaction.followup.send(
                    f"⚠️ Data harga untuk `{raw_symbol}` tidak ditemukan di semua sumber.\n"
                    f"Pastikan simbol valid (misal: `BTCUSDT`, `EURUSD`, `XAUUSD`, `OIL`).",
                    ephemeral=True
                )
                return

            # Ambil info sumber cache (untuk tahu dari mana data diambil)
            cache_info = await PriceFetcher.get_cache_info()
            symbol_key = PriceFetcher._get_symbol(clean_symbol)
            source = "Tidak diketahui"
            if symbol_key in cache_info:
                source = cache_info[symbol_key].get("source", "unknown").replace("_try_", "")

            # Tentukan warna embed
            color = discord.Color(COLOR_GREEN) if (change_24h or 0) >= 0 else discord.Color.red()

            # Format harga
            price_str = format_price(price)

            # === Buat embed hasil ===
            embed = discord.Embed(
                title=f"📈 {raw_symbol} — Analisis Harga Multi-Sumber",
                color=color,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="💰 Harga Terkini", value=f"**${price_str}**", inline=False)
            embed.add_field(name="📊 Perubahan 24 Jam", value=f"{(change_24h or 0):.2f}%", inline=True)
            embed.add_field(name="📦 Volume 24 Jam", value=f"{(volume_24h or 0):,.2f}", inline=True)
            embed.add_field(name="🌐 Sumber Data", value=f"`{source}`", inline=False)
            embed.set_footer(
                text=f"Diperbarui: {datetime.now(jakarta_tz).strftime('%d/%m/%Y %H:%M WIB')}"
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            logging.error(f"Kesalahan di AssetPriceModal: {e}", exc_info=True)
            await interaction.followup.send(
                f"🚫 Terjadi kesalahan saat mengambil data harga:\n`{str(e)}`",
                ephemeral=True
            )
            
# ===================== UTILITY SERVER BUILDER =====================
class ServerBuilder:
    @staticmethod
    async def setup_server(guild: discord.Guild):
        """Setup struktur server lengkap dengan penanganan error solid"""
        # Inisialisasi statistik dan logger
        stats = {
            "categories_created": 0,
            "channels_created": 0,
            "roles_created": 0,
            "errors": 0
        }
        error_details = []
        channel_map = {}  # Untuk menyimpan referensi channel
        
        # Pembersihan server yang aman
        await ServerBuilder.safe_cleanup(guild, stats)
        
        # ----------------------- Langkah 1: Buat Role Utama -----------------------
        core_roles = ["Member", "WizardMemberBulanan","WizardMemberTahunan", "Admin", "Muted", "Unverified"]
        for role_name in core_roles:
            try:
                role = discord.utils.get(guild.roles, name=role_name)
                if not role:
                    color = {
                        "Member": discord.Color(COLOR_CYAN),
                        "WizardMemberBulanan": discord.Color.gold(),
                        "WizardMemberTahunan": discord.Color(COLOR_VIOLET),
                        "Admin": discord.Color.red(),
                        "Unverified": discord.Color(COLOR_DARK),
                        "Muted": discord.Color(COLOR_DARK)
                    }.get(role_name, discord.Color.default())
                    
                    perms = discord.Permissions(administrator=True) if role_name == "Admin" else discord.Permissions.none()
                    await guild.create_role(
                        name=role_name,
                        color=color,
                        permissions=perms,
                        reason="Setup otomatis"
                    )
                    stats["roles_created"] += 1
                elif role_name == "Admin" and not role.permissions.administrator:
                    try:
                        await role.edit(permissions=discord.Permissions(administrator=True))
                    except Exception as e:
                        logging.error(f"Gagal mengedit permissions Admin di setup_server: {e}")
            except Exception as e:
                stats["errors"] += 1
                error_details.append(f"Gagal buat role {role_name}: {str(e)}")
        
        # ----------------------- Langkah 2: Buat Struktur Kategori & Channel -----------------------
        for category_config in SERVER_STRUCTURE:
            category_name, allowed_roles, channels = category_config
            
            try:
                # Buat kategori
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False)
                }
                
                # Atur izin untuk role yang diizinkan
                for role_name in allowed_roles:
                    role = discord.utils.get(guild.roles, name=role_name.replace("@", ""))
                    if role:
                        overwrites[role] = discord.PermissionOverwrite(read_messages=True)
                
                category = await guild.create_category(
                    category_name,
                    overwrites=overwrites,
                    reason="Auto setup"
                )
                stats["categories_created"] += 1
                
                # Buat channel di dalam kategori
                for channel_config in channels:
                    channel_name = channel_config[0]
                    description = channel_config[1]
                    channel_roles = channel_config[2]
                    try:
                        # Salin overwrites dari kategori
                        channel_overwrites = overwrites.copy()
                        
                        # Modifikasi izin spesifik channel
                        for role_name in channel_roles:
                            if role_name == "@everyone":
                                channel_overwrites[guild.default_role] = discord.PermissionOverwrite(read_messages=True)
                            else:
                                role = discord.utils.get(guild.roles, name=role_name.replace("@", ""))
                                if role:
                                    # Terapkan template izin
                                    if channel_name in CHANNEL_PERMISSIONS:
                                        if role_name in CHANNEL_PERMISSIONS[channel_name]:
                                            perm_overwrite = PermissionOverwrite()
                                            for perm, value in CHANNEL_PERMISSIONS[channel_name][role_name].items():
                                                setattr(perm_overwrite, perm, value)
                                            channel_overwrites[role] = perm_overwrite
                                    
                        # Buat channel
                        ch_type = channel_config[3] if len(channel_config) > 3 else "text"
                        if ch_type == "voice":
                            channel = await category.create_voice_channel(
                                channel_name,
                                overwrites=channel_overwrites,
                                reason="Auto setup"
                            )
                        elif ch_type == "stage":
                            channel = await category.create_stage_channel(
                                channel_name,
                                overwrites=channel_overwrites,
                                reason="Auto setup"
                            )
                        else:
                            channel = await category.create_text_channel(
                                channel_name,
                                topic=description,
                                overwrites=channel_overwrites,
                                reason="Auto setup"
                            )
                        stats["channels_created"] += 1
                        
                        # Simpan ke mapping
                        channel_map[channel_name] = channel
                        
                    except Exception as e:
                        stats["errors"] += 1
                        error_details.append(f"Gagal buat channel {channel_name}: {str(e)}")
            
            except Exception as e:
                stats["errors"] += 1
                error_details.append(f"Gagal buat kategori {category_name}: {str(e)}")
        
        # ----------------------- Langkah 3: Inisialisasi Konten Channel -----------------------
        await ServerBuilder.initialize_channel_content(guild, channel_map)
        
        # ----------------------- Logging & Return -----------------------
        logging.info(f"Setup server berhasil di {guild.name} | " 
                    f"Kategori: {stats['categories_created']}, "
                    f"Channel: {stats['channels_created']}, "
                    f"Error: {stats['errors']}")
        
        return {
            "stats": stats,
            "errors": error_details,
            "channel_map": channel_map
        }

    @staticmethod
    async def safe_cleanup(guild: discord.Guild, stats: dict):
        """Hapus semua channel dan kategori dengan aman"""
        # Hapus semua channel text
        for channel in guild.text_channels:
            try:
                await channel.delete(reason="Cleaning for server setup")
                await asyncio.sleep(0.2)  # Hindari rate limit
            except Exception as e:
                stats["errors"] += 1
                logging.warning(f"Gagal hapus channel {channel.name}: {str(e)}")
        
        # Hapus semua kategori
        for category in guild.categories:
            try:
                await category.delete(reason="Cleaning for server setup")
                await asyncio.sleep(0.5)
            except Exception as e:
                stats["errors"] += 1
                logging.warning(f"Gagal hapus category {category.name}: {str(e)}")
        
        # Hapus semua voice channel
        for voice_channel in guild.voice_channels:
            try:
                await voice_channel.delete(reason="Cleaning for server setup")
                await asyncio.sleep(0.2)
            except Exception as e:
                stats["errors"] += 1
                logging.warning(f"Gagal hapus voice channel {voice_channel.name}: {str(e)}")

        # Hapus semua stage channel
        for stage_channel in guild.stage_channels:
            try:
                await stage_channel.delete(reason="Cleaning for server setup")
                await asyncio.sleep(0.2)
            except Exception as e:
                stats["errors"] += 1
                logging.warning(f"Gagal hapus stage channel {stage_channel.name}: {str(e)}")

    @staticmethod
    async def initialize_channel_content(guild: discord.Guild, channel_map: dict):
        """Isi konten awal untuk channel khusus"""
        init_functions = {
            "welcome": send_welcome_embed,
            "peraturan": send_peraturan_embed,
            "disclaimer": send_disclaimer_embed,
            "verifikasi": lambda ch: VerificationSystem.update_verification_channel(ch),
            "bantuan": send_bantuan_embed,
            "lounge-chat": send_obrolan_embed,
            "wizard-lounge-chat": send_wizard_lounge_embed,
            "kontrol-pengguna": send_kontrol_pengguna_embed,
            "kontrol-admin": send_kontrol_admin_embed,
            "wizard-toolkits": send_wizard_toolkits_embed
        }
        
        for channel_name, init_func in init_functions.items():
            channel = channel_map.get(channel_name)
            if channel:
                try:
                    # Hapus pesan lama terlebih dahulu
                    await channel.purge(limit=100)
                    await init_func(channel)
                except Exception as e:
                    logging.error(f"Gagal inisialisasi {channel_name}: {str(e)}")

    @staticmethod
    async def get_or_create_role(guild, role_name):
        clean_name = role_name.replace("@", "")
        role = discord.utils.get(guild.roles, name=clean_name)
        if not role:
            perms = discord.Permissions(administrator=True) if clean_name == "Admin" else discord.Permissions.none()
            role = await guild.create_role(name=clean_name, permissions=perms)
        elif clean_name == "Admin" and not role.permissions.administrator:
            try:
                await role.edit(permissions=discord.Permissions(administrator=True))
            except Exception as e:
                logging.error(f"Gagal mengedit permissions Admin di get_or_create_role: {e}")
        return role

    @staticmethod
    def get_role(guild, role_name):
        clean_name = role_name.replace("@", "")
        return discord.utils.get(guild.roles, name=clean_name)

    @classmethod
    async def setup_server(cls, guild):
        for category in guild.categories:
            try:
                await category.delete()
            except:
                pass
        for channel in guild.channels:
            try:
                await channel.delete()
            except:
                pass
        all_roles = set()
        for kategori, roles, channels in SERVER_STRUCTURE:
            all_roles.update([r for r in roles if r != "@everyone"])
            for ch_info in channels:
                ch_roles = ch_info[2]
                all_roles.update([r for r in ch_roles if r != "@everyone"])
        for role_name in all_roles:
            await cls.get_or_create_role(guild, role_name)
        channel_map = {}
        for kategori, roles, channels in SERVER_STRUCTURE:
            overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False)}
            for role_name in roles:
                if role_name == "@everyone":
                    overwrites[guild.default_role] = discord.PermissionOverwrite(read_messages=True)
                else:
                    role = cls.get_role(guild, role_name)
                    if role:
                        overwrites[role] = discord.PermissionOverwrite(read_messages=True)
            category = await guild.create_category(kategori, overwrites=overwrites)
            for ch_info in channels:
                ch_name = ch_info[0]
                desc = ch_info[1]
                ch_roles = ch_info[2]
                ch_overwrites = overwrites.copy()
                for role_name in ch_roles:
                    if role_name == "@everyone":
                        ch_overwrites[guild.default_role] = discord.PermissionOverwrite(read_messages=True)
                    else:
                        role = cls.get_role(guild, role_name)
                        if role:
                            ch_overwrites[role] = discord.PermissionOverwrite(read_messages=True)
                ch_type = ch_info[3] if len(ch_info) > 3 else "text"
                if ch_type == "voice":
                    ch = await category.create_voice_channel(ch_name, overwrites=ch_overwrites)
                elif ch_type == "stage":
                    ch = await category.create_stage_channel(ch_name, overwrites=ch_overwrites)
                else:
                    ch = await guild.create_text_channel(ch_name, category=category, overwrites=ch_overwrites, topic=desc)
                channel_map[ch_name] = ch
        if "welcome" in channel_map:
            await send_welcome_embed(channel_map["welcome"])
        if "peraturan" in channel_map:
            await send_peraturan_embed(channel_map["peraturan"])
        if "disclaimer" in channel_map:
            await send_disclaimer_embed(channel_map["disclaimer"])
        if "verifikasi" in channel_map:
            await send_verifikasi_embed(channel_map["verifikasi"])
        if "bantuan" in channel_map:
            await send_bantuan_embed(channel_map["bantuan"])
        if "lounge-chat" in channel_map:
            await send_obrolan_embed(channel_map["lounge-chat"])
        if "wizard-lounge-chat" in channel_map:
            await send_wizard_lounge_embed(channel_map["wizard-lounge-chat"])
        if "kontrol-pengguna" in channel_map:
            await send_kontrol_pengguna_embed(channel_map["kontrol-pengguna"])
        if "kontrol-admin" in channel_map:
            await send_kontrol_admin_embed(channel_map["kontrol-admin"])
        if "wizard-toolkits" in channel_map:
            await send_wizard_toolkits_embed(channel_map["wizard-toolkits"])
      
# ===================== EVENT HANDLER & COMMAND =====================
# Pertama-tama setup database sebelum bot start
async def bot_setup():
    await Database.setup()

@bot.event
async def setup_hook():
    """Hook inisialisasi async yang dijalankan sebelum bot mulai berjalan"""
    try:
        await Database.setup()
        logging.info("✅ Database setup selesai di setup_hook")

        # Load global donation settings
        global DONATION_ACTIVE, PAYMENT_DANA_ACTIVE, PAYMENT_CRYPTO_ACTIVE, PAYMENT_CARD_ACTIVE
        donation_setting = await Database.get_setting("donation_button_active", "False")
        DONATION_ACTIVE = (donation_setting == "True")
        PAYMENT_DANA_ACTIVE = (await Database.get_setting("payment_dana_active", "True") == "True")
        PAYMENT_CRYPTO_ACTIVE = (await Database.get_setting("payment_crypto_active", "True") == "True")
        PAYMENT_CARD_ACTIVE = (await Database.get_setting("payment_card_active", "True") == "True")
        logging.info(f"🫂 Status tombol donasi awal: {DONATION_ACTIVE}")
        logging.info(f"📱 Status DANA: {PAYMENT_DANA_ACTIVE} | 🪙 USDC: {PAYMENT_CRYPTO_ACTIVE} | 💳 Bank/Card: {PAYMENT_CARD_ACTIVE}")
    except Exception as e:
        logging.error(f"❌ Gagal setup database: {e}")

@bot.event
async def on_ready():
    """Inisialisasi sistem utama MountAlgo saat bot siap digunakan"""
    print(f'✅ Bot is ready as {bot.user.name} ({bot.user.id})')
    logging.info(f"🚀 MountAlgo BOT aktif sebagai {bot.user.name} ({bot.user.id})")

    # Hindari duplikasi startup karena reconnect
    if getattr(bot, "already_ready", False):
        logging.info("♻️ Bot reconnect terdeteksi, abaikan inisialisasi ulang.")
        return
    bot.already_ready = True

    # =====================
    # 1️⃣ SINKRONISASI AWAL
    # =====================
    total_fixed = 0
    total_expired = 0

    for guild in bot.guilds:
        try:
            start_time = datetime.now(timezone.utc)
            logging.info(f"🧩 Memulai sinkronisasi awal untuk {guild.name}")
            await synchronize_users_and_roles(guild)

            # Auto perbaiki data invalid
            fixed_users = await find_invalid_status_users(guild)
            total_fixed += len(fixed_users)
            if fixed_users:
                logging.info(f"🔧 {len(fixed_users)} user diperbaiki di {guild.name}")

            duration = (datetime.now(timezone.utc) - start_time).total_seconds()
            logging.info(f"✅ Sinkronisasi awal selesai untuk {guild.name} ({duration:.2f}s)")
        except Exception as e:
            logging.error(f"❌ Gagal sinkronisasi awal untuk {guild.name}: {str(e)}")

    # =====================
    # 2️⃣ CEK KEDALUWARSA Wizard Member
    # =====================
    expired_users = await Database.check_expiry()
    total_expired = len(expired_users)
    for user_id, username, old_status in expired_users:
        for guild in bot.guilds:
            member = guild.get_member(user_id)
            if member:
                await apply_user_roles(member, "member")
                await Database.update_user_status(user_id, "member", None, None)
                try:
                    await member.send(
                        f"⚠️ Halo **{member.display_name}**, langganan **{old_status}** kamu telah berakhir.\n"
                        "Sekarang kamu kembali ke status **Member Biasa**.\n"
                        "Gunakan tombol **Langganan Premium** di #verifikasi untuk memperpanjang."
                    )
                except:
                    pass

    # =====================
    # 3️⃣ JADWALKAN SEMUA TASK OTOMATIS
    # =====================
    async def subscription_expiry_task():
        """Cek dan update status WizardMember bulanan/tahunan setiap 24 jam"""
        while True:
            try:
                expired_users = await Database.check_expiry()
                for user_id, username, old_status in expired_users:
                    for guild in bot.guilds:
                        member = guild.get_member(user_id)
                        if member:
                            await apply_user_roles(member, "member")
                            await Database.update_user_status(user_id, "member", None, None)
                            try:
                                await member.send(
                                    f"⚠️ Langganan {old_status} kamu telah berakhir. "
                                    f"Status kamu kini kembali menjadi **Member Biasa**."
                                )
                            except:
                                pass
                await asyncio.sleep(86400)
            except Exception as e:
                logging.error(f"Error subscription_expiry_task: {str(e)}")
                await asyncio.sleep(3600)

    bot.loop.create_task(subscription_expiry_task())

    jakarta_tz = pytz.timezone("Asia/Jakarta")

    async def sync_scheduler():
        """Sinkronisasi dan validasi user tiap 2 jam"""
        while True:
            try:
                now = datetime.now(jakarta_tz).strftime("%d/%m/%Y %H:%M")
                for guild in bot.guilds:
                    logging.info(f"🔄 Sinkronisasi rutin di {guild.name} ({now})")
                    await synchronize_users_and_roles(guild)
                    await find_invalid_status_users(guild)
            except Exception as e:
                logging.error(f"Error sync_scheduler: {e}")
            await asyncio.sleep(7200)  # 2 jam

    bot.loop.create_task(sync_scheduler())

    async def verification_scheduler():
        """Jalankan sistem verifikasi tiap 6 jam"""
        while True:
            try:
                for guild in bot.guilds:
                    await VerificationSystem.apply_verification_workflow(guild)
            except Exception as e:
                logging.error(f"Verification scheduler error: {e}")
            await asyncio.sleep(6 * 3600)

    bot.loop.create_task(verification_scheduler())

    async def daily_sync():
        """Sinkronisasi harian jam 8 pagi WIB"""
        while True:
            try:
                now = datetime.now(jakarta_tz)
                target_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
                if now > target_time:
                    target_time += timedelta(days=1)

                seconds_until = (target_time - now).total_seconds()
                await asyncio.sleep(seconds_until)
                for guild in bot.guilds:
                    await sync_verification_system(guild)
                logging.info("🌅 Daily sync selesai dijalankan.")
            except Exception as e:
                logging.error(f"Daily sync error: {e}")
                await asyncio.sleep(3600)

    bot.loop.create_task(daily_sync())

    # =====================
    # 4️⃣ REGISTER VIEW
    # =====================
    bot.add_view(VerifView())
    bot.add_view(BantuanView())
    bot.add_view(ObrolanView())
    bot.add_view(WizardLoungeView())
    bot.add_view(KontrolPenggunaView())
    bot.add_view(KontrolAdminView())
    bot.add_view(WizardToolkitsView())
    bot.add_view(ThreadManagementView())

    # =====================
    # 5️⃣ SETUP THREAD ANALISIS
    # =====================
    for guild in bot.guilds:
        try:
            channel = discord.utils.get(guild.text_channels, name="wizard-analisis")
            if channel:
                await create_analysis_threads(channel)
                await sync_members_to_threads(guild)
                logging.info(f"🧠 Thread Wizard Analisis siap di {guild.name}")
        except Exception as e:
            logging.error(f"Error setup thread di {guild.name}: {str(e)}")

    # =====================
    # 6️⃣ EMBED LAPORAN STARTUP
    # =====================
    for guild in bot.guilds:
        log_channel = discord.utils.get(guild.text_channels, name="laporan")
        if log_channel:
            total_members = guild.member_count
            Wizard_bulanan = len([m for m in guild.members if any(r.name == "WizardMemberBulanan" for r in m.roles)])
            Wizard_tahunan = len([m for m in guild.members if any(r.name == "WizardMemberTahunan" for r in m.roles)])

            embed = discord.Embed(
                title="📊 MountAlgo SYSTEM STATUS",
                description="Laporan otomatis saat bot aktif sepenuhnya.",
                color=discord.Color(COLOR_GREEN),
                timestamp=datetime.now(timezone.utc)
            )
            embed.add_field(name="🏠 Server", value=f"{guild.name}", inline=True)
            embed.add_field(name="👥 Total Member", value=str(total_members), inline=True)
            embed.add_field(name="💎 Wizard Bulanan", value=str(Wizard_bulanan), inline=True)
            embed.add_field(name="👑 Wizard Tahunan", value=str(Wizard_tahunan), inline=True)
            embed.add_field(name="🔧 Diperbaiki", value=str(total_fixed), inline=True)
            embed.add_field(name="⏳ Expired", value=str(total_expired), inline=True)
            embed.add_field(name="🕒 Waktu", value=datetime.now(pytz.timezone("Asia/Jakarta")).strftime("%d %B %Y • %H:%M WIB"), inline=False)
            embed.set_footer(text="MountAlgo System • by @Pratama")
            embed.set_thumbnail(url=bot.user.display_avatar.url)

            await log_channel.send(embed=embed)

    logging.info(f"✅ Bot fully initialized on {len(bot.guilds)} servers")
            

@bot.event
async def on_member_join(member: discord.Member):
    """
    Menangani peristiwa user bergabung ke server dengan sistem verifikasi terpadu.
    - User lama: otomatis dikembalikan ke status sesuai database.
    - User baru: otomatis status PendingVerification + role Unverified.
    """
    try:
        # 1️⃣ Ambil data user dari database
        user_data = await Database.get_user_data(member.id)

        # 2️⃣ Definisikan role yang dibutuhkan
        unverified_role = discord.utils.get(member.guild.roles, name="Unverified")
        member_role = discord.utils.get(member.guild.roles, name="Member")
        Wizard_bulanan_role = discord.utils.get(member.guild.roles, name="WizardMemberBulanan")
        Wizard_tahunan_role = discord.utils.get(member.guild.roles, name="WizardMemberTahunan")
        admin_role = discord.utils.get(member.guild.roles, name="Admin")

        # 3️⃣ Kasus: User sudah terdaftar di database
        if user_data:
            user_id, username, status, sub_type, expiry = user_data

            if status == "WizardMemberBulanan":
                if Wizard_bulanan_role:
                    await member.add_roles(Wizard_bulanan_role)
                await member.send(
                    "💎 **Selamat Datang Kembali Wizard Member Bulanan!**\n"
                    "Langganan bulanan Anda masih aktif. Nikmati kembali akses premium MountAlgo."
                )

            elif status == "WizardMemberTahunan":
                if Wizard_tahunan_role:
                    await member.add_roles(Wizard_tahunan_role)
                await member.send(
                    "👑 **Selamat Datang Kembali Wizard Member Tahunan!**\n"
                    "Langganan tahunan Anda tetap aktif. Terima kasih atas dukungan Anda!"
                )

            elif status == "Admin":
                if admin_role:
                    await member.add_roles(admin_role)
                await member.send(
                    "🔒 **Akses Admin Diaktifkan**\n"
                    "Anda telah dikembalikan ke role administrator MountAlgo."
                )

            elif status == "member":
                if member_role:
                    await member.add_roles(member_role)
                await member.send(
                    "👋 **Selamat Datang Kembali di MountAlgo!**\n"
                    "Status Anda tetap sebagai Member Biasa."
                )

            else:  # Status tidak dikenal → Unverified
                if unverified_role:
                    await member.add_roles(unverified_role)
                await member.send(
                    "⚠️ **Status Anda Perlu Verifikasi Ulang.**\n"
                    "Silakan:\n"
                    "1️⃣ Buka channel `#verifikasi`\n"
                    "2️⃣ Klik tombol **Setuju & Verifikasi**"
                )

            logging.info(f"🔁 Member lama kembali: {member.display_name} ({status})")
            return

        # 4️⃣ Kasus: User baru (belum terdaftar)
        if unverified_role:
            await member.add_roles(unverified_role)

        await Database.add_user(
            user_id=member.id,
            username=member.name,
            status="PendingVerification",
            subscription_type=None,
            expiry_date=None
        )

        # 5️⃣ Kirim pesan sambutan via DM
        try:
            rules_channel = discord.utils.get(member.guild.text_channels, name="peraturan")
            verif_channel = discord.utils.get(member.guild.text_channels, name="verifikasi")

            welcome_msg = [
                "👋 **SELAMAT DATANG DI MountAlgo TRADING COMMUNITY!**",
                "",
                "Sebelum mengakses seluruh channel, Anda perlu menyelesaikan verifikasi singkat:",
                "",
                f"1️⃣ Baca peraturan di {rules_channel.mention if rules_channel else '#peraturan'}",
                f"2️⃣ Pergi ke {verif_channel.mention if verif_channel else '#verifikasi'}",
                "3️⃣ Klik tombol **Setuju & Verifikasi**",
                "",
                "✅ Setelah verifikasi, Anda akan otomatis mendapatkan akses penuh.",
                "",
                "Jika butuh bantuan, silakan kirim DM ke admin atau buka #bantuan."
            ]

            await member.send("\n".join(welcome_msg))
        except discord.Forbidden:
            logging.warning(f"Tidak bisa kirim DM ke {member.name} ({member.id})")

        # 6️⃣ Catat ke log server
        logging.info(f"🆕 User baru bergabung: {member.name} ({member.id}) | Status: PendingVerification")

    except Exception as e:
        error_msg = f"Error pada on_member_join: {str(e)}"
        logging.error(error_msg, exc_info=True)

        admin_channel = discord.utils.get(member.guild.text_channels, name="laporan")
        if admin_channel:
            await admin_channel.send(f"❌ **ERROR JOIN**: <@{member.id}>\n```{error_msg}```")
            
@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    """
    Fungsi ini memeriksa perubahan role user secara real-time.
    Bot akan otomatis menyelaraskan status user di database dengan role barunya.
    """

    try:
        if before.bot or after.bot:
            return  # Abaikan bot

        guild = after.guild
        user_id = after.id

        # Ambil role sebelum & sesudah
        before_roles = {r.name for r in before.roles}
        after_roles = {r.name for r in after.roles}

        # Deteksi perubahan role
        added_roles = after_roles - before_roles
        removed_roles = before_roles - after_roles

        # Jika tidak ada perubahan role, abaikan
        if not added_roles and not removed_roles:
            return

        # Log perubahan
        logging.info(
            f"[on_member_update] {after.display_name} → Tambah: {added_roles}, Hapus: {removed_roles}"
        )

        # Tentukan status dari roles saat ini
        role_names = [r.name for r in after.roles]
        resolved_status = "PendingVerification"
        if "Admin" in role_names:
            resolved_status = "Admin"
        elif "WizardMemberTahunan" in role_names:
            resolved_status = "WizardMemberTahunan"
        elif "WizardMemberBulanan" in role_names:
            resolved_status = "WizardMemberBulanan"
        elif "Member" in role_names:
            resolved_status = "member"

        # Dapatkan data user saat ini dari database
        user_data = await Database.get_user_data(user_id)

        if not user_data:
            new_sub_type = None
            new_expiry = None
            if resolved_status == "WizardMemberBulanan":
                new_sub_type = "bulanan"
                new_expiry = (datetime.utcnow() + timedelta(days=30)).isoformat()
            elif resolved_status == "WizardMemberTahunan":
                new_sub_type = "tahunan"
                new_expiry = (datetime.utcnow() + timedelta(days=365)).isoformat()

            await Database.add_user(
                user_id=user_id,
                username=after.name,
                status=resolved_status,
                subscription_type=new_sub_type,
                expiry_date=new_expiry
            )
            logging.info(f"[on_member_update] User {after.display_name} baru ditambahkan ke database dengan status {resolved_status}.")
            return

        db_status = user_data[2]
        db_sub_type = user_data[3]
        db_expiry = user_data[4]

        if resolved_status != db_status:
            new_sub_type = None
            new_expiry = None
            if resolved_status == "WizardMemberBulanan":
                new_sub_type = "bulanan"
                new_expiry = db_expiry if (db_status == "WizardMemberBulanan" and db_expiry) else (datetime.utcnow() + timedelta(days=30)).isoformat()
            elif resolved_status == "WizardMemberTahunan":
                new_sub_type = "tahunan"
                new_expiry = db_expiry if (db_status == "WizardMemberTahunan" and db_expiry) else (datetime.utcnow() + timedelta(days=365)).isoformat()

            await Database.update_user_status(
                user_id=user_id,
                status=resolved_status,
                subscription_type=new_sub_type,
                expiry_date=new_expiry
            )

            # Kirim DM notifikasi ke user
            try:
                if resolved_status in ["WizardMemberBulanan", "WizardMemberTahunan"]:
                    sub_title = "Bulanan" if resolved_status == "WizardMemberBulanan" else "Tahunan"
                    embed = discord.Embed(
                        title="🎉 Selamat! Anda Diupgrade",
                        description=(
                            f"Halo {after.display_name},\n\n"
                            f"Anda telah diupgrade menjadi **{sub_title} Wizard Member** di server **{guild.name}**.\n\n"
                            f"🗓️ Berlaku hingga: **{new_expiry.split('T')[0]}**\n"
                            f"Terima kasih telah mempercayai layanan premium kami! 💎"
                        ),
                        color=discord.Color.gold() if sub_title == "Bulanan" else discord.Color(COLOR_VIOLET)
                    )
                    await after.send(embed=embed)
                elif db_status in ["WizardMemberBulanan", "WizardMemberTahunan"] and resolved_status == "member":
                    # Downgrade dari Wizard ke Member
                    dm_embed = discord.Embed(
                        title="⚠️ Langganan Berakhir",
                        description=(
                            f"Halo {after.display_name},\n\n"
                            "Langganan **WizardMember** Anda telah berakhir.\n"
                            "Akses Anda kini kembali ke status **member biasa**.\n\n"
                            "Anda masih dapat memperpanjang kapan pun untuk kembali menikmati fitur premium. 💎"
                        ),
                        color=discord.Color(COLOR_DARK)
                    )
                    await after.send(embed=dm_embed)
                elif resolved_status == "Admin":
                    dm_embed = discord.Embed(
                        title="👑 Akses Admin Diaktifkan",
                        description=(
                            f"Halo {after.display_name},\n\n"
                            f"Anda sekarang memiliki peran **Admin** di server **{guild.name}**."
                        ),
                        color=discord.Color(COLOR_VIOLET)
                    )
                    await after.send(dm_embed)
                elif resolved_status == "member" and db_status == "PendingVerification":
                    dm_embed = discord.Embed(
                        title="✅ Verifikasi Selesai",
                        description=(
                            f"Halo {after.display_name},\n\n"
                            f"Verifikasi Anda selesai! Anda sekarang adalah **Member** resmi di server **{guild.name}**."
                        ),
                        color=discord.Color(COLOR_GREEN)
                    )
                    await after.send(dm_embed)
            except discord.Forbidden:
                logging.warning(f"Tidak dapat mengirim DM ke {after.display_name} (DM tertutup).")

            # Kirim log ke channel admin
            admin_log = discord.utils.get(guild.text_channels, name="laporan")
            if admin_log:
                if resolved_status in ["WizardMemberBulanan", "WizardMemberTahunan"]:
                    await admin_log.send(
                        f"✅ **{after.display_name}** diupgrade ke **{resolved_status}** (berlaku sampai {new_expiry.split('T')[0]})."
                    )
                elif db_status in ["WizardMemberBulanan", "WizardMemberTahunan"] and resolved_status == "member":
                    await admin_log.send(
                        f"⚠️ **{after.display_name}** kehilangan status WizardMember dan diturunkan menjadi member biasa."
                    )
                elif resolved_status == "Admin":
                    await admin_log.send(
                        f"👑 **{after.display_name}** sekarang memiliki role **Admin**."
                    )
                elif db_status == "Admin" and resolved_status != "Admin":
                    await admin_log.send(
                        f"👤 **{after.display_name}** telah kehilangan role Admin dan statusnya disinkronkan ke **{resolved_status}**."
                    )
                elif resolved_status == "member" and db_status == "PendingVerification":
                    await admin_log.send(
                        f"✅ **{after.display_name}** berhasil diverifikasi sebagai **Member**."
                    )
                else:
                    await admin_log.send(
                        f"🔄 **{after.display_name}** status berubah dari **{db_status}** menjadi **{resolved_status}**."
                    )

            logging.info(
                f"[on_member_update] {after.display_name} (ID: {user_id}) status diupdate ke {resolved_status}"
            )

    except Exception as e:
        logging.error(f"Error pada on_member_update Check Subscription: {e}", exc_info=True)
        
@bot.event
async def on_message(message):
    # Abaikan pesan dari bot
    if message.author.bot:
        return
    
    # Channel yang diawasi: lounge-chat utama dan thread turunannya
    valid_parents = ["lounge-chat", "share-your-profits", "member-voice", "member-stage", "wizard-voice", "wizard-stage", "wizard-lounge-chat"]
    
    # Identifikasi channel utama
    parent_channel = message.channel
    if isinstance(message.channel, discord.Thread):
        # Jika ini thread, gunakan parent channel-nya
        parent_channel = message.channel.parent
    
    # Periksa apakah channel termasuk yang diawasi
    if parent_channel and parent_channel.name not in valid_parents:
        await bot.process_commands(message)
        return
    
    # 1. Deteksi spam di channel utama saja (bukan thread)
    if not isinstance(message.channel, discord.Thread) and message.channel.name == "lounge-chat":
        spam_data = await Database.get_spam(message.author.id)
        if spam_data:
            last_msg, count = spam_data
            if last_msg == message.content:
                count += 1
                await Database.update_spam(message.author.id, message.content, count)
                
                # Terapkan sanksi jika spam berulang
                if count > 3:
                    await message.delete()
                    await message.channel.send(
                        f"{message.author.mention}, Anda mengirim pesan berulang lebih dari 3x! ✘",
                        delete_after=5
                    )
                    return
            else:
                await Database.update_spam(message.author.id, message.content, 1)
        else:
            await Database.update_spam(message.author.id, message.content, 1)
    
    # 2. Filter kata terlarang (berlaku di main channel DAN thread)
    lowered = message.content.lower()
    if any(bad_word in lowered for bad_word in BLACKLIST_WORDS):
        await message.delete()
        count = await Database.add_violation(message.author.id)
        
        # Format lokasi pelanggaran
        if isinstance(message.channel, discord.Thread):
            location = f"{parent_channel.mention} > {message.channel.mention}"
        else:
            location = parent_channel.mention
            
        # Buat laporan ke channel admin
        await send_laporan_embed(
            bot,
            judul="🚨 Pelanggaran Terdeteksi",
            deskripsi=f"User {message.author.mention} melakukan pelanggaran di {location}",
            fields=[
                ("User", f"{message.author} ({message.author.id})"),
                ("Isi Pesan", f"```{message.content[:800]}```" if message.content else "[Konten Kosong]"),
                ("Jumlah Pelanggaran", str(count)),
                ("Waktu", f"<t:{int(time.time())}:F>")
            ],
            warna=0xe74c3c,
            thumbnail="https://cdn-icons-png.flaticon.com/512/595/595067.png"
        )
        
        # Sistem sanksi bertingkat
        if count < WARNING_LIMIT:
            # Peringatan saja
            try:
                warning_msg = await message.channel.send(
                    f"{message.author.mention} ⚠️ Peringatan {count}/{WARNING_LIMIT}: Pesan Anda melanggar ketentuan server!",
                    delete_after=10
                )
            except:
                pass
            
        elif count == WARNING_LIMIT:
            # Mute dengan durasi
            mute_role = discord.utils.get(message.guild.roles, name="Muted")
            if not mute_role:
                mute_role = await message.guild.create_role(
                    name="Muted",
                    reason="Auto-create peran muted"
                )
                # Set permission di semua channel
                for ch in message.guild.channels:
                    try:
                        await ch.set_permissions(mute_role, send_messages=False)
                    except:
                        pass
            
            try:
                await message.author.add_roles(mute_role)
                # Notifikasi
                notify = await message.channel.send(
                    f"⛔ {message.author.mention} di-mute selama {MUTE_DURATION} menit karena pelanggaran!",
                    delete_after=15
                )
                # Jadwalkan unmute
                bot.loop.create_task(unmute_later(member=message.author, mute_role=mute_role, duration_minutes=MUTE_DURATION))
            except Exception as e:
                logging.error(f"Gagal mute user {message.author.id}: {str(e)}")
                
        elif count >= MUTE_LIMIT:
            # Kick user
            try:
                reason = f"Melanggar peraturan ({count}x pelanggaran)"
                await message.author.kick(reason=reason)
                await message.channel.send(
                    f"🚫 {message.author.mention} dikeluarkan karena pelanggaran berulang!",
                    delete_after=10
                )
            except Exception as e:
                logging.error(f"Gagal kick user {message.author.id}: {str(e)}")
                
        elif count >= KICK_LIMIT:
            # Ban permanen
            try:
                reason = f"Pelanggaran berat ke-{count}x"
                await message.author.ban(reason=reason, delete_message_days=0)
                await message.channel.send(
                    f"🚨 {message.author.mention} DI-BAN PERMANEN karena pelanggaran berat!",
                    delete_after=10
                )
            except Exception as e:
                logging.error(f"Gagal ban user {message.author.id}: {str(e)}")
                
        return
    
    # Lanjutkan pemrosesan command
    await bot.process_commands(message)

async def unmute_later(member, mute_role, duration_minutes):
    await asyncio.sleep(duration_minutes * 60)
    await member.remove_roles(mute_role)
    await Database.reset_violations(member.id)
    try:
        await member.send("Mute kamu sudah dicabut. Silakan gunakan #lounge-chat dengan bijak and patuhi peraturan server.")
    except:
        pass

@bot.command()
@commands.has_permissions(administrator=True)
async def setupserver(ctx):
    """Setup struktur server + sinkronisasi database"""
    # Setup logging ekstra untuk perintah ini
    log_header = f"[SETUPSERVER] [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"
    logger = logging.getLogger('discord.setupserver')
    
    try:
        # 1. Siapkan lingkungan eksekusi
        admin = ctx.author
        guild = ctx.guild
        original_channel = ctx.channel
        start_time = datetime.now(jakarta_tz)
        
        # List untuk menampung semua laporan output
        status_reports = []
        errors = []
        
        # 2. Fungsi untuk mengirim update status secara aman
        async def safe_update(content: str, critical=False):
            """Kirim update status ke berbagai saluran sebagai fallback"""
            targets = []
            
            # Prioritas: channel asal -> DM admin -> channel laporan
            targets.append(original_channel)
            targets.append(admin)
            
            # Tambahkan channel laporan jika berbeda
            laporan_ch = discord.utils.get(guild.text_channels, name="laporan")
            if laporan_ch and laporan_ch.id != original_channel.id:
                targets.append(laporan_ch)
                
            # Kirim ke semua target sampai berhasil
            sent = False
            failure_reason = ""
            
            for target in targets:
                try:
                    if isinstance(target, discord.TextChannel):
                        if critical:
                            msg = f"🚨 {content}"
                        else:
                            msg = f"ℹ️ {content}"
                            
                        await target.send(msg)
                        sent = True
                        break
                    elif isinstance(target, discord.Member):
                        await target.send(content)
                        sent = True
                        break
                except discord.Forbidden as fe:
                    failure_reason = f" Forbidden({target})"
                except discord.NotFound as nfe:
                    failure_reason = f" NotFound({target})"
                except Exception as e:
                    failure_reason = f" Error({type(e).__name__})"
            
            if not sent:
                logger.error(f"FAILED TO SEND UPDATE: {content} | Reason: {failure_reason}")
            return sent
        
        # 3. Kirim notifikasi awal
        try:
            start_msg = await ctx.send("🏗️ **Memulai setup server...** (`Proses bisa memakan waktu ±3 menit`)")
            status_reports.append(start_msg)
        except Exception:
            await safe_update("🏗️ Setup server dimulai... Silakan tunggu")
        
        # 4. Eksekusi langkah-langkah setup
        current_step = ""
        
        try:
            # Step 1: Inisialisasi server
            current_step = "Setup struktur server"
            logger.info(f"{log_header} Step: {current_step}")
            await safe_update("🛠️ Memulai inisialisasi struktur server...")
            
            # Jalankan setup server dengan timeout protection
            try:
                server_result = await asyncio.wait_for(
                    ServerBuilder.setup_server(guild),
                    timeout=300  # Timeout 5 menit
                )
                await safe_update(f"✅ Struktur server selesai! Hasil: {server_result}")
            except asyncio.TimeoutError:
                await safe_update("⚠️ Waktu setup server habis! Lanjut ke penerapan izin...", True)
            
            # Step 2: Terapkan izin channel
            current_step = "Penerapan izin channel"
            logger.info(f"{log_header} Step: {current_step}")
            await safe_update("🔐 Menerapkan izin channel...")
            
            success_count, error_count, permission_errors = await apply_channel_permissions(guild)
            
            # Catat error untuk laporan akhir
            if permission_errors:
                errors.extend(permission_errors)
            
            # Step 3: Sinkronisasi database
            current_step = "Sinkronisasi user & role"
            logger.info(f"{log_header} Step: {current_step}")
            await safe_update("🔄 Memulai sinkronisasi user dan role...")
            
            sync_report = await synchronize_users_and_roles(guild)
            
            # Step 4: Kirim konten ke roadmap_trader - PASTIKAN CHANNEL ADA
            current_step = "Pengiriman roadmap trader"
            logger.info(f"{log_header} Step: {current_step}")
            await safe_update("📝 Mengirim konten ke channel roadmap_trader...")
            
            # Coba dapatkan channel roadmap_trader
            roadmap_channel = discord.utils.get(guild.text_channels, name="roadmap_trader")
            
            # Jika channel tidak ada, buat secara darurat
            if not roadmap_channel:
                await safe_update("⚠️ Channel #roadmap_trader tidak ditemukan, membuat secara manual...", True)
                
                # Cari kategori NEXUS HUB (harusnya ada di struktur server)
                nexus_category = discord.utils.get(guild.categories, name="🔥|NEXUS HUB|")
                if not nexus_category:
                    nexus_category = await guild.create_category("🔥|NEXUS HUB|")
                    await asyncio.sleep(1)  # Beri waktu sinkronisasi
                
                # Buat channel roadmap_trader
                roadmap_channel = await guild.create_text_channel(
                    name="roadmap_trader",
                    category=nexus_category,
                    topic="Perjalanan seorang trader yang berkelanjutan",
                    position=3,  # Posisi di dalam kategori
                    overwrites={
                        guild.default_role: discord.PermissionOverwrite(read_messages=True)
                    }
                )
                await safe_update(f"✅ Channel #roadmap_trader berhasil dibuat (ID: {roadmap_channel.id})")
            
            # Step 5: Kirim roadmap trader ke channel
            try:
                await send_roadmap_trader(roadmap_channel)
                await safe_update("✅ Konten roadmap trader berhasil dikirim!")
                
                # Konfirmasi ke channel asal
                try:
                    if original_channel != roadmap_channel:
                        await original_channel.send("✅ Roadmap trader telah dikirim ke channel #roadmap_trader")
                except discord.NotFound:
                    await roadmap_channel.send("✅ Setup server selesai! Roadmap trader telah dikirim")
            except Exception as e:
                error_msg = f"Gagal mengirim konten roadmap trader: {str(e)}"
                errors.append(error_msg)
                await safe_update(error_msg, True)
                logger.error(error_msg, exc_info=True)
            
            # Step 6: Setup thread analisis (opsional)
            try:
                current_step = "Setup thread analisis"
                channel = discord.utils.get(guild.text_channels, name="wizard-analisis")
                if channel:
                    created_threads = await create_analysis_threads(channel)
                    if created_threads:
                        await safe_update(f"✅ Thread Wizard Analisis dibuat: {', '.join(created_threads)}")
                        # Sinkronisasi member ke thread
                        await sync_members_to_threads(guild)
            except Exception as e:
                error_msg = f"Gagal setup thread: {str(e)}"
                errors.append(error_msg)
                await safe_update(error_msg, True)
            
            # Laporkan selesai
            duration = (datetime.now(jakarta_tz) - start_time).total_seconds()
            await safe_update(f"🟢 Semua proses setup selesai! Durasi: {duration:.1f} detik")
            
        except Exception as step_error:
            # Tangkap error di level langkah utama
            error_msg = f"🔥 **GAGAL** pada langkah `{current_step}`: {str(step_error)}"
            errors.append(error_msg)
            logger.critical(f"{log_header} SETUP FAILED AT STEP {current_step}: {str(step_error)}", exc_info=True)
            await safe_update(error_msg, True)
        
        # 5. Buat laporan akhir
        try:
            # Kompilasi laporan
            duration = (datetime.now(jakarta_tz) - start_time).total_seconds()
            result_message = [
                f"## 🤖 Laporan Setup Server",
                f"**Server**: {guild.name}",
                f"**Admin**: {admin.mention}",
                f"**Durasi**: {duration:.2f} detik",
                f"**Selesai**: <t:{int(time.time())}:R>",
                ""
            ]
            
            # Tambahkan hasil sinkronisasi
            if 'sync_report' in locals():
                result_message.append("### 🔄 Sinkronisasi User/Role")
                result_message.append(f"```\n{sync_report}\n```")
            
            # Tambahkan statistik izin
            result_message.append(f"### 🔓 Izin Channel")
            result_message.append(f"Channel berhasil: **{success_count}**")
            result_message.append(f"Error izin: **{error_count}**")
            
            # Tambahkan error jika ada
            if errors:
                result_message.append("### 🚨 Error yang Terjadi")
                for i, error in enumerate(errors[:5]):  # Maks 5 error
                    result_message.append(f"{i+1}. {error}")
                    
            # Potong jika terlalu panjang
            full_report = "\n".join(result_message)
            if len(full_report) > 2000:
                full_report = full_report[:1900] + "\n... [laporan dipotong]"
            
            # Kirim laporan utama
            await safe_update(full_report)
            
        except Exception as report_error:
            logger.error(f"{log_header} FAILED TO SEND FINAL REPORT: {str(report_error)}")
            try:
                await admin.send("ℹ️ Setup selesai tapi ada masalah dengan laporan. Cek log server")
            except:
                logger.critical("COMPLETE REPORT DELIVERY FAILURE")
                
    except Exception as outer_error:
        # Tangani error komprehensif yang mungkin terjadi
        logger.critical(f"{log_header} OUTER SETUP ERROR: {str(outer_error)}", exc_info=True)
        
        try:
            # Usaha kirim ke admin
            error_message = (
                f"🚨 **EMERGENCY SYSTEM FAILURE**\n"
                f"Error global saat eksekusi setup server:\n"
                f"```{str(outer_error)}```\n"
                f"Timestamp: {datetime.now(jakarta_tz).isoformat()}\n"
                "Silakan cek log server untuk detail!"
            )
            
            # Coba kirim ke admin dengan berbagai metode
            await admin.send(error_message[:2000])  # Pastikan tidak melebihi batas karakter
        except:
            logger.critical("ABSOLUTE FAILURE: CANNOT NOTIFY ADMIN")

async def send_roadmap_trader(channel: discord.TextChannel):
    """Kirim roadmap trader ke channel tertentu"""
    # Clear existing messages
    try:
        await channel.purge(limit=100)
        await asyncio.sleep(1)
    except Exception as e:
        logging.error(f"Gagal membersihkan channel roadmap: {str(e)}")
    
    # =====================================================================
    # Embed 1: Cover Roadmap
    embed1 = discord.Embed(
        title="🚀 ROADMAP TRADER",
        description=(
            "```diff\n"
            "+======= JOURNEY MENUJU TRADER ======+\n"
            "|   SUKSES BERKELANJUTAN & BERMAKNA  |\n"
            "+====================================+\n"
            "|     Alur Terstruktur Membangun     |\n"
            "|    Karir Trading Jelas dan Kokoh   |\n"
            "+====================================+\n"
            "```"),
        color=COLOR_VIOLET
    )
    
    # Embed 2: Step 1
    embed2 = discord.Embed(
        color=COLOR_GREEN
    )
    embed2.add_field(
        name="➊ ILMU DASAR SEORANG TRADER",
        value=(
            "```\n"
            "├──🔹 Apa yang dimaksud dengan \n"
            "│     aset kripto, forex, komoditas\n"
            "├──🔹 Bagaimana terbentuknya suatu aset\n"
            "│     kripto, forex, komoditas ?\n"
            "├──🔹 Bagaimana cara memperoleh dan menjual\n"
            "│     suatu aset kripto, forex, komoditas?\n"
            "├──🔹 Apa saja faktor yang menyebabkan\n"
            "│     fluktuasi harga suatu aset\n"
            "│     kripto, forex, komoditas?\n"
            "```"
        ),
        inline=False
    )
    embed2.set_footer(text="Fase Pembangunan Pondasi")

    # Embed 3: Step 2
    embed3 = discord.Embed(
        color=COLOR_GREEN
    )
    embed3.add_field(
        name="➋ PSIKOLOGI DAN MENTAL TRADER",
        value=(
            "```\n"
            "├──🔸 Mengontrol nafsu dan emosi\n"
            "│     (fase takut & serakah)\n"
            "├──🔸 Membangun disiplin eksekusi trading\n"
            "│     yang konsisten\n"
            "├──🔸 Teknik manajemen stres saat loss\n"
            "├──🔸 Mindset dan perilaku sifat seorang\n"
            "│     profesional trader jangka panjang\n"
            "```"
        ),
        inline=False
    )
    embed3.set_footer(text="Fase Penguasaan Diri")

    # Embed 4: Step 3
    embed4 = discord.Embed(
        color=COLOR_GREEN
    )
    embed4.add_field(
        name="➌ RISK REWARD DAN MONEY MANAGEMENT",
        value=(
            "```\n"
            "├──🔹 Menetapkan rasio risk:reward optimal\n"
            "├──🔹 Teknik menentukan ukuran posisi\n"
            "│     (position sizing) yang aman\n"
            "├──🔹 Pengaturan stop loss dan take\n"
            "│     profit efektif\n"
            "└──🔹 Strategi diversifikasi portofolio\n"
            "```"
        ),
        inline=False
    )
    embed4.set_footer(text="Fase Perlindungan Modal")

    # Embed 5: Step 4
    embed5 = discord.Embed(
        color=COLOR_GREEN
    )
    embed5.add_field(
        name="➍ STRATEGI OPEN POSISI",
        value=(
            "```\n"
            "├──🔸 Mengembangkan rencana trading\n"
            "│     komprehensif\n"
            "├──🔸 menggunakan dan Membangun strategi\n"
            "│     dengan sumberdaya yang ada\n"
            "├──🔸 Identifikasi pola entry/exit presisi\n"
            "├──🔸 Manajemen posisi dinamis sesuai\n"
            "│     kondisi pasar\n"
            "├──🔸 Backtesting dan forward testing\n"
            "│     strategi\n"
            "```"
        ),
        inline=False
    )
    embed5.set_footer(text="Fase Penyempurnaan Sistem")
    
    # Embed 6: Step 5
    embed6 = discord.Embed(
        color=COLOR_GREEN
    )
    embed6.add_field(
        name="➎ SESI AWAL TRADE (FASE TOURNAMENT)",
        value=(
            "```\n"
            "├──🔸 Cari dan Ikuti Tournament Trading yang\n"
            "│     Akan datang\n"
            "├──🔸 Ikuti Tournament Secara Disiplin\n"
            "│     Untuk Mengasah Skill Trading dan \n"
            "│     mengumpulkan modal trading jangka\n"
            "│     panjang(portofolio Pribadi)\n"
            "├──🔸 Mempunyai target jangka panjang yang jelas\n"
            "│     misal memenangkan Tournament 4-5 X\n"
            "│     berturut-turut\n"
            "├──🔸 Setelah mengumpulkan  dana dari Tournament\n"
            "│     dari Tournament gunakan modal untuk \n"
            "│     trading di portofolio pribadi\n"
            "```"
        ),
        inline=False
    )
    embed6.set_footer(text="Fase penyempurnaan Skill dan modal")
    
    # Embed 7: Step 6
    embed7 = discord.Embed(
        color=COLOR_GREEN
    )
    embed7.add_field(
        name="➏ KOMITMEN PADA PORTOFOLIO PRIBADI",
        value=(
            "```\n"
            "├──🔸 Mempersiapkan rencana trading rill\n"
            "│     untuk portofolio pribadi\n"
            "├──🔸 menggunakan strategi sesuai trading\n"
            "│     untuk keberhasilan jangka panjang\n"
            "```"
        ),
        inline=False
    )
    embed7.set_footer(text="Fase Pembukaan akun rill")
    
    # Embed 8: Step 7
    embed8 = discord.Embed(
        color=COLOR_GREEN
    )
    embed8.add_field(
        name="➐ KOMITMEN DAN KONSISTENSI",
        value=(
            "```\n"
            "├──🔹 Pembuatan trading journal rutin\n"
            "├──🔹 Review performa strategi berkala\n"
            "├──🔹 Evaluasi berkelanjutan dan\n"
            "│     penyempurnaan metode strategi\n"
            "├──🔹 Disiplin terhadap rencana trading\n"
            "│     jangka panjang\n"
            "```"
        ),
        inline=False
    )
    embed8.set_footer(text="Fase Pembentukan Rutinitas")

    # Embed 9: Step 8
    embed9 = discord.Embed(
        color=COLOR_GREEN
    )
    embed9.add_field(
        name="➑ AKUMULASI ASET SIGNIFIKAN",
        value=(
            "```\n"
            "├──🔸 Teknik pengkompaunan modal efektif\n"
            "├──🔸 Diversifikasi aliran pendapatan\n"
            "│     (multi-instrumen)\n"
            "├──🔸 Pengelolaan pertumbuhan portofolio\n"
            "│     yang bijak\n"
            "└──🔸 Pengembangan pendapatan pasif\n"
            "```"
        ),
        inline=False
    )
    embed9.set_footer(text="Fase Akumulasi Kekayaan")

    # Embed 10: Step 9
    embed10 = discord.Embed(
        color=COLOR_GREEN
    )
    embed10.add_field(
        name="➒ GUNAKAN ASET UNTUK KEBAIKAN",
        value=(
            "```\n"
            "├──🔹 membelanjakan kebutuhan seperti\n"
            "│     sandang pangan dan lainya\n"
            "│     untuk kebutuhan hidup di \n"
            "│     masyarakat yang tidak dan belum mampu\n"
            "├──🔹 dukungan sandang pangan tempat tinggal\n"
            "│     yang berkelanjutan jangka panjang\n"
            "│     untuk masyarakat\n"
            "├──🔹 Dukungan pendidikan finansial\n"
            "│     masyarakat\n"
            "├──🔹 Investasi dalam bisnis pemberdaya\n"
            "│     ekonomi lokal\n"
            "├──🔹 Filantropi strategis jangka panjang\n"
            "└──🔹 Membangun warisan keberlanjutan\n"
            "```"
        ),
        inline=False
    )
    embed10.set_footer(text="Fase Pemberian Makna")

    # Embed 11: Step 10 & 9
    embed11 = discord.Embed(
        color=COLOR_VIOLET
    )
    embed11.add_field(
        name="➓ MENINGGAL DALAM BAHAGIA & KEDAMAIAN ABADI",
        value=(
            "```\n"
            "├──✅ Kebebasan finansial penuh tanpa\n"
            "│     ketergantungan\n"
            "├──✅ Kemerdekaan waktu dan lokasi\n"
            "├──✅ Kepuasan batin dan ketenangan jiwa\n"
            "└──✅ Warisan positif bagi generasi mendatang\n"
            "+=======================================+\n"
            "|  🏁 FINISHED: Meninggalkan dunia      |\n"
            "|dalam kondisi kembali kosong kepenuhan |\n"
            "|   makna, spiritual dan kedamaian      |\n"
            "+=======================================+\n"
            "```"
        ),
        inline=False
    )
    embed11.set_footer(text="Puncak Perjalanan Trader")

    # Kirim dengan jeda anti rate limit
    embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8, embed9,embed10,embed11]
    for embed in embeds:
        try:
            await channel.send(embed=embed)
            await asyncio.sleep(0.8)  # Jeda antara pengiriman
        except Exception as e:
            logging.error(f"Gagal mengirim embed: {str(e)}")
    
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Daftar Perintah Bot", color=COLOR_CYAN)
    embed.add_field(name="!setupserver", value="Setup ulang seluruh struktur server (ADMIN ONLY)", inline=False)
    embed.add_field(name="Interaksi", value="Gunakan tombol di channel kontrol-pengguna/kontrol-admin untuk fitur lainnya.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def kontrolpengguna(ctx):
    await send_kontrol_pengguna_embed(ctx.channel)

@bot.command(name="loungechat", aliases=["obrolan"])
async def loungechat(ctx):
    await send_obrolan_embed(ctx.channel)

@bot.command()
async def bantuan(ctx):
    await send_bantuan_embed(ctx.channel)

@bot.command()
@commands.has_permissions(administrator=True)
async def kontroladmin(ctx):
    await send_kontrol_admin_embed(ctx.channel)

@bot.command()
@commands.has_permissions(administrator=True)
async def syncusers(ctx):
    """Jalankan sinkronisasi sistem"""
    try:
        msg = await ctx.send("🔄 Memulai sinkronisasi database-server...")
        result = await synchronize_users_and_roles(ctx.guild)
        await msg.edit(content=f"✅ {result}")
    except Exception as e:
        await ctx.send(f"❌ Error selama sinkronisasi: {str(e)}")

@bot.command()
@commands.has_permissions(administrator=True)
async def verifsync(ctx):
    """Manual trigger untuk sinkronisasi verifikasi"""
    try:
        await synchronize_users_and_roles(ctx.guild)
        await VerificationSystem.apply_verification_workflow(guild=ctx.guild)
        await ctx.send("✅ Sistem verifikasi berhasil disinkronisasi!")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@commands.has_permissions(administrator=True)
async def verif_sync(ctx):
    """Paksa sinkronisasi verifikasi"""
    result = await sync_verification_system(ctx.guild)
    await ctx.send(result)

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_verifikasi(ctx: commands.Context):
    """Setup channel verifikasi dengan tombol interaktif"""
    channel = discord.utils.get(ctx.guild.channels, name="verifikasi")
    if not channel:
        return await ctx.send("❌ Channel #verifikasi tidak ditemukan")
    
    await VerificationSystem.update_verification_channel(channel)
    await ctx.send("✅ Sistem verifikasi berhasil diinstal!")

@bot.command()
@commands.has_permissions(administrator=True)
async def forcesync(ctx):
    """Paksa sinkronisasi segera"""
    start_msg = await ctx.send("⏳ Memulai sinkronisasi paksa...")
    result = await synchronize_users_and_roles(ctx.guild)
    await start_msg.edit(content=f"✅ {result}")

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_threads(ctx):
    """Setup thread Wizard Analisis"""
    channel = discord.utils.get(ctx.guild.text_channels, name="wizard-analisis")
    
    if not channel:
        await ctx.send("❌ Channel #wizard-analisis tidak ditemukan")
        return
    
    try:
        msg = await ctx.send("🔄 Membuat thread analisis...")
        created = await create_analysis_threads(channel)
        
        if created:
            await msg.edit(content=f"✅ Thread berhasil dibuat: {', '.join(created)}")
        else:
            await msg.edit(content="ℹ️ Semua thread sudah ada, tidak ada yang baru dibuat")
            
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")
        
async def sync_members_to_threads(guild: discord.Guild):
    """
    Sinkronisasi semua WizardMember (Bulanan & Tahunan) serta Admin
    ke thread Wizard Analisis.
    """
    try:
        # 1️⃣ Cari channel utama untuk Wizard Analisis
        channel = discord.utils.get(guild.text_channels, name="wizard-analisis")
        if not channel:
            logging.warning(f"Tidak ditemukan channel 'wizard-analisis' di {guild.name}")
            return

        # 2️⃣ Ambil semua thread aktif (non-archived)
        active_threads = [t for t in channel.threads if not t.archived]
        if not active_threads:
            logging.info(f"Tidak ada thread aktif di {channel.name}")
            return

        # 3️⃣ Ambil semua target member (Wizard & admin)
        target_members = []
        for member in guild.members:
            if any(role.name in ["WizardMemberBulanan", "WizardMemberTahunan", "Admin"] for role in member.roles):
                target_members.append(member)

        logging.info(f"🧩 {len(target_members)} member premium (Wizard Member)/admin akan disinkronkan ke thread analisis.")

        # 4️⃣ Sinkronisasi ke setiap thread
        for thread in active_threads:
            added_count = 0
            for member in target_members:
                try:
                    # Cek apakah member sudah tergabung
                    if member not in thread.members:
                        await thread.add_user(member)
                        added_count += 1
                except discord.Forbidden:
                    logging.warning(f"Bot tidak punya izin menambahkan {member.name} ke thread {thread.name}.")
                except discord.HTTPException as e:
                    logging.error(f"HTTP Error menambahkan {member.name} ke thread {thread.name}: {str(e)}")
                except Exception as e:
                    logging.error(f"Gagal menambahkan {member.name} ke thread {thread.name}: {str(e)}")

            logging.info(f"✅ Menambahkan {added_count} user baru ke thread {thread.name}")

        logging.info(f"🎯 Sinkronisasi thread analisis selesai untuk {guild.name}")

    except Exception as e:
        logging.error(f"❌ Error di sync_members_to_threads: {str(e)}", exc_info=True)
        

# --- Task background untuk menjaga kategori tetap aktif ---
class CategoryMaintainer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ensure_categories.start()

    def cog_unload(self):
        self.ensure_categories.cancel()

    @tasks.loop(minutes=1)
    async def ensure_categories(self):
        """Loop setiap menit untuk memastikan kategori & channel tetap aktif dan aman."""
        try:
            for guild in self.bot.guilds:
                if not guild.me.guild_permissions.manage_channels or not guild.me.guild_permissions.manage_roles:
                    logging.warning(f"[CategoryMaintainer] Bot lacks necessary permissions (Manage Channels / Manage Roles) in guild '{guild.name}'")
                    continue

                for cat_config in SERVER_STRUCTURE:
                    try:
                        cat_name, allowed_roles, channels = cat_config
                        category = discord.utils.get(guild.categories, name=cat_name)

                        if category is None:
                            # Buat kategori baru jika hilang dengan overwrites yang tepat agar aman
                            overwrites = {
                                guild.default_role: discord.PermissionOverwrite(read_messages=False)
                            }
                            for role_name in allowed_roles:
                                role = discord.utils.get(guild.roles, name=role_name.replace("@", ""))
                                if role:
                                    overwrites[role] = discord.PermissionOverwrite(read_messages=True)

                            try:
                                category = await guild.create_category(cat_name, overwrites=overwrites)
                                print(f"[AutoFix] Kategori '{cat_name}' dibuat ulang dengan pengamanan izin.")
                            except Exception as e:
                                logging.error(f"[CategoryMaintainer] Gagal membuat kategori '{cat_name}': {e}")
                                continue

                        # Pastikan channel di dalam kategori ada dan aktif
                        for ch_info in channels:
                            try:
                                ch_name = ch_info[0]
                                desc = ch_info[1]
                                ch_roles = ch_info[2]
                                channel = discord.utils.get(category.channels, name=ch_name)

                                if channel is None:
                                    # Bangun overwrites untuk channel
                                    channel_overwrites = {
                                        guild.default_role: discord.PermissionOverwrite(read_messages=False)
                                    }
                                    # Beri izin berdasarkan allowed roles kategori
                                    for role_name in allowed_roles:
                                        role = discord.utils.get(guild.roles, name=role_name.replace("@", ""))
                                        if role:
                                            channel_overwrites[role] = discord.PermissionOverwrite(read_messages=True)

                                    # Modifikasi izin spesifik channel
                                    for role_name in ch_roles:
                                        if role_name == "@everyone":
                                            channel_overwrites[guild.default_role] = discord.PermissionOverwrite(read_messages=True)
                                        else:
                                            role = discord.utils.get(guild.roles, name=role_name.replace("@", ""))
                                            if role:
                                                if ch_name in CHANNEL_PERMISSIONS:
                                                    if role_name in CHANNEL_PERMISSIONS[ch_name]:
                                                        perm_overwrite = discord.PermissionOverwrite()
                                                        for perm, value in CHANNEL_PERMISSIONS[ch_name][role_name].items():
                                                            setattr(perm_overwrite, perm, value)
                                                        channel_overwrites[role] = perm_overwrite

                                    ch_type = ch_info[3] if len(ch_info) > 3 else "text"
                                    if ch_type == "voice":
                                        await category.create_voice_channel(ch_name, overwrites=channel_overwrites)
                                    elif ch_type == "stage":
                                        await category.create_stage_channel(ch_name, overwrites=channel_overwrites)
                                    else:
                                        await category.create_text_channel(ch_name, topic=desc, overwrites=channel_overwrites)
                                    print(f"[AutoFix] Channel '{ch_name}' ({ch_type}) dibuat di kategori '{cat_name}' dengan pengamanan izin.")
                            except Exception as ch_err:
                                logging.error(f"[CategoryMaintainer] Error checking/creating channel in category '{cat_name}': {ch_err}")
                    except Exception as cat_err:
                        logging.error(f"[CategoryMaintainer] Error checking/creating category: {cat_err}")
        except Exception as global_err:
            logging.error(f"[CategoryMaintainer] Critical global error in ensure_categories loop: {global_err}")

    @ensure_categories.before_loop
    async def before_ensure_categories(self):
        await self.bot.wait_until_ready()


# --- Tambahkan ke setup bot utama ---
async def setup(bot):
    await bot.add_cog(CategoryMaintainer(bot))
    
# ===================== RUN BOT =====================
"""
Entrypoint utama untuk menjalankan bot
"""
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
    
# ===================== END OF FILE =====================
