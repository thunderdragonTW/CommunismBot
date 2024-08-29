# 導入Discord.py模組
import discord
# 導入commands指令模組
from discord.ext import commands
import os
import asyncio
import logging
import logging.handlers


from package.config import  FILENAME



log = logging.getLogger(FILENAME)

# intents是要求機器人的權限
intents = discord.Intents.all()
# command_prefix是前綴符號，可以自由選擇($, #, &...)
bot = commands.Bot(command_prefix = "?", intents = intents)

def init_logger(self, debug: bool=False):
        
        formatter = logging.Formatter("[{asctime}] {levelname} {name}: {message}", datefmt="%Y-%m-%d %H:%M:%S", style="{")
        
        if debug:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)
            
        file_handler = logging.handlers.RotatingFileHandler(
            filename=f"{FILENAME}.log",
            encoding="utf-8",
            maxBytes=8**7, 
            backupCount=8
        )
        
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logging.getLogger().addHandler(file_handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)

# 當機器人完成啟動
@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f"成功登入，目前登入身份 --> {bot.user}")
    print(f"成功載入 {len(slash)} 個斜線指令")
 
@bot.command(name="sync") 
async def sync(ctx):
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s).")

async def load_extensions():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cogs_dir = os.path.join(base_dir, "cogs")
    
    #Cog導向路徑處理
    print("Cog導向路徑:", cogs_dir)
    
   
    if not os.path.exists(cogs_dir):
        print(f"Directory '{cogs_dir}' does not exist.")
        return
   
    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start("YOUR TOKEN HERE, I GUESS")

if __name__ == "__main__":
    asyncio.run(main())





    