# QUICK START GUIDE: NETWEHUB PROTOTYPE 🚀

## За 15 минут к первому работающему прототипу

Это **краткая версия** для быстрого старта. Полная документация в `Protokol-NETWEHUB.md`.

---

## 1️⃣ ТРЕБОВАНИЯ (5 минут)

Установи на компьютер:

```bash
# macOS
brew install python3 postgresql node

# Ubuntu/Debian
sudo apt install python3 postgresql nodejs npm

# Windows
# Скачай с:
# - Python: https://www.python.org/downloads/
# - PostgreSQL: https://www.postgresql.org/download/
# - Node.js: https://nodejs.org/
```

Проверь версии:
```bash
python3 --version  # 3.9+
psql --version     # 12+
node --version     # 16+
npm --version      # 8+
```

---

## 2️⃣ BACKEND: БЫСТРАЯ ВЕРСИЯ (10 минут)

### Создай структуру

```bash
mkdir netwehub && cd netwehub
mkdir backend frontend
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Установи зависимости
pip install flask flask-cors psycopg2-binary pandas networkx
```

### Создай файл `app.py`

```python
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Временное хранилище (без БД для быстрого старта)
users_db = {}
metrics_db = {}

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify({
        'user_id': user_id,
        'name': f'User {user_id}',
        'level': 2,
        'hsk_level': 3,
        'email': f'user{user_id}@netwehub.com'
    })

@app.route('/api/user/<int:user_id>/metrics', methods=['GET'])
def get_metrics(user_id):
    metrics = [
        {'week': i, 'self_awareness': 50 + i*2, 'empathy': 50 + i*1.5, 
         'communication': 50 + i*2.5, 'motivation': 50 + i*2}
        for i in range(12)
    ]
    return jsonify({'metrics': metrics})

@app.route('/api/network/<int:user_id>', methods=['GET'])
def get_network(user_id):
    nodes = [
        {'id': 1, 'label': 'You', 'size': 30, 'color': '#38bdf8'},
        {'id': 2, 'label': 'Masha', 'size': 20, 'color': '#22c55e'},
        {'id': 3, 'label': 'Ivan', 'size': 20, 'color': '#22c55e'},
        {'id': 4, 'label': 'Oleg', 'size': 15, 'color': '#f97316'},
    ]
    edges = [
        {'from': 1, 'to': 2, 'weight': 3},
        {'from': 1, 'to': 3, 'weight': 2},
        {'from': 1, 'to': 4, 'weight': 1},
        {'from': 2, 'to': 3, 'weight': 2},
    ]
    return jsonify({'nodes': nodes, 'edges': edges})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'total_users': 147,
        'in_program': 18,
        'active_projects': 5,
        'network_density': 0.34
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Запусти backend

```bash
python app.py
# Будет на http://localhost:5000
```

---

## 3️⃣ FRONTEND: HTML ПРОТОТИП (уже готов!)

Просто открой файл `prototype-app.html` в браузере. Он работает локально, без подключения к backend'у (или с mock-данными).

Или создай простой React app:

```bash
cd ../frontend
npx create-react-app .
npm install d3 chart.js react-chartjs-2
npm start
# Будет на http://localhost:3000
```

---

## 4️⃣ DATABASE: PostgreSQL СХЕМА (опционально)

Если хочешь работать с реальной БД:

```bash
# Подключись к PostgreSQL
psql -U postgres

# Создай БД
CREATE DATABASE netwehub;
\c netwehub

# Создай таблицы
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    hsk_level INT DEFAULT 1,
    level INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE ei_metrics (
    metric_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    timestamp TIMESTAMP DEFAULT NOW(),
    self_awareness FLOAT DEFAULT 50,
    empathy FLOAT DEFAULT 50,
    communication FLOAT DEFAULT 50,
    motivation FLOAT DEFAULT 50
);

CREATE TABLE connections (
    connection_id SERIAL PRIMARY KEY,
    user_1 INT REFERENCES users(user_id),
    user_2 INT REFERENCES users(user_id),
    strength INT DEFAULT 1
);

-- Вставь тестовые данные
INSERT INTO users (name, hsk_level, level) VALUES 
('Alice', 3, 2),
('Bob', 2, 2),
('Charlie', 1, 1),
('Diana', 4, 3);

INSERT INTO connections (user_1, user_2, strength) VALUES 
(1, 2, 3),
(1, 3, 2),
(2, 3, 2);

-- Проверь
SELECT * FROM users;
SELECT * FROM connections;
```

---

## 5️⃣ АНАЛИЗ ГРАФОВ: NetworkX (Python)

```python
# Создай файл `graph_analysis.py`

import networkx as nx
import pandas as pd

# Создай граф сети
G = nx.Graph()

# Добавь узлы (люди)
users = [(1, 'Alice'), (2, 'Bob'), (3, 'Charlie'), (4, 'Diana')]
for user_id, name in users:
    G.add_node(user_id, name=name)

# Добавь связи
connections = [(1, 2, 3), (1, 3, 2), (2, 3, 2), (2, 4, 1)]
for u1, u2, strength in connections:
    G.add_edge(u1, u2, weight=strength)

# Анализируй сеть
print("=== СЕТЕВОЙ АНАЛИЗ ===")
print(f"Узлов: {G.number_of_nodes()}")
print(f"Связей: {G.number_of_edges()}")
print(f"Плотность: {nx.density(G):.2f}")
print(f"Средний коэффициент кластеризации: {nx.average_clustering(G):.2f}")

# Найди самых важных людей
centrality = nx.degree_centrality(G)
print("\nЦентральность (кто самый связанный):")
for node, cent in sorted(centrality.items(), key=lambda x: x[1], reverse=True):
    user_name = [name for uid, name in users if uid == node][0]
    print(f"  {user_name}: {cent:.2f}")

# Найди сообщества
from networkx.algorithms import community
communities = list(community.greedy_modularity_communities(G))
print(f"\nСообщества: {len(communities)}")
for i, comm in enumerate(communities):
    print(f"  Группа {i+1}: {comm}")

# Экспортируй в JSON (для визуализации)
import json

nodes = []
for node in G.nodes():
    user_name = [name for uid, name in users if uid == node][0]
    nodes.append({
        'id': node,
        'label': user_name,
        'size': 20 + centrality[node] * 50
    })

edges = []
for u1, u2, data in G.edges(data=True):
    edges.append({
        'from': u1,
        'to': u2,
        'weight': data.get('weight', 1)
    })

output = {'nodes': nodes, 'edges': edges}
with open('network.json', 'w') as f:
    json.dump(output, f)

print("\n✅ Экспортировано в network.json")
```

Запусти:
```bash
python graph_analysis.py
```

---

## 6️⃣ МАКРОЭКОНОМИЧЕСКАЯ МОДЕЛЬ

```python
# `economic_model.py`

class EconomicImpact:
    def __init__(self, num_participants=100):
        self.num_participants = num_participants
    
    def productivity_boost(self, ei_improvement):
        """EI -> производительность"""
        # На каждые 20 пунктов EI — 10% рост производительности
        return 1 + (ei_improvement / 20) * 0.1
    
    def startup_probability(self, ei_score, connections):
        """Вероятность создания стартапа"""
        base = 0.1
        ei_factor = (ei_score - 50) / 100 * 0.2
        network_factor = (connections / 20) * 0.2
        return min(base + ei_factor + network_factor, 0.4)
    
    def calculate_gdp_impact(self, avg_ei_change, avg_connections, success_rate):
        """Влияние на ВНП"""
        base_salary = 600000  # рублей в год на человека
        
        # Производительность
        productivity_mult = self.productivity_boost(avg_ei_change)
        productivity_impact = self.num_participants * base_salary * (productivity_mult - 1)
        
        # Стартапы
        startup_prob = self.startup_probability(50 + avg_ei_change, avg_connections)
        expected_startups = int(self.num_participants * startup_prob * success_rate)
        startup_impact = expected_startups * 2000000  # средний доход стартапа
        
        total_impact = productivity_impact + startup_impact
        roi = (total_impact / (self.num_participants * 100000)) * 100  # ROI%
        
        return {
            'productivity_impact': int(productivity_impact),
            'expected_startups': expected_startups,
            'startup_impact': int(startup_impact),
            'total_gdp_impact': int(total_impact),
            'roi_percent': roi,
            'jobs_created': expected_startups * 5
        }

# Используй
model = EconomicImpact(100)
impact = model.calculate_gdp_impact(
    avg_ei_change=25,      # +25 пунктов
    avg_connections=9,     # +9 новых связей
    success_rate=0.8       # 80% успеха проектов
)

print("=== ЭКОНОМИЧЕСКОЕ ВОЗДЕЙСТВИЕ ===")
print(f"Прирост ВНП: {impact['total_gdp_impact']:,} руб")
print(f"Ожидаемые стартапы: {impact['expected_startups']}")
print(f"Созданные рабочие места: {impact['jobs_created']}")
print(f"ROI: {impact['roi_percent']:.1f}%")
```

Запусти:
```bash
python economic_model.py
```

---

## 7️⃣ ВИЗУАЛИЗАЦИЯ В БРАУЗЕРЕ

Создай `index.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>NETWEHUB</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        body { 
            background: #0f172a; 
            color: #f1f5f9;
            font-family: Arial;
            margin: 20px;
        }
        .card { 
            background: #1e293b; 
            padding: 20px; 
            margin: 20px 0;
            border-radius: 8px;
        }
        canvas { max-width: 100%; }
    </style>
</head>
<body>
    <h1>NETWEHUB Analytics</h1>
    
    <div class="card">
        <h2>EI Development</h2>
        <canvas id="myChart"></canvas>
    </div>

    <script>
        // Fetch данные с backend
        fetch('http://localhost:5000/api/user/1/metrics')
            .then(r => r.json())
            .then(data => {
                const weeks = Array.from({length: 12}, (_, i) => `W${i+1}`);
                const metrics = data.metrics;
                
                new Chart(document.getElementById('myChart'), {
                    type: 'line',
                    data: {
                        labels: weeks,
                        datasets: [
                            {
                                label: 'Self-Awareness',
                                data: metrics.map(m => m.self_awareness),
                                borderColor: '#38bdf8'
                            },
                            {
                                label: 'Communication',
                                data: metrics.map(m => m.communication),
                                borderColor: '#22c55e'
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { labels: { color: '#cbd5e1' } }
                        },
                        scales: {
                            y: { ticks: { color: '#cbd5e1' } },
                            x: { ticks: { color: '#cbd5e1' } }
                        }
                    }
                });
            });
    </script>
</body>
</html>
```

Открой в браузере: `http://localhost:3000`

---

## ✅ ФИНАЛЬНЫЙ ЧЕКЛИСТ

- [x] Backend Flask app запущен
- [x] Frontend HTML открывается
- [x] Network analysis работает
- [x] Economic model считает
- [x] Графики рисуются
- [x] Данные текут между слоями

**Поздравляю! 🎉 Твой первый прототип готов за 30 минут!**

---

## 📚 СЛЕДУЮЩИЕ ШАГИ

1. **Подключи реальную БД** (PostgreSQL)
2. **Добавь аутентификацию** (JWT tokens)
3. **Развернись на сервер** (Docker + AWS)
4. **Кастомизируй UI** (Figma дизайн)
5. **Наполни реальными данными** (10+ реальных пользователей)

**За помощью:** смотри `Protokol-NETWEHUB.md`

---

*Made with ❤️ for first-year students building the future*
