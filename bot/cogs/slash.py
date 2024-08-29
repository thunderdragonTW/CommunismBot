import discord
import random
import math
from math import *
from discord.ext import commands
from discord import app_commands, Interaction
from typing import Optional
from discord.app_commands import Choice
import os
import asyncio
import re
from pypinyin import lazy_pinyin, Style
import logging
import logging.handlers

log = logging.getLogger(__name__)

class MyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    

    @app_commands.command(name = "misc", description = "測試指令而已，不要亂戳")
    async def hello(self, interaction: discord.Interaction):
    # 回覆使用者的訊息
        await interaction.response.send_message("就叫你別亂戳")

   


    @app_commands.command(name="msg")
    async def my_command(self, interaction: discord.Interaction) -> None:
        """ 敲機器人一下 """
        await interaction.response.send_message("沒事敲我幹啥", ephemeral=True)
    
    @app_commands.command(name = "say", description = "昭告天下")
    @app_commands.describe(name = "輸入大名", text = "輸入聖旨")
    async def say(self, interaction: discord.Interaction, name: str, text: Optional[str] = None):
        if text == None:
            text = "(一片安靜)"
        await interaction.response.send_message(f"奉天承運皇帝 {name} 詔曰 「{text}」。欽此。")
    
    @app_commands.command(name="encryption",description="加密一段文字")
    @app_commands.describe(text = "輸入要加密的文字(測試版)" )
    async def encryption(self, interaction: discord.Interaction, text: str):
        def chinese_to_pinyin_array(chinese_text):
            bopomofo_to_number = {
                'ㄅ': '11', 'ㄆ': '12', 'ㄇ': '13', 'ㄈ': '14',
                'ㄉ': '21', 'ㄊ': '22', 'ㄋ': '23', 'ㄌ': '24',
                'ㄍ': '31', 'ㄎ': '32', 'ㄏ': '33', 'ㄐ': '41',
                'ㄑ': '42', 'ㄒ': '43', 'ㄓ': '51', 'ㄔ': '52',
                'ㄕ': '53', 'ㄖ': '54', 'ㄗ': '61', 'ㄘ': '62',
                'ㄙ': '63', 'ㄧ': '71', 'ㄨ': '72', 'ㄩ': '73',
                'ㄦ': '74', 'ㄚ': '81', 'ㄛ': '82', 'ㄜ': '83',
                'ㄝ': '84', 'ㄞ': '91', 'ㄟ': '92', 'ㄠ': '93',
                'ㄡ': '94', 'ㄢ': '01', 'ㄣ': '02', 'ㄤ': '03',
                'ㄥ': '04'
            }
            pinyin_with_tone = lazy_pinyin(chinese_text, style=Style.BOPOMOFO)
            result = []
            for pinyin in pinyin_with_tone:
                num_value = ''
                tone = pinyin[-1] if pinyin[-1] in '˙ˊˇˋ' else '1'
                bopomofo_symbols = pinyin[:-1] if tone != '1' else pinyin

                for i in range(3):
                    if i < len(bopomofo_symbols):
                        num_value += bopomofo_to_number[bopomofo_symbols[i]]
                    else:
                        num_value += '00'

                if tone in '˙ˊˇˋ':
                    tone_number = '˙ˊˇˋ'.index(tone)
                    num_value += str(tone_number + 1)
                else:
                    num_value += '1'

                result.append(num_value)

            return result

        pinyin_array = chinese_to_pinyin_array(text)
        response = "\n".join(pinyin_array)
        await interaction.response.send_message(f'輸入的文字: {text}\n轉換後的注音及聲調數值:\n{response}')
    # 參數: Optional[資料型態]，參數變成可選，可以限制使用者輸入的內容
    @app_commands.command(name = "attack", description = "你要攻擊誰")
    @app_commands.describe(name = "輸入攻擊者的名字",name2 = "輸入被攻擊者的名字", text = "想要用什麼攻擊?")
    async def attack(self, interaction: discord.Interaction ,name: str, name2: str, text: Optional[str] = None):
        
        
        if text == "黑色高級車":
            attak = "追撞"
            tmp = 1145141919810
        else:
            if text == "昏睡紅茶":
                attak = "雷普"
                tmp = 1145141919810
            else:
                if text == "刺槍術":
                    attak = "夜♂襲"
                    tmp = random.randint(114514, 228922)
                else:
                    if name == "鏡瓜" or name == "<@465448546259173377>":
                        attak = "物理超渡"
                        text = "女裝"
                        tmp = 999999999999
                    else:
                        attak="攻擊"
                        tmp = random.randint(1, 114514)
        if text == None:
            text = "空氣"
           
        
        await interaction.response.send_message(f"{name} 用 {text}{attak}了 {name2}，造成了{tmp}傷害。")

    @app_commands.command(name = "dice", description = "骰骰子")
    @app_commands.describe(amount="輸入骰子數量(預設1,最大3)")
    async def dice(self, interaction: discord.Interaction , amount: Optional[int] = None):
        
        
        if amount == None:
            amount = 1
        if amount == 1:
            out = random.randint(1,6)
        else:
            if amount == 2:
                out = random.randint(2,12)
            else:
                if amount == 3:
                    out = out = random.randint(3,18)

            
        
        await interaction.response.send_message(f"結果為{out}")

    @app_commands.command(name = "game1", description = "猜數字")
    @app_commands.describe(guess="輸入1~5的數字")
    async def game1(self, interaction: discord.Interaction ,guess:int):
        
        ans = random.randint(1, 5)
        if ans == guess:
            text = "猜對力OAO"
        else :

           text = f"猜錯了哈哈笑死，答案是{ans}啦"
        
        await interaction.response.send_message(f"{text}")

    @app_commands.command(name="russian_roulette", description="俄羅斯輪盤")
    @app_commands.describe(ammo="輸入總共有幾發(不小於2)", shots="開幾槍", bullets="輸入其中幾發是子彈(默認1)")
    async def russianroutelette(self, interaction: discord.Interaction, ammo: int, shots: int, bullets: Optional[int] = None):
        if ammo < 2:
            await interaction.response.send_message("總彈數不能小於2")
            return

        if bullets is None:
            bullets = 1
        elif bullets >= ammo:
            bullets = ammo

        # Create the chamber with empty slots
        chamber = [0] * ammo

        # Place bullets in random slots
        bullet_positions = random.sample(range(ammo), bullets)
        for pos in bullet_positions:
            chamber[pos] = 1

        # Simulate shots
        result = "恭喜你成功活了OAO"
        for shot_num in range(1, shots + 1):
            if chamber.pop(0) == 1:
                result = f"你在第 {shot_num} 槍被 bang 死了，可憐哪"
                break

        await interaction.response.send_message(f"{result}")

    @app_commands.command(name="random_6_digit", description="隨機六位數產生器")
    async def sixdigit(self, interaction: discord.Interaction ):
        firstdigit = random.randint(1, 3)
        seconddigit = random.randint(0, 9)
        thirddigit = random.randint(0, 9)
        fourthdigit = random.randint(0, 9)
        fifthdigit = random.randint(0, 9)
        sixthdigit = random.randint(0, 9)
        result = f"{firstdigit}{seconddigit}{thirddigit}{fourthdigit}{fifthdigit}{sixthdigit}"
        

        await interaction.response.send_message(f"{result}")

    @app_commands.command(name = "game2", description = "比大小")
    @app_commands.describe(p1="輸入玩家一的名稱",p2="輸入玩家二的名稱")
    async def game2(self, interaction: discord.Interaction ,p1:str,p2:str):
        
        ans1 = random.randint(1, 100)
        ans2 = random.randint(1, 100)
        if ans1>ans2:
            text = f"{p1}擲出了{ans1}點，贏過了{p2}的{ans2}點!"
        else :

           text = f"{p2}擲出了{ans2}點，贏過了{p1}的{ans1}點!"
        
        await interaction.response.send_message(f"{text}")


    @app_commands.command(name = "trash-talk", description = "生成一則幹話")
    async def trashtalk(self, interaction: discord.Interaction ):
        
        randomed = random.randint(1, 5)
        if randomed == 1:
            text = "你最新的照片是你最老的照片"
        else :
            if randomed == 2:
                text = "殺人不眨眼的人眼睛不會很乾嗎"
            else :
                if randomed == 3:
                    text = "玉皇大帝住平流層、對流層、中氣層還是增溫層？"
                else:
                    if randomed == 4:
                        text = "狗狗看到警犬會覺得警察來了嗎"
                    else:
                        if randomed == 5:
                            text = "一個半小時其實是三個半小時"
        
        await interaction.response.send_message(f"{text}")

    @app_commands.command(name = "ask-me", description = "問機器人問題")
    async def asking(self, interaction: discord.Interaction , text:str):
        
        randomed = random.randint(1, 21)
        if randomed >= 1 and randomed < 5:
            text = "建議您洽詢印度尼西亞最高諮詢委員會(DPA)"
        else :
            if randomed >= 5 and randomed < 8:
                text = "你說得對，但是你說的也不完全對。從某種角度來說，你說的有一點對，可是從另一個角度看，你說得不對。也不能說是完全不對，只能說離完全對之間還有一點不對。"
            else :
                if randomed >= 8 and randomed < 11:
                    text = "這個問題請文化局長回答，謝謝"
                else:
                    if randomed >=11 and randomed < 14:
                        text = "等等，都什麼時候了你還在這邊問問題?"
                    else:
                        if randomed >=14 and randomed < 17:
                            text = "如果他失敗了，那就代表他沒有成功。"
                        else:
                            if randomed >=17 and randomed < 21:
                                text = "糾結這種問題有甚麼意義呢?"  
                            else:
                                if randomed ==21:
                                    text = "對不起"  
        
        await interaction.response.send_message(f"{text}")


    

    @app_commands.command(name="three-round-battle", description="三回戰")
    @app_commands.describe(player1="輸入玩家一的名稱", player2="輸入玩家二的名稱")
    async def threeroundbattle(self, interaction: discord.Interaction, player1: str, player2: str):
        user_pattern = r'<@(\d+)>'
        id_pattern = r'\d+'
        #抓使用者id
        for user_string in [player1, player2]:
            match = re.match(user_pattern, user_string)
            if match:
                user_id = match.group(1)
                user = self.bot.get_user(int(user_id))
                if user:
                    player1 = player1.replace(user_string, user.name)
                    player2 = player2.replace(user_string, user.name)

        ans1 = random.randint(1, 100)
        ans2 = random.randint(1, 100)
        awin = 0
        bwin = 0

        # 使用for迴圈計算各回合對戰結果
        for i in range(3):
            if ans1 > ans2:
                texttemp = f"{player1}擲出了{ans1}點，贏過了{player2}的{ans2}點!"
                awin += 1
            else:
                texttemp = f"{player2}擲出了{ans2}點，贏過了{player1}的{ans1}點!"
                bwin += 1

            # 記錄每個回合的結果
            if i == 0:
                round1 = texttemp
            elif i == 1:
                round2 = texttemp
            elif i == 2:
                round3 = texttemp

            ans1 = random.randint(1, 100)
            ans2 = random.randint(1, 100)

        # 計算最後獲勝者
        if awin > bwin:
            text = f"{player1}獲勝!"
        else:
            text = f"{player2}獲勝!"

        # embed之類的東西
        embed = discord.Embed(title="三回戰!", description="賭博那是三回啊三回....", color=0xa600ff)
        embed.add_field(name="第一回合", value=f"{round1}", inline=True)
        embed.add_field(name="第二回合", value=f"{round2}", inline=True)
        embed.add_field(name="第三回合", value=f"{round3}", inline=True)
        embed.set_footer(text=f"結果:{text}")

        await interaction.response.send_message(embed=embed)

    
        
    

    # @app_commands.choices(參數 = [Choice(name = 顯示名稱, value = 隨意)])
    @app_commands.command(name = "caculate_def_old", description = "陸軍戰鬥分數計算(防守方)(舊版)")
    @app_commands.describe(army = "輸入軍隊數量", equipment = "輸入步兵裝備數量",tank = "輸入裝甲車輛數量",antitank = "輸入反坦克武器數量",antiair ="輸入防空武器數量",enemytank = "敵方是否具有裝甲單位",enemyair ="敵方是否具有空中單位", land = "選擇地形",land2 = "選擇地形(裝甲單位計算)", weather = "選擇氣候", support = "是否受補給懲罰", crypt = "是否破譯敵方密碼", other = "其他戰力加成(為1則免填)")
    @app_commands.choices(
    enemytank = [
        Choice(name = "是", value = 5.0),
        Choice(name = "否", value = 3.0),
    ] ,
    enemyair = [
        Choice(name = "是", value = 5.0),
        Choice(name = "否", value = 1.0),
    ] ,
    land = [
        Choice(name = "平原", value = 1.0),
        Choice(name = "山地與丘陵", value = 1.25),
        Choice(name = "叢林", value = 1.25),
        Choice(name = "沙漠", value = 0.5),
    ] ,
    land2 = [
        Choice(name = "平原", value = 1.5),
        Choice(name = "山地與丘陵", value = 0.5),
        Choice(name = "叢林", value = 0.5),
        Choice(name = "沙漠", value = 0.75),
    ] ,
    weather = [
        Choice(name = "炎熱", value = 0.5),
        Choice(name = "寒冷", value = 0.5),
        Choice(name = "沙塵暴", value = 0.25),
        Choice(name = "暴風雪", value = 0.25),
        Choice(name = "颱風", value = 0.25),
        Choice(name = "暴雨", value = 0.25),
        Choice(name = "無修正", value = 1.0),
    ] ,
    support = [
        Choice(name = "是", value = 0.75),
        Choice(name = "否", value = 1.0),
    ] ,
    crypt = [
        Choice(name = "是", value = 2.5),
        Choice(name = "否", value = 1.0),
    ] ,
    
)   
    async def caculate(self, interaction: discord.Interaction, army: int,equipment: int,tank: int,antitank :int,antiair :int,enemytank: Choice[float],enemyair: Choice[float] ,land: Choice[float],land2: Choice[float], weather: Choice[float], support: Choice[float], crypt: Choice[float],other: Optional[float] = None):
    # 獲取使用指令的使用者名稱
        customer = interaction.user.name
    # 使用者選擇的選項資料，可以使用name或value取值
        if other == None:
            other = 1.0
        enemyair = enemyair.value
        enemytank = enemytank.value
        land = land.value
        land2 = land2.value
        weather = weather.value
        support = support.value
        crypt = crypt.value
     
        totalscore = (army/10 + equipment + tank * land2 + antiair * enemyair + antitank * enemytank)
        output = (totalscore * land *  weather * support * crypt * other)
        await interaction.response.send_message(f"{customer} 的計算結果: {output}")

    @app_commands.command(name = "caculate_atk_old", description = "陸軍戰鬥分數計算(進攻方))(舊版)")
    @app_commands.describe(army = "輸入軍隊數量", equipment = "輸入步兵裝備數量",tank = "輸入裝甲車輛數量",antitank = "輸入反坦克武器數量",antiair ="輸入防空武器數量",enemytank = "敵方是否具有裝甲單位",enemyair ="敵方是否具有空中單位", land = "選擇地形",land2 = "選擇地形(裝甲單位計算)", weather = "選擇氣候", support = "是否受補給懲罰", crypt = "是否破譯敵方密碼", surprise = "是否奇襲" , other = "其他戰力加成(為1則免填)")
    @app_commands.choices(
    enemytank = [
        Choice(name = "是", value = 5.0),
        Choice(name = "否", value = 3.0),
    ] ,
    enemyair = [
        Choice(name = "是", value = 5.0),
        Choice(name = "否", value = 1.0),
    ] ,
    land = [
        Choice(name = "平原", value = 1.0),
        Choice(name = "山地與丘陵", value = 1.0),
        Choice(name = "叢林", value = 1.0),
        Choice(name = "沙漠", value = 0.5),
    ] ,
    land2 = [
        Choice(name = "平原", value = 1.5),
        Choice(name = "山地與丘陵", value = 0.5),
        Choice(name = "叢林", value = 0.5),
        Choice(name = "沙漠", value = 0.75),
    ] ,
    weather = [
        Choice(name = "炎熱", value = 0.5),
        Choice(name = "寒冷", value = 0.5),
        Choice(name = "沙塵暴", value = 0.25),
        Choice(name = "暴風雪", value = 0.25),
        Choice(name = "颱風", value = 0.25),
        Choice(name = "暴雨", value = 0.25),
        Choice(name = "無修正", value = 1.0),
    ] ,
    support = [
        Choice(name = "是", value = 0.75),
        Choice(name = "否", value = 1.0),
    ] ,
    crypt = [
        Choice(name = "是", value = 2.5),
        Choice(name = "否", value = 1.0),
    ] ,
    surprise = [
        Choice(name = "是", value = 1.5),
        Choice(name = "否", value = 1.0),
    ]
)   
    async def caculate2(self, interaction: discord.Interaction, army: int,equipment: int,tank: int,antitank :int,antiair :int,enemytank: Choice[float],enemyair: Choice[float] ,land: Choice[float],land2: Choice[float], weather: Choice[float], support: Choice[float], crypt: Choice[float], surprise: Choice[float],other: Optional[float] = None):
    # 獲取使用指令的使用者名稱
        customer = interaction.user.name
    # 使用者選擇的選項資料，可以使用name或value取值
        if other == None:
            other = 1.0
        enemyair = enemyair.value
        enemytank = enemytank.value
        land = land.value
        land2 = land2.value
        weather = weather.value
        support = support.value
        crypt = crypt.value
        surprise = surprise.value
        army = army/10
        tank = tank*10*land2
        antiair = antiair*enemyair
        antitank = antitank*enemytank
        totalscore = (army + equipment + tank  + antiair  + antitank )
        output = (totalscore * land *  weather * support * crypt * surprise * other)
        await interaction.response.send_message(f"{customer} 的計算結果: {output}")    

async def setup(bot: commands.Bot):
  await bot.add_cog(MyCog(bot))