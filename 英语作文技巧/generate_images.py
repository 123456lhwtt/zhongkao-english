#!/usr/bin/env python3
"""
中考英语写作技巧 - 小红书图文生成器
输出9张 1080×1440 竖版图片
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# === 配置 ===
W, H = 1080, 1440
OUTPUT_DIR = "/Users/wtt/Desktop/鲁欣雨-英语/英语作文技巧/output_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 字体
FONT_TITLE = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 72)
FONT_SUBTITLE = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 44)
FONT_BODY = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", 32)
FONT_SMALL = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", 26)
FONT_MINI = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", 22)
FONT_BOLD = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 36)
FONT_NUM = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 56)

# 配色方案
BG_CREAM = "#FEF9F0"
BG_BLUE = "#E8F0FE"
BG_WHITE = "#FFFFFF"
RED = "#E8553D"
DARK = "#2C3E50"
GOLD = "#D4A574"
BLUE = "#4A90D9"
GREEN = "#5CB85C"
LIGHT_GRAY = "#F5F5F5"
MID_GRAY = "#888888"
BLACK = "#1A1A1A"
CARD_SHADOW = "#D0D0D0"


def hex_to_rgb(hex_color):
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def create_base(bg_color=BG_CREAM):
    """创建基础画布"""
    return Image.new("RGB", (W, H), hex_to_rgb(bg_color))


def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    """绘制圆角矩形"""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_card(draw, x, y, card_w, card_h, fill="#FFFFFF", radius=20, shadow=True):
    """绘制卡片（带阴影效果）"""
    if shadow:
        draw_rounded_rect(draw, (x+5, y+5, x+card_w+5, y+card_h+5),
                         radius=radius, fill=hex_to_rgb(CARD_SHADOW))
    draw_rounded_rect(draw, (x, y, x+card_w, y+card_h),
                     radius=radius, fill=hex_to_rgb(fill))


def draw_tag(draw, x, y, text, bg_color=RED, font=FONT_MINI):
    """绘制标签"""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = 10
    draw_rounded_rect(draw, (x, y, x+tw+pad*2, y+th+pad*2),
                     radius=th//2+pad, fill=hex_to_rgb(bg_color))
    draw.text((x+pad, y+pad), text, fill="#FFFFFF", font=font)


def draw_centered_text(draw, text, y, font=FONT_BODY, fill=BLACK, max_width=None):
    """居中绘制文本，返回下一行的 y 坐标"""
    color = hex_to_rgb(fill)
    if max_width is None:
        max_width = W - 120
    # 简单换行
    lines = []
    current_line = ""
    for char in text:
        test = current_line + char
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] > max_width:
            lines.append(current_line)
            current_line = char
        else:
            current_line = test
    if current_line:
        lines.append(current_line)

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, y), line, fill=color, font=font)
        y += bbox[3] - bbox[1] + 8
    return y


def draw_left_text(draw, text, x, y, font=FONT_BODY, fill=BLACK):
    """左对齐绘制，返回 y 坐标"""
    color = hex_to_rgb(fill)
    draw.text((x, y), text, fill=color, font=font)
    bbox = draw.textbbox((0, 0), text, font=font)
    return y + bbox[3] - bbox[1] + 4


def draw_section_title(draw, text, y, icon=""):
    """绘制章节标题"""
    full_text = f"{icon} {text}" if icon else text
    bbox = draw.textbbox((0, 0), full_text, font=FONT_SUBTITLE)
    tw = bbox[2] - bbox[0]
    x = 60
    # 左侧色块装饰
    draw.rectangle((x, y+8, x+6, y+bbox[3]-bbox[1]-8), fill=hex_to_rgb(RED))
    draw.text((x+22, y), full_text, fill=hex_to_rgb(DARK), font=FONT_SUBTITLE)
    return y + bbox[3] - bbox[1] + 30


def draw_bottom_bar(draw):
    """绘制底部标签栏"""
    y_bar = H - 80
    draw.rectangle((0, y_bar, W, H), fill=hex_to_rgb(DARK))
    tags = ["#中考英语", "#英语作文", "#中考冲刺", "#学英语", "#学霸秘籍"]
    tag_font = FONT_SMALL
    total_w = 0
    for tag in tags:
        b = draw.textbbox((0, 0), tag, font=tag_font)
        total_w += b[2] - b[0] + 30
    start_x = (W - total_w) // 2
    for tag in tags:
        b = draw.textbbox((0, 0), tag, font=tag_font)
        draw.text((start_x, y_bar+20), tag, fill="#FFFFFF", font=tag_font)
        start_x += b[2] - b[0] + 30


def save_image(img, name):
    path = os.path.join(OUTPUT_DIR, name)
    img.save(path, quality=95)
    print(f"  ✓ 已保存: {name}")


# ============================================================
# 图1: 封面
# ============================================================
def generate_cover():
    img = create_base(BG_BLUE)
    draw = ImageDraw.Draw(img)

    # 右上角装饰
    draw_rounded_rect(draw, (W-200, 60, W-40, 200), radius=20, fill=hex_to_rgb(RED))
    draw.text((W-165, 80), "🏆", font=FONT_NUM)

    # 主标题
    y = 280
    draw_centered_text(draw, "中考英语作文", y, font=FONT_TITLE, fill=DARK)
    y += 120
    draw_centered_text(draw, "满分秘籍", y, font=FONT_TITLE, fill=RED)
    y += 150

    # 副标题
    draw_centered_text(draw, "万能模板 + 高分句型", y, font=FONT_SUBTITLE, fill=DARK)
    y += 70
    draw_centered_text(draw, "背完直接套！", y, font=FONT_SUBTITLE, fill=RED)

    # 装饰分隔线
    y += 80
    x_line = W//2 - 200
    draw.line((x_line, y, x_line+400, y), fill=hex_to_rgb(GOLD), width=3)

    # 底部副标题
    y += 60
    draw_centered_text(draw, "初三党必藏 ⭐", y, font=FONT_BOLD, fill=DARK)
    y += 60
    draw_centered_text(draw, "写作模板 × 高分句型 × 加分技巧", y, font=FONT_BODY, fill=MID_GRAY)

    # 左上角装饰
    draw_rounded_rect(draw, (40, 60, 160, 200), radius=15, fill=hex_to_rgb(GOLD))
    draw.text((65, 90), "A+", font=FONT_TITLE, fill="#FFFFFF")

    draw_bottom_bar(draw)
    save_image(img, "01_封面.png")


# ============================================================
# 图2: 写作四步法
# ============================================================
def generate_step2():
    img = create_base(BG_CREAM)
    draw = ImageDraw.Draw(img)

    y = draw_section_title(draw, '写作“四步法”——别上来就写！', 80, "✍️")

    # 四步卡片 - 2x2 网格
    steps = [
        ("①", "审", "看清题目要求、文体、\n人称、时态", RED),
        ("②", "列", "列提纲，不会的词用\n同义词替换，避难就易", BLUE),
        ("③", "连", "连句成文分3段，\n长短句+复合句搭配", GREEN),
        ("④", "改", "检查拼写/时态/单复数\n/主谓一致/标点", GOLD),
    ]

    card_w, card_h = 440, 260
    positions = [(60, 240), (580, 240), (60, 530), (580, 530)]

    for (num, title, desc, color), (cx, cy) in zip(steps, positions):
        draw_card(draw, cx, cy, card_w, card_h)

        # 编号圆圈
        draw_rounded_rect(draw, (cx+20, cy+20, cx+80, cy+80),
                         radius=30, fill=hex_to_rgb(color))
        draw.text((cx+35, cy+28), num, fill="#FFFFFF", font=FONT_NUM)

        # 标题
        draw.text((cx+100, cy+30), title, fill=hex_to_rgb(color), font=FONT_BOLD)
        # 描述
        draw_left_text(draw, desc, cx+100, cy+90, font=FONT_BODY, fill=DARK)

    # 底部口诀卡片
    y_card = 830
    draw_card(draw, 60, y_card, W-120, 220, fill="#FFF3E0", shadow=False)

    # 口诀标题
    bbox = draw.textbbox((0, 0), "💡 牢记口诀", font=FONT_BOLD)
    draw.text((100, y_card+30), "💡 牢记口诀：", fill=hex_to_rgb(RED), font=FONT_BOLD)

    mantra = "三审：体裁 → 时态 → 人称\n三思：词汇 → 短语 → 句式\n三查：要点 → 拼写语法 → 连贯"
    y_line = y_card + 80
    for line in mantra.split('\n'):
        draw_left_text(draw, line, 120, y_line, font=FONT_BODY, fill=DARK)
        y_line += 42

    # 右侧装饰
    draw_rounded_rect(draw, (W-200, y_card+30, W-100, y_card+190),
                     radius=15, fill=hex_to_rgb(BLUE))

    draw_bottom_bar(draw)
    save_image(img, "02_写作四步法.png")


# ============================================================
# 图3: 万能三段式
# ============================================================
def generate_step3():
    img = create_base(BG_WHITE)
    draw = ImageDraw.Draw(img)

    y = draw_section_title(draw, "万能三段式——什么作文都能套", 80, "🎯")

    # 三段式可视化
    sections = [
        ("第1段 · 引入", "1-2句 · 引入主题 + 亮出观点",
         "例：With the development of..., more and more\npeople are paying attention to...",
         RED),
        ("第2段 · 正文", "3-6句 · 2~3个论点 + 过渡连接词",
         "必用：First... Besides... What's more...\nFinally... / On the one hand... On the other hand...",
         BLUE),
        ("第3段 · 结尾", "1-2句 · 总结升华",
         "万能金句：I'm confident that a bright future\nis awaiting us because...",
         GREEN),
    ]

    y_card = 240
    for title, subtitle, example, color in sections:
        draw_card(draw, 60, y_card, W-120, 280)
        # 左侧色条
        draw.rectangle((60, y_card, 72, y_card+280), fill=hex_to_rgb(color))
        # 标题
        draw.text((100, y_card+30), title, fill=hex_to_rgb(color), font=FONT_BOLD)
        # 副标题
        draw.text((100, y_card+80), subtitle, fill=hex_to_rgb(MID_GRAY), font=FONT_SMALL)
        # 分隔线
        draw.line((100, y_card+130, W-120, y_card+130), fill=hex_to_rgb(LIGHT_GRAY), width=2)
        # 例句
        y_ex = y_card + 155
        for line in example.split('\n'):
            draw_left_text(draw, line, 100, y_ex, font=FONT_BODY, fill=DARK)
            y_ex += 38
        y_card += 310

    draw_bottom_bar(draw)
    save_image(img, "03_万能三段式.png")


# ============================================================
# 图4: 十大万能句型（上）
# ============================================================
def generate_step4():
    img = create_base(BG_CREAM)
    draw = ImageDraw.Draw(img)

    y = draw_section_title(draw, "必背万能句型（上）", 80, "🏆")

    patterns = [
        ("1️⃣", "It goes without saying that...", "不用说……",
         "It goes without saying that it pays to keep early hours.", RED),
        ("2️⃣", "Among various kinds of..., ...", "在各种……之中",
         "Among various kinds of sports, I like jogging in particular.", BLUE),
        ("3️⃣", "In my opinion / As far as I am concerned", "就我而言……",
         "In my opinion, playing video games is harmful to health.", GREEN),
        ("4️⃣", "With the development of...", "随着……的发展",
         "With the rapid development of economy, our life has changed a lot.", GOLD),
        ("5️⃣", "Every coin has two sides.", "凡事都有两面性",
         "Every coin has two sides. Mobile phones have both advantages and disadvantages.", RED),
    ]

    y_card = 240
    for num, en, cn, example, color in patterns:
        draw_card(draw, 60, y_card, W-120, 160)
        # 编号
        draw.text((90, y_card+20), num, font=FONT_BOLD)
        # 英文句型
        draw.text((160, y_card+18), en, fill=hex_to_rgb(color), font=FONT_BOLD)
        # 中文
        draw.text((160, y_card+58), cn, fill=hex_to_rgb(MID_GRAY), font=FONT_SMALL)
        # 例句
        draw_left_text(draw, f"📝 {example}", 100, y_card+95, font=FONT_MINI, fill=DARK)
        y_card += 180

    draw_bottom_bar(draw)
    save_image(img, "04_万能句型上.png")


# ============================================================
# 图5: 十大万能句型（下）+ 高级替换词
# ============================================================
def generate_step5():
    img = create_base(BG_WHITE)
    draw = ImageDraw.Draw(img)

    y = draw_section_title(draw, "必背万能句型（下）", 80, "🏆")

    patterns2 = [
        ("6️⃣", "not only...but also...", "不仅……而且……（用倒装更高级！）",
         "Not only can she play well, but she also writes music.", BLUE),
        ("7️⃣", "so + adj./adv. + that...", "如此……以至于……",
         "I was so upset that I wanted to give up.", GREEN),
        ("8️⃣", "Whenever I..., I cannot but feel...", "每当……我就忍不住……",
         "Whenever I think of home, I cannot but feel warm.", RED),
        ("9️⃣", "It is + adj. + for sb. to do sth.", "对某人来说做某事是……的",
         "It is important for us to protect the environment.", GOLD),
        ("🔟", "There is no denying that...", "毫无疑问……",
         "There is no denying that education plays a key role in our life.", RED),
    ]

    y_card = 240
    for num, en, cn, example, color in patterns2:
        draw_card(draw, 60, y_card, W-120, 145)
        draw.text((90, y_card+15), num, font=FONT_BOLD)
        draw.text((160, y_card+12), en, fill=hex_to_rgb(color), font=FONT_BOLD)
        draw.text((160, y_card+50), cn, fill=hex_to_rgb(MID_GRAY), font=FONT_SMALL)
        draw_left_text(draw, f"📝 {example}", 100, y_card+85, font=FONT_MINI, fill=DARK)
        y_card += 162

    # 高级替换词表
    y_card += 5
    draw_section_title(draw, "阅卷老师最爱的替换词", y_card, "✨")
    y_card += 55

    replacements = [
        ("think", "believe / hold the view that / maintain"),
        ("very", "extremely / remarkably"),
        ("more and more", "an increasing number of"),
        ("good", "beneficial / positive / favorable"),
        ("bad", "harmful / negative / detrimental"),
        ("important", "essential / significant / indispensable"),
    ]

    draw_card(draw, 60, y_card, W-120, 220)
    draw.text((90, y_card+15), "普通词", fill=hex_to_rgb(RED), font=FONT_BOLD)
    draw.text((280, y_card+15), "→", fill=hex_to_rgb(MID_GRAY), font=FONT_BOLD)
    draw.text((330, y_card+15), "高级替换", fill=hex_to_rgb(GREEN), font=FONT_BOLD)

    y_r = y_card + 55
    for plain, fancy in replacements:
        draw.text((90, y_r), plain, fill=hex_to_rgb(MID_GRAY), font=FONT_SMALL)
        draw.text((260, y_r), "→", fill=hex_to_rgb(RED), font=FONT_SMALL)
        draw.text((290, y_r), fancy, fill=hex_to_rgb(DARK), font=FONT_SMALL)
        y_r += 30

    draw_bottom_bar(draw)
    save_image(img, "05_万能句型下_替换词.png")


# ============================================================
# 图6: 议论文模板
# ============================================================
def generate_step6():
    img = create_base(BG_CREAM)
    draw = ImageDraw.Draw(img)

    y = draw_section_title(draw, "议论文万能模板（最常考！）", 80, "📖")

    templates = [
        ("正反观点型", RED,
         "P1: Recently we've had a discussion about\n    whether...Our opinions are divided.\n"
         "P2: Most students are in favour of it.\n    First... Second... Finally...\n"
         "P3: However, the others are strongly\n    against it. Their reasons are as follows...\n"
         "P4: Personally, the advantages overweigh\n    the disadvantages. I support it."),
        ("观点论述型（总-分-总）", BLUE,
         "P1: As a student, I'm strongly in favour of...\n    The reasons are as follows.\n"
         "P2: First of all... Secondly... Besides...\n"
         "P3: In conclusion, I believe that..."),
        ("How to 解决问题型", GREEN,
         "P1: 提出现象/困难作为话题引入\n"
         "P2: Many ways can help to solve it.\n    First of all... Another way... Finally...\n"
         "P3: These are the most effective measures.\n    We should take action to..."),
        ("利弊分析型", GOLD,
         "P1: Nowadays, there is widespread concern\n    over ___ . It has both advantages and\n    disadvantages.\n"
         "P2: Advantages: Firstly... Secondly...\n"
         "P3: Disadvantages: To begin with...\n    In addition...\n"
         "P4: To sum up, we should bring advantages\n    into full play and reduce disadvantages."),
    ]

    y_card = 240
    for title, color, content in templates:
        draw_card(draw, 60, y_card, W-120, 220)
        # 标题栏
        draw_rounded_rect(draw, (60, y_card, W-60, y_card+50),
                         radius=20, fill=hex_to_rgb(color))
        draw.text((90, y_card+10), f"📌 {title}", fill="#FFFFFF", font=FONT_BOLD)

        y_line = y_card + 65
        for line in content.split('\n'):
            if line.strip():
                draw_left_text(draw, line, 90, y_line, font=FONT_SMALL, fill=DARK)
                y_line += 30
        y_card += 240

    draw_bottom_bar(draw)
    save_image(img, "06_议论文模板.png")


# ============================================================
# 图7: 书信 & 口头通知
# ============================================================
def generate_step7():
    img = create_base(BG_WHITE)
    draw = ImageDraw.Draw(img)

    y = draw_section_title(draw, "书信 & 口头通知——格式分必拿！", 80, "✉️📢")

    # 书信（左）
    y_s = 240
    draw_card(draw, 40, y_s, 485, 520)

    draw.text((65, y_s+20), "✉️ 书信模板", fill=hex_to_rgb(RED), font=FONT_BOLD)

    letter = [
        ("【开头】", [
            "How nice to hear from you again.",
            "I'm glad to receive your letter of...",
            "I'm writing to thank you for...",
        ]),
        ("【正文过渡】", [
            "Let me tell you about...",
            "I'd like to introduce... to you.",
        ]),
        ("【结尾】", [
            "I'm looking forward to your reply.",
            "I'd appreciate it if you could reply.",
            "With best wishes.",
        ]),
    ]

    y_l = y_s + 65
    for section, lines in letter:
        draw_left_text(draw, section, 65, y_l, font=FONT_SMALL, fill=RED)
        y_l += 32
        for line in lines:
            draw_left_text(draw, f"• {line}", 75, y_l, font=FONT_MINI, fill=DARK)
            y_l += 28
        y_l += 8

    # 口头通知（右）
    draw_card(draw, 555, y_s, 485, 520)

    draw.text((580, y_s+20), "📢 口头通知", fill=hex_to_rgb(BLUE), font=FONT_BOLD)

    notice = [
        ("【呼语】", [
            "Ladies and gentlemen,",
            "May I have your attention, please?",
            "I have an announcement to make.",
        ]),
        ("【正文】", [
            "All the teachers and students",
            "are required to attend it.",
            "Please take your notebooks",
            "and make notes.",
        ]),
        ("【结束语】", [
            "Everybody is welcome to attend.",
            "I hope you'll have a nice time.",
            "That's all. Thank you!",
        ]),
    ]

    y_n = y_s + 65
    for section, lines in notice:
        draw_left_text(draw, section, 580, y_n, font=FONT_SMALL, fill=BLUE)
        y_n += 32
        for line in lines:
            draw_left_text(draw, f"• {line}", 590, y_n, font=FONT_MINI, fill=DARK)
            y_n += 28
        y_n += 8

    # 底部警告
    y_w = 800
    draw_card(draw, 40, y_w, W-80, 100, fill="#FFF3E0", shadow=False)
    draw.text((80, y_w+20), "⚠️", font=FONT_BOLD)
    draw.text((120, y_w+22), "书信格式完整性很重要！称呼→正文→结束语→签名，缺一不可！",
              fill=hex_to_rgb(RED), font=FONT_BODY)

    draw_bottom_bar(draw)
    save_image(img, "07_书信口头通知.png")


# ============================================================
# 图8: 连接词大全 + 加分技巧
# ============================================================
def generate_step8():
    img = create_base(BG_CREAM)
    draw = ImageDraw.Draw(img)

    y = draw_section_title(draw, "连接词大全 + 加分技巧", 80, "🔗✨")

    # 左侧：连接词表
    draw_card(draw, 40, 240, 520, 580)
    draw.text((65, 260), "🔗 连接词分类速记", fill=hex_to_rgb(RED), font=FONT_BOLD)

    connectors = [
        ("顺序", "first, to begin with, what's more,\nfinally, last but not least"),
        ("转折", "however, nevertheless,\non the other hand, whereas"),
        ("递进", "in addition, besides, moreover,\nfurthermore"),
        ("因果", "therefore, thus, as a result,\nconsequently"),
        ("举例", "for example, for instance,\nsuch as, take...as an example"),
        ("总结", "in a word, in conclusion,\nto sum up, in brief"),
    ]

    y_c = 310
    for title, words in connectors:
        draw_tag(draw, 65, y_c, title, bg_color=BLUE if title in ["顺序", "递进"] else
                 RED if title in ["转折", "因果"] else GREEN)
        draw_left_text(draw, words, 160, y_c-2, font=FONT_MINI, fill=DARK)
        y_c += 68

    # 右侧：加分技巧
    draw_card(draw, 580, 240, 460, 580)
    draw.text((610, 260), "✨ 加分大招", fill=hex_to_rgb(RED), font=FONT_BOLD)

    tips = [
        ("倒装句", "Only in this way can we\nsolve the problem."),
        ("强调句", "It is...that...\nIt was Jack who helped me."),
        ("名言开头", "As a proverb says,\n\"No pains, no gains.\""),
        ("数字论证", "According to a survey,\n85% of students..."),
        ("结尾升华", "I'm confident that a bright\nfuture is awaiting us."),
        ("感叹句", "What a meaningful\nactivity it was!"),
    ]

    y_t = 310
    for title, example in tips:
        draw_tag(draw, 610, y_t, title, bg_color=GOLD)
        draw_left_text(draw, example, 610, y_t+35, font=FONT_MINI, fill=DARK)
        y_t += 90

    # 底部提示
    y_b = 870
    draw_card(draw, 40, y_b, W-80, 80, fill="#E8F5E9", shadow=False)
    draw.text((80, y_b+20), "💡 每段至少用1个连接词，作文立马上一个档次！",
              fill=hex_to_rgb(GREEN), font=FONT_BODY)

    draw_bottom_bar(draw)
    save_image(img, "08_连接词_加分技巧.png")


# ============================================================
# 图9: 10大热门话题 + 结尾
# ============================================================
def generate_step9():
    img = create_base(BG_WHITE)
    draw = ImageDraw.Draw(img)

    y = draw_section_title(draw, "10大中考英语热门话题", 80, "🎁")

    topics = [
        ("♻️ 环保", "Protect the environment", "take effective measures"),
        ("💪 健康", "Healthy habits are important", "get enough sleep, exercise"),
        ("😌 减压", "Pressure is a serious problem", "talk with parents / teachers"),
        ("📚 读书", "Reading is a good habit", "improve knowledge, think deeply"),
        ("📱 手机", "Every coin has two sides", "advantages & disadvantages"),
        ("❤️ 志愿服务", "To help others = help ourselves", "make a big difference"),
        ("🛡️ 校园安全", "Treasure and protect our lives", "obey rules, eat healthy"),
        ("📝 学习方法", "Practice makes perfect", "listen, speak, read, write"),
        ("🏮 传统节日", "Introduce Chinese festivals", "Spring Festival, Mid-Autumn"),
        ("🌟 梦想", "Everyone has dreams", "work hard to achieve them"),
    ]

    y_card = 230
    col = 0
    for i, (label, en, key) in enumerate(topics):
        if i % 2 == 0:
            y_card = 230 + (i // 2) * 100

        cx = 40 if i % 2 == 0 else 555
        card_w = 485

        draw_card(draw, cx, y_card, card_w, 82, radius=12)
        draw.text((cx+20, y_card+8), label, font=FONT_SMALL)
        draw.text((cx+110, y_card+8), en, fill=hex_to_rgb(DARK), font=FONT_SMALL)
        draw_left_text(draw, f"⇢ {key}", cx+110, y_card+42, font=FONT_MINI, fill=MID_GRAY)

    # 结尾金句
    y_end = 780
    draw_card(draw, 40, y_end, W-80, 180, fill=BG_BLUE, shadow=False)
    draw_centered_text(draw, "💬 中考英语作文就这回事！", y_end+30, font=FONT_BOLD, fill=DARK)
    draw_centered_text(draw, "背模板 + 记句型 + 三段式 + 连接词 + 高级词", y_end+75,
                      font=FONT_SMALL, fill=DARK)
    draw_centered_text(draw, "= 高分稳了！", y_end+110, font=FONT_BOLD, fill=RED)

    # 底部
    y_act = 1000
    draw_centered_text(draw, "收藏 ★ 打印贴书桌，考前翻一遍 🔖", y_act, font=FONT_BODY, fill=DARK)
    draw_centered_text(draw, "评论区欢迎交流英语学习问题 👇", y_act+50, font=FONT_SMALL, fill=MID_GRAY)

    draw_bottom_bar(draw)
    save_image(img, "09_热门话题_结尾.png")


# ============================================================
# 主函数
# ============================================================
def main():
    print("\n🎨 开始生成小红书图文（1080×1440）...\n")

    generators = [
        ("封面", generate_cover),
        ("写作四步法", generate_step2),
        ("万能三段式", generate_step3),
        ("万能句型(上)", generate_step4),
        ("万能句型(下)+替换词", generate_step5),
        ("议论文模板", generate_step6),
        ("书信口头通知", generate_step7),
        ("连接词+加分技巧", generate_step8),
        ("热门话题+结尾", generate_step9),
    ]

    for name, func in generators:
        print(f"  生成第{generators.index((name, func))+1}张: {name}...")
        func()

    print(f"\n✅ 全部完成！共9张图片已保存到:")
    print(f"   {OUTPUT_DIR}\n")


if __name__ == "__main__":
    main()
