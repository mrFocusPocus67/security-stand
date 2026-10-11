import json
from collections import Counter
from pathlib import Path

R = Path("reports")


def load(name):
    try:
        return json.loads((R / name).read_text())
    except Exception:
        return None


bandit = load("bandit.json")
osv = load("osv.json")
leaks = load("gitleaks.json")

print("Результаты сканирования\n")

#Bandit
print("### Bandit (SAST)\n")
if bandit:
    items = bandit.get("results", [])
    count = Counter(i["issue_severity"] for i in items)
    print(f"Всего находок: {len(items)} "
          f"(HIGH: {count['HIGH']}, MEDIUM: {count['MEDIUM']}, LOW: {count['LOW']})\n")
    print("Правило Серьёзность Файл:строка Описание ")
    for i in items:
        print(f" {i['test_id']} {i['issue_severity']} "
              f"{i['filename']}:{i['line_number']} {i['issue_text']}")
else:
    print("Отчёта нет.")

#OSV-Scanner
print("\nOSV-Scanner (SCA)\n")
if osv:
    print(" Библиотека Версия Кол-во уязвимостей Примеры ID |")
    for res in osv.get("results", []):
        for pkg in res.get("packages", []):
            info = pkg["package"]
            vulns = pkg.get("vulnerabilities", [])
            ids = ", ".join(v["id"] for v in vulns[:3])
            print(f"| {info['name']} | {info['version']} | {len(vulns)} | {ids} |")
else:
    print("Отчёта нет.")

#Gitleaks
print("\nGitleaks (secret scanning)\n")
if leaks is not None:
    print(f"Найдено секретов: {len(leaks)}\n")
    print(" Правило Файл  Строка ")
    for l in leaks:
        print(f" {l['RuleID']} {l['File']} {l['StartLine']} ")
else:
    print("Отчёта нет.")

print("\nВерсии инструментов в этом запуске\n")
v = R / "versions.txt"
print(v.read_text() if v.exists() else "нет данных")
