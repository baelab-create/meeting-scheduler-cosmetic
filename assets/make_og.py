# 카톡 공유 썸네일(1200x630) — 세미나 페이지 모티브: 갈색 책상 + 흰 슬라이드 + 빨간 사선 탭
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = sys.argv[1]
FONT_DIR = r"C:\Users\user\Downloads\GmarketSansTTF"
BOLD = FONT_DIR + r"\GmarketSansTTFBold.ttf"
MED = FONT_DIR + r"\GmarketSansTTFMedium.ttf"
LIGHT = FONT_DIR + r"\GmarketSansTTFLight.ttf"

W, H = 1200, 630
img = Image.new("RGB", (W, H))
px = img.load()
# 책상: #6B6058 → #574E47 대각 그라데이션
c1, c2 = (0x6B, 0x60, 0x58), (0x57, 0x4E, 0x47)
for y in range(H):
    for x in range(W):
        t = (x / W * 0.4 + y / H * 0.6)
        px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

# 슬라이드 그림자
M = 54  # 바깥 여백
TAB_H = 64
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle((M, M + TAB_H + 12, W - M, H - M + 10), 10, fill=(0, 0, 0, 120))
shadow = shadow.filter(ImageFilter.GaussianBlur(22))
img = Image.alpha_composite(img.convert("RGBA"), shadow)

d = ImageDraw.Draw(img)
PAPER = (0xE8, 0xE5, 0xDF)
WHITE = (255, 255, 255)
RED = (0xFF, 0x4F, 0x4F)
RED_DIM = (0xEC, 0x52, 0x4E)
NAVY = (0x1F, 0x3A, 0x5C)
INK = (0x26, 0x26, 0x24)
SUB = (0x5E, 0x5B, 0x55)
GOLD = (0x8E, 0x82, 0x71)

# 슬라이드(뉴모픽 바탕)
d.rounded_rectangle((M, M + TAB_H, W - M, H - M), 8, fill=PAPER)

# 탭 줄: 흰 탭(공통 가능 시간) + 빨간 사선 탭 3개
def slanted(x0, x1, y0, y1, fill, skew=26):
    # 아래가 오른쪽으로 기운 평행사변형
    d.polygon([(x0, y0), (x1, y0), (x1 + skew, y1), (x0 + skew, y1)], fill=fill)

tab_y0, tab_y1 = M, M + TAB_H + 6
white_w = 300
d.rounded_rectangle((M, tab_y0, M + white_w, tab_y1 + 10), 14, fill=WHITE)
slanted(M + white_w - 40, M + white_w, tab_y0, tab_y1 + 10, WHITE)
labels = ["01  박래형 님", "02  배원규 교수님", "03  코스메틱 대표님"]
tab_w = (W - M - (M + white_w) - 30) // 3
f_tab = ImageFont.truetype(BOLD, 24)
x = M + white_w - 10
for i, lab in enumerate(labels):
    fill = RED if i == 0 else RED_DIM
    slanted(x, x + tab_w, tab_y0 + 8, tab_y1 + 10, fill)
    tw = d.textlength(lab, font=f_tab)
    d.text((x + (tab_w - tw) / 2 + 12, tab_y0 + 24), lab, font=f_tab, fill=(255, 237, 236))
    x += tab_w - 6
# 흰 탭 글자
f_bt = ImageFont.truetype(BOLD, 26)
f_bs = ImageFont.truetype(LIGHT, 14)
d.text((M + 26, tab_y0 + 14), "공통 가능 시간", font=f_bt, fill=INK)
d.text((M + 26, tab_y0 + 46), "미팅 일정 조율", font=f_bs, fill=GOLD)

# 본문: 제목 + 설명
f_h1 = ImageFont.truetype(BOLD, 64)
f_h2 = ImageFont.truetype(MED, 30)
f_p = ImageFont.truetype(LIGHT, 24)
top = M + TAB_H + 56
d.text((M + 70, top), "미팅 일정 조율", font=f_h1, fill=NAVY)
d.text((M + 70, top + 92), "박래형 님 · 배원규 교수님 · 코스메틱 대표님", font=f_h2, fill=INK)
d.text((M + 70, top + 150), "본인 탭에서 가능한 시간을 눌러 주세요.", font=f_p, fill=SUB)
d.text((M + 70, top + 188), "세 분 모두 되는 시간이 자동으로 모입니다.", font=f_p, fill=SUB)
d.text((M + 70, top + 226), "이번 주부터 3주 (월~금 10시~7시)", font=f_p, fill=GOLD)

# 오른쪽: 뉴모픽 시간표 미니어처
gx, gy = 760, M + TAB_H + 60
cell_w, cell_h, gap = 58, 40, 10
days = ["월", "화", "수", "목", "금"]
f_d = ImageFont.truetype(BOLD, 18)
f_c = ImageFont.truetype(BOLD, 18)
for c, day in enumerate(days):
    tw = d.textlength(day, font=f_d)
    d.text((gx + c * (cell_w + gap) + (cell_w - tw) / 2, gy), day, font=f_d, fill=NAVY)
pattern = [  # 0 떠 있음, 1 눌림(체크), 2 모두(빨강)
    [0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 1, 2, 1, 0],
    [0, 0, 2, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
]
light = Image.new("RGBA", img.size, (0, 0, 0, 0))
dark = Image.new("RGBA", img.size, (0, 0, 0, 0))
ld, dd = ImageDraw.Draw(light), ImageDraw.Draw(dark)
for r, row in enumerate(pattern):
    for c, v in enumerate(row):
        x0 = gx + c * (cell_w + gap)
        y0 = gy + 34 + r * (cell_h + gap)
        if v == 0:
            ld.rounded_rectangle((x0 - 4, y0 - 4, x0 + cell_w - 4, y0 + cell_h - 4), 10, fill=(255, 255, 255, 230))
            dd.rounded_rectangle((x0 + 4, y0 + 4, x0 + cell_w + 4, y0 + cell_h + 4), 10, fill=(163, 152, 136, 140))
light = light.filter(ImageFilter.GaussianBlur(5))
dark = dark.filter(ImageFilter.GaussianBlur(5))
img = Image.alpha_composite(img, dark)
img = Image.alpha_composite(img, light)
d = ImageDraw.Draw(img)
for r, row in enumerate(pattern):
    for c, v in enumerate(row):
        x0 = gx + c * (cell_w + gap)
        y0 = gy + 34 + r * (cell_h + gap)
        box = (x0, y0, x0 + cell_w, y0 + cell_h)
        if v == 0:
            d.rounded_rectangle(box, 10, fill=PAPER)
        elif v == 1:
            d.rounded_rectangle(box, 10, fill=(0xDD, 0xD9, 0xD2))
            d.rounded_rectangle((x0 + 1, y0 + 1, x0 + cell_w - 1, y0 + cell_h - 1), 10, outline=(0xD2, 0xCD, 0xC4))
            # 체크 표시는 폰트에 없으므로 선으로 그린다
            cx, cy = x0 + cell_w / 2, y0 + cell_h / 2
            d.line([(cx - 9, cy), (cx - 3, cy + 6), (cx + 9, cy - 7)], fill=RED_DIM, width=4, joint="curve")
        else:
            d.rounded_rectangle(box, 10, fill=RED_DIM)
            tw = d.textlength("모두", font=f_c)
            d.text((x0 + (cell_w - tw) / 2, y0 + 9), "모두", font=f_c, fill=WHITE)

img.convert("RGB").save(OUT, "JPEG", quality=90, optimize=True)
print("saved", OUT)
