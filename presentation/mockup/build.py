#!/usr/bin/env python3
"""
Собирает эталонные слайды по спеке brand.md как HTML 1920x1080 и снимает PNG
через встроенный Chromium. Нужно, потому что генератор Canva до этого вида
не дотягивает — эти кадры служат визуальным образцом для сборки в Canva.

Запуск: python3 build.py
"""
import pathlib
import subprocess

OUT = pathlib.Path(__file__).parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

# Палитра из brand.md
BG, BG_DEEP = "#0E1116", "#05070A"
FG, DIM = "#F2F5F7", "#7E8B9A"
COLD, WARM = "#22D3EE", "#FF9F45"

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1920px;height:1080px;overflow:hidden}}
body{{background:{BG};color:{FG};
  font-family:"Liberation Sans","DejaVu Sans",sans-serif;
  -webkit-font-smoothing:antialiased}}
.slide{{position:relative;width:1920px;height:1080px;padding:110px 130px;
  display:flex;flex-direction:column}}
/* лёгкая виньетка, чтобы графит не читался плоским пятном */
.slide::after{{content:"";position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(120% 120% at 50% 40%,transparent 45%,rgba(0,0,0,.55) 100%)}}
.hud{{font-family:"Liberation Mono","DejaVu Sans Mono",monospace;
  font-size:19px;letter-spacing:.18em;color:{DIM};line-height:2.1}}
.hud .on{{color:{COLD}}}
.corner{{position:absolute;top:110px;right:130px;text-align:right}}
.body{{flex:1;display:flex;flex-direction:column;justify-content:center}}
h1{{font-size:88px;line-height:1.08;font-weight:700;letter-spacing:-.02em;max-width:1400px}}
.sub{{font-size:34px;line-height:1.5;color:{DIM};margin-top:34px;max-width:1250px}}
.hero{{font-size:210px;font-weight:700;letter-spacing:-.045em;line-height:.92}}
.hero.cold{{color:{COLD}}}
.kicker{{font-family:"Liberation Mono",monospace;font-size:20px;letter-spacing:.22em;
  color:{DIM};margin-bottom:26px}}
.rule{{height:1px;background:rgba(242,245,247,.13);margin:42px 0}}
/* варианты ответа */
.opts{{margin-top:60px;display:flex;flex-direction:column;gap:30px}}
.opt{{display:flex;align-items:baseline;gap:34px;font-size:42px}}
.opt b{{font-family:"Liberation Mono",monospace;font-size:34px;color:{COLD};
  min-width:52px}}
.hint{{margin-top:64px;font-size:24px;color:{DIM};letter-spacing:.02em}}
/* таблица */
table{{border-collapse:collapse;width:100%;font-size:30px}}
th{{text-align:left;font-family:"Liberation Mono",monospace;font-size:18px;
  letter-spacing:.16em;color:{DIM};font-weight:400;padding:0 0 22px}}
td{{padding:26px 0;border-top:1px solid rgba(242,245,247,.1)}}
td.n{{text-align:right;font-variant-numeric:tabular-nums}}
tr.key td{{color:{FG}}}
tr.key td.big{{color:{COLD};font-weight:700;font-size:38px}}
/* две колонки */
.cols{{display:flex;gap:130px;margin-top:20px}}
.col{{flex:1}}
.col h2{{font-family:"Liberation Mono",monospace;font-size:22px;letter-spacing:.2em;
  color:{DIM};font-weight:400;padding-bottom:30px;
  border-bottom:1px solid rgba(242,245,247,.13)}}
.col.win h2{{color:{COLD}}}
.row{{display:flex;justify-content:space-between;align-items:baseline;
  padding:23px 0;font-size:34px}}
.row span.v{{font-variant-numeric:tabular-nums;color:{DIM}}}
.col.win .row span.v{{color:{COLD}}}
.row.low span.v{{color:{DIM}}}
.note{{margin-top:52px;font-size:30px;line-height:1.5;max-width:1500px}}
.note em{{font-style:normal;color:{COLD}}}
"""

SLIDES = {
    "01-standby": f"""
<div class="slide">
  <div class="hud">MISSION CONTROL<br>РИНОК АПТЕК УКРАЇНИ · 2026<br>STATUS: <span class="on">STANDBY</span></div>
  <div class="body"></div>
</div>""",

    "07-signal-01": f"""
<div class="slide">
  <div class="hud">INCOMING SIGNAL 01</div>
  <div class="corner hud">T+00:04:12</div>
  <div class="body">
    <h1>Де у нас найбільший<br>невикористаний потенціал?</h1>
    <div class="opts">
      <div class="opt"><b>1</b><span>У преміум-аптеках. Там великі обороти</span></div>
      <div class="opt"><b>2</b><span>У G-категорії. Там, де майже нічого немає</span></div>
      <div class="opt"><b>3</b><span>Різниці немає</span></div>
    </div>
    <div class="hint">Покажіть пальцями. 1, 2 або 3.</div>
  </div>
</div>""",

    "08-213-mln": f"""
<div class="slide">
  <div class="hud">SIGNAL 01 · DECODED</div>
  <div class="corner hud">MEDIAN-BASED</div>
  <div class="body">
    <div class="kicker">СУКУПНИЙ ПОТЕНЦІАЛ G-КАТЕГОРІЇ</div>
    <div class="hero cold">213 000 000 ₴</div>
    <div class="rule"></div>
    <table>
      <tr><th>Категорія</th><th class="n">Приріст на точку</th>
          <th class="n">Ще не відвідано</th><th class="n">Потенціал</th></tr>
      <tr><td>A — преміум</td><td class="n">27 507 ₴</td><td class="n">572</td><td class="n">15,7 млн</td></tr>
      <tr class="key"><td>G — нижчий пріоритет</td><td class="n">24 282 ₴</td>
          <td class="n big">8 781</td><td class="n big">213 млн</td></tr>
    </table>
    <div class="note">Приріст на одну точку — практично однаковий.
      <em>Різниця тільки в тому, скільки точок ми ще не бачили.</em></div>
  </div>
</div>""",

    "11-visit-vs-shelf": f"""
<div class="slide">
  <div class="hud">SIGNAL 02 · DECODED</div>
  <div class="corner hud">TIER-CONTROLLED</div>
  <div class="body">
    <div class="cols">
      <div class="col">
        <h2>ПОЛИЦЯ</h2>
        <div class="row"><span>Зест</span><span class="v">2,69×</span></div>
        <div class="row"><span>Упсарин</span><span class="v">2,44×</span></div>
        <div class="row"><span>Мультигрип</span><span class="v">2,00×</span></div>
        <div class="row"><span>Дефлю</span><span class="v">1,10×</span></div>
        <div class="row low"><span>Бестиа</span><span class="v">0,60×</span></div>
      </div>
      <div class="col win">
        <h2>ВІЗИТ</h2>
        <div class="row"><span>Энзибар</span><span class="v">3,06×</span></div>
        <div class="row"><span>Зест</span><span class="v">2,94×</span></div>
        <div class="row"><span>Бестиа</span><span class="v">2,21×</span></div>
        <div class="row"><span>Дефлю</span><span class="v">1,92×</span></div>
        <div class="row"><span>Фервекс</span><span class="v">1,28×</span></div>
      </div>
    </div>
    <div class="note">Візит — плюс на кожному бренді, найгірший результат <em>×1,28</em>.
      Полиця вибіркова: один бренд узагалі в мінусі.</div>
  </div>
</div>""",
}


def main():
    for name, html in SLIDES.items():
        f = OUT / f"{name}.html"
        f.write_text(
            f"<!doctype html><meta charset='utf-8'><style>{CSS}</style>{html}",
            encoding="utf-8",
        )
        subprocess.run(
            [CHROME, "--headless", "--no-sandbox", "--disable-gpu",
             "--hide-scrollbars", "--force-device-scale-factor=1",
             "--window-size=1920,1080",
             f"--screenshot={OUT / (name + '.png')}", f"file://{f}"],
            check=True, capture_output=True,
        )
        print("rendered", name)


if __name__ == "__main__":
    main()
