# MoneyGraph Frontend

MVP интерфейса AML / financial network analytics для HackAlem AI. Сейчас используется только mock data: backend и AI-agent подключаются командой отдельно.

## Запуск

```bash
npm install
npm run dev
```

Проверка production-сборки:

```bash
npm run build
```

## Что реализовано

- тёмный enterprise fintech layout под ноутбук 1440×900;
- поиск и центрирование графа по GID;
- приоритетные узлы с фильтрами по роли и кластеру;
- направленный интерактивный граф payer → receiver на Cytoscape.js;
- zoom / pan / fit / reset и выбор узла;
- карточка Node Details с role score, priority score и связями;
- заметный explainability-блок “Why this role?”;
- mock-данные с ролями consolidator, transit, distributor, terminal, coordinator, peripheral.

## Границы MVP

API, расчёт ролей, кластеры и реальные транзакции намеренно не подключены. Компоненты готовы заменить mock data на контракт backend без изменения основного layout.
