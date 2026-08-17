#!/usr/bin/env python3
"""
Аудит аналитики Хлои + поиск дополнительных сигналов.
Воспроизводит все цифры, попавшие в slides.md, и все находки из analysis-findings.md.

Запуск:  python3 verify.py /path/to/Mission_Control.xlsx
Зависимости: pandas, openpyxl
"""
import sys
import pandas as pd
import numpy as np

pd.set_option("display.width", 230)
XLSX = sys.argv[1] if len(sys.argv) > 1 else "Mission_Control.xlsx"

ta = pd.read_excel(XLSX, sheet_name="ТА_повна_база")
sb = pd.read_excel(XLSX, sheet_name="Продажі_точка_бренд")
rb = pd.read_excel(XLSX, sheet_name="Рейтинг_брендів")
am = pd.read_excel(XLSX, sheet_name="Активності_мережа")

ta["vis"] = ta.Візит.eq("VISIT")
ta["fa"] = ta.Візит_ФА.eq("VISIT")
ta["gf"] = ta.Візит_ГФ.eq("VISIT")


def head(t):
    print("\n" + "=" * 72 + f"\n{t}\n" + "=" * 72)


def tier_weighted_ratio(df, flag, value, tier="Tier", min_n=30):
    """Средний по тирам ratio (взвешенный числом наблюдений в тире)."""
    num = den = 0.0
    for _, s in df.groupby(tier):
        a = s.loc[s[flag], value]
        b = s.loc[~s[flag], value]
        if len(a) < min_n or len(b) < min_n or b.mean() <= 0:
            continue
        num += len(s) * (a.mean() / b.mean())
        den += len(s)
    return num / den if den else np.nan


# --------------------------------------------------------------------------
head("S01 — 213 млн грн. Хлоя считала по МЕДИАНАМ, воспроизводится точно")
rows = []
for t in ["A", "B", "C", "G", "X"]:
    s = ta[ta.Tier_Group == t]
    inc = s[s.vis].DM_оборот.median() - s[~s.vis].DM_оборот.median()
    n_un = int((~s.vis).sum())
    rows.append([t, round(inc), n_un, round(inc * n_un / 1e6, 1)])
print(pd.DataFrame(rows, columns=["Tier", "приріст_медіана", "невідвідано", "потенціал_млн"]))
print("\nОжидается: A 27 507 / 572 / 15,7   G 24 282 / 8 781 / 213,2")
print("\nX — выбросы: mean NO VISIT 233k против median 13k. Исключён из истории.")

cov = ta.groupby("Tier_Group").agg(n=("vis", "size"), visited=("vis", "sum"))
cov["pct_visited"] = (cov.visited / cov.n * 100).round(1)
print("\nПокрытие:")
print(cov)

# --------------------------------------------------------------------------
head("НОВОЕ: соблюдение плана — 41% запланированных точек не посещено ни разу")
pl = ta[ta.План_частота_міс.notna()]
print(f"точек с планом: {len(pl)}   из них NO VISIT: {(~pl.vis).sum()} ({(~pl.vis).mean()*100:.1f}%)")
print(
    pl.groupby("План_частота_міс")
    .agg(n=("vis", "size"), novisit=("vis", lambda s: (~s).sum()))
    .assign(pct=lambda d: (d.novisit / d.n * 100).round(1))
)
print(f"\nбез плана вообще: {ta.План_частота_міс.isna().sum()}"
      f"   из них посещено: {ta[ta.План_частота_міс.isna()].vis.sum()}")
print("\nДоля точек тира, попавших в план — главный аргумент слайда 10:")
print(
    ta.assign(has_plan=ta.План_частота_міс.notna())
    .groupby("Tier_Group")
    .agg(n=("vis", "size"), planned=("has_plan", "sum"))
    .assign(pct_planned=lambda d: (d.planned / d.n * 100).round(1))
)

# --------------------------------------------------------------------------
head("НОВОЕ: две полевые команды — ФА и ГФ равны, вместе дают больше")
ta["team"] = np.select(
    [ta.fa & ta.gf, ta.fa & ~ta.gf, ~ta.fa & ta.gf],
    ["both", "FA only", "GPh only"],
    "neither",
)
print("медиана DM_оборот, tier-controlled:")
print(ta.pivot_table(index="Tier_Group", columns="team", values="DM_оборот", aggfunc="median").round(0))
print("\nn по ячейкам (ГФ в тире A = 18, ненадёжно):")
print(ta.pivot_table(index="Tier_Group", columns="team", values="DM_оборот", aggfunc="size"))
print("\n⚠️ 'both' = точка получила визиты от двух команд, то есть больше визитов вообще.")
print("   Эффект координации от эффекта дозы этими данными не отделяется.")
print("   Свободно от этого confound только сравнение FA only против GPh only.")

# --------------------------------------------------------------------------
head("S04/S05 — ratio брендов: проверка Рейтинг_брендів пересчётом из сырых данных")
out = []
for br, s in sb.groupby("Бренд"):
    out.append([br,
                round(tier_weighted_ratio(s, "Є_полиця", "Середньомісячні_продажі"), 2),
                round(tier_weighted_ratio(s, "Є_візит", "Середньомісячні_продажі"), 2)])
mine = pd.DataFrame(out, columns=["Бренд", "полиця_перерахунок", "візит_перерахунок"])
print(rb.merge(mine, on="Бренд", how="outer").sort_values("полиця_перерахунок").to_string(index=False))
print("\nПорядок совпадает, магнитуды расходятся (иная схема взвешивания).")
print("Устойчиво: Бестиа — единственный бренд ниже 1,0 при обоих методах.")
print("Ибупром и Дип Рилиф сидят на границе 1,0 и меняют знак от метода — на слайд не выносить.")
print(f"\nВизит: минимум по Рейтингу = {rb.Ratio_візит.min()} "
      f"({rb.loc[rb.Ratio_візит.idxmin(),'Бренд']}), брендов с рейтингом: {len(rb)} из {sb.Бренд.nunique()}")

# --------------------------------------------------------------------------
head("HIDDEN PATTERN — Бестиа. Тест на обратную причинность")
bes = sb[sb.Бренд == "Бестиа"]
print(f"Бестиа: tier-weighted полиця = {tier_weighted_ratio(bes,'Є_полиця','Середньомісячні_продажі'):.2f}"
      f"   візит = {tier_weighted_ratio(bes,'Є_візит','Середньомісячні_продажі'):.2f}")
print("\nЧетыре ячейки, Бестиа (средние месячные продажи):")
print(bes.pivot_table(index="Є_полиця", columns="Є_візит", values="Середньомісячні_продажі", aggfunc="mean").round(1))
print("\nТе же четыре ячейки для всех ОСТАЛЬНЫХ брендов:")
print(sb[sb.Бренд != "Бестиа"].pivot_table(
    index="Є_полиця", columns="Є_візит", values="Середньомісячні_продажі", aggfunc="mean").round(1))

print("\n--- ТЕСТ: продаются ли ОСТАЛЬНЫЕ бренды хуже в точках с полкой Бестиа? ---")
print("Если да — полки ставили в слабые точки, и −33% это артефакт отбора.")
oth = sb[sb.Бренд != "Бестиа"].groupby("Код_ТА").Середньомісячні_продажі.sum().rename("other_sales")
m = bes.set_index("Код_ТА")[["Є_полиця", "Tier"]].join(oth)
res = []
for t in ["A", "B", "C", "G"]:
    s = m[m.Tier == t]
    a, b = s[s.Є_полиця].other_sales, s[~s.Є_полиця].other_sales
    res.append([t, len(s), round(a.mean()), round(b.mean()), round(a.mean() / b.mean(), 2)])
print(pd.DataFrame(res, columns=["Tier", "n", "полиця_Бестиа", "без_полиці", "ratio_інших_брендів"]))
print("\nВывод: ratio других брендов ≈ 1,0 во всех тирах → точки нормальные.")
print("Проседает только Бестиа. Версия 'полки купили в слабых точках' отпадает.")

# --------------------------------------------------------------------------
head("S06 — активности. Эффект сжимается по мере ужесточения контроля")
a, b = am[am.Є_активність].Продажі_грн.mean(), am[~am.Є_активність].Продажі_грн.mean()
print(f"1) наивно, между сетями:  ×{a/b:.2f}")

nz = am.groupby("Мережа").Продажі_грн.sum().rename("net_sales")
am3 = am.join(nz, on="Мережа")
am3["q"] = pd.qcut(am3.net_sales, 4, labels=["Q1 малі", "Q2", "Q3", "Q4 найбільші"])
print("\nпокрытие активностями по квартилю размера сети:")
print(am3.groupby("q", observed=True).Є_активність.mean().mul(100).round(1))
print("2) контроль размера сети:  ×3,6–4,6 (расчёт Хлои)")

g = am.groupby(["Мережа", "Бренд"]).Є_активність.agg(n_states="nunique")
sw = g[g.n_states > 1].reset_index()[["Мережа", "Бренд"]]
r = (am.merge(sw, on=["Мережа", "Бренд"])
       .pivot_table(index=["Мережа", "Бренд"], columns="Є_активність", values="Продажі_грн", aggfunc="mean"))
r.columns = ["no_act", "act"]
r = r.dropna()
r = r[r.no_act > 0]
r["ratio"] = r.act / r.no_act
print(f"\n3) та же сеть + тот же бренд, месяц против месяца: ×{r.ratio.median():.2f} "
      f"(median, n={len(r)} пар, положительных {(r.ratio>1).mean()*100:.0f}%)")
print("   Хлоя тем же путём через темп роста: −5,9% против +2,8%, разница ~8,7 п.п., n≈50.")
print("   Два независимых расчёта сходятся: эффект реален, но втрое-вчетверо меньше заявленного.")

# --------------------------------------------------------------------------
head("НОВОЕ: 307 крупных аптек A/B, где Delta Medical продаёт около нуля")
t = ta[(ta.Загальний_оборот_тис > 0) & ta.DM_оборот.notna()].copy()
t["share"] = t.DM_оборот / t.Загальний_оборот_тис
cand = t[(t.Загальний_оборот_тис >= t.Загальний_оборот_тис.quantile(.75))
         & (t.share <= t.share.quantile(.25))]
print(f"n = {len(cand)}   посещено: {cand.vis.sum()} ({cand.vis.mean()*100:.1f}%)   с полкой: {cand.Є_полиця.sum()}")
print(cand.groupby("Tier_Group").size().to_string())
print(f"медианный оборот аптеки: {cand.Загальний_оборот_тис.median():,.0f}"
      f"   медианный DM_оборот: {cand.DM_оборот.median():,.0f}")
print("\nЭто целевой список, а не статистическая находка: отбор по определению.")
print("Ценность в том, что это крупные аптеки премиум-тиров, и 62% из них даже не посещаются.")

# --------------------------------------------------------------------------
head("ОТБРАКОВАНО: кривая насыщения полки — немонотонна, в деку не идёт")
s = ta[ta.Кількість_брендів_на_полиці.notna()].copy()
s["bin"] = pd.cut(s.Кількість_брендів_на_полиці, [-.1, 0, 2, 5, 9, 13, 17, 21, 27],
                  labels=["0", "1-2", "3-5", "6-9", "10-13", "14-17", "18-21", "22+"])
print(s[~s.vis].pivot_table(index="bin", columns="Tier_Group", values="DM_оборот",
                            aggfunc="median", observed=True).round(0))
print("\n0 брендов выше, чем 1-2; рост до 10-17; обвал на 22+ при малом n.")
print("Механизм неясен, кривая шумная — как сигнал не годится.")

# --------------------------------------------------------------------------
head("ВОПРОС К ХЛОЕ: две таблицы продаж не сходятся")
tot = sb.groupby("Код_ТА").Продажі_за_4міс.sum().rename("sb_4m")
j = ta.set_index("Код_ТА")[["DM_оборот"]].join(tot, how="inner").dropna()
print(f"точек в обеих таблицах: {len(j)} из {len(ta)}")
print(f"корреляция DM_оборот и суммы по 20 брендам: {j.DM_оборот.corr(j.sb_4m):.3f}")
print(f"медианное отношение: {(j.DM_оборот/j.sb_4m.replace(0,np.nan)).median():.2f}")
print("Корреляция 0,20 для двух измерений одного и того же — слишком низкая.")
