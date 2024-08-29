import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="?", intents=intents)

class Player:
    def __init__(self):
        self.points = 0
        self.defense = 0
        self.action = None

class GameState:
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.turn = 0
        self.game_over = False
        self.player1_id = None
        self.player2_id = None

game_state = GameState()

def process_turn():
    player1_action = game_state.player1.action
    player2_action = game_state.player2.action
    result = f"玩家1選擇了{player1_action}，玩家2選擇了{player2_action}。\n"

    # 檢查玩家點數是否足夠
    if (player1_action == '輕攻擊' and game_state.player1.points < 1) or \
       (player1_action == '重攻擊' and game_state.player1.points < 2) or \
       (player1_action == '特殊攻擊' and game_state.player1.points < 4):
        result += "玩家1點數不足，無法使用該技能。\n"
        return result

    if (player2_action == '輕攻擊' and game_state.player2.points < 1) or \
       (player2_action == '重攻擊' and game_state.player2.points < 2) or \
       (player2_action == '特殊攻擊' and game_state.player2.points < 4):
        result += "玩家2點數不足，無法使用該技能。\n"
        return result
   
    # 處理玩家1行動
    if player1_action == '蓄力':
        game_state.player1.points += 1
        result += "玩家1獲得一點點數。\n"
    elif player1_action == '普通防禦':
        game_state.player1.defense += 1
    elif player1_action == '輕攻擊':
        game_state.player1.points -= 1
    elif player1_action == '重攻擊':
        game_state.player1.points -= 2
    elif player1_action == '特殊防禦':
        pass
    elif player1_action == '特殊攻擊':
        game_state.player1.points -= 4

    # 處理玩家2行動
    if player2_action == '蓄力':
        game_state.player2.points += 1
        result += "玩家2獲得一點點數。\n"
    elif player2_action == '普通防禦':
        game_state.player2.defense += 1
    elif player2_action == '輕攻擊':
        game_state.player2.points -= 1
    elif player2_action == '重攻擊':
        game_state.player2.points -= 2
    elif player2_action == '特殊防禦':
        pass
    elif player2_action == '特殊攻擊':
        game_state.player2.points -= 4

    # 判斷結果
    if player1_action == '蓄力' and player2_action in ['輕攻擊', '重攻擊', '特殊攻擊']:
        result += "玩家1在蓄力時被攻擊，玩家1死亡！\n"
        game_state.game_over = True
        result += "玩家2獲勝！"
    elif player2_action == '蓄力' and player1_action in ['輕攻擊', '重攻擊', '特殊攻擊']:
        result += "玩家2在蓄力時被攻擊，玩家2死亡！\n"
        game_state.game_over = True
        result += "玩家1獲勝！"
    elif player1_action == '輕攻擊' and player2_action == '普通防禦':
        result += "玩家2使用普通防禦抵擋了輕攻擊。\n"
    elif player1_action == '重攻擊' and player2_action == '普通防禦':
        result += "玩家2使用普通防禦抵擋了重攻擊。\n"
    elif player1_action == '特殊攻擊' and player2_action == '特殊防禦':
        result += "玩家2使用特殊防禦抵擋了特殊攻擊。\n"
    elif player1_action == '特殊攻擊' and player2_action not in ['特殊防禦']:
        result += "玩家2被特殊攻擊穿透，玩家2死亡！\n"
        game_state.game_over = True
        result += "玩家1獲勝！"
    elif player1_action == '重攻擊' and player2_action == '輕攻擊':
        result += "玩家1的重攻擊穿透了玩家2的輕攻擊，玩家2死亡！\n"
        game_state.game_over = True
        result += "玩家1獲勝！"
    elif player2_action == '輕攻擊' and player1_action == '普通防禦':
        result += "玩家1使用普通防禦抵擋了輕攻擊。\n"
    elif player2_action == '重攻擊' and player1_action == '普通防禦':
        result += "玩家1使用普通防禦抵擋了重攻擊。\n"
    elif player2_action == '重攻擊' and player1_action == '輕攻擊':
        result += "玩家2的重攻擊穿透了玩家1的輕攻擊，玩家1死亡！\n"
        game_state.game_over = True
        result += "玩家2獲勝！"
    elif player2_action == '特殊攻擊' and player1_action == '特殊防禦':
        result += "玩家1使用特殊防禦抵擋了特殊攻擊。\n"
    elif player2_action == '特殊攻擊' and player1_action not in ['特殊防禦']:
        result += "玩家1被特殊攻擊穿透，玩家1死亡！\n"
        game_state.game_over = True
        result += "玩家2獲勝！"

    return result
class MYCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @commands.command(name='start_duo')
    async def start_duo_game(self,ctx):
        game_state.__init__()  # 重置遊戲狀態
        game_state.player1_id = ctx.author.id
        game_state.turn = 1
        await ctx.send("雙人遊戲開始！玩家1請使用?moves <skill>來選擇你的技能。技能有：蓄力, 普通防禦, 輕攻擊, 重攻擊, 特殊防禦, 特殊攻擊")

    @commands.command(name='join')
    async def join_game(self,ctx):
        if game_state.player1_id is None:
            await ctx.send("請先使用?start_duo來開始雙人遊戲。")
            return

        if game_state.player2_id is None:
            game_state.player2_id = ctx.author.id
            await ctx.send("玩家2已加入遊戲！玩家2請使用?moves <skill>來選擇你的技能。")
        else:
            await ctx.send("遊戲已滿，請等待下一局。")

    @commands.command(name='moves')
    async def player_move(self,ctx, skill: str):
        if game_state.game_over:
            await ctx.send("遊戲已結束，請使用?start_duo來重新開始遊戲。")
            return

        if ctx.author.id != game_state.player1_id and ctx.author.id != game_state.player2_id:
            await ctx.send("你不是遊戲中的玩家。")
            return

        valid_skills = ['蓄力', '普通防禦', '輕攻擊', '重攻擊', '特殊防禦', '特殊攻擊']
        if skill not in valid_skills:
            await ctx.send("無效的技能，請選擇：蓄力, 普通防禦, 輕攻擊, 重攻擊, 特殊防禦, 特殊攻擊")
            return

        if ctx.author.id == game_state.player1_id:
            game_state.player1.action = skill
        elif ctx.author.id == game_state.player2_id:
            game_state.player2.action = skill

        if game_state.player1.action and game_state.player2.action:
            result = process_turn()
            await ctx.send(result)
            game_state.player1.action = None
            game_state.player2.action = None
            if not game_state.game_over:
                await ctx.send("請玩家1和玩家2選擇下一個技能。")
        else:
            await ctx.send(f"{ctx.author.name} 已選擇了技能，等待另一位玩家的選擇。")

# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(MYCog(bot))
