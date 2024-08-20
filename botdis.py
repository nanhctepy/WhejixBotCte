import random
import asyncio
import discord
from colorama import Fore, Style
from time import sleep,strftime
import requests
import datetime
from atexit import register
from time import sleep
import sys
import threading,base64
import os,time,re,json,random
from discord import FFmpegPCMAudio
from discord import Permissions
from discord.ext import commands, tasks
from discord.utils import get
from urllib.parse import quote
import os
import ssl
from urllib.parse import urlencode
from http import cookiejar
from urllib3.exceptions import InsecureRequestWarning
import hashlib
import random
from colorama import Fore, Style, init
from http.client import HTTPSConnection

try:
    import base64
    from requests.exceptions import RequestException
    import requests
    import pystyle
    from concurrent.futures import ThreadPoolExecutor
    from faker import Faker
    from requests import session
    import concurrent.futures
    
except ImportError:
    import os
    os.system("pip install faker")
    os.system("pip install colorama")
    os.system("pip install requests")
    os.system("pip install pystyle")
    os.system("pip install concurrent.futures")
    os.system("pip install base64")
import requests,os,time,re,json,uuid,random,sys
from concurrent.futures import ThreadPoolExecutor
import datetime
import requests,json
import uuid
import requests
from time import sleep
from random import choice, randint, shuffle
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
from os.path import isfile
from pystyle import Colors, Colorate, Write, Center, Add, Box
from time import sleep,strftime
import socket
from pystyle import *
import json,requests,time
import string
import secrets
import time
from itertools import cycle

from discord import app_commands
CHANNELS = None
VOICE = None
ROLE = None
NAME = None
white_list = None
MSG = None
boucle2 = True
sent_count = 0
MAX_RETRIES = 3
MAX_MESSAGES_BEFORE_CLEAR = 100
from bs4 import BeautifulSoup




TOKEN = "MTIzOTg4MTAxMDgxMzA3NTUxNg.Gfkifo.o0SwQNsCvcddk6c-Fe5S1HiefWG1qruosaFK8o"
PREFIX = "/"

thoigianguitinnhan = 1 

cooldown_data = {}
money_file = "money_data.json"

if os.path.exists(money_file):
    with open(money_file, "r") as file:
        money_data = json.load(file)
else:
    money_data = {}

def save_money_data():
    with open(money_file, "w") as file:
        json.dump(money_data, file)

def add_money(user_id, amount):
    if user_id in money_data:
        money_data[user_id] += amount
    else:
        money_data[user_id] = amount
    save_money_data()

def subtract_money(user_id, amount):
    if user_id in money_data:
        money_data[user_id] -= amount
        if money_data[user_id] < 0:
            money_data[user_id] = 0
    save_money_data()

def get_money(user_id):
    return money_data.get(user_id, 0)
from datetime import datetime, timedelta
def check_cooldown(author_id, job_id):
    if author_id in cooldown_data:
        if job_id in cooldown_data[author_id]:
            if datetime.now() < cooldown_data[author_id][job_id]:
                return True
    return False

def update_cooldown(author_id, job_id):
    if author_id not in cooldown_data:
        cooldown_data[author_id] = {}
    cooldown_data[author_id][job_id] = datetime.now() + timedelta(seconds=60)


jobs = {
    "1": {"name": "Làm đĩ", "reward_range": (500000, 700000)},
    "2": {"name": "Làm ôsin", "reward_range": (15000, 25000)},
    "3": {"name": "Làm điếm", "reward_range": (700000, 900000)},
    "4": {"name": "Bán máu", "reward_range": (300000, 500000)},
    "5": {"name": "Làm thợ sửa chữa", "reward_range": (100000, 200000)},
    "6": {"name": "Làm phục vụ quán ăn", "reward_range": (20000, 40000)},
    "7": {"name": "Dạy kèm", "reward_range": (40000, 60000)},
    "8": {"name": "Làm bảo vệ", "reward_range": (50000, 90000)},
    "9": {"name": "Làm tài xế", "reward_range": (100000, 150000)},
    "10": {"name": ":Làm nhà báo", "reward_range": (200000, 300000)},
}

def get_random_reward(job_id):
    if job_id in jobs:
        min_reward, max_reward = jobs[job_id]['reward_range']
        return random.randint(min_reward, max_reward)
    return 0


def load_nhay_messages():
    nhay_messages = []
    try:
        with open("nhay.txt", "r", encoding="utf-8") as file:
            for line in file:
                nhay_messages.append(line.strip())
    except FileNotFoundError:
        print("Không tìm thấy file nhay.txt. Hãy tạo file và nhập các tin nhắn vào đó.", delete_after = 1)
    return nhay_messages
nhay_messages = load_nhay_messages()

def get_user_money(user_id):
    return money_data.get(str(user_id), 0)

def set_user_money(self, user_id, amount):
    self.user_money[user_id] = amount
    print(f"Updated money for {user_id}: {amount}")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


spam_task = None  
nhay_tasks = {}
nhaybth_tasks = {}

allow_admin = False

# Danh sách quản trị viên
admin_list = {709056652543918132}  
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.tree.command(name="allowadmin", description="Bật hoặc tắt chế độ cho phép lệnh chỉ dành cho quản trị viên")
async def allow_admin_cmd(interaction: discord.Interaction, enable: bool):
    global allow_admin
    if interaction.user.id not in admin_list:
        return

    allow_admin = enable
    status = "bật" if enable else "tắt"
    await interaction.response.send_message(f"Chế độ cho phép lệnh admin đã {status}.", ephemeral=True)

@bot.tree.command(name="addadmin", description="Thêm một quản trị viên vào danh sách")
async def add_admin(interaction: discord.Interaction, user: discord.User):
    global admin_list

    if interaction.user.id not in admin_list:
        return


    admin_list.add(user.id)
    await interaction.response.send_message(f"Đã thêm {user.mention} vào danh sách quản trị viên.", ephemeral=True)


@bot.tree.command(name="removeadmin", description="Xóa một quản trị viên khỏi danh sách")
async def remove_admin(interaction: discord.Interaction, user: discord.User):
    global admin_list

    if interaction.user.id not in admin_list:
        return


    admin_list.discard(user.id)
    await interaction.response.send_message(f"Đã xóa {user.mention} khỏi danh sách quản trị viên.", ephemeral=True)


@bot.tree.command(name="listadmins", description="Xem danh sách các quản trị viên")
async def list_admins(interaction: discord.Interaction):
    global admin_list

    if interaction.user.id not in admin_list:
        return

    if not admin_list:
        await interaction.response.send_message("Danh sách quản trị viên hiện đang trống.", ephemeral=True)
        return


    admin_mentions = [f"<@{admin_id}>" for admin_id in admin_list]
    admin_list_str = "\n".join(admin_mentions)
    await interaction.response.send_message(f"Danh sách quản trị viên:\n{admin_list_str}", ephemeral=True)

@bot.tree.command(name="ping", description="Kiểm tra độ trễ Bot.")
async def ping(interaction: discord.Interaction):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:

        return

    try:
        latency = round(bot.latency * 1000) 
        await interaction.response.send_message(f"🎾 | **Ping Pong!** Độ trễ của Bot hiện tại là: `{latency}ms`")
    except Exception as e:
        await asyncio.sleep(5)
        try:
            latency = round(bot.latency * 1000)
            await interaction.response.send_message(f"🎾 | **Ping Pong!** Độ trễ của Bot hiện tại là: `{latency}ms`")
        except Exception as retry_exception:
            await interaction.response.send_message(f":x: | **Lỗi rồi!** {retry_exception}", ephemeral=True)
image_links = [
    "https://cdn.myphamsakura.edu.vn/wp-content/uploads/2024/06/gai-xinh-vu-to-trang-1.jpg",
    "https://gaixinhkhoehang.com/wp-content/uploads/2022/10/20221021-Smileyee-22-808x1212.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4fdM_O4uBRDo67ImEwq-vt003s7Spb5Kv7Q&s",
    "https://bloggioitre.net/wp-content/uploads/2022/01/hinh-vu-dep-2.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDXnI1MGlw0VRyjyB3VJYDTP3PGmUBqn4tMw&s",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQneHmeurOFyPOJI9LuS6ljOKpSsfyr3CWfcQ&s",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTUc8uJZzFjouj7C_-XLyxMqvNIYcblgijpJQ&s",
    "https://teletiengviet.com/wp-content/uploads/2022/12/ANH-KHOE-NGUC-1.jpeg",
    "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhMWpcCrVNKDGym14pGn1yMu-jH1UTR7zaFqHzKrIGJJRMGnxiGnjcJppGqWrtv8ke21ashsZaUq2sDiMmsTVhpnKzuuj0-f7mTMMIYVMjT-ggFd2HFh9p3nMfHkaI5DKOfMfOONtQ2os4KaEQ3Uy4avJ132XSRcvhmSP5RjAXl4kF02Ajqv8DaBEYm1g/s1600/anh-sex-1221-10194108-008.jpg",
    "https://condomviet.com/wp-content/uploads/2021/04/hinh-anh-vu-dep.jpeg",
    "https://topgaixinh.com/wp-content/uploads/2022/11/20221118-Nguyen-Thi-Thu-20-808x1290.jpg",
    "https://cdn.career.edu.vn/wp-content/uploads/2024/04/anh-girl-khoe-vu-1.jpg",
    "https://kenh14cdn.com/203336854389633024/2021/11/28/photo-4-1638069722997887427202.jpg",
    "https://thegioimypham123.com/images/companies/1/vhhh/fe75d657ba6bde9ff77dc481c0ce1a52.jpg?1687574613212",
    "https://condomviet.com/wp-content/uploads/2021/04/hinh-anh-vu-dep-4.jpg",
    "https://gaixinhkhoehang.com/wp-content/uploads/2023/02/anh-gai-nguc-to-19.jpg",
    "https://kenh14cdn.com/2019/8/27/6625837813537884714440914756382156664602624o-1566876775503776987849.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5GWmPZw7stVCGTSjHC3168Sy0r_tsxdDDKA&s",
    "https://bloggioitre.net/wp-content/uploads/2021/11/hinh-anh-goi-cam-che-mat-28.jpg",
    "https://shop.muoitamcong.vn/wp-content/uploads/2023/10/Gai-xinh-khoe-vu-dep-nguc-to.jpg.webp",
    "https://anhgaimup.com/wp-content/uploads/2023/12/hinh-anh-gai-vu-to-tren-website-anh-gai-mup-134.webp",
    "https://cdn.eva.vn/upload/3-2021/images/2021-07-03/new-project-235-1625324052-571-width800height700.jpg",
    "https://anhgaidep.net/wp-content/uploads/2024/01/anh-gai-xinh-khoe-nguc-7.webp",
    "https://teletiengviet.com/wp-content/uploads/2022/11/anh-gai-xinh-khoe-vu-dep-to-ho-ti-61.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXZBQudOC25qlouMANOoCxZEkq75BlhP6MNA&s",
    "https://japans.vn/wp-content/uploads/2023/06/vu-dep-24-22.jpg",
    "https://thegioimypham123.com/images/companies/1/cuong/vudep/anh-gai-xinh-khoe-vu-3.jpg?1687425499329",
    "https://i.vietgiaitri.com/2013/12/6/bo-anh-girl-xinh-chau-a-khoe-than-hinh-dep-nguc-trang-muot-9c16eb.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSM0irVCVWXb0cCDEo-gfo15_87KVuDL-8Kvw&s",
    "https://bloggioitre.net/wp-content/uploads/2021/11/hinh-anh-goi-cam-che-mat-11.jpg",
    "https://thegioimypham123.com/images/companies/1/cuong/vudep/anh-gai-xinh-khoe-vu-7.jpg?1687425529203",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRrEnUCbaTnDA_iZa1Z8exJHxtfBsGKt8Ikcw&s",
    "https://gentlenobra.net/wp-content/uploads/2023/02/anh-gai-xinh-khoe-vu-30.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4k_sJ3aZ8RL7W7HztsW7ZJe7z_7wVOKXJxQ&s",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRdlJjNyuGbEly05jiglQCT6bsZMTL6vVWUw&s",
    "https://girlxinhblog.com/wp-content/uploads/2023/02/hinh-anh-gai-xinh-ho-vu-to-num-hong-loi-ti-10.jpg",
    "https://anhgaimup.com/wp-content/uploads/2023/12/anh-gai-vu-to-tren-website-anh-gai-mup.webp",
    "https://shop.muoitamcong.vn/wp-content/uploads/2023/10/Vu-dep-Viet-Nam-2.jpg.webp",
    "https://pbs.twimg.com/media/Faserf2UIAIk1YF?format=jpg&name=large",
    "https://gaixinh.photo/wp-content/uploads/2022/03/gai-xinh-khoe-vu-02.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7bZofNrtYyaqOdJMFo0Ab5BMSK0_xcfB89A&s",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQ5J1rPm-PRtzOSu1S9hfGjcknlZI3FMQn5A&s",
    "https://anhgaisexy.net/wp-content/uploads/2023/03/anh-lo-vu-021.jpg",
]
@bot.tree.command(name="vu", description="Random Vú.")
async def vu(interaction: discord.Interaction):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return

    try:
        image_url = random.choice(image_links)
        await interaction.response.send_message(image_url)
    except Exception as e:
        await interaction.response.send_message(f'Lỗi khi gửi liên kết hình ảnh: {e}')

@bot.tree.command(name="n", description="Nhây tag user.")
async def n(interaction: discord.Interaction, user: discord.Member):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return

    task_key = (interaction.channel.id, user.id)
    if task_key in nhay_tasks and not nhay_tasks[task_key].done():
        await interaction.response.send_message("Đang gửi tin nhắn!", ephemeral=True)
        return

    async def send_nhayten(interaction: discord.Interaction, user: discord.Member):
        index = 0
        while True:
            try:
                formatted_message = f"{nhay_messages[index % len(nhay_messages)]}"
                await interaction.channel.send(f"{formatted_message} <@{user.id}>")
                index += 1
            except Exception as e:
                await asyncio.sleep(5)  
                continue
            await asyncio.sleep(2)
    nhay_tasks[task_key] = bot.loop.create_task(send_nhayten(interaction, user))

@bot.tree.command(name="checkmoney", description="Kiểm tra số dư")
@app_commands.describe(user="Người dùng mà bạn muốn kiểm tra số dư")
async def checkmoney(interaction: discord.Interaction, user: discord.User = None):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return

    if user is None:
        user = interaction.user

    user_money = get_money(str(user.id))


    embed = discord.Embed(
        title=f"💎 Thông Tin Tài Khoản của {user.display_name} 💎",
        description=f"🌟 **Tên:** {user.display_name}\n"
                    f"💰 **Số tiền hiện có:** {user_money:,} VND",
        color=discord.Color.blue() 
    )
    

    embed.add_field(name="💡 Lưu ý", value="Đảm bảo kiểm tra số dư của bạn thường xuyên và quản lý tài chính một cách hợp lý.", inline=False)
    embed.add_field(name="✨ Chúc bạn chơi vui vẻ và may mắn!", value="\u200b", inline=False)


    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="setmoney", description="Biến động số dư")
@app_commands.describe(user="Người nhận tiền", amount="Số tiền thêm vào")
async def setmoney(interaction: discord.Interaction, user: discord.User, amount: int):
    global admin_list

    if interaction.user.id not in admin_list:
        return

    add_money(str(user.id), amount)


    embed = discord.Embed(
        title="✨ Cập Nhật Tài Khoản Thành Công! ✨",
        description=f"👤 **Người Nhận:** {user.mention} ({user.display_name})\n"
                    f"💸 **Số Tiền Đã Thêm:** {amount:,} VND",
        color=discord.Color.green()  
    )

    embed.add_field(name="🔍 Chi Tiết", value=f"   - **Tài khoản:** {user.id}\n   - **Số dư hiện tại:** {get_money(str(user.id)):,} VND", inline=False)
    embed.add_field(name="🎉 Cảm ơn bạn đã cập nhật số dư!", value="👉 **Đừng quên kiểm tra lại số dư của người dùng để xác nhận.**", inline=False)

    await interaction.response.send_message(embed=embed)
@bot.tree.command(name='help', description='Hướng dẫn Play Game.')
async def help(interaction: discord.Interaction):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return

    help_message = (
        "🎉 **Các Chức Năng Có Sẵn** 🎉\n\n"
        "📜 **1. Kiểm Tra Tiền**\n"
        "   - **Cú pháp:** `checkmoney`\n"
        "   - **Mô tả:** Kiểm tra số tiền hiện tại của bạn.\n\n"
        
        "💰 **2. Đặt Tiền Cho Người Dùng**\n"
        "   - **Cú pháp:** `setmoney @người_dùng <số tiền>`\n"
        "   - **Mô tả:** Đặt số tiền cho người dùng cụ thể.\n\n"
        
        "📋 **3. Xem Danh Sách Công Việc**\n"
        "   - **Cú pháp:** `lamviec`\n"
        "   - **Mô tả:** Hiển thị danh sách công việc hiện có.\n\n"
        
        "🔨 **4. Chọn Công Việc**\n"
        "   - **Cú pháp:** `lamviec <số>`\n"
        "   - **Mô tả:** Chọn công việc và nhận tiền tương ứng.\n\n"
        
        "🎲 **5. Chơi Tài Xỉu**\n"
        "   - **Cú pháp:** `taixiu <Tài/Xỉu> <số tiền cược>`\n"
        "   - **Mô tả:** Đặt cược vào tài hoặc xỉu.\n\n"
        
        "💡 **Ghi chú:**\n"
        "   - Số tiền cược tối thiểu là **1000 VND**.\n"
        "   - Để biết thêm thông tin, vui lòng liên hệ với quản trị viên.\n\n"
        
        "🎉 **Chúc bạn chơi vui vẻ!** 🎉"
    )

    gif_url = "https://i.pinimg.com/originals/5c/82/fb/5c82fb5223f823b89cc6bd78f0e47218.gif" 


    embed = discord.Embed(
        description=help_message,
        color=discord.Color.purple()
    )
    embed.set_image(url=gif_url)

    await interaction.response.send_message(embed=embed)
from discord import Embed
job_list = [
    ("Làm Đĩ", "500.000 - 700.000 VND", "💵"),
    ("Làm Ôsin", "15.000 - 25.000 VND", "🧹"),
    ("Làm Điếm", "700.000 - 900.000 VND", "💸"),
    ("Bán Máu", "300.000 - 500.000 VND", "🩸"),
    ("Làm Thợ Sửa Chữa", "100.000 - 200.000 VND", "🔧"),
    ("Làm Phục Vụ Quán Ăn", "20.000 - 40.000 VND", "🍽️"),
    ("Dạy Kèm", "40.000 - 60.000 VND", "📚"),
    ("Làm Bảo Vệ", "50.000 - 90.000 VND", "🛡️"),
    ("Làm Tài Xế", "100.000 - 150.000 VND", "🚗"),
    ("Làm Nhà Báo", "200.000 - 300.000 VND", "📰")
]

@bot.tree.command(name="lamviec", description="Chọn công việc và nhận tiền")
@app_commands.describe(job_id="ID công việc bạn muốn chọn")
async def lamviec(interaction: discord.Interaction, job_id: str = None):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return

    if job_id is None:

        embed = discord.Embed(
            title="🎯 Danh Sách Công Việc 🎯",
            color=0x1E90FF  # Màu xanh dương nhẹ
        )
        for i, (name, reward, icon) in enumerate(job_list, 1):
            embed.add_field(name=f"{i}️⃣ {icon} {name}", value=f"💵 Phạm vi: {reward}", inline=False)
        embed.set_footer(text="📌 Chọn một công việc bằng cách sử dụng ID của nó (ví dụ: `/lamviec 1`).")
        await interaction.response.send_message(embed=embed)
        return

    if not job_id.isdigit() or int(job_id) < 1 or int(job_id) > len(job_list):

        embed = discord.Embed(
            title="❌ Công Việc Không Hợp Lệ",
            description="Vui lòng chọn một công việc hợp lệ:",
            color=0xFF6347  # Màu đỏ tươi
        )
        job_options = "\n".join([f"{i}: {name}" for i, (name, _, _) in enumerate(job_list, 1)])
        embed.add_field(name="Danh sách công việc:", value=job_options, inline=False)
        await interaction.response.send_message(embed=embed)
        return

    if check_cooldown(str(interaction.user.id), job_id):
        embed = discord.Embed(
            title="⏳ Chờ Đợi",
            description="Bạn phải chờ 60 giây để làm công việc này lại.",
            color=0xFFA07A  # Màu cam nhạt
        )
        await interaction.response.send_message(embed=embed)
        return


    update_cooldown(str(interaction.user.id), job_id)
    job_name = job_list[int(job_id) - 1][0]
    job_reward = get_random_reward(job_id)
    add_money(str(interaction.user.id), job_reward)
    embed = discord.Embed(
        title="🎉 Thành Công!",
        description=f"Bạn đã chọn công việc **{job_name}** và nhận được **{job_reward} VND**.",
        color=0x32CD32  # Màu xanh lá cây tươi sáng
    )
    await interaction.response.send_message(embed=embed)
@bot.tree.command(name='chanle', description='Chơi xúc xắc với cược và đoán lẻ hoặc chẵn!')
@app_commands.describe(bet_type="Loại cược ('Lẻ' hoặc 'Chẵn')", bet_amount="Số tiền cược")
async def chanle(interaction: discord.Interaction, bet_type: str, bet_amount: int):
    user_id = str(interaction.user.id)
    current_money = get_money(user_id)


    if bet_amount <= 0:
        await interaction.response.send_message("🔴 **Số tiền cược phải lớn hơn 0.**", ephemeral=True)
        return

    if bet_amount > current_money:
        await interaction.response.send_message("🔴 **Bạn không có đủ tiền để đặt cược.**", ephemeral=True)
        return

    dice_numbers = [1, 2, 3, 4, 5, 6]
    chosen_number = random.choice(dice_numbers)
    is_odd = chosen_number % 2 != 0
    result = "Lẻ" if is_odd else "Chẵn"

    image_path = f'chanle/{chosen_number}.jpeg'
    
    if not os.path.isfile(image_path):
        await interaction.response.send_message("🔴 **Không tìm thấy hình ảnh cho số xúc xắc.**", ephemeral=True)
        return

    win = (bet_type == result)
    if win:
        add_money(user_id, bet_amount)
        result_message = f"🎉 **Chúc mừng! Bạn đã thắng cược {bet_amount} VND.**"
    else:
        subtract_money(user_id, bet_amount)
        result_message = f"❌ **Rất tiếc! Bạn đã thua cược {bet_amount} VND.**"


    embed = discord.Embed(
        title="Kết quả Xúc Xắc",
        description=f"Số xúc xắc: **{chosen_number}**\nKết quả: **{result}**\n{result_message}",
        color=discord.Color.green() if win else discord.Color.red()
    )
    
    await interaction.response.send_message(embed=embed)
    await interaction.followup.send(file=discord.File(image_path))


@bot.tree.command(name="taixiu", description="Chơi tài xỉu với cược.")
@app_commands.describe(bet_type="Loại cược ('Tài' hoặc 'Xỉu')", bet_amount="Số tiền cược")
async def taixiu(interaction: discord.Interaction, bet_type: str, bet_amount: int):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return

    user_id = str(interaction.user.id)
    current_money = get_money(user_id)

    if current_money < 1000:
        await interaction.response.send_message("🔴 **Bạn cần ít nhất 1000 VND để chơi tài xỉu.**", ephemeral=True)
        return

    if bet_amount < 1000:
        await interaction.response.send_message("🔴 **Số tiền cược tối thiểu là 1000 VND.**", ephemeral=True)
        return

    if bet_amount > current_money:
        await interaction.response.send_message("🔴 **Bạn không có đủ tiền để đặt cược.**", ephemeral=True)
        return

    try:
        total = random.randint(3, 18)
        result = "Tài" if total > 10 else "Xỉu"

        image_directory = "taixiu"
        image_filename = f"{total}.jpg"
        image_path = os.path.join(image_directory, image_filename)

        if not os.path.exists(image_path):
            await interaction.response.send_message(f"🔴 **Không tìm thấy hình ảnh cho tổng điểm {total}.**", ephemeral=True)
            return
        embed = discord.Embed(
            title="Kết quả Tài Xỉu",
            description=f"Tổng điểm: **{total}**\nKết quả: **{result}**",
            color=discord.Color.green() if bet_type == result else discord.Color.red()
        )
        
        if bet_type == result:
            add_money(user_id, bet_amount)
            embed.add_field(name="Chúc mừng!", value=f"Bạn đã thắng cược **{bet_amount} VND**!", inline=False)
        else:
            subtract_money(user_id, bet_amount)
            embed.add_field(name="Thất bại!", value=f"Bạn đã thua cược **{bet_amount} VND**.", inline=False)

        await interaction.response.send_message(embed=embed)
        await interaction.followup.send(file=discord.File(image_path))
    except Exception as e:
        await interaction.response.send_message(f"🔴 **Lỗi không mong muốn: {e}**")


@bot.tree.command(name="c", description="Chửi nhau.")
async def c(interaction: discord.Interaction):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return

    if interaction.channel.id in nhaybth_tasks and not nhaybth_tasks[interaction.channel.id].done():
        await interaction.response.send_message("🔄 **Lệnh đang chạy trong kênh này.**", ephemeral=True)
        return

    async def send_nhay(ctx):
        index = 0
        while True:
            try:
                formatted_message = f"{nhay_messages[index % len(nhay_messages)]}"
                await ctx.send(f"{formatted_message}")
                index += 1
            except Exception as e:
                await asyncio.sleep(5)
                continue
            await asyncio.sleep(2)

    nhaybth_tasks[interaction.channel.id] = bot.loop.create_task(send_nhay(interaction.channel))
    await interaction.response.send_message("✅ **Đã bắt đầu gửi thông điệp.**", ephemeral=True)

@bot.command()
async def stc(ctx):
    if ctx.channel.id in nhaybth_tasks and nhaybth_tasks[ctx.channel.id] and not nhaybth_tasks[ctx.channel.id].done():
        nhaybth_tasks[ctx.channel.id].cancel()
        nhaybth_tasks[ctx.channel.id] = None
        try:
            await ctx.send("Đã dừng lệnh nhây.", delete_after=1)
        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(e.retry_after)
                await ctx.send("Đã dừng lệnh nhây.", delete_after=1)
    else:
        try:
            await ctx.send("Lệnh nhây không hoạt động.", delete_after=1)
        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(e.retry_after)
                await ctx.send("Lệnh nhây không hoạt động.", delete_after=1)

    if ctx.channel.id in nhaybth_tasks:
        del nhaybth_tasks[ctx.channel.id]

@bot.command()
async def stn(ctx, user: discord.Member):
    task_key = (ctx.channel.id, user.id)
    if task_key not in nhay_tasks or nhay_tasks[task_key].done():
        await ctx.send("Không có tin nhắn nào đang gửi cho người dùng này trong kênh này.", delete_after=1)
        return

    nhay_tasks[task_key].cancel()
    del nhay_tasks[task_key]  
    await ctx.send("Đã dừng gửi tin nhắn!", delete_after=1)

nhayanh_tasks = {}

@bot.tree.command(name="fsm", description="Face shaming mấy đứa ngu")
async def fsm(
    interaction: discord.Interaction,
    user: discord.Member,
    image_urls: str
):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return

    task_key = (interaction.channel.id, user.id)
    if task_key in nhayanh_tasks and not nhayanh_tasks[task_key].done():
        await interaction.response.send_message("A task is already running for this user.", ephemeral=True)
        return


    image_urls = image_urls.split()

    async def send_nhayanh():
        index = 0
        while True:
            for nhay_message in nhay_messages:
                try:
                    formatted_image_url = f"[{nhay_message}]({image_urls[index % len(image_urls)]})"
                    await interaction.channel.send(f"# > <@{user.id}> {formatted_image_url}")
                    index += 1
                except Exception as e:
                    await asyncio.sleep(5)
                    continue
                await asyncio.sleep(2)

    nhayanh_tasks[task_key] = bot.loop.create_task(send_nhayanh())
    await interaction.response.send_message("Started sending messages!", ephemeral=True)
@bot.command()
async def stfsm(ctx, user: discord.Member):
    task_key = (ctx.channel.id, user.id)
    if task_key in nhayanh_tasks and nhayanh_tasks[task_key] and not nhayanh_tasks[task_key].done():
        nhayanh_tasks[task_key].cancel()
        nhayanh_tasks[task_key] = None
        try:
            await ctx.send("Đã dừng lệnh nhayanh.", delete_after=1)
        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(e.retry_after)
                await ctx.send("Đã dừng lệnh nhayanh.", delete_after=1)
    else:
        try:
            await ctx.send("Lệnh nhayanh không hoạt động.", delete_after=1)
        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(e.retry_after)
                await ctx.send("Lệnh nhayanh không hoạt động.", delete_after=1)

    if task_key in nhayanh_tasks:
        del nhayanh_tasks[task_key]


gadit_tasks = {}
@bot.tree.command(name="chich", description="Gạ địt")
async def chich(
    interaction: discord.Interaction,
    member: discord.Member
):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return

    task_key = (interaction.channel.id, member.id)
    if task_key in gadit_tasks and not gadit_tasks[task_key].done():
        await interaction.response.send_message("A task is already running for this user.", ephemeral=True)
        return

    async def gadit_loop():
        tán_gái_messages = [
            f"{member.mention} ơi, anh muốn some bé vê lờ 😉",
            f"{member.mention} làm anh thèm quá.",
            f"Anh chờ cả ngày chỉ muốn làm chuyện ấy với {member.mention}.",
            f"Mùi mu {member.mention} thật hấp dẫn.",
            f"{member.mention} thật khéo làm anh hưng phấn",
            f"Anh thích nhìn {member.mention} cởi áo",
            f"{member.mention} rất thích cởi quần áo trước mặt anh đúng kh.",
            f"{member.mention} thích nằm trên hay nằm dưới.",
            f"a muốn la hán đẩy xe bò với {member.mention} ",
            f"{member.mention} thích tư thế nào nhất dạ!!!",
            f"anh muốn bé hột lu {member.mention}",
            f"anh ăn {member.mention} nhé",
            f"{member.mention} đẹp gái quá cho a some tí",
            f"đi nhà nghỉ không {member.mention} eyyy",
            f"Anh bao phòng {member.mention} nhaaa 500k chịu hongg!!!",
            f"Trông {member.mention} thật quyến rũ",
            f"bím {member.mention} sướng quá anh không chịu được",
            f"{member.mention} muốn mạnh bạo hay là nhẹ nhàng",
            f"a thèm sờ mu {member.mention} vãi l",
            f"{member.mention} ngồi trên đùi anh đi",
            f"anh nhấp nhô toco {member.mention} nhé-))",
            f"thứ a cần là nụ cười dọc của {member.mention}",
            f"mặc váy vào đi lát a chở {member.mention} đi nhà nghỉ",
            f"anh thèm địt {member.mention} vl",
            f"trông {member.mention} ngon vl lột quần ra đi bé",
            f"đi nhà nghỉ kh {member.mention}",
            f"anh thèm dit cái mu {member.mention} vl",
            f"mình lôi nhau lên giường đi {member.mention}",
            f"mình xem phim sex cùng nhau nhé {member.mention}",
            f"muốn ôm {member.mention} vào lòng và hôn vào nụ cười dọc ngay lập tức!!",
            f"anh sẽ khiến {member.mention} phát điênn",
            f"sao ngực {member.mention} to vậy",
            f"{member.mention} vú bơm silicon à ",
            f"chỏng mông lên đi {member.mention}",
            f"cời quần ra đi {member.mention}",
            f"a muốn doggy {member.mention} vll",
            f"{member.mention} làm a hưng phán hơn đi",
            f"phê vl {member.mention} ơii",
            f"a thèm sờ mu {member.mention}",
        ]
        
        for message in tán_gái_messages:
            await interaction.channel.send(message)
            await asyncio.sleep(2)

    gadit_tasks[task_key] = bot.loop.create_task(gadit_loop())
    await interaction.response.send_message("Started sending messages!", ephemeral=True)




@bot.command()
async def stchich(ctx, member: discord.Member):

    task_key = (ctx.channel.id, member.id)
    if task_key in gadit_tasks and not gadit_tasks[task_key].done():
        gadit_tasks[task_key].cancel()
        del gadit_tasks[task_key]
        await ctx.send(f"Đã dừng lệnh gadit cho {member.mention}.", delete_after = 1)
    else:
        await ctx.send(f"Không có lệnh gadit nào đang chạy cho {member.mention}.", delete_after = 1)

from discord.ui import Select, View
class ChannelSelect(Select):
    def __init__(self, channels):
        options = [
            discord.SelectOption(label=channel.name, value=str(channel.id))
            for channel in channels
        ]
        super().__init__(placeholder="Chọn một kênh voice...", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        channel_id = int(self.values[0])
        channel = interaction.guild.get_channel(channel_id)
        
        if isinstance(channel, discord.VoiceChannel):
            voice_client = interaction.guild.voice_client
            if voice_client is not None:
                await voice_client.move_to(channel)
            else:
                await channel.connect()
            await interaction.response.send_message(f"Đã kết nối tới kênh voice {channel.name}.", ephemeral=True)
        else:
            await interaction.response.send_message("ID không phải là kênh voice. Vui lòng chọn kênh voice hợp lệ.", ephemeral=True)

@bot.tree.command(name="vc", description="Chọn một kênh voice để kết nối")
async def vc(interaction: discord.Interaction):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return

    voice_channels = [channel for channel in interaction.guild.channels if isinstance(channel, discord.VoiceChannel)]
    
    if not voice_channels:
        await interaction.response.send_message("Không có kênh voice nào trong máy chủ.", ephemeral=True)
        return

    select = ChannelSelect(voice_channels)
    view = View()
    view.add_item(select)
    
    await interaction.response.send_message("Chọn một kênh voice từ danh sách bên dưới:", view=view, ephemeral=True)


kiss_image_url = ['https://i.pinimg.com/originals/de/da/c9/dedac9ceaace3856b6fe85522579fb88.gif',
                  'https://genk.mediacdn.vn/2018/8/10/574fcc5512062-15338767229791206235517.gif',
                  'https://genk.mediacdn.vn/2018/8/10/574fcc092e9f0-15338766633901877145999.gif',
                  'https://genk.mediacdn.vn/2018/8/10/574fcc797b21e-1533876813029926506824.gif',
                  "https://genk.mediacdn.vn/2018/8/10/574fcc92e98c3-1533876840028170363441.gif",
                  "https://media1.giphy.com/media/l0HlwzGiIYBzfAx7q/giphy.gif?cid=6c09b952mkwovcan2r978b4f9orc3ckwfr0juoj1n843iq1q&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
                  "https://steamuserimages-a.akamaihd.net/ugc/882005587667465433/0C4C638277B865B1C228FAA3E06DEA6672431633/?imw=512&&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false",
                  "https://kenh14cdn.com/zoom/700_438/2019/1/14/jan-14-2019-20-41-32-15474733155841964222776-crop-15474733839431503452567.gif",
                  "https://i.vietgiaitri.com/2022/5/4/tan-chay-voi-4-canh-hon-ngot-lim-nhat-lang-anime-doi-so-2-chuan-ngon-tinh-xem-conan---ran-hon-nhau-ma-quan-queo-6cf-6430200.gif",
                  "https://img.docnhanh.vn/images/uploads/2020/10/13/honeycam-2020-09-07-14-36-53-159946431430428789450-1602558968030153784454.gif",
                  ]

kiss_index = 0
@bot.tree.command(name="kiss", description="Hun ai đó!!!")
async def kiss(
    interaction: discord.Interaction,
    member: discord.Member
):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return

    global kiss_index

    kiss_message = f'# {member.mention} ơi,  đôi môi của bé thật quyến rũ! Anh muốn chạm nhẹ lên bờ môi đó của em 💋!'
    kiss_image = kiss_image_url[kiss_index]

    await interaction.response.send_message(kiss_message)
    await interaction.followup.send(kiss_image)
    
    kiss_index = (kiss_index + 1) % len(kiss_image_url)




chat_task = None 

@bot.tree.command(name="chat", description="Spam nội dung bất kì")
async def chat(
    interaction: discord.Interaction,
    message: str
):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return

    global chat_task

    if len(message.strip()) == 0:
        await interaction.response.send_message("Cung cấp nội dung muốn chat", ephemeral=True)
        return

    async def send_chatspam():
        while True:
            await interaction.channel.send(message)
            await asyncio.sleep(3)
    if chat_task is not None and not chat_task.done():
        chat_task.cancel()

    chat_task = bot.loop.create_task(send_chatspam())
    await interaction.response.send_message(f"Started sending messages: {message}", ephemeral=True)




@bot.command()
async def stchat(ctx):
    global chat_task

    if chat_task:
        chat_task.cancel()  
        await ctx.send('Đã dừng Chat.', delete_after = 1)
    else:
        await ctx.send('Không có hoạt động nào diễn ra!.', delete_after = 1 )

@bot.tree.command(name="girl", description="Random ảnh gái")
async def girl(interaction: discord.Interaction):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return

    messages = [
        "Vợ chồng lục đục, tình dục làm hòa.",
        "Ngày Iphone mở bán… tôi mong em đừng mở háng 🙁",
        "Em có một con quỷ cái hố, anh có thể nhốt quái vật của anh vào trong này được không..",
        "Gió đưa cành trúc sau hè, Đây em nằm sẵn anh đè ngay đi",
        "Từ lâu em đã yêu anh, Hôm nay em muốn thả phanh xếp hình",
        "Bắc thang lên hỏi ông trời, Bán dâm một buổi kiếm lời bao nhiêu",
        "Ba dạy em: Nước biển làm ra muối, mía làm ra đường… và cái giường làm ra em.",
        "Theo như em được biết thì 70% cơ thể em là nước, vậy anh có thể cho em nuôi vài con nòng nọc được hong…",
        "Ngày ấy rũ em đi học đàn, không ngờ trở thành nhạc cụ để cho em thổi.",
        "Đôi khi có những mối quan hệ chỉ để quan hệ…",
        "Quy luật của tình yêu là: chụt, mút, đút, rút, phụt, cút",
        "Nhà em lấy chiếu làm giường, Tuy hơi mục nát, nhưng tường cách âm",
        "Sống nội tâm, thủ dâm là chính.",
        "Kim đâm vào thịt thì đau, Thịt đâm vào thịt nhớ nhau cả đời.",
        "Hoa hồng nào chẳng có gai, Yêu nhau thì phải có thai mới bền",
        "Ước gì anh hoá thành dưa, Để đêm em nhớ, em đưa anh vào.",
        "Yêu là sự rung động của bốn chân giường và là sự trần truồng của hai cá thể.",
        "Nếu ai đó quay lưng lại với bạn…, Hãy vỗ vào mông họ.",
        "Anh mệt hả, kiếm nhà nào nghỉ nhé!",
        "Chụp hình em không ăn ảnh, nhưng bỏ dấu hỏi thì em ăn được.",
        "Không thích history, tôi thích cậu hi story."
    ]
    image_dir = "image/gai"
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]

    if not image_files:
        await interaction.response.send_message("No images found in the directory.", ephemeral=True)
        return

    random_image = random.choice(image_files)
    image_path = os.path.join(image_dir, random_image)

    random_message = random.choice(messages)


    await interaction.response.send_message(random_message)
    await interaction.followup.send(file=discord.File(image_path))

video_links = [
    "https://i.imgur.com/v8L0Z7o.mp4",
    "https://i.imgur.com/SVqByRi.mp4",
    "https://i.imgur.com/mLzOqdS.mp4",
    "https://i.imgur.com/OvmKQf0.mp4",
    "https://i.imgur.com/sgrFwbX.mp4",
    "https://i.imgur.com/dRZzs3k.mp4",
    "https://i.imgur.com/XmSH5A4.mp4",
    "https://i.imgur.com/6qIKkvf.mp4",
    "https://i.imgur.com/igcTSj5.mp4",
    "https://i.imgur.com/R4uYMsI.mp4",
    "https://i.imgur.com/Mnb8ZlI.mp4",
    "https://i.imgur.com/6g4Abkd.mp4",
    "https://i.imgur.com/GzD1xIU.mp4",
    "https://i.imgur.com/xn29pLP.mp4",
    "https://i.imgur.com/IybO14I.mp4",
    "https://i.imgur.com/tVjs4Fl.mp4",
    "https://i.imgur.com/np2Q1aj.mp4",
    "https://i.imgur.com/voHNL7N.mp4",
    "https://i.imgur.com/iUyOq33.mp4",
    "https://i.imgur.com/kZJYB6z.mp4",
    "https://i.imgur.com/kZJYB6z.mp4",
    "https://i.imgur.com/RSsJj2x.mp4",
    "https://i.imgur.com/3EzsldO.mp4",
    "https://i.imgur.com/y2aK7rX.mp4",
    "https://i.imgur.com/5VrV3Mt.mp4",
    "https://i.imgur.com/arbi4DK.mp4",
    "https://i.imgur.com/YKunVev.mp4",
    "https://i.imgur.com/kMNuv22.mp4",
    "https://i.imgur.com/zO36tlx.mp4",
    "https://i.imgur.com/zO36tlx.mp4",
    "https://i.imgur.com/DzVF3Xd.mp4",
    "https://i.imgur.com/S3Srowd.mp4",
    "https://i.imgur.com/iGYbVki.mp4",
    "https://i.imgur.com/yG97dVV.mp4",
    "https://i.imgur.com/PdaQfZc.mp4",
    "https://i.imgur.com/AggzTzb.mp4",
    "https://i.imgur.com/QT3Wccr.mp4",
    "https://i.imgur.com/jlmECIM.mp4",
    "https://i.imgur.com/4FxQawG.mp4",
    "https://i.imgur.com/PmiZtKo.mp4",
    "https://i.imgur.com/94lNxgu.mp4",
    "https://i.imgur.com/7uWOf1a.mp4",
    "https://i.imgur.com/sGuHy1x.mp4",
    "https://i.imgur.com/rTosLi7.mp4",
    "https://i.imgur.com/kMNuv22.mp4",
    "https://i.imgur.com/kMNuv22.mp4",
    "https://i.imgur.com/ldX0qPY.mp4",
    "https://i.imgur.com/R1v7i9p.mp4",


]
@bot.tree.command(name="anime", description="Random Video Anime")
async def anime(interaction: discord.Interaction):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return

    try:
        video_url = random.choice(video_links)
        await interaction.response.send_message(video_url)
    except Exception as e:
        await interaction.response.send_message(f'Lỗi khi gửi liên kết video: {e}', ephemeral=True)
@bot.tree.command(name="id", description="Get ID User")
async def id(
    interaction: discord.Interaction,
    member: discord.Member
):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return

    member_id = member.id
    response_message = f"𝙂𝙀𝙏𝙄𝘿 𝙐𝙎𝙀𝙍 🍪 : {member.display_name} ----> {member_id}"
    

    await interaction.response.send_message(response_message)

@bot.tree.command(name="kick", description="Kick member")
async def kick(interaction: discord.Interaction, user: discord.User, reason: str = "Không có lý do"):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("Bạn không có quyền để kick người dùng.", ephemeral=True)
        return

    if user == bot.user:
        await interaction.response.send_message("Bot không thể tự kick chính mình.", ephemeral=True)
        return

    try:

        await interaction.guild.kick(user, reason=reason)
        await interaction.response.send_message(f"Đã kick {user.mention} khỏi server với lý do: {reason}")

    except discord.Forbidden:
        await interaction.response.send_message("Bot không có quyền để kick người dùng.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"Đã xảy ra lỗi khi cố gắng kick người dùng: {e}", ephemeral=True)
@bot.tree.command(name='mute', description='Hạn chế mấy thằng xạo lồn')
@app_commands.describe(member='Người bị mute', duration='Thời gian mute')
async def mute(interaction: discord.Interaction, member: discord.Member, duration: int):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return
    if interaction.user.guild_permissions.administrator:
        mute_role = discord.utils.get(interaction.guild.roles, name='Muted')
        if not mute_role:
            mute_role = await interaction.guild.create_role(name='Muted')
            for channel in interaction.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False)
        
        await member.add_roles(mute_role)
        await interaction.response.send_message(f'{member.mention} đã bị mute trong {duration} phút.')
        
        await asyncio.sleep(duration * 60)
        
        await member.remove_roles(mute_role)
        await mute_role.delete()
        
        await interaction.followup.send(f'{member.mention} đã được gỡ mute và vai trò Muted đã bị xóa.')
    else:
        await interaction.response.send_message('Bạn không có quyền sử dụng lệnh này.', ephemeral=True)
MUSIC_CATEGORIES = {
    'speedup': './speedup',
    'remix': './remix',
    'lofi' : "./lofi",
}
@bot.tree.command(name="play", description="Phát nhạc theo thể loại")
async def play(interaction: discord.Interaction):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return

    if interaction.user.voice is None:
        await interaction.response.send_message("Bạn không ở trong kênh thoại nào!", ephemeral=True)
        return

    channel = interaction.user.voice.channel
    voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)

    if voice_client is None or not voice_client.is_connected():
        try:
            voice_client = await channel.connect()
        except Exception as e:
            await interaction.response.send_message(f"Lỗi kết nối: {e}", ephemeral=True)
            return

    select = discord.ui.Select(
        placeholder="Chọn thể loại nhạc...",
        options=[
            discord.SelectOption(label="Speedup", value="speedup"),
            discord.SelectOption(label="Remix", value="remix"),
            discord.SelectOption(label="Lofi Chill", value="lofi"),
        ]
    )

    async def select_callback(interaction: discord.Interaction):
        category = select.values[0]
        audio_folder = MUSIC_CATEGORIES.get(category)

        if audio_folder is None:
            await interaction.response.send_message("Thể loại nhạc không hợp lệ!", ephemeral=True)
            return

        audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3')]

        if not audio_files:
            await interaction.response.send_message("Thư mục không chứa file âm thanh nào.", ephemeral=True)
            return

        async def play_audio_from_files():
            if voice_client is None or not voice_client.is_connected():
                print("Voice client không kết nối.")
                return

            while True:
                for file_name in audio_files:
                    file_path = os.path.join(audio_folder, file_name)
                    if not os.path.exists(file_path):
                        print(f"File không tồn tại: {file_path}")
                        continue

                    source = discord.FFmpegPCMAudio(file_path, executable='ffmpeg')


                    def after_playing(error):
                        if error:
                            print(f"Đã có lỗi xảy ra khi phát âm thanh: {error}")
                        if not voice_client.is_playing():
                            voice_client.stop()

                    if voice_client.is_playing():
                        voice_client.stop()
                    voice_client.play(source, after=after_playing)
                    while voice_client.is_playing():
                        await asyncio.sleep(1)

        bot.loop.create_task(play_audio_from_files())
        await interaction.response.send_message(f"Đang phát nhạc từ thể loại: {category}", ephemeral=True)

    select.callback = select_callback
    view = discord.ui.View()
    view.add_item(select)

    await interaction.response.send_message("Chọn thể loại nhạc bạn muốn phát:", view=view, ephemeral=True)
@bot.tree.command(name="stop", description="Dừng phát nhạc và rời khỏi kênh thoại")
async def stop(interaction: discord.Interaction):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return

    voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    if voice_client is None or not voice_client.is_connected():
        await interaction.response.send_message("Bot không đang phát nhạc hoặc không kết nối kênh thoại.", ephemeral=True)
        return

    voice_client.stop()
    await voice_client.disconnect()
    await interaction.response.send_message("Đã dừng phát nhạc và rời khỏi kênh thoại.", ephemeral=True)

@bot.tree.command(name='unmute', description='Gỡ mute cho người dùng')
@app_commands.describe(member='Người được gỡ mute')
async def unmute(interaction: discord.Interaction, member: discord.Member):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return
    if interaction.user.guild_permissions.administrator:
        mute_role = discord.utils.get(interaction.guild.roles, name='Muted')
        if mute_role and mute_role in member.roles:
            await member.remove_roles(mute_role)
            await interaction.response.send_message(f'{member.mention} đã được gỡ mute.')
        else:
            await interaction.response.send_message(f'{member.mention} không có vai trò Muted hoặc đã được gỡ mute trước đó.')
    else:
        await interaction.response.send_message('Bạn không có quyền sử dụng lệnh này.', ephemeral=True)
@bot.tree.command(name="info", description="Thông tin về Bot Sever.")
async def info(interaction: discord.Interaction):
    global allow_admin
    if allow_admin and interaction.user.id not in admin_list:
        return
    num_guilds = len(bot.guilds)
    num_members = sum(len(guild.members) for guild in bot.guilds)  
    num_channels = sum(len(guild.channels) for guild in bot.guilds)  
    ping = round(bot.latency * 1000) 
    num_commands = len(bot.commands)  


    embed = discord.Embed(
        title="**Bot Information**",
        description="Một vài thông tin Bot Sever Operation By Lê Ngọc Anh!!",
        color=discord.Color.blurple()
    )
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
    embed.set_thumbnail(url=bot.user.avatar.url)
    
    embed.add_field(name="**Bot Name**", value=f"**{bot.user.name}**", inline=True)
    embed.add_field(name="**Bot ID**", value=f"`{bot.user.id}`", inline=True)
    embed.add_field(name="**Admin Bot**", value=f"**Lê Ngọc Anh**", inline=True)
    embed.add_field(name="**Servers Joined**", value=f"**{num_guilds}**", inline=True)
    embed.add_field(name="**Members**", value=f"**{num_members}**", inline=True)
    embed.add_field(name="**Channels**", value=f"**{num_channels}**", inline=True)
    embed.add_field(name="**Ping**", value=f"**{ping} ms**", inline=True)
    embed.add_field(name="**Total Commands**", value=f"**{num_commands}**", inline=True)

    embed.add_field(name="**Support Us**", value=(
        "🔰 **Thanh toán Ngân hàng/Momo:**\n"
        "📎 4027082007 - MB BANK\n"
        "📎 0339992592 - MoMo\n"
        "📎 5811808105 - BIDV\n\n"
        "🔰 **Thanh toán Card:**\n\n"
        "⚠️ **Lưu ý:**\n"
        "Cảm ơn các bạn vì đã sử dụng dịch vụ Bot bên chúng tôi! Nếu có sai sót bạn có thể liên hệ với Admin Lê Ngọc Anh qua:\n"
        "Facebook : https://www.facebook.com/nanh.nlmn/\n"
        "Zalo : 0339992592\n"
    ), inline=False)
    
    embed.add_field(name="**Version**", value=f"**1.0.0**", inline=True)
    embed.add_field(name="**Description**", value="I'm here to make your server a better place with useful commands and fun features!", inline=False)

    embed.set_image(url="https://i.pinimg.com/originals/be/53/fc/be53fc5350400539c44b3bc7c2552fe9.gif")  
    embed.set_footer(text="Thank you for using our bot!", icon_url=bot.user.avatar.url)

    await interaction.response.send_message(embed=embed)
import aiohttp

def transfer_money(sender_id, receiver_id, amount):
    sender_id = str(sender_id)
    receiver_id = str(receiver_id)
    
    if sender_id not in money_data or money_data[sender_id] < amount:
        return False 

    if receiver_id not in money_data:
        money_data[receiver_id] = 0

    money_data[sender_id] -= amount
    money_data[receiver_id] += amount
    save_money_data()
    return True

@bot.tree.command(name='bank', description='Chuyển tiền cho người khác.')
async def bank(interaction: discord.Interaction, recipient: discord.User, amount: int):
    sender_id = interaction.user.id
    receiver_id = recipient.id

    if amount <= 0:
        await interaction.response.send_message("💸 **Số tiền chuyển phải lớn hơn 0.**")
        return

    if get_user_money(sender_id) < amount:
        await interaction.response.send_message("❌ **Bạn không có đủ tiền để chuyển.**")
        return

    if not transfer_money(sender_id, receiver_id, amount):
        await interaction.response.send_message("⚠️ **Đã xảy ra lỗi khi chuyển tiền. Vui lòng thử lại.**")
        return


    embed = discord.Embed(
        title="💰 **Chuyển Tiền Thành Công!**",
        description=f"**Người gửi:** {interaction.user.mention}\n**Người nhận:** {recipient.mention}\n**Số tiền:** {amount}",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url="https://i.pinimg.com/originals/f3/e0/5e/f3e05e008d8d5e0eda6c0fa8f559ab28.gif") 
    embed.set_footer(text="Chúc bạn giao dịch vui vẻ!")
    
    await interaction.response.send_message(embed=embed)

class VoiceChannelSelect(Select):
    def __init__(self, channels):
        options = [discord.SelectOption(label=channel.name, value=str(channel.id)) for channel in channels]
        super().__init__(placeholder='Chọn một kênh thoại...', options=options)

    async def callback(self, interaction: discord.Interaction):
        channel_id = int(self.values[0])
        channel = bot.get_channel(channel_id)
        if not channel or not isinstance(channel, discord.VoiceChannel):
            await interaction.response.send_message("Không tìm thấy kênh thoại này!")
            return

        voice_bot = await channel.connect()
        file_path = 'xa.mp3'
        source = discord.FFmpegPCMAudio(file_path, executable='ffmpeg')

        def after_playing(error):
            if error:
                print('An error occurred while playing:', error)
            voice_bot.play(source, after=after_playing)

        voice_bot.play(source, after=after_playing)
        await interaction.response.send_message("Đang phát âm thanh vô hạn trong kênh thoại!")

@bot.tree.command(name="xa", description="Xả mic.")
async def xa(interaction: discord.Interaction):
    voice_channels = [channel for channel in interaction.guild.voice_channels]

    if not voice_channels:
        await interaction.response.send_message("Không có kênh thoại nào trong server!")
        return

    select = VoiceChannelSelect(voice_channels)
    view = View()
    view.add_item(select)
    await interaction.response.send_message("Chọn kênh thoại để phát âm thanh:", view=view)

intents.voice_states = True
import yt_dlp
import imageio_ffmpeg as ffmpeg


bot_start_time = None


def update_bot_start_time():
    global bot_start_time
    bot_start_time = datetime.now()


gif_link = ["https://i.pinimg.com/originals/02/83/bb/0283bbc5a5abffd81997a357d076f043.gif",
            "https://i.pinimg.com/originals/b9/1b/80/b91b804c5760a415a883369cd128c6ad.gif",
            "https://i.pinimg.com/originals/3e/ef/1d/3eef1de6ece00c4c46d33f19eb9db00c.gif",
            "https://i.pinimg.com/originals/f1/cb/af/f1cbaf64745c20caf69135114651f2b4.gif",
            "https://i.pinimg.com/originals/d0/45/11/d04511e2c4522a8148ea1b71b42ac795.gif",
            "https://i.pinimg.com/originals/03/50/34/035034a8d71bfa7202944cd397f9c20b.gif",
            "https://i.pinimg.com/originals/4f/e7/2e/4fe72ed1d58e6edffa4d3ed733bee7ff.gif",
            "https://i.pinimg.com/originals/40/ad/d0/40add08405dd875431b858f2a0419224.gif",
            "https://i.pinimg.com/originals/f1/2b/21/f12b218969982a3a699fc6004120d8b3.gif",

]
gif_index = 0
@bot.tree.command(name="menu", description="Xem menu của bot")
async def menu(interaction: discord.Interaction):
    global gif_index  
    if allow_admin and interaction.user.id not in admin_list:
        return

    try:
        bot_user = bot.user
        bot_name = bot_user.name
        bot_id = bot_user.id
        PREFIX = "/"  

        if bot_start_time:
            uptime_delta = datetime.now() - bot_start_time
            days = uptime_delta.days
            hours = uptime_delta.seconds // 3600
            minutes = (uptime_delta.seconds // 60) % 60

            uptime_str = f"{days} ngày, {hours} giờ, {minutes} phút" if days > 0 else f"{hours} giờ, {minutes} phút"
        else:
            uptime_str = "Bot chưa được bật"

        help_message = f"""
🎐 **𝐋𝐢𝐬𝐭 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐁𝐨𝐭** 🎐
Dưới đây là danh sách các lệnh có sẵn của bot:

🌸 **Lệnh Nhây 𝐃𝐢𝐬𝐜𝐨𝐫𝐝** 🌸
🏷️ **{PREFIX}n [id_user]**: Nhây tag tên.
📌 **{PREFIX}c**: Nhây.
📸 **{PREFIX}fsm [UID_User] [link_ảnh]**: Face Shaming

⚙️ **Lệnh Hệ Thống cho 𝐃𝐢𝐬𝐜𝐨𝐫𝐝** ⚙️
⏹️ **{PREFIX}st + lệnh + [UID - Nếu có]**: Stop lệnh
🚪 **{PREFIX}vc [id_kênh]**: Treo room 
🍭 **{PREFIX}id [@Tag]**: Lấy ID User
🍄 **{PREFIX}help**: Hướng dẫn chơi game 
🐇 **{PREFIX}stop**: Dừng phát nhạc
🤡 **{PREFIX}kick [user]**: Kick người dùng
🍪 **{PREFIX}unmute [user]** : Gỡ mute 
🌊 **{PREFIX}mute [user] [time] : Mute
💬 **{PREFIX}info** : Thông tin về Bot
🧩 **{PREFIX}play [typemusic]** : Nghe nhạc
📁 **{PREFIX}bank [user] [money]: Chuyển tiền

🎲🎲 **Lệnh Giải Trí 𝐃𝐢𝐬𝐜𝐨𝐫𝐝** 🎲🎲
👻 **{PREFIX}chat [Nội dung]**: Spam nội dung
💋 **{PREFIX}kiss [@Tag]**: Hôn
🍆 **{PREFIX}chich [id_user]**: Gạ địt !!
🎀 **{PREFIX}vu**: Ảnh vú
💤 **{PREFIX}anime**: Video Anime
👻 **{PREFIX}girl**: Ảnh gái
📢 **{PREFIX}chanle [Lẻ/Chẵn] [tiền cược]**: Game đố vui
🔴**{PREFIX}xa [id channel]**: Xả mic

🔧 **Lệnh Admin 𝐃𝐢𝐬𝐜𝐨𝐫𝐝** 🔧
🆕 **{PREFIX}addadmin [User]**: Thêm người dùng vào danh sách Admin.
✔️ **{PREFIX}allowadmin [True Or False]**: Bật tắt Lệnh Admin.
❌ **{PREFIX}removeadmin [User]**: Xóa quyền admin của người dùng.
📋 **{PREFIX}listadmins**: Xem danh sách các admin hiện tại.

🎨 **𝘊𝘰𝘱𝘺𝘙𝘪𝘨𝘩𝘁 𝘈𝘥𝘮𝘪𝘯 𝘉𝘰𝘁 𝘓𝘦 𝘕𝘨𝘰𝘤 𝘈𝘯𝘩 𝘤𝘵𝘦𝘴1𝘮𝘹𝘩** 🎨
🔑 **𝘼𝙘𝙘𝙤𝙪𝙣𝙩𝙨**: {bot_name}
🆔 **ID**: {bot_id}
⏲️ **Thời gian hoạt động**: {uptime_str}
"""
        gif_url = gif_link[gif_index]  
        embed = discord.Embed(
            description=help_message,
            color=discord.Color.purple()
        )
        embed.set_image(url=gif_url)  


        await interaction.response.send_message(embed=embed)

        gif_index = (gif_index + 1) % len(gif_link)

    except Exception as e:
        print(f'Lỗi khi xử lý lệnh menu: {e}')
        await interaction.response.send_message("Đã xảy ra lỗi khi xử lý lệnh menu.", ephemeral=True)
@bot.event
async def on_ready():
    print(f"{bot.user.name} Updating Bot Sever - Running By Nanh.")
    update_bot_start_time()
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(e)

bot.run(TOKEN) 
