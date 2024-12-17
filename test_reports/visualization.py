import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

# Ścieżka do raportu XML
xml_path = "test_reports/test_results.xml"

# Funkcja do parsowania raportu XML
def parse_test_results(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    passed = 0
    failed = 0
    errors = 0
    skipped = 0

    # Analiza wyników testów
    for testcase in root.findall(".//testcase"):
        if testcase.find("failure") is not None:
            failed += 1
        elif testcase.find("error") is not None:
            errors += 1
        elif testcase.find("skipped") is not None:
            skipped += 1
        else:
            passed += 1
    
    return {"passed": passed, "failed": failed, "errors": errors, "skipped": skipped}

# Funkcja do rysowania wykresu
def plot_results(results):
    labels = [f"{label} ({size})" if size > 0 else "" for label, size in results.items()]
    sizes = results.values()
    colors = ['#4CAF50', '#FF5252', '#FFC107', '#2196F3']
    
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct=lambda p: f'{p:.1f}%' if p > 0 else '', colors=colors, startangle=140)
    plt.title("Test Results")
    plt.axis('equal')  # Równe proporcje
    plt.show()


# Parsowanie i rysowanie wykresu
results = parse_test_results(xml_path)
plot_results(results)
