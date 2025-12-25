# NETWEHUB: ПОЛНАЯ ТЕХНИЧЕСКАЯ ИНСТРУКЦИЯ
## Как создать первый прототип системы моделирования человеческого капитала

---

## ЧАСТЬ 1: НАУЧНОЕ ОБОСНОВАНИЕ (для курсовой)

### Актуальность проблемы

В современной экономике **человеческий капитал** (Human Capital) становится основным конкурентным преимуществом. Но как его измерить? Как отследить его развитие?

**Традиционные методы:**
- ❌ Тесты и сертификаты (статичны, не отражают прогресс)
- ❌ Оценки экспертов (субъективны)
- ❌ Опросы (редкие, затратные)

**Новый подход (NETWEHUB):**
- ✅ Система непрерывного отслеживания
- ✅ Объективные метрики (логируются в базу данных)
- ✅ Сетевой анализ (связи между людьми = социальный капитал)
- ✅ Моделирование динамики развития

### Теоретическая база

**Три компонента человеческого капитала в NETWEHUB:**

1. **Когнитивный капитал** (знания, навыки)
   - Уровень китайского (HSK 1-6)
   - Знания о бизнесе (кейсы, проекты)
   - Технические навыки (программирование, аналитика)

2. **Некогнитивный капитал** (эмоциональный интеллект)
   - Самопознание (self-awareness)
   - Управление эмоциями (self-regulation)
   - Социальные навыки (empathy, communication)
   - Мотивация (goal-setting, resilience)

3. **Социальный капитал** (сетевые связи)
   - Количество и качество связей в сообществе
   - Бридж-позиции (люди, соединяющие разные группы)
   - Плотность сети (как много люди друг друга знают)

### Связь с макроэкономикой

**Закономерность:** Инвестиции в человеческий капитал → рост производительности → увеличение ВНП на душу населения

**На микроуровне:**
- Участник NETWEHUB развивает компетенции → может создать стартап или получить лучшую работу
- Сеть создает возможности → совместные проекты → создание новой стоимости

**На макроуровне:**
- Если 100 студентов разовьют эмоциональный интеллект → они станут лучшими лидерами → их компании будут эффективнее

**Экономический показатель:** Средний ROI (Return on Investment) в развитие человеческого капитала = +300-400% (по исследованиям Всемирного банка)

### Исследовательская гипотеза для курсовой

**H0 (нулевая):** Эмоциональный интеллект не влияет на эффективность работы в проектных командах.

**H1 (альтернативная):** Участники с высоким EI показывают лучшие результаты в проектах, больше часов тратят на обучение, создают больше связей в сети.

**Как измерять:**
- Временные ряды метрик EI (еженедельно)
- Граф сетевых связей (ежемесячно)
- Результаты проектов (оценка наставников)
- Корреляционный анализ

---

## ЧАСТЬ 2: АРХИТЕКТУРА ПРИЛОЖЕНИЯ

### Стек технологий (MVP)

```
FRONTEND:
├─ React.js (UI компоненты)
├─ D3.js или Vis.js (graph visualization)
├─ Chart.js (статистика, графики)
└─ Tailwind CSS (стили)

BACKEND:
├─ Python (Flask или FastAPI)
├─ PostgreSQL (основная база данных)
├─ NetworkX (анализ графов)
├─ Pandas + NumPy (обработка данных)
└─ Scikit-learn (ML модели для анализа)

INFRASTRUCTURE:
├─ Docker (контейнеризация)
├─ GitHub (версионирование)
└─ AWS/Heroku (хостинг)
```

### Структура базы данных

```sql
-- Таблица пользователей
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name VARCHAR(255),
    telegram_handle VARCHAR(255),
    level INT (1, 2, 3),
    hsk_level INT (1-6),
    join_date TIMESTAMP,
    current_project VARCHAR(255)
);

-- Таблица метрик эмоционального интеллекта
CREATE TABLE ei_metrics (
    metric_id INT PRIMARY KEY,
    user_id INT,
    timestamp TIMESTAMP,
    self_awareness FLOAT (0-100),
    self_regulation FLOAT (0-100),
    empathy FLOAT (0-100),
    communication FLOAT (0-100),
    motivation FLOAT (0-100),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Таблица проектов
CREATE TABLE projects (
    project_id INT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    team_lead INT,
    status VARCHAR(50),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    FOREIGN KEY (team_lead) REFERENCES users(user_id)
);

-- Таблица членства в проектах
CREATE TABLE project_members (
    id INT PRIMARY KEY,
    project_id INT,
    user_id INT,
    hours_invested INT,
    role VARCHAR(100),
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Таблица связей между пользователями
CREATE TABLE connections (
    connection_id INT PRIMARY KEY,
    user_1 INT,
    user_2 INT,
    connection_type VARCHAR(50), -- 'project', 'study_buddy', 'mentor'
    created_date TIMESTAMP,
    strength INT (1-5), -- насколько сильная связь
    FOREIGN KEY (user_1) REFERENCES users(user_id),
    FOREIGN KEY (user_2) REFERENCES users(user_id)
);

-- Таблица логов активности
CREATE TABLE activity_log (
    log_id INT PRIMARY KEY,
    user_id INT,
    event_type VARCHAR(100),
    event_data JSON,
    timestamp TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

---

## ЧАСТЬ 3: ПОШАГОВАЯ ИНСТРУКЦИЯ ДЛЯ ПРОТОТИПА

### ШАГ 1: Локальная среда разработки (неделя 1)

**Установка (MacOS/Linux):**

```bash
# 1. Установить Python 3.10+
python3 --version

# 2. Установить git
git clone https://github.com/yourusername/netwehub.git
cd netwehub

# 3. Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# 4. Установить зависимости
pip install flask flask-cors psycopg2-binary pandas numpy networkx matplotlib scikit-learn

# 5. Установить Node.js (для фронтенда)
# Скачать с https://nodejs.org/ (LTS версия)
node --version

# 6. Создать React приложение
npx create-react-app frontend
cd frontend
npm install d3 chart.js react-chartjs-2 vis-network
```

### ШАГ 2: Backend структура (неделя 2-3)

**Структура проекта:**

```
backend/
├── app.py                 # Основное приложение Flask
├── config.py              # Конфигурация БД
├── models.py              # Модели данных
├── routes.py              # API endpoints
├── analytics.py           # Анализ и статистика
├── graph_analysis.py      # Анализ графов сетей
└── requirements.txt       # Зависимости
```

**Файл: backend/app.py**

```python
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import pandas as pd
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Подключение к БД
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="netwehub",
        user="postgres",
        password="your_password",
        port=5432
    )
    return conn

# API: Получить данные пользователя
@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    
    if user:
        return jsonify({
            'user_id': user[0],
            'name': user[1],
            'level': user[3],
            'hsk_level': user[4]
        })
    return jsonify({'error': 'User not found'}), 404

# API: Получить метрики EI пользователя
@app.route('/api/user/<int:user_id>/metrics', methods=['GET'])
def get_user_metrics(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT timestamp, self_awareness, self_regulation, empathy, 
               communication, motivation 
        FROM ei_metrics 
        WHERE user_id = %s 
        ORDER BY timestamp DESC 
        LIMIT 12
    ''', (user_id,))
    
    metrics = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify({
        'user_id': user_id,
        'metrics': [
            {
                'date': m[0].isoformat(),
                'self_awareness': m[1],
                'self_regulation': m[2],
                'empathy': m[3],
                'communication': m[4],
                'motivation': m[5]
            } for m in metrics
        ]
    })

# API: Загрузить новые метрики (логирование в течение программы)
@app.route('/api/user/<int:user_id>/metrics', methods=['POST'])
def create_metric(user_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        INSERT INTO ei_metrics 
        (user_id, timestamp, self_awareness, self_regulation, empathy, communication, motivation)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (
        user_id,
        datetime.now(),
        data['self_awareness'],
        data['self_regulation'],
        data['empathy'],
        data['communication'],
        data['motivation']
    ))
    
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({'status': 'success', 'user_id': user_id}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### ШАГ 3: Анализ графов (неделя 3)

**Файл: backend/graph_analysis.py**

```python
import networkx as nx
import pandas as pd
import psycopg2
from collections import defaultdict

class NetworkAnalyzer:
    def __init__(self, db_connection):
        self.conn = db_connection
        self.graph = nx.Graph()
        self.load_network()
    
    def load_network(self):
        """Загрузить сетевые связи из БД в граф"""
        cur = self.conn.cursor()
        cur.execute('SELECT user_1, user_2, strength FROM connections')
        
        for user_1, user_2, strength in cur.fetchall():
            self.graph.add_edge(user_1, user_2, weight=strength)
        
        cur.close()
    
    def get_network_stats(self):
        """Получить основные статистики сети"""
        return {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph),
            'avg_clustering_coefficient': nx.average_clustering(self.graph),
            'diameter': nx.diameter(self.graph) if nx.is_connected(self.graph) else None
        }
    
    def get_node_centrality(self):
        """Найти самых важных людей в сети (центральность по связям)"""
        centrality = nx.degree_centrality(self.graph)
        sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'top_connectors': sorted_nodes[:10],  # ТОП-10 самых связанных людей
            'all_centrality': dict(centrality)
        }
    
    def get_communities(self):
        """Найти подгруппы (сообщества) в сети"""
        from networkx.algorithms import community
        
        communities = list(community.greedy_modularity_communities(self.graph))
        
        return {
            'num_communities': len(communities),
            'communities': [
                {
                    'id': i,
                    'members': list(c),
                    'size': len(c)
                } for i, c in enumerate(communities)
            ]
        }
    
    def get_shortest_path(self, user_1, user_2):
        """Найти кратчайший путь между двумя пользователями"""
        try:
            path = nx.shortest_path(self.graph, user_1, user_2)
            return {
                'path': path,
                'distance': len(path) - 1,
                'description': f"Ты можешь познакомиться с {user_2} через {len(path)-2} человека(а)"
            }
        except nx.NetworkXNoPath:
            return {'error': 'No connection found'}
    
    def get_graph_json(self):
        """Преобразовать граф в JSON для визуализации"""
        nodes = []
        edges = []
        
        # Получить центральность (для размера узла)
        centrality = nx.degree_centrality(self.graph)
        
        for node in self.graph.nodes():
            nodes.append({
                'id': node,
                'label': f'User {node}',
                'size': 20 + centrality[node] * 50  # Размер пропорционален центральности
            })
        
        for edge in self.graph.edges(data=True):
            edges.append({
                'from': edge[0],
                'to': edge[1],
                'weight': edge[2].get('weight', 1)
            })
        
        return {
            'nodes': nodes,
            'edges': edges
        }
```

### ШАГ 4: Frontend визуализация (неделя 4)

**Файл: frontend/src/components/NetworkGraph.js**

```javascript
import React, { useEffect, useRef } from 'react';
import vis from 'vis-network/standalone';

function NetworkGraph({ userId }) {
  const containerRef = useRef(null);
  const networkRef = useRef(null);

  useEffect(() => {
    // Получить данные сети с backend
    fetch(`/api/network/${userId}`)
      .then(res => res.json())
      .then(data => {
        const options = {
          physics: {
            enabled: true,
            stabilization: {
              iterations: 200
            }
          },
          interaction: {
            navigationButtons: true,
            keyboard: true,
            zoomView: true,
            dragView: true
          },
          nodes: {
            shape: 'circle',
            color: {
              background: '#38bdf8',
              border: '#0f172a',
              highlight: {
                background: '#00ff00',
                border: '#0f172a'
              }
            },
            font: {
              color: '#f1f5f9'
            }
          },
          edges: {
            color: {
              color: '#475569',
              highlight: '#38bdf8'
            },
            width: 1.5,
            smooth: {
              type: 'continuous'
            }
          }
        };

        const network = new vis.Network(
          containerRef.current,
          { nodes: data.nodes, edges: data.edges },
          options
        );

        networkRef.current = network;

        // Логирование кликов на узлы
        network.on('click', (params) => {
          if (params.nodes.length > 0) {
            const clickedUserId = params.nodes[0];
            console.log(`Clicked user: ${clickedUserId}`);
            // Можно открыть профиль или показать подробные данные
          }
        });
      });

    return () => {
      if (networkRef.current) {
        networkRef.current.destroy();
      }
    };
  }, [userId]);

  return (
    <div
      ref={containerRef}
      style={{
        width: '100%',
        height: '500px',
        backgroundColor: '#0f172a',
        borderRadius: '8px',
        border: '1px solid #334155'
      }}
    />
  );
}

export default NetworkGraph;
```

**Файл: frontend/src/components/EIMetricsChart.js**

```javascript
import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

function EIMetricsChart({ userId }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`/api/user/${userId}/metrics`)
      .then(res => res.json())
      .then(response => {
        const metrics = response.metrics;
        
        const chartData = {
          labels: metrics.map(m => new Date(m.date).toLocaleDateString()),
          datasets: [
            {
              label: 'Self-Awareness',
              data: metrics.map(m => m.self_awareness),
              borderColor: '#38bdf8',
              backgroundColor: 'rgba(56, 189, 248, 0.1)',
              fill: true,
              tension: 0.4
            },
            {
              label: 'Empathy',
              data: metrics.map(m => m.empathy),
              borderColor: '#22c55e',
              backgroundColor: 'rgba(34, 197, 94, 0.1)',
              fill: true,
              tension: 0.4
            },
            {
              label: 'Communication',
              data: metrics.map(m => m.communication),
              borderColor: '#f97316',
              backgroundColor: 'rgba(249, 115, 22, 0.1)',
              fill: true,
              tension: 0.4
            },
            {
              label: 'Motivation',
              data: metrics.map(m => m.motivation),
              borderColor: '#ec4899',
              backgroundColor: 'rgba(236, 72, 153, 0.1)',
              fill: true,
              tension: 0.4
            }
          ]
        };

        setData(chartData);
      });
  }, [userId]);

  if (!data) return <div>Loading...</div>;

  return (
    <div style={{ backgroundColor: '#0f172a', padding: '20px', borderRadius: '8px' }}>
      <h3 style={{ color: '#38bdf8', marginBottom: '20px' }}>
        Твой прогресс развития (Emotional Intelligence)
      </h3>
      <Line
        data={data}
        options={{
          responsive: true,
          plugins: {
            legend: {
              labels: { color: '#cbd5e1' }
            }
          },
          scales: {
            y: {
              min: 0,
              max: 100,
              ticks: { color: '#cbd5e1' },
              grid: { color: '#334155' }
            },
            x: {
              ticks: { color: '#cbd5e1' },
              grid: { color: '#334155' }
            }
          }
        }}
      />
    </div>
  );
}

export default EIMetricsChart;
```

---

## ЧАСТЬ 4: КОД ДЛЯ OBSIDIAN-СТИЛЬ ГРАФОВ

Если ты хочешь создать визуализацию как в Obsidian, используй **D3.js** вместо vis.js:

**Файл: frontend/src/components/ObsidianGraph.js**

```javascript
import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

function ObsidianGraph({ userId }) {
  const svgRef = useRef(null);

  useEffect(() => {
    fetch(`/api/network/${userId}`)
      .then(res => res.json())
      .then(data => {
        if (!svgRef.current) return;

        const width = 1000;
        const height = 600;

        // Очистить предыдущий граф
        d3.select(svgRef.current).selectAll("*").remove();

        const svg = d3.select(svgRef.current)
          .attr('width', width)
          .attr('height', height)
          .attr('style', 'background-color: #0f172a; border-radius: 8px;');

        // Симуляция физики для красивого расположения узлов
        const simulation = d3.forceSimulation(data.nodes)
          .force('link', d3.forceLink(data.edges)
            .id(d => d.id)
            .distance(100)
            .strength(0.5)
          )
          .force('charge', d3.forceManyBody().strength(-300))
          .force('center', d3.forceCenter(width / 2, height / 2))
          .force('collision', d3.forceCollide().radius(40));

        // Рисовать связи (edges)
        const link = svg.selectAll('line')
          .data(data.edges)
          .enter()
          .append('line')
          .attr('stroke', '#334155')
          .attr('stroke-width', d => d.weight)
          .attr('opacity', 0.6);

        // Рисовать узлы (nodes)
        const node = svg.selectAll('circle')
          .data(data.nodes)
          .enter()
          .append('circle')
          .attr('r', d => d.size || 20)
          .attr('fill', '#38bdf8')
          .attr('stroke', '#0f172a')
          .attr('stroke-width', 2)
          .call(drag(simulation));

        // Добавить текстовые метки
        const labels = svg.selectAll('text')
          .data(data.nodes)
          .enter()
          .append('text')
          .attr('font-size', 10)
          .attr('fill', '#f1f5f9')
          .attr('text-anchor', 'middle')
          .attr('dy', '.3em')
          .text(d => d.label);

        // Обновлять позиции при каждом шаге симуляции
        simulation.on('tick', () => {
          link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

          node
            .attr('cx', d => d.x = Math.max(20, Math.min(width - 20, d.x)))
            .attr('cy', d => d.y = Math.max(20, Math.min(height - 20, d.y)));

          labels
            .attr('x', d => d.x)
            .attr('y', d => d.y);
        });

        // Функция для перетаскивания узлов мышкой
        function drag(simulation) {
          function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          }

          function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
          }

          function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          }

          return d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended);
        }

        // Интерактивность: при наведении на узел показать подробности
        node.on('mouseover', function(event, d) {
          d3.select(this)
            .attr('fill', '#00ff00')
            .attr('r', d => (d.size || 20) + 5);
          
          labels.style('opacity', e => {
            // Показать только соседние узлы
            return data.edges.some(edge =>
              (edge.source.id === d.id && edge.target.id === e.id) ||
              (edge.target.id === d.id && edge.source.id === e.id)
            ) ? 1 : 0.2;
          });
        })
        .on('mouseout', function(event, d) {
          d3.select(this)
            .attr('fill', '#38bdf8')
            .attr('r', d => d.size || 20);
          
          labels.style('opacity', 1);
        });

      });
  }, [userId]);

  return <svg ref={svgRef} style={{ maxWidth: '100%', height: 'auto' }} />;
}

export default ObsidianGraph;
```

---

## ЧАСТЬ 5: МАКРОЭКОНОМИЧЕСКОЕ МОДЕЛИРОВАНИЕ

Для привязки к макроэкономике нужна модель, которая показывает, как развитие человеческого капитала влияет на экономические показатели.

**Файл: backend/economic_model.py**

```python
import numpy as np
import pandas as pd

class HumanCapitalEconomicModel:
    """
    Модель, связывающая развитие человеческого капитала в NETWEHUB
    с макроэкономическими показателями
    """
    
    def __init__(self, num_participants=100):
        self.num_participants = num_participants
        self.average_ei_score = 50  # начальный уровень
        self.productivity_factor = 1.0
    
    def calculate_ei_to_productivity(self, avg_ei_score):
        """
        Модель: EI → производительность
        Люди с высоким EI работают эффективнее
        """
        # Формула: Производительность = базовая * (1 + 0.005 * EI_улучшение)
        ei_improvement = avg_ei_score - 50
        productivity_multiplier = 1 + (ei_improvement / 100) * 0.5
        
        return productivity_multiplier
    
    def calculate_network_effects(self, avg_connections):
        """
        Модель: Сетевой эффект
        Больше связей → больше обмена идеями → выше инновационность
        """
        # Формула Меткалфа: ценность сети = n * (n-1) / 2
        network_value_multiplier = 1 + np.log(1 + avg_connections) * 0.1
        
        return network_value_multiplier
    
    def calculate_project_success_rate(self, avg_ei_score, avg_connections):
        """
        Вероятность успеха проекта зависит от EI и сети
        """
        ei_factor = avg_ei_score / 100  # нормализация 0-1
        connection_factor = min(avg_connections / 20, 1)  # нормализация
        
        success_rate = 0.3 + (ei_factor * 0.4) + (connection_factor * 0.3)
        
        return success_rate
    
    def calculate_startup_potential(self, avg_ei_score, avg_connections, num_projects):
        """
        Потенциал создания стартапов
        """
        base_probability = 0.1  # 10% вероятность, что участник запустит стартап
        
        ei_boost = (avg_ei_score - 50) / 100 * 0.15
        network_boost = (avg_connections / 20) * 0.2
        project_boost = min(num_projects / 5, 1) * 0.15
        
        total_probability = base_probability + ei_boost + network_boost + project_boost
        
        expected_startups = self.num_participants * min(total_probability, 0.5)
        
        return {
            'expected_startups': int(expected_startups),
            'total_probability': total_probability,
            'estimated_jobs_created': expected_startups * 5  # каждый стартап = 5 рабочих мест
        }
    
    def calculate_gdp_impact(self, avg_ei_score, avg_connections, num_projects):
        """
        Оценка влияния на ВНП (макроэкономический уровень)
        """
        # Базовый расчет дополнительного ВНП
        productivity_gain = self.calculate_ei_to_productivity(avg_ei_score)
        network_multiplier = self.calculate_network_effects(avg_connections)
        
        # Каждый участник = среднему российскому рабочему (около 600,000 руб/год)
        base_output_per_person = 600000
        
        # Дополнительный выход благодаря развитию
        additional_output = base_output_per_person * (productivity_gain - 1) + (network_multiplier - 1) * 50000
        
        total_additional_gdp = self.num_participants * additional_output
        
        startup_impact = self.calculate_startup_potential(avg_ei_score, avg_connections, num_projects)
        startup_gdp = startup_impact['expected_startups'] * 2000000  # средний доход стартапа
        
        return {
            'productivity_gain_percent': (productivity_gain - 1) * 100,
            'network_multiplier': network_multiplier,
            'additional_gdp_from_productivity': total_additional_gdp,
            'additional_gdp_from_startups': startup_gdp,
            'total_additional_gdp': total_additional_gdp + startup_gdp,
            'roi_percent': ((total_additional_gdp + startup_gdp) / (self.num_participants * 100000)) * 100
        }

# Пример использования
if __name__ == '__main__':
    model = HumanCapitalEconomicModel(num_participants=100)
    
    # Сценарий 1: исходное состояние
    initial_impact = model.calculate_gdp_impact(
        avg_ei_score=50,
        avg_connections=3,
        num_projects=0
    )
    
    # Сценарий 2: после 6 месяцев программы
    final_impact = model.calculate_gdp_impact(
        avg_ei_score=75,  # +25 пунктов в среднем
        avg_connections=12,  # +9 связей
        num_projects=5  # 5 проектов запущено
    )
    
    print("=" * 60)
    print("МАКРОЭКОНОМИЧЕСКОЕ ВОЗДЕЙСТВИЕ NETWEHUB")
    print("=" * 60)
    print(f"\nДО ПРОГРАММЫ:")
    print(f"  Доп. ВНП: {initial_impact['total_additional_gdp']:,.0f} руб")
    print(f"\nПОСЛЕ 6 МЕСЯЦЕВ:")
    print(f"  Дополнительный ВНП: {final_impact['total_additional_gdp']:,.0f} руб")
    print(f"  Рост производительности: +{final_impact['productivity_gain_percent']:.1f}%")
    print(f"  Ожидаемые стартапы: {final_impact['startup_potential']['expected_startups']}")
    print(f"  Созданные рабочие места: {final_impact['startup_potential']['estimated_jobs_created']}")
    print(f"  ROI (Return on Investment): {final_impact['roi_percent']:.1f}%")
```

---

## ЧАСТЬ 6: РАЗВЕРТЫВАНИЕ ПРОТОТИПА (неделя 5-6)

### Локальный запуск:

```bash
# Терминал 1: Backend
cd backend
source venv/bin/activate
python app.py
# Server запущен на http://localhost:5000

# Терминал 2: Frontend
cd frontend
npm start
# App запущен на http://localhost:3000
```

### Docker (опционально):

```dockerfile
# Dockerfile
FROM python:3.10

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

---

## ЧАСТЬ 7: ЧЕКЛИСТ ДЛЯ КУРСОВОЙ РАБОТЫ

Структура курсовой:

```
1. ВВЕДЕНИЕ
   └─ Актуальность: человеческий капитал в экономике
   └─ Проблема: как его измерить?
   └─ Гипотеза: EI влияет на производительность

2. ТЕОРЕТИЧЕСКАЯ ЧАСТЬ (20%)
   └─ Концепция человеческого капитала (Беккер, Шульц)
   └─ Эмоциональный интеллект (Гоулман)
   └─ Социальный капитал (Путнэм, Бурдье)
   └─ Сетевой анализ (Грановеттер)

3. МЕТОДИКА (20%)
   └─ Дизайн исследования
   └─ Описание NETWEHUB как экспериментальной платформы
   └─ Метрики и их сбор
   └─ Архитектура БД

4. ПРАКТИЧЕСКАЯ ЧАСТЬ (50%)
   └─ Описание платформы
   └─ Скриншоты интерфейса
   └─ Код ключевых компонентов
   └─ Результаты первых тестов (если есть данные)
   └─ Граф сетевых связей
   └─ Примеры метрик EI

5. МАКРОЭКОНОМИЧЕСКИЙ АНАЛИЗ (10%)
   └─ Модель влияния на ВНП
   └─ Расчет ROI
   └─ Масштабирование модели

6. ЗАКЛЮЧЕНИЕ
   └─ Выводы
   └─ Дальнейшие направления
   └─ Возможность коммерциализации
```

---

**Готово!** Это полный план для создания прототипа. Начни с ШАГ 1, потом переходи на ШАГ 2 и так далее. Примерно за 5-6 недель должен быть работающий MVP.

Вопросы? 🚀
