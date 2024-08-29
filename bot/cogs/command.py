import discord
import random
from discord.ext import commands
from discord import app_commands, Interaction
from typing import Optional
import os
import re
import asyncio
import sqlite3
from discord.ui import View, Button
import time
from datetime import datetime, timedelta
from collections import defaultdict
from discord.ext import tasks
intents = discord.Intents.default()
intents.message_content = True
intents.members = True 
import logging
import logging.handlers


def setup_database():
    dbfile = "socialcredit.db"
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()

    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        member_id INTEGER PRIMARY KEY,
        score INTEGER NOT NULL,
        xp INTEGER NOT NULL DEFAULT 0,
        level INTEGER NOT NULL DEFAULT 1
    )
    """)

    conn.commit()
    conn.close()

setup_database()
log = logging.getLogger(__name__)

scores = defaultdict(int)

def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

class GameState:
    def __init__(self):
        self.player_points = 0
        self.player_defense = 0
        self.player_consecutive_normal_defense = 0
        self.computer_points = 0
        self.computer_defense = 0
        self.computer_consecutive_normal_defense = 0
        self.game_over = False



game_state = GameState()

games = {}

class Game:
    def __init__(self):
        self.answer = random.sample(range(1, 10), 4)
        self.attempts = 0
        self.start_time = time.time()

class RankView(View):
    def __init__(self, bot, ctx, ranking, per_page=5):
        super().__init__(timeout=None)
        self.bot = bot
        self.ctx = ctx
        self.ranking = ranking
        self.per_page = per_page
        self.current_page = 0

        self.total_pages = (len(ranking) - 1) // per_page + 1
        self.update_buttons()

    def update_buttons(self):
        self.children[0].disabled = self.current_page == 0
        self.children[1].disabled = self.current_page == self.total_pages - 1

    def get_embed(self):
        start = self.current_page * self.per_page
        end = start + self.per_page
        page_ranking = self.ranking[start:end]

        embed = discord.Embed(title="偉大光榮正確的社會信用排名", color=discord.Color.blue())
        for idx, (member_name, score) in enumerate(page_ranking, start=start + 1):
            embed.add_field(name=f"{idx}. {member_name}", value=f"{score} 分", inline=False)

        embed.set_footer(text=f"Page {self.current_page + 1}/{self.total_pages}")
        return embed

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

# 定義名為 Main 的 Cog
class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    
    


    @commands.command()
    async def sixdigitpro(self,message: discord.Message ):
        firstdigit = random.randint(1, 3)
        seconddigit = random.randint(0, 9)
        thirddigit = random.randint(0, 9)
        fourthdigit = random.randint(0, 9)
        fifthdigit = random.randint(0, 9)
        sixthdigit = random.randint(0, 9)
        result = f"{firstdigit}{seconddigit}{thirddigit}{fourthdigit}{fifthdigit}{sixthdigit}"
        

        await message.channel.send(f"{result}")
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        emoji = '🛐'
        emoji2 = '🈸'
        emoji3 = '↖️'
        emoji4 = '<:overdismisnonabunuselessfullyabl:1209885696421273710>'
        keyword = "女裝"
        keyword2 = "蝦蝦是電"
        keyword3 = "輸光"
        keyword4 = "NTR"
        keyword5 = "甲"
        keyword5a = "數甲"
        keyword6 = "確實"
        keyword7 = "toma"
        keyword8 = "🍅"
        keyword9 = "Toma"
        #if  message.author.id == 825721815192174633:
            #await message.add_reaction(emoji)
        #else:
             #if message.author.id == 465448546259173377 :
               #await message.add_reaction(emoji2) 
        if message.author == self.bot.user:
            return
    
        if keyword in message.content and message.author.id != 559206037207515137:
            await message.channel.send("女裝女裝趕快女裝")
        
        if keyword2 in message.content:
            await message.channel.send("蝦蝦是超級大電神她要卷爛我們了")

        if keyword3 in message.content and message.author.id != 644041612682330112:
             await message.channel.send("你好了啦佬不要再裝弱了")

        if keyword4 in message.content :
             await message.channel.send("**杜絕ntr人人有責**")
        if keyword5 in message.content and message.author.id != 644041612682330112 and keyword5a not in message.content:
             await message.add_reaction(emoji3)

        if keyword7 in message.content or keyword8 in message.content or keyword9 in message.content:
             await message.add_reaction(emoji4)
        if keyword6 in message.content:
             await message.channel.send("!")
        return
    

# 加分
    @commands.command(name="addscore")
    @is_admin()  
    async def add_score(self, ctx, member: discord.Member, points: int):
        dbfile = "socialcredit.db"
        conn = None
        try:
            conn = sqlite3.connect(dbfile)
            cursor = conn.cursor()

            #查詢分數之類的
            cursor.execute("SELECT score FROM scores WHERE member_id = ?", (member.id,))
            row = cursor.fetchone()

            if row is None:
            #創建紀錄
                cursor.execute("INSERT INTO scores (member_id, score) VALUES (?, ?)", (member.id, points))
                current_score = points
            else:
            #更新紀錄
                current_score = row[0] + points
                cursor.execute("UPDATE scores SET score = ? WHERE member_id = ?", (current_score, member.id))

            conn.commit()

        
            scores[member.id] = current_score

            await ctx.send(f"{member.mention} 的社會信用點數增加了 {points} 點，共計 {current_score} 點。")
            log.debug(f"已添加{points}點社會信用至成員{member.mention}")
        #偵錯之類的
        except sqlite3.Error as e:
            await ctx.send(f"你的piyan發生錯誤: {str(e)}")
        finally:
            if conn:
                conn.close()

    @commands.command(name="deductscore")
    @is_admin()  # Ensure this decorator is defined correctly
    async def deduct_score(self, ctx, member: discord.Member, points: int):
        dbfile = "socialcredit.db"
        conn = None
        try:
            conn = sqlite3.connect(dbfile)
            cursor = conn.cursor()

        
            cursor.execute("SELECT score FROM scores WHERE member_id = ?", (member.id,))
            row = cursor.fetchone()

            if row is None:
            
                current_score = 0
                new_score = current_score - points
                cursor.execute("INSERT INTO scores (member_id, score) VALUES (?, ?)", (member.id, new_score))
            else:
           
                current_score = row[0]
                new_score = current_score - points
                cursor.execute("UPDATE scores SET score = ? WHERE member_id = ?", (new_score, member.id))

            conn.commit()

            await ctx.send(f"{member.mention} 的社會信用減少了 {points} 點，共計 {new_score} 點。")
            log.debug(f"已減少{points}點社會信用至成員{member.mention}")

        except sqlite3.Error as e:
            await ctx.send(f"發生錯誤: {str(e)}")
        finally:
            if conn:
                conn.close()

    @commands.command(name="setscore")
    @is_admin()  
    async def set_score(self, ctx, member: discord.Member, points: int):
        dbfile = "socialcredit.db"
        conn = None
        try:
            conn = sqlite3.connect(dbfile)
            cursor = conn.cursor()

            #查詢分數之類的
            cursor.execute("SELECT score FROM scores WHERE member_id = ?", (member.id,))
            row = cursor.fetchone()

            if row is None:
            #創建紀錄
                cursor.execute("INSERT INTO scores (member_id, score) VALUES (?, ?)", (member.id, points))
                current_score = points
            else:
            #更新紀錄
                current_score = points
                cursor.execute("UPDATE scores SET score = ? WHERE member_id = ?", (current_score, member.id))

            conn.commit()

        
            scores[member.id] = current_score

            await ctx.send(f"{member.mention} 的社會信用點數成功設置為 {current_score} 點。")
            log.debug(f"已設定成員{member.mention}的社會信用為{points}點")
        #偵錯之類的
        except sqlite3.Error as e:
            await ctx.send(f"你的piyan發生錯誤: {str(e)}")
        finally:
            if conn:
                conn.close()

    @commands.command(name="forcescore")
    @is_admin()  
    async def force_score(self, ctx, member: discord.Member):
        dbfile = "socialcredit.db"
        conn = None
        try:
            conn = sqlite3.connect(dbfile)
            cursor = conn.cursor()

            #查詢分數之類的
            cursor.execute("SELECT score FROM scores WHERE member_id = ?", (member.id,))
            row = cursor.fetchone()

            current_score = row[0]
            if row is None:
            #創建紀錄
                cursor.execute("INSERT INTO scores (member_id, score) VALUES (?, ?)", (member.id, 0))
                current_score = 0
            else:
            #更新紀錄
                if current_score >= 2147483647:
                    current_score = 2147483647
                else :
                    return
                cursor.execute("UPDATE scores SET score = ? WHERE member_id = ?", (current_score, member.id))

            conn.commit()

        
            scores[member.id] = current_score

            embed = discord.Embed(title="設置成功", color=discord.Color.red())
            embed.add_field(name="結果", value=f"由於{member.mention}的社會信用點數過高，已經設置為2147483647點。", inline=False)
            await ctx.send(embed=embed)

            log.debug(f"由於分數過高，已設定成員{member.mention}的社會信用為2147483647點")
        #偵錯之類的
        except sqlite3.Error as e:
            await ctx.send(f"你的piyan發生錯誤: {str(e)}")
        finally:
            if conn:
                conn.close()
# 顯示指定成員的分數
    @commands.command(name="showscore")
    async def show_score(self, ctx, member: discord.Member):
        if member is None:
            member = ctx.author
        dbfile = "socialcredit.db"
        conn = None
        
        try:
            conn = sqlite3.connect(dbfile)
            cursor = conn.cursor()

        
            cursor.execute("SELECT score FROM scores WHERE member_id = ?", (member.id,))
            row = cursor.fetchone()

            if row is None:
            
                result = f"{member.mention} 的當前社會信用為 0 點。\n"
                result += "警告：您的社會信用點數過低，若點數持續過低，將可能被遣送至新疆"
                await ctx.send(f"{result}")
            else:
                current_score = row[0]
                result = f"{member.mention} 的當前社會信用為 {current_score} 點。\n"
                if row[0] <= 0:
                    result += "警告：您的社會信用評級為欠佳，若點數持續過低，將可能被遣送至新疆。"
                if row[0] >=1000 and row[0] <=10000000:
                    result += "您的社會信用評級良好，請繼續保持。"
                if row[0] >= 10000000 and row[0] <=10000000000:
                    result += "您的社會信用高於正常值，請小心遭到批鬥"
                if row[0] >= 10000000000 :
                    result += "您的社會信用點數有異常。請聯絡當地黨部以獲得更多資訊。"
                await ctx.send(f"{result}")

        except sqlite3.Error as e:
            await ctx.send(f"發生錯誤: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @commands.command(name="achievement")
    async def achievement(self, ctx, member: discord.Member):
        current_time = datetime.now()
        dbfile = "socialcredit.db"
        conn = None
        achievementp = 0  

        try:
            conn = sqlite3.connect(dbfile)
            cursor = conn.cursor()

        
            cursor.execute("SELECT score FROM scores WHERE member_id = ?", (member.id,))
            buyer_row = cursor.fetchone()

            if buyer_row:
                buyer_score = buyer_row[0]
                cursor.execute("UPDATE cooldowns SET score = ? WHERE member_id = ?", (buyer_score, member.id))
                conn.commit()

        
            cursor.execute("""
            SELECT raped_times, rape_success_times, score, ringo, rob_last_used, gamble_last_used, xijingping, ringo_boss, gulag ,rob_success_times
            FROM cooldowns WHERE member_id = ?
        """, (member.id,))
            row = cursor.fetchone()

            embed = discord.Embed(title="查詢結果", description=f"--成就列表--", color=discord.Color.green())

            if row is None:
           
                embed.add_field(name="錯誤", value=f"{member.mention} 目前尚無被雷普或雷普別人的紀錄。", inline=False)
                await ctx.send(embed=embed)
                return

        
            raped_times, rape_success_times, score, ringo, rob_last_used, gamble_last_used, xijingping, ringo_boss, gulag, rob_success_times = row
            last_used = datetime.fromisoformat(rob_last_used) 
            
            

            if raped_times >= 0 and rape_success_times >= 0:
                embed.add_field(name="查詢成功", value=f"{member.mention} 目前被雷普了 {raped_times} 次，成功雷普別人了 {rape_success_times} 次。", inline=False)
                embed.add_field(name="第二列", value=f"{member.mention} 目前持有 {score} 點社會信用以及 {ringo} 顆林檎。", inline=False)

            if raped_times >= 10:
                embed.add_field(name="成就達成✅--「慾都孤兒I」", value="達成條件：被雷普10次以上", inline=False)
                achievementp += 1
            else:
                embed.add_field(name="成就尚未達成❎--「慾都孤兒I」", value="達成條件：被雷普10次以上", inline=False)
            if raped_times >= 200:
                embed.add_field(name="成就達成✅--「慾都孤兒II」", value="達成條件：被雷普200次以上", inline=False)
                achievementp += 1
            else:
                embed.add_field(name="成就尚未達成❎--「慾都孤兒II」", value="達成條件：被雷普200次以上", inline=False)
            if rape_success_times >= 10:
                embed.add_field(name="成就達成✅--「精蟲衝腦I」", value="達成條件：雷普別人10次以上", inline=False)
                achievementp += 1
            else:
                embed.add_field(name="成就尚未達成❎--「精蟲衝腦I」", value="達成條件：雷普別人10次以上", inline=False)
            if rape_success_times >= 200:
                embed.add_field(name="成就達成✅--「精蟲衝腦II」", value="達成條件：雷普別人200次以上", inline=False)
                achievementp += 1
            else:
                embed.add_field(name="成就尚未達成❎--「精蟲衝腦II」", value="達成條件：雷普別人200次以上", inline=False)
            if rape_success_times >= 114514:
                embed.add_field(name="成就達成✅--「野獸先輩」", value="達成條件：雷普別人達到114514次", inline=False)
                achievementp += 1
            else:
                embed.add_field(name="成就尚未達成❎--「野獸先輩」", value="達成條件：雷普別人達到114514次", inline=False)
            if score >= 2147483647 or xijingping == 'yes':
                embed.add_field(name="成就達成✅--「習近平」", value="達成條件：持有至少2147483647點社會信用", inline=False)
                achievementp += 1
                cursor.execute("UPDATE cooldowns SET xijingping = ? WHERE member_id = ?", ("yes", member.id))
                conn.commit()
            else:
                embed.add_field(name="成就尚未達成❎--「習近平」", value="達成條件：持有至少2147483647點社會信用", inline=False)
            if ringo >= 114514 or ringo_boss == 'yes':
                embed.add_field(name="成就達成✅--「林檎大亨」", value="達成條件：持有114514顆林檎", inline=False)
                achievementp += 1
                cursor.execute("UPDATE cooldowns SET ringo_boss = ? WHERE member_id = ?", ("yes", member.id))
                conn.commit()
            else:
                embed.add_field(name="成就尚未達成❎--「林檎大亨」", value="達成條件：持有114514顆林檎", inline=False)
            
                
            if last_used and datetime.now() - last_used < timedelta(minutes=41) or gulag == 'yes':
                embed.add_field(name="成就達成✅--「古拉格地縛靈」", value="達成條件：在古拉格的剩餘時間達2500秒以上", inline=False)
                achievementp += 1
                cursor.execute("UPDATE cooldowns SET gulag = ? WHERE member_id = ?", ("yes", member.id))
                conn.commit()
            else: 
                 embed.add_field(name="成就尚未達成❎--「古拉格地縛靈」", value="達成條件：在古拉格的剩餘時間達2500秒以上", inline=False)
            if rob_success_times >=10:
                embed.add_field(name="成就達成✅--「平均巴爾幹人」", value="達成條件：搶劫成功10次以上", inline=False)
                achievementp += 1
            else:
                embed.add_field(name="成就尚未達成❎--「平均巴爾幹人」", value="達成條件：搶劫成功10次以上", inline=False)
            if rob_success_times >=200:
                embed.add_field(name="成就達成✅--「奇蹟製造者」", value="達成條件：搶劫成功200次以上", inline=False)
                achievementp += 1
            else:
                embed.add_field(name="成就尚未達成❎--「奇蹟製造者」", value="達成條件：搶劫成功200次以上", inline=False)    
                

            if achievementp == 10:
                embed.add_field(name="全成就蒐集！！", value="恭喜！您已經蒐集完所有成就！", inline=False)
            else:
                embed.add_field(name="成就進度", value=f"距離全成就還有{10-achievementp}項成就，請加油！", inline=False)
            await ctx.send(embed=embed)

        except sqlite3.Error as e:
            await ctx.send(f"發生錯誤: {str(e)}")
        finally:
            if conn:
                conn.close()


# 顯示分數排名
    @commands.command(name="rank")
    async def show_ranking(self, ctx):
        dbfile = "socialcredit.db"
        conn = None
        try:
            conn = sqlite3.connect(dbfile)
            cursor = conn.cursor()

        
            cursor.execute("SELECT member_id, score FROM scores ORDER BY score DESC")
            rows = cursor.fetchall()

            if not rows:
                await ctx.send("目前沒有任何成員的社會信用紀錄。")
                return

       
            ranking = []
            for member_id, score in rows:
                user = ctx.guild.get_member(int(member_id))
                if user:
                    ranking.append((user.name, score))
                else:
                    ranking.append((f"未知成員 ({member_id})", score))

        
            view = RankView(ctx.bot, ctx, ranking)
            embed = view.get_embed()
            await ctx.send(embed=embed, view=view)

        except sqlite3.Error as e:
            await ctx.send(f"發生錯誤: {str(e)}")
        finally:
            if conn:
                conn.close()

    @commands.command(name="gamble")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def gamble(self, ctx):
        dbfile = "socialcredit.db"
        conn = None
        try:
            conn = sqlite3.connect(dbfile)
            cursor = conn.cursor()

            cursor.execute("SELECT gamble_last_used FROM cooldowns WHERE member_id = ?", (ctx.author.id,))
            row = cursor.fetchone()

            if row:
                last_used = datetime.fromisoformat(row[0]) if row[0] else None
                if last_used and datetime.now() - last_used < timedelta(minutes=1):
                    remaining_time = timedelta(minutes=1) - (datetime.now() - last_used)
                    await ctx.send(f"十分不幸的，同志，你被遣送古拉格（或是被雷普了）！請等待 {remaining_time.total_seconds() } 秒後再試。")
                    return

            cursor.execute("SELECT score, xp, level FROM scores WHERE member_id = ?", (ctx.author.id,))
            row = cursor.fetchone()

            if row is None or row[0] <= 0:
                await ctx.send("你的社會信用點數不足，無法參加賭博。")
                return

            current_score, current_xp, level = row

            success_chance = min(0.5 + (level / 20), 0.95)  # 50% base + 5% per level, max 95% chance
            embed = discord.Embed(title="賭博結果", color=discord.Color.red())

            if random.random() < success_chance:
                new_score = current_score * 2
                embed.add_field(name="結果", value="恭喜！您的社會信用點數翻倍了！", inline=False)

          
                new_xp = current_xp + 10
                cursor.execute("UPDATE scores SET score = ?, xp = ?, level = ? WHERE member_id = ?",
                           (new_score, new_xp, level, ctx.author.id))
                conn.commit()

            def check_level_up(level, xp):
                    """Check if a user has enough XP to level up and return the new level."""
                    xp_thresholds = {1: 100,2: 200, 3: 400, 4: 800, 5: 1600, 6: 3200, 7: 6400, 8: 12800, 9: 25600}
                    if level >= 10:
                        return False, level

                    if xp >= xp_thresholds.get(level, float('inf')):
                        return True, level + 1

                    else:
                        return False, level

            async def send_level_up_message(ctx, level):
                    embed = discord.Embed(title="升級通知", description=f"恭喜！你已經升級到 {level} 級！", color=discord.Color.green())
                    await ctx.send(embed=embed)
            
            level_up, new_level = check_level_up(level, new_xp)
            if level_up:
                await send_level_up_message(ctx, new_level)

            else:
                
                new_score = new_score = current_score * 0.5
                embed.add_field(name="結果", value=f"你的社會信用已被減半。準備好前往古拉格吧。", inline=False)
                cursor.execute("UPDATE scores SET score = ? WHERE member_id = ?", (new_score, ctx.author.id))
                conn.commit()
            
            cursor.execute("INSERT OR REPLACE INTO cooldowns (member_id, gamble_last_used) VALUES (?, ?)",
                               (ctx.author.id, datetime.now().isoformat()))
            embed.add_field(name="當前社會信用點數", value=f"{new_score} 點", inline=False)
            await ctx.send(embed=embed)

        except sqlite3.Error as e:
            await ctx.send(f"發生錯誤: {str(e)}")
        finally:
            if conn:
                conn.close()
    @commands.command(name="transfer")
    async def transfer_credits(self, ctx, member: discord.Member, amount: int):
        embed = discord.Embed(title="轉移結果", color=discord.Color.red())
        if amount <= 0:
            embed.add_field(name="錯誤", value="轉移的點數必須大於0", inline=False)
            await ctx.send(embed=embed)
            return
        if ctx.author == member:
                
            embed.add_field(name="錯誤", value=f"不可以轉帳給自己", inline=False)
            await ctx.send(embed=embed)
            return
        dbfile = "socialcredit.db"
        conn = None
        try:
            conn = sqlite3.connect(dbfile)
            cursor = conn.cursor()

        
            cursor.execute("SELECT score FROM scores WHERE member_id = ?", (ctx.author.id,))
            sender_row = cursor.fetchone()

            if sender_row is None or sender_row[0] < amount:
                embed.add_field(name="錯誤", value="同志，你的社會信用過低，無法轉帳，笑死", inline=False)
                await ctx.send(embed=embed)
                return

            sender_score = sender_row[0] - amount

        
            cursor.execute("SELECT score FROM scores WHERE member_id = ?", (member.id,))
            recipient_row = cursor.fetchone()

            if recipient_row is None:
                recipient_score = amount
                cursor.execute("INSERT INTO scores (member_id, score) VALUES (?, ?)", (member.id, recipient_score))
            else:
                recipient_score = recipient_row[0] + amount
                cursor.execute("UPDATE scores SET score = ? WHERE member_id = ?", (recipient_score, member.id))

        
            cursor.execute("UPDATE scores SET score = ? WHERE member_id = ?", (sender_score, ctx.author.id))
            conn.commit()

           
            embed.add_field(name="轉移成功", value=f"你已經將 {amount} 點社會信用轉移給 {member.mention}。你現在有 {sender_score} 點社會信用，他現在有 {recipient_score} 點社會信用。", inline=False)
            await ctx.send(embed=embed)

        except sqlite3.Error as e:
            await ctx.send(f"發生錯誤: {str(e)}")
        finally:
            if conn:
                conn.close()
    @commands.command(name="work")
    @commands.cooldown(1, 30, commands.BucketType.user)  # 0.5 minute cooldown per user
    async def work(self, ctx):
        dbfile = "socialcredit.db"
        conn = None
        try:
            conn = sqlite3.connect(dbfile)
            cursor = conn.cursor()

        
            cursor.execute("SELECT score FROM scores WHERE member_id = ?", (ctx.author.id,))
            row = cursor.fetchone()
            if random.randint(1, 10) < 3:
                if row is None:
            
                    new_score = 250
                    cursor.execute("INSERT INTO scores (member_id, score) VALUES (?, ?)", (ctx.author.id, new_score))
                else:
            
                    new_score = row[0] + 250
                    cursor.execute("UPDATE scores SET score = ? WHERE member_id = ?", (new_score, ctx.author.id))
                
                embed = discord.Embed(title="工作結果", color=discord.Color.green())
                embed.add_field(name="史達林同志的餽贈!", value=f"{ctx.author.mention} 史達林同志看見你如此辛勤勞動，便決定獎賞你250點社會信用點數。", inline=False)
                embed.add_field(name="當前社會信用點數", value=f"{new_score} 點", inline=False)

        
                await ctx.send(embed=embed)
            else:
                if row is None:
            # If the user does not exist in the database, add them with an initial score of 1
                    new_score = 10
                    cursor.execute("INSERT INTO scores (member_id, score) VALUES (?, ?)", (ctx.author.id, new_score))
                else:
            # If the user exists, increment their score by 1
                    new_score = row[0] + 10
                    cursor.execute("UPDATE scores SET score = ? WHERE member_id = ?", (new_score, ctx.author.id))
                # Create an embed message to confirm the work action
                embed = discord.Embed(title="工作結果", color=discord.Color.green())
                embed.add_field(name="辛苦了，同志！", value=f"{ctx.author.mention} 你已經成功勞動並獲得了 10 點社會信用。", inline=False)
                embed.add_field(name="當前社會信用點數", value=f"{new_score} 點", inline=False)

        # Send the embed message
                await ctx.send(embed=embed)
            conn.commit()

        

        except sqlite3.Error as e:
            await ctx.send(f"發生錯誤: {str(e)}")
        finally:
            if conn:
                conn.close()

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
        
            embed = discord.Embed(title="冷卻中", color=discord.Color.red())
            embed.add_field(name="請稍等，同志！", value=f"你已經勞動過了，請等待 {round(error.retry_after, 2)} 秒後再試。", inline=False)
            await ctx.send(embed=embed)
        else:
        # Handle other errors
            await ctx.send(f"發生錯誤: {str(error)}")



    @commands.command(name="guesses")
    @commands.cooldown(1, 10, commands.BucketType.user)  # 1/6 minute cooldown per user
    async def guesses(self, ctx, guess: int):
        dbfile = "socialcredit.db"
        conn = None
        try:
            conn = sqlite3.connect(dbfile)
            cursor = conn.cursor()

       
            cursor.execute("SELECT score FROM scores WHERE member_id = ?", (ctx.author.id,))
            row = cursor.fetchone()
            if random.randint(1, 10) == guess:
                if row is None:
            
                    new_score = 2000
                    cursor.execute("INSERT INTO scores (member_id, score) VALUES (?, ?)", (ctx.author.id, new_score))
                else:
            
                    new_score = row[0] + 2000
                    cursor.execute("UPDATE scores SET score = ? WHERE member_id = ?", (new_score, ctx.author.id))
                
                embed = discord.Embed(title="猜數字結果", color=discord.Color.green())
                embed.add_field(name="恭喜同志！你成功猜對了！", value=f"{ctx.author.mention}同志，蘇維埃科學院決定授予你1000社會信用點數作為獎勵。", inline=False)
                embed.add_field(name="當前社會信用點數", value=f"{new_score} 點", inline=False)

        
                await ctx.send(embed=embed)
            else:
                if row is None:
            
                    new_score = -20
                    cursor.execute("INSERT INTO scores (member_id, score) VALUES (?, ?)", (ctx.author.id, new_score))
                else:
            
                    new_score = row[0] - 20
                    cursor.execute("UPDATE scores SET score = ? WHERE member_id = ?", (new_score, ctx.author.id))
                
                embed = discord.Embed(title="猜數字結果", color=discord.Color.green())
                embed.add_field(name="猜錯了，同志！", value=f"{ctx.author.mention}，由於你提供了錯誤資訊，蘇維埃科學院決定扣除20點社會信用以示懲罰。", inline=False)
                embed.add_field(name="當前社會信用點數", value=f"{new_score} 點", inline=False)

        
                await ctx.send(embed=embed)
            conn.commit()

        

        except sqlite3.Error as e:
            await ctx.send(f"發生錯誤: {str(e)}")
        finally:
            if conn:
                conn.close()

    @guesses.error
    async def guesses_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
        
            embed = discord.Embed(title="冷卻中", color=discord.Color.red())
            embed.add_field(name="請稍等，同志！", value=f"你已經猜過了數字了，請等待 {round(error.retry_after, 2)} 秒後再試。", inline=False)
            await ctx.send(embed=embed)
        else:
        
            await ctx.send(f"發生錯誤: {str(error)}")
    @commands.command(name="rob")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def rob_credits(self, ctx, target: discord.Member):
        dbfile = "socialcredit.db"
        conn = None
        try:
            conn = sqlite3.connect(dbfile)
            cursor = conn.cursor()

        
            cursor.execute("SELECT rob_last_used FROM cooldowns WHERE member_id = ?", (ctx.author.id,))
            row = cursor.fetchone()

            if row:
                last_used = datetime.fromisoformat(row[0]) if row[0] else None
                if last_used and datetime.now() - last_used < timedelta(minutes=1):
                    remaining_time = timedelta(minutes=1) - (datetime.now() - last_used)
                    await ctx.send(f"十分不幸的，同志，你被遣送古拉格（或是被雷普了）！請等待 {remaining_time.total_seconds() } 秒後再試。")
                    return

        
            cursor.execute("SELECT score, xp, level FROM scores WHERE member_id = ?", (ctx.author.id,))
            robber_row = cursor.fetchone()

            cursor.execute("SELECT score FROM scores WHERE member_id = ?", (target.id,))
            target_row = cursor.fetchone()

            if target_row is None or target_row[0] <= 0:
                await ctx.send("百姓成窮鬼啦，沒油水可搶啦!")
                return

            if robber_row[0]>target_row[0]:
                await ctx.send("請不要對無產者出手，同志!")
                return

            robber_score, robber_xp, robber_level = robber_row
            target_score = target_row[0]

        
            success_chance = min(0.3 + (robber_level / 20), 0.75)  # 50% base + 5% per level, max 75% chance

        
            if random.random() < success_chance:
                percentage = random.randint(1, 5) / 100  # Random percentage between 1% and 5%
                stolen_amount = int(target_score * percentage)
                target_loss = random.randint(2, 4) * stolen_amount

    
                new_robber_score = robber_score + stolen_amount
                new_target_score = target_score - target_loss
                new_robber_xp = robber_xp + 10  # Gain XP for successful rob
                cursor.execute("UPDATE scores SET score = ?, xp = ?, level = ? WHERE member_id = ?",
                   (new_robber_score, new_robber_xp, robber_level, ctx.author.id))
                cursor.execute("UPDATE scores SET score = ? WHERE member_id = ?", (new_target_score, target.id))

    
                cursor.execute("SELECT rob_success_times FROM cooldowns WHERE member_id = ?", (ctx.author.id,))
                robber_succ = cursor.fetchone()

    
                if robber_succ is not None:
        
                    robber_new_succ = robber_succ[0] + 1
                    cursor.execute("UPDATE cooldowns SET rob_success_times = ? WHERE member_id = ?",
                       (robber_new_succ, ctx.author.id))
                else:
        
                    cursor.execute("INSERT INTO cooldowns (member_id, rob_success_times) VALUES (?, ?)",
                       (ctx.author.id, 1))

    
                conn.commit()
                

                def check_level_up(level, xp):
                    """Check if a user has enough XP to level up and return the new level."""
                    xp_thresholds = {1: 100, 2: 200, 3: 400, 4: 800, 5: 1600, 6: 3200, 7: 6400, 8: 12800, 9: 25600}
                    if level >= 10:
                        return False, level

                    if xp >= xp_thresholds.get(level, float('inf')):
                        return True, level + 1

                    else:
                        return False, level

                async def send_level_up_message(ctx, level):
                    embed = discord.Embed(title="升級通知", description=f"恭喜！你已經升級到 {level} 級！", color=discord.Color.green())
                    await ctx.send(embed=embed)
            
                    level_up, new_level = check_level_up(robber_level, new_robber_xp)
                    if level_up:
                        cursor.execute("SELECT level FROM scores WHERE member_id = ?", (ctx.author.id,))
                        cursor.execute("UPDATE scores SET level = ? WHERE member_id = ?", (new_level, ctx.author.id))
                        await send_level_up_message(ctx, new_level)

                embed = discord.Embed(title="搶劫結果", color=discord.Color.red())
                embed.add_field(name="搶劫成功！", value=f"{ctx.author.mention} 搶劫了 {target.mention} 並獲得了 {stolen_amount} 點社會信用。", inline=False)
                embed.add_field(name=f"{ctx.author.display_name} 的新社會信用點數", value=f"{new_robber_score} 點", inline=True)
                embed.add_field(name=f"{target.display_name} 的新社會信用點數", value=f"{new_target_score} 點", inline=True)

            else:
            
                chooser = random.randint(1,20)
                if chooser == 4:
                    penalty_type = "gulag"
                else:
                    penalty_type = "fine"
                if penalty_type == "fine":
                    if robber_row[0] >100000000000:
                        fine_amount = random.randint(1500000000, 750000000000)
                    else:
                        if robber_row[0] >10000000:
                            fine_amount = random.randint(1000000,7500000)
                        else:
                            fine_amount = random.randint(1000,75000)
                    new_robber_score = robber_score - fine_amount
                    cursor.execute("UPDATE scores SET score = ? WHERE member_id = ?", (new_robber_score, ctx.author.id))
                    embed = discord.Embed(title="搶劫失敗！", color=discord.Color.red())
                    embed.add_field(name="結果", value=f"你失敗了！你被公安罰款 {fine_amount} 點。", inline=False)

                elif penalty_type == "gulag":
                    if robber_row[0]>=0:
                        new_robber_score = 0  # No change in score
                    else:
                        new_robber_score = robber_score
                    cursor.execute("UPDATE scores SET score = ? WHERE member_id = ?", (new_robber_score, ctx.author.id))
                    embed = discord.Embed(title="搶劫失敗！", color=discord.Color.red())
                    embed.add_field(name="結果", value="你被秘密警察逮了個正著，被送往古拉格！除了社會信用歸零外，1 分鐘內無法使用 ?rob 和 ?gamble。", inline=False)
                
                
                    cursor.execute("UPDATE cooldowns SET  rob_last_used = ? WHERE member_id = ?",
                               ( datetime.now().isoformat(),ctx.author.id))

                conn.commit()

                embed.add_field(name=f"{ctx.author.display_name} 的新社會信用點數", value=f"{new_robber_score} 點", inline=True)
                embed.add_field(name=f"{target.display_name} 的社會信用點數", value=f"{target_score} 點", inline=True)

       
            cursor.execute("INSERT OR REPLACE INTO cooldowns (member_id, rob_last_used) VALUES (?, ?)",
                       (ctx.author.id, datetime.now().isoformat()))

            await ctx.send(embed=embed)

        except sqlite3.Error as e:
            await ctx.send(f"發生錯誤: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @commands.command(name="rape")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def rape(self, ctx, target: discord.Member):
        if ctx.author == target:
                embed = discord.Embed(title="我撅我自己(難視)", color=discord.Color.red())
                embed.add_field(name="出現錯誤", value=f"{ctx.author.mention}，請不要雷普你自己(困惑)", inline=False)
                await ctx.send(embed=embed)
                return
        dbfile = "socialcredit.db"
        conn = None
        try:
            conn = sqlite3.connect(dbfile)
            cursor = conn.cursor()

            

        
            success_chance = random.randint(1,10)  # 50% success chance
            rape_success = 5 < success_chance

            if rape_success:
            
                penalty_duration = timedelta(minutes=5)
                cursor.execute("SELECT rob_last_used, gamble_last_used, raped_times FROM cooldowns WHERE member_id = ?", (target.id,))
                row = cursor.fetchone()

                current_time = datetime.now()

                if row:
                    rob_last_used, gamble_last_used, raped_times = row
                    new_rob_last_used = max(current_time, datetime.fromisoformat(rob_last_used)) + penalty_duration if rob_last_used else current_time + penalty_duration
                    new_gamble_last_used = max(current_time, datetime.fromisoformat(gamble_last_used)) + penalty_duration if gamble_last_used else current_time + penalty_duration

                    cursor.execute("""
                    UPDATE cooldowns SET rob_last_used = ?, gamble_last_used = ?, raped_times = ? WHERE member_id = ?
                """, (new_rob_last_used.isoformat(), new_gamble_last_used.isoformat(), raped_times + 1, target.id))
                else:
                    cursor.execute("""
                    INSERT INTO cooldowns (member_id, rob_last_used, gamble_last_used, raped_times) 
                    VALUES (?, ?, ?, ?)
                """, (target.id, (current_time + penalty_duration).isoformat(), (current_time + penalty_duration).isoformat(), 1))

            
                cursor.execute("SELECT rape_success_times FROM cooldowns WHERE member_id = ?", (ctx.author.id,))
                row = cursor.fetchone()
                rape_success_times = row[0] if row else 0
                cursor.execute("UPDATE cooldowns SET rape_success_times = ? WHERE member_id = ?", (rape_success_times + 1, ctx.author.id))

                conn.commit()

                embed = discord.Embed(title="雷普結果", color=discord.Color.red())
                embed.add_field(name="雷普成功！", value=f"{ctx.author.mention} 成功雷普了一個一個一個 {target.mention}。{target.mention} 將因為過於疲憊而無法使用 `?rob` 和 `?gamble` 5 分鐘。", inline=False)
                

            else:
            
                penalty_duration = timedelta(minutes=10)
                cursor.execute("SELECT rob_last_used, gamble_last_used, ringo FROM cooldowns WHERE member_id = ?", (ctx.author.id,))
                row = cursor.fetchone()

                current_time = datetime.now()

                if row:
                    rob_last_used, gamble_last_used, ringo = row
                    new_rob_last_used = max(current_time, datetime.fromisoformat(rob_last_used)) + penalty_duration if rob_last_used else current_time + penalty_duration
                    new_gamble_last_used = max(current_time, datetime.fromisoformat(gamble_last_used)) + penalty_duration if gamble_last_used else current_time + penalty_duration
                    cursor.execute("UPDATE cooldowns SET rob_last_used = ?, gamble_last_used = ? WHERE member_id = ?",
                               (new_rob_last_used.isoformat(), new_gamble_last_used.isoformat(), ctx.author.id))
                else:
                    cursor.execute("INSERT INTO cooldowns (member_id, rob_last_used, gamble_last_used) VALUES (?, ?, ?)",
                               (ctx.author.id, (current_time + penalty_duration).isoformat(), (current_time + penalty_duration).isoformat()))

                embed = discord.Embed(title="雷普結果", color=discord.Color.red())
                embed.add_field(name="雷普失敗！（絕望）", value=f"{ctx.author.mention} 遭到一轉攻勢，將無法使用 `?rob` 和 `?gamble` 10 分鐘。", inline=False)
                cursor.execute("SELECT ringo FROM cooldowns WHERE member_id = ?", (ctx.author.id,))
                row = cursor.fetchone()

                

                ringo_count = row[0]
                if random.randint(1,10)<9:
                    
                    cursor.execute("UPDATE cooldowns SET ringo = ? WHERE member_id = ?",
                               (ringo_count + 1, ctx.author.id))
                    embed.add_field(name="哦？（察覺）", value=f"...你在被一轉攻勢時，意外發現了一個一個一個林檎。", inline=False)

            conn.commit()
            await ctx.send(embed=embed)

        except sqlite3.Error as e:
            await ctx.send(f"發生錯誤: {str(e)}")
        finally:
            if conn:
                conn.close()
    @rape.error
    async def rape_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
        
            embed = discord.Embed(title="脫出中", color=discord.Color.red())
            embed.add_field(name="嗯、嘛、啊...", value=f"你剛剛已經雷普過別人了，請等待 {round(error.retry_after, 2)} 秒後再試。", inline=False)
            await ctx.send(embed=embed)
        else:
        
            await ctx.send(f"發生錯誤: {str(error)}")

    @commands.command(name="useringo")
    async def use_ringo(self, ctx, amount:int):
        if amount <=0:
            embed = discord.Embed(title="林檎使用結果", color=discord.Color.green())
            embed.add_field(name="林檎使用失敗(絕望)！", value=f"homo特有的零比一大(惱)", inline=False)
            await ctx.send(embed=embed)
            return
        dbfile = "socialcredit.db"
        conn = None
        try:
            conn = sqlite3.connect(dbfile)
            cursor = conn.cursor()

        
            cursor.execute("SELECT ringo FROM cooldowns WHERE member_id = ?", (ctx.author.id,))
            row = cursor.fetchone()

            if row is None or row[0] < amount:
                embed = discord.Embed(title="林檎使用結果", color=discord.Color.green())
                embed.add_field(name="林檎使用失敗(絕望)！", value=f"你的林檎不夠用力(大悲)！", inline=False)
                await ctx.send(embed=embed)
                return

            ringo_count = row[0]

        
            cursor.execute("SELECT rob_last_used, gamble_last_used FROM cooldowns WHERE member_id = ?", (ctx.author.id,))
            cooldowns = cursor.fetchone()

            if cooldowns:
                rob_last_used, gamble_last_used = cooldowns
                current_time = datetime.now()

            
                if rob_last_used:
                    rob_last_used = datetime.fromisoformat(rob_last_used)
                    new_rob_last_used = max(current_time, rob_last_used) - timedelta(minutes=2*amount)
                else:
                    new_rob_last_used = None

                if gamble_last_used:
                    gamble_last_used = datetime.fromisoformat(gamble_last_used)
                    new_gamble_last_used = max(current_time, gamble_last_used) - timedelta(minutes=2*amount)
                else:
                    new_gamble_last_used = None

            
                cursor.execute("""
                    UPDATE cooldowns 
                    SET rob_last_used = ?, gamble_last_used = ?, ringo = ? 
                    WHERE member_id = ?
                """, (new_rob_last_used.isoformat() if new_rob_last_used else None,
                    new_gamble_last_used.isoformat() if new_gamble_last_used else None,
                    ringo_count - 1*amount, ctx.author.id))

                conn.commit()

                embed = discord.Embed(title="林檎使用結果", color=discord.Color.green())
                embed.add_field(name="成功使用林檎！", value=f"你成功使用了一個一個一個林檎，減少了 {amount*2} 分鐘的古拉格(或雷普)懲罰。", inline=False)
                embed.add_field(name="剩餘林檎數量", value=f"你現在有 {ringo_count - amount} 個林檎。", inline=False)
                await ctx.send(embed=embed)

            else:
                await ctx.send("你目前不在古拉格，也沒有被雷普(疑惑)。")

        except sqlite3.Error as e:
            await ctx.send(f"發生錯誤: {str(e)}")
        finally:
            if conn:
                conn.close()

    @commands.command(name="sellringo")
    async def buy_ringo(self, ctx, amount: int):
        dbfile = "socialcredit.db"
        conn = None
        try:
            conn = sqlite3.connect(dbfile)
            cursor = conn.cursor()

        
            cursor.execute("SELECT score FROM scores WHERE member_id = ?", (ctx.author.id,))
            buyer_row = cursor.fetchone()

            

            buyer_score = buyer_row[0] 

            cursor.execute("SELECT score, ringo FROM cooldowns WHERE member_id = ?", (ctx.author.id,))
            row = cursor.fetchone()

            cursor.execute("UPDATE cooldowns SET score = ? WHERE member_id = ?", ( buyer_score, ctx.author.id))
            conn.commit()

            if row is None:
            
                cursor.execute("INSERT INTO cooldowns (member_id, score, ringo) VALUES (?, ?, ?)", (ctx.author.id, 0, 0))
                conn.commit()
                await ctx.send("你的數據已初始化，請再次嘗試購買林檎。")
                return

            current_score, current_ringo = row

            if current_ringo < amount:
                await ctx.send("你的林檎不足，無法出售(悲)。")
                return
            

        
            ringo_sell = 1000 * amount
            new_score = current_score + 1000 * amount
            new_ringo = current_ringo - 1 * amount
            cursor.execute("UPDATE cooldowns SET score = ?, ringo = ? WHERE member_id = ?", (new_score, new_ringo, ctx.author.id))
            cursor.execute("UPDATE scores SET score = ? WHERE member_id = ?", (new_score,  ctx.author.id))
            conn.commit()

            embed = discord.Embed(title="購買結果", color=discord.Color.green())
            embed.add_field(name="成功購買！", value=f"你已經成功出售了{amount}個林檎，獲得了{ringo_sell}點社會信用。下北澤會員制餐廳感謝您的光臨！", inline=False)
            embed.add_field(name="剩餘社會信用點數", value=f"你現在有 {new_score} 點社會信用。", inline=False)
            embed.add_field(name="林檎數量", value=f"你現在有 {new_ringo} 個林檎。", inline=False)
            await ctx.send(embed=embed)

        except sqlite3.Error as e:
            await ctx.send(f"發生錯誤: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @commands.command(name="buyringo")
    async def buy_ringo(self, ctx, amount: int):
        if amount>114514:
                await ctx.send("你買太多林檎力（震聲）。")
                return
        dbfile = "socialcredit.db"
        conn = None
        try:
            conn = sqlite3.connect(dbfile)
            cursor = conn.cursor()

        
            cursor.execute("SELECT score FROM scores WHERE member_id = ?", (ctx.author.id,))
            buyer_row = cursor.fetchone()

            

            buyer_score = buyer_row[0] 

            cursor.execute("SELECT score, ringo FROM cooldowns WHERE member_id = ?", (ctx.author.id,))
            row = cursor.fetchone()

            cursor.execute("UPDATE cooldowns SET score = ? WHERE member_id = ?", ( buyer_score, ctx.author.id))
            conn.commit()

            if row is None:
            
                cursor.execute("INSERT INTO cooldowns (member_id, score, ringo) VALUES (?, ?, ?)", (ctx.author.id, 0, 0))
                conn.commit()
                await ctx.send("你的數據已初始化，請再次嘗試購買林檎。")
                return

            current_score, current_ringo = row

            if current_score < 10000 * amount:
                await ctx.send("你的社會信用點數不足，無法購買林檎（絕望）。")
                return
            if current_ringo >= 114514:
                await ctx.send("你太多林檎啦！不要浪費錢力(困惑)。")
                return

        
            ringo_buy = 10000 * amount
            new_score = current_score - 10000 * amount
            new_ringo = current_ringo + 1 * amount
            cursor.execute("UPDATE cooldowns SET score = ?, ringo = ? WHERE member_id = ?", (new_score, new_ringo, ctx.author.id))
            cursor.execute("UPDATE scores SET score = ? WHERE member_id = ?", (new_score,  ctx.author.id))
            conn.commit()

            embed = discord.Embed(title="購買結果", color=discord.Color.green())
            embed.add_field(name="成功購買！", value=f"你已經成功購買了{amount}個林檎，花費了{ringo_buy}點社會信用。下北澤會員制餐廳感謝您的光臨！", inline=False)
            embed.add_field(name="剩餘社會信用點數", value=f"你現在有 {new_score} 點社會信用。", inline=False)
            embed.add_field(name="林檎數量", value=f"你現在有 {new_ringo} 個林檎。", inline=False)
            await ctx.send(embed=embed)

        except sqlite3.Error as e:
            await ctx.send(f"發生錯誤: {str(e)}")
        finally:
            if conn:
                conn.close()

    @commands.command(name="transferringo")
    async def transfer_ringo(self, ctx, target: discord.Member,amount: int):
        if amount == None:
            amount = 1
        if target == ctx.author:
            await ctx.send("你不能將林檎轉移給自己。")
            return
        if amount <0:
            await ctx.send("你不能轉移負數顆林檎。")
            return

        dbfile = "socialcredit.db"
        conn = None
        try:
            conn = sqlite3.connect(dbfile)
            cursor = conn.cursor()

        
            
            cursor.execute("SELECT ringo FROM cooldowns WHERE member_id = ?", (ctx.author.id,))
            sender_row = cursor.fetchone()

            if sender_row is None or sender_row[0] < amount:
                await ctx.send("你沒有林檎可以轉移(大悲)。")
                return

        
            cursor.execute("SELECT ringo FROM cooldowns WHERE member_id = ?", (target.id,))
            recipient_row = cursor.fetchone()

            sender_ringo = sender_row[0]
            recipient_ringo = recipient_row[0] if recipient_row else 0

        
            new_sender_ringo = sender_ringo - amount
            new_recipient_ringo = recipient_ringo + amount

            cursor.execute("UPDATE cooldowns SET ringo = ? WHERE member_id = ?", (new_sender_ringo, ctx.author.id))
            cursor.execute("INSERT OR REPLACE INTO cooldowns (member_id, ringo) VALUES (?, ?)",
                       (target.id, new_recipient_ringo))

            conn.commit()

            embed = discord.Embed(title="轉移結果", color=discord.Color.blue())
            embed.add_field(name="成功轉移！", value=f"你已經將{amount}個林檎轉移給了 {target.mention}（難視）。", inline=False)
            embed.add_field(name="你的林檎數量", value=f"你現在有 {new_sender_ringo} 個林檎。", inline=False)
            embed.add_field(name=f"{target.display_name} 的林檎數量", value=f"{target.display_name} 現在有 {new_recipient_ringo} 個林檎。", inline=False)
            await ctx.send(embed=embed)

        except sqlite3.Error as e:
            await ctx.send(f"發生錯誤: {str(e)}")
        finally:
            if conn:
                conn.close()

    # 前綴指令
    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send("早安你好")

    @commands.command()
    async def toma(self, ctx: commands.Context):
        await ctx.send("<:overdismisnonabunuselessfullyabl:1209885696421273710><:toma_right:1209885793641041982><:toma_45degree:1226836654380159048><:toma_freedomdive:1209885934057951252><:toma_left:1209885868026892339><:toma_question:1234344570423214240><a:toma_114515:1234671113489874975><a:toma_planet:1226845181882662992><a:3toma_spining:1226845962237116476><a:4toma_Spining:1226839307755589643><a:4toma_pedestrian_scramble:1226839961555308636>")
        
    @commands.command()
    async def black_luxury_car(self, ctx: commands.Context,name:str,name2:str):
        tmp = random.randint(114514, 1919810)
        await ctx.send(f"{name} 用黑色高級車追撞了 {name2}，造成了{tmp}傷害。")

    

# 遊戲指令
    @commands.command(name='1a2b')
    async def oneatwob(self,ctx):
        games[ctx.author.id] = Game()
        await ctx.send("遊戲開始!請用?guess<四位數字>來遊玩。請記得不要輸入0。")

    @commands.command(name='guess')
    async def guess(self, ctx, guess: str):
        if ctx.author.id not in games:
            await ctx.send("請先以?1a2b開始遊戲")
            return
    
        game = games[ctx.author.id]
    
        if len(guess) != 4 or not guess.isdigit():
            await ctx.send("請輸入四位數字")
            return
    
        guess = list(map(int, guess))
        game.attempts += 1
        a = b = 0
        answer_checked = [False] * 4
        guess_checked = [False] * 4

    # Check for correct positions (A)
        for i in range(4):
            if guess[i] == game.answer[i]:
                a += 1
                answer_checked[i] = True
                guess_checked[i] = True

    # Check for correct digits in wrong positions (B)
        for i in range(4):
            if not guess_checked[i]:
                for j in range(4):
                    if not answer_checked[j] and guess[i] == game.answer[j]:
                        b += 1
                        answer_checked[j] = True
                        break

        if a == 4:
            total_time = round((time.time() - game.start_time), 3)
            await ctx.send(f"恭喜!你成功在{game.attempts}次內以{total_time}秒的時間答出了答案{''.join(map(str, game.answer))}")
            del games[ctx.author.id]
        else:
            output = ''.join(map(str, guess))
            await ctx.send(f'{output}: {a}A{b}B')

    @commands.command(name='endgame')
    async def endgame(self,ctx):
        if ctx.author.id in games:
            answer = ''.join(map(str, games[ctx.author.id].answer))
            del games[ctx.author.id]
            await ctx.send(f"遊戲結束。正確答案為{answer}.你可以以?1a2b來開啟另一局遊戲。")
        else:
            await ctx.send("當前沒有已開啟的遊戲。")
    
    @commands.command(name='rule')
    async def rule(self,ctx):
        


        embed = discord.Embed(title="規則", description="遊戲規則介紹", color=0xa600ff)
        embed.add_field(name="蓄力", value="可以獲得一點", inline=True)
        embed.add_field(name="普通防禦", value="不消耗點數，可以抵擋輕攻擊&重攻擊，無法抵擋特殊攻擊，不能連續使用超過兩次", inline=True)
        embed.add_field(name="特殊防禦", value="不消耗點數，只能抵擋特殊攻擊，無法抵擋輕攻擊或重攻擊", inline=True)
        embed.add_field(name="輕攻擊", value="消耗一點", inline=True)
        embed.add_field(name="重攻擊", value="消耗兩點，可穿透輕攻擊", inline=True)
        embed.add_field(name="特殊攻擊", value="消耗四點，可穿透輕攻擊、重攻擊與普通防禦", inline=True)
        embed.set_footer(text="玩家只有一點血量，被任何攻擊直接命中或是攻擊/防禦被穿透時即死亡，也就是遊戲結束。每個回合可以使用上列任一技能(若點數不足則不可使用)，目標為擊敗對手，也就是使其血量歸零。")
        await ctx.send(embed=embed)
        
    @commands.command(name='start')
    async def start_game(self,ctx):
        
        global game_state
        game_state = GameState() #重置遊戲狀態
        await ctx.send("遊戲開始！請使用?move <技能名稱(直接打出中文)>來選擇你的技能。技能有：蓄力, 普通防禦, 輕攻擊, 重攻擊, 特殊防禦, 特殊攻擊")
        game_state.player_points = 0
        game_state.computer_points = 0 
    @commands.command(name='move')
    async def player_move(self,ctx, skill: str):
        valid_skills = ['蓄力', '普通防禦', '輕攻擊', '重攻擊', '特殊防禦', '特殊攻擊']
        if skill not in valid_skills:
            await ctx.send("無效的技能，請選擇：蓄力, 普通防禦, 輕攻擊, 重攻擊, 特殊防禦, 特殊攻擊")
            return
        if game_state.game_over:
            await ctx.send("遊戲已結束，請使用?start來重新開始遊戲。")
        player_action = skill
        computer_action = random.choice(valid_skills)
        

        result = process_turn(player_action, computer_action)
        await ctx.send(result)

def process_turn(player_action, computer_action):
    result = f"玩家選擇了{player_action}，電腦選擇了{computer_action}。\n"

    point_costs = {
        '輕攻擊': 1,
        '重攻擊': 2,
        '特殊攻擊': 4
    }

    # 檢查玩家點數是否足夠
    if player_action in point_costs and game_state.player_points < point_costs[player_action]:
        result += "玩家點數不足，無法使用該技能。\n"
        return result

    # 檢查電腦點數是否足夠
    while computer_action in point_costs and game_state.computer_points < point_costs[computer_action]:
        computer_action = random.choice(['蓄力', '普通防禦', '特殊防禦'])
        result = f"玩家選擇了{player_action}，電腦選擇了{computer_action}。\n"  # 更新結果信息

    # 檢查連續普通防禦次數
    if player_action == '普通防禦':
        game_state.player_consecutive_normal_defense += 1
    else:
        game_state.player_consecutive_normal_defense = 0

    if computer_action == '普通防禦':
        game_state.computer_consecutive_normal_defense += 1
    else:
        game_state.computer_consecutive_normal_defense = 0

    if game_state.player_consecutive_normal_defense > 2:
        result += "玩家無法連續三次使用普通防禦。\n"
        return result

    if game_state.computer_consecutive_normal_defense > 2:
        computer_action = random.choice(['蓄力', '輕攻擊', '重攻擊', '特殊防禦'])
        result = f"玩家選擇了{player_action}，電腦選擇了{computer_action}。\n"  # 更新結果信息
        game_state.computer_consecutive_normal_defense = 0

    # 處理玩家行動
    if player_action == '蓄力':
        game_state.player_points += 1
        result += "玩家獲得一點點數。\n"
    elif player_action == '普通防禦':
        game_state.player_defense += 1
    elif player_action == '輕攻擊':
        game_state.player_points -= 1
    elif player_action == '重攻擊':
        game_state.player_points -= 2
    elif player_action == '特殊防禦':
        pass
    elif player_action == '特殊攻擊':
        game_state.player_points -= 4

    # 處理電腦行動
    if computer_action == '蓄力':
        game_state.computer_points += 1
        result += "電腦獲得一點點數。\n"
    elif computer_action == '普通防禦':
        game_state.computer_defense += 1
    elif computer_action == '輕攻擊':
        game_state.computer_points -= 1
    elif computer_action == '重攻擊':
        game_state.computer_points -= 2
    elif computer_action == '特殊防禦':
        pass
    elif computer_action == '特殊攻擊':
        game_state.computer_points -= 4

    # 判斷結果
    if player_action == '蓄力' and computer_action in ['輕攻擊', '重攻擊', '特殊攻擊']:
        result += "玩家在蓄力時被攻擊，玩家死亡！\n"
        game_state.game_over = True
        result += "電腦獲勝！"
    elif computer_action == '蓄力' and player_action in ['輕攻擊', '重攻擊', '特殊攻擊']:
        result += "電腦在蓄力時被攻擊，電腦死亡！\n"
        game_state.game_over = True
        result += "玩家獲勝！"
    elif player_action == '輕攻擊' and computer_action == '普通防禦':
        result += "電腦使用普通防禦抵擋了輕攻擊。\n"
    elif player_action == '重攻擊' and computer_action == '普通防禦':
        if game_state.computer_defense > 1:
            result += "電腦使用普通防禦抵擋了重攻擊。\n"
        else:
            result += "電腦普通防禦被穿透，電腦死亡！\n"
            game_state.game_over = True
            result += "玩家獲勝！"
    elif player_action == '特殊攻擊' and computer_action == '特殊防禦':
        result += "電腦使用特殊防禦抵擋了特殊攻擊。\n"
    elif player_action == '特殊攻擊' and computer_action not in ['特殊防禦']:
        result += "電腦被特殊攻擊穿透，電腦死亡！\n"
        game_state.game_over = True
        result += "玩家獲勝！"
    elif player_action == '重攻擊' and computer_action == '輕攻擊':
        result += "玩家的重攻擊穿透了電腦的輕攻擊，電腦死亡！\n"
        game_state.game_over = True
        result += "玩家獲勝！"
    elif computer_action == '輕攻擊' and player_action == '普通防禦':
        result += "玩家使用普通防禦抵擋了輕攻擊。\n"
    elif computer_action == '重攻擊' and player_action == '普通防禦':
        if game_state.player_defense > 1:
            result += "玩家使用普通防禦抵擋了重攻擊。\n"
        else:
            result += "玩家普通防禦被穿透，玩家死亡！\n"
            game_state.game_over = True
            result += "電腦獲勝！"
    elif computer_action == '重攻擊' and player_action == '輕攻擊':
        result += "電腦的重攻擊穿透了玩家的輕攻擊，玩家死亡！\n"
        game_state.game_over = True
        result += "電腦獲勝！"
    elif computer_action == '特殊攻擊' and player_action == '特殊防禦':
        result += "玩家使用特殊防禦抵擋了特殊攻擊。\n"
    elif computer_action == '特殊攻擊' and player_action not in ['特殊防禦']:
        result += "玩家被特殊攻擊穿透，玩家死亡！\n"
        game_state.game_over = True
        result += "電腦獲勝！"

    return result
        
    
        
    
    
       



    # 關鍵字觸發
    
        

        
        



# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Main(bot))
