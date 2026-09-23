import type { Language } from "./i18n"

// Original analysis text from the server remains unchanged.
export const interfaceCopy: Record<string, { en: string; kk: string }> = {
  "Расследование": {
    "en": "Investigation",
    "kk": "Зерттеу"
  },
  "Обновить данные": {
    "en": "Refresh data",
    "kk": "Деректерді жаңарту"
  },
  "Показать ещё 100": {
    "en": "Show 100 more",
    "kk": "Тағы 100 көрсету"
  },
  "Показать кластер": {
    "en": "Show cluster",
    "kk": "Кластерді көрсету"
  },
  "Подробнее о правиле": {
    "en": "Rule details",
    "kk": "Ереже туралы толығырақ"
  },
  "Повторить загрузку": {
    "en": "Retry loading",
    "kk": "Қайта жүктеу"
  },
  "Проверка API": {
    "en": "Check API",
    "kk": "API тексеру"
  },
  "Загружаем результат анализа…": {
    "en": "Loading analysis…",
    "kk": "Талдау нәтижесі жүктелуде…"
  },
  "В результате нет узлов": {
    "en": "No nodes in this result",
    "kk": "Нәтижеде түйіндер жоқ"
  },
  "Данные анализа": {
    "en": "Analysis data",
    "kk": "Талдау деректері"
  },
  "Последний пересчёт не удался. Показан предыдущий корректный результат.": {
    "en": "The last analysis failed. Showing the previous valid result.",
    "kk": "Соңғы есептеу сәтсіз аяқталды. Алдыңғы дұрыс нәтиже көрсетілген."
  },
  "Результаты — гипотезы для проверки, а не выводы о виновности.": {
    "en": "Results are hypotheses for review, not findings of wrongdoing.",
    "kk": "Нәтижелер — тексеруге арналған болжамдар, кінә туралы қорытынды емес."
  },
  "Узлы": {
    "en": "Nodes",
    "kk": "Түйіндер"
  },
  "Кластеры": {
    "en": "Clusters",
    "kk": "Кластерлер"
  },
  "Приоритеты": {
    "en": "Priorities",
    "kk": "Басымдықтар"
  },
  "Загружаем карточку…": {
    "en": "Loading node details…",
    "kk": "Түйін карточкасы жүктелуде…"
  },
  "Правило из рассчитанного снимка": {
    "en": "Rule from the analysis snapshot",
    "kk": "Талдау кескініндегі ереже"
  },
  "Граница обхода: исходящие не прослежены": {
    "en": "Traversal boundary: outgoing links not traced",
    "kk": "Іздеу шекарасы: шығыс байланыстар қадағаланбаған"
  },
  "Изолированный узел": {
    "en": "Isolated node",
    "kk": "Оқшауланған түйін"
  },
  "Внутренний оборот": {
    "en": "Internal turnover",
    "kk": "Ішкі айналым"
  },
  "Снимок": {
    "en": "Snapshot",
    "kk": "Деректер кескіні"
  },
  "Связи выбранного узла": {
    "en": "Selected node connections",
    "kk": "Таңдалған түйіннің байланыстары"
  },
  "Связи узла": {
    "en": "Node connections",
    "kk": "Түйін байланыстары"
  },
  "Все узлы": {
    "en": "All nodes",
    "kk": "Барлық түйіндер"
  },
  "Топ-{n}": {
    "en": "Top {n}",
    "kk": "Үздік {n}"
  },
  "Вернуться к сети": {
    "en": "Back to network",
    "kk": "Желіге оралу"
  },
  "Сбросить уровень": {
    "en": "Clear priority filter",
    "kk": "Басымдық сүзгісін тазарту"
  },
  "Направленная цепочка · {n} связей": {
    "en": "Directed path · {n} connections",
    "kk": "Бағытталған тізбек · {n} байланыс"
  },
  "Нажмите на связь, чтобы открыть факты": {
    "en": "Select a connection to view its facts",
    "kk": "Деректерін көру үшін байланысты басыңыз"
  },
  "все непосредственные соседи и связи между ними": {
    "en": "all direct neighbors and connections between them",
    "kk": "барлық тікелей көршілер және олардың арасындағы байланыстар"
  },
  "Обведённые узлы — выбранный уровень": {
    "en": "Outlined nodes match the selected priority",
    "kk": "Жиектелген түйіндер таңдалған басымдыққа сәйкес"
  },
  "Цепочка": {
    "en": "Path",
    "kk": "Тізбек"
  },
  "Полное окружение": {
    "en": "Full neighborhood",
    "kk": "Толық көршілестік"
  },
  "Приоритетные": {
    "en": "Priority nodes",
    "kk": "Басым түйіндер"
  },
  "{visible} из {total} узлов · {edges} связей": {
    "en": "{visible} of {total} nodes · {edges} connections",
    "kk": "{total} түйіннің {visible} көрсетілген · {edges} байланыс"
  },
  "ОТ СВЯЗИ К ПРОВЕРЯЕМОМУ ФАКТУ": {
    "en": "FROM CONNECTION TO VERIFIABLE FACT",
    "kk": "БАЙЛАНЫСТАН ТЕКСЕРІЛЕТІН ДЕРЕККЕ"
  },
  "Рабочее досье": {
    "en": "Investigation dossier",
    "kk": "Зерттеу досьесі"
  },
  "Закрыть расследование": {
    "en": "Close investigation",
    "kk": "Зерттеуді жабу"
  },
  "Раздел расследования": {
    "en": "Investigation section",
    "kk": "Зерттеу бөлімі"
  },
  "Связи": {
    "en": "Connections",
    "kk": "Байланыстар"
  },
  "Досье · {n}": {
    "en": "Dossier · {n}",
    "kk": "Досье · {n}"
  },
  "Этот факт уже в досье.": {
    "en": "This fact is already in the dossier.",
    "kk": "Бұл дерек досьеге қосылған."
  },
  "В досье уже 30 фактов. Удалите ненужные перед добавлением.": {
    "en": "The dossier has 30 facts. Remove an item before adding more.",
    "kk": "Досьеде 30 дерек бар. Жаңасын қосу үшін қажетсізін өшіріңіз."
  },
  "Факт добавлен в досье.": {
    "en": "Fact added to the dossier.",
    "kk": "Дерек досьеге қосылды."
  },
  "Направленный путь до {n} связей не найден в этом снимке. Обратное направление может дать другой результат.": {
    "en": "No directed path of up to {n} connections was found in this snapshot. The reverse direction may give a different result.",
    "kk": "Бұл кескінде {n} байланысқа дейінгі бағытталған жол табылмады. Кері бағыттың нәтижесі басқа болуы мүмкін."
  },
  "Не удалось найти путь.": {
    "en": "Could not find a path.",
    "kk": "Жолды табу мүмкін болмады."
  },
  "Один из GID отсутствует в снимке.": {
    "en": "One of the GIDs is missing from the snapshot.",
    "kk": "GID мәндерінің бірі кескінде жоқ."
  },
  "Выберите два разных GID.": {
    "en": "Choose two different GIDs.",
    "kk": "Екі түрлі GID таңдаңыз."
  },
  "PDF-экспорт пока недоступен на сервере.": {
    "en": "PDF export is not available on the server yet.",
    "kk": "Серверде PDF экспорты әзірге қолжетімсіз."
  },
  "Не удалось сформировать PDF.": {
    "en": "Could not generate the PDF.",
    "kk": "PDF жасау мүмкін болмады."
  },
  "Сервер не вернул PDF. Попробуйте ещё раз.": {
    "en": "The server did not return a PDF. Please try again.",
    "kk": "Сервер PDF қайтармады. Қайталап көріңіз."
  },
  "PDF сформирован. Файл передан браузеру для скачивания.": {
    "en": "PDF generated. The file was sent to your browser for download.",
    "kk": "PDF дайын. Файл жүктеп алу үшін браузерге жіберілді."
  },
  "Сервер не успел сформировать PDF. Попробуйте ещё раз.": {
    "en": "PDF generation timed out. Please try again.",
    "kk": "PDF жасау уақыты аяқталды. Қайталап көріңіз."
  },
  "Не удалось скачать PDF.": {
    "en": "Could not download the PDF.",
    "kk": "PDF жүктеп алу мүмкін болмады."
  },
  "ВЫБРАННАЯ СВЯЗЬ": {
    "en": "SELECTED CONNECTION",
    "kk": "ТАҢДАЛҒАН БАЙЛАНЫС"
  },
  "{n} переводов": {
    "en": "Transfers: {n}",
    "kk": "Аударымдар: {n}"
  },
  "Агрегат по направлению плательщик → получатель за наблюдаемый период.": {
    "en": "An aggregate from payer to receiver over the observed period.",
    "kk": "Бақыланған кезеңдегі төлеушіден алушыға бағытталған жиынтық."
  },
  "В досье": {
    "en": "Add to dossier",
    "kk": "Досьеге қосу"
  },
  "Исследовать путь": {
    "en": "Explore path",
    "kk": "Жолды зерттеу"
  },
  "Направление": {
    "en": "Direction",
    "kk": "Бағыт"
  },
  "Все связи": {
    "en": "All connections",
    "kk": "Барлық байланыстар"
  },
  "Входящие": {
    "en": "Incoming",
    "kk": "Кіріс"
  },
  "Исходящие": {
    "en": "Outgoing",
    "kk": "Шығыс"
  },
  "По убыванию наблюдаемой суммы. Нажмите связь для подробностей.": {
    "en": "Sorted by observed amount, largest first. Select a connection for details.",
    "kk": "Бақыланған сома бойынша кему ретімен. Толығырақ көру үшін байланысты басыңыз."
  },
  "В этом направлении наблюдаемых связей нет. Это не доказывает отсутствие операций вне выборки.": {
    "en": "No connections observed in this direction. This does not rule out transactions outside the sample.",
    "kk": "Бұл бағытта бақыланған байланыстар жоқ. Бұл іріктемеден тыс операциялар жоқ дегенді білдірмейді."
  },
  "Ещё 20 связей": {
    "en": "Show 20 more connections",
    "kk": "Тағы 20 байланыс"
  },
  "Как связаны два узла?": {
    "en": "How are two nodes connected?",
    "kk": "Екі түйін қалай байланысқан?"
  },
  "Кратчайшая направленная цепочка по числу связей. Поиск по всему снимку, до {n} связей, независимо от фильтров графа.": {
    "en": "Shortest directed path by connection count. Searches the whole snapshot, up to {n} connections, regardless of graph filters.",
    "kk": "Байланыс саны бойынша ең қысқа бағытталған тізбек. Граф сүзгілеріне қарамастан, бүкіл кескін бойынша {n} байланысқа дейін іздейді."
  },
  "Откуда": {
    "en": "From",
    "kk": "Қайдан"
  },
  "Куда": {
    "en": "To",
    "kk": "Қайда"
  },
  "GID начала пути": {
    "en": "Starting GID",
    "kk": "Бастапқы GID"
  },
  "GID конца пути": {
    "en": "Destination GID",
    "kk": "Соңғы GID"
  },
  "Взять выбранный узел": {
    "en": "Use selected node",
    "kk": "Таңдалған түйінді алу"
  },
  "Найти цепочку": {
    "en": "Find path",
    "kk": "Тізбекті табу"
  },
  "Поменять местами": {
    "en": "Swap endpoints",
    "kk": "Орындарын ауыстыру"
  },
  "Найдено связей: {n}": {
    "en": "Connections found: {n}",
    "kk": "Табылған байланыстар: {n}"
  },
  "Сбросить": {
    "en": "Reset",
    "kk": "Тазарту"
  },
  "Проверка хронологии": {
    "en": "Chronology check",
    "kk": "Хронологияны тексеру"
  },
  "Обсудить с AI": {
    "en": "Discuss with AI",
    "kk": "AI арқылы талқылау"
  },
  "Факты для ручной проверки": {
    "en": "Facts for manual review",
    "kk": "Қолмен тексеруге арналған деректер"
  },
  "Досье привязано к снимку. Хранится в этой вкладке до обновления страницы. Скачайте отчёт, чтобы сохранить результат.": {
    "en": "The dossier belongs to this snapshot and stays in this tab until you reload. Download the report to save your work.",
    "kk": "Досье осы кескінге тиесілі және бет жаңартылғанша осы қойындыда сақталады. Нәтижені сақтау үшін есепті жүктеп алыңыз."
  },
  "Добавить выбранный узел": {
    "en": "Add selected node",
    "kk": "Таңдалған түйінді қосу"
  },
  "Начните с узла, связи или найденной цепочки. В отчёт попадут только добавленные факты.": {
    "en": "Start with a node, connection or path. Only added facts appear in the report.",
    "kk": "Түйіннен, байланыстан немесе табылған тізбектен бастаңыз. Есепке тек қосылған деректер кіреді."
  },
  "Убрать из досье": {
    "en": "Remove from dossier",
    "kk": "Досьеден алып тастау"
  },
  "Готовим PDF…": {
    "en": "Generating PDF…",
    "kk": "PDF дайындалуда…"
  },
  "Скачать PDF ({n})": {
    "en": "Download PDF ({n})",
    "kk": "PDF жүктеп алу ({n})"
  },
  "Скачать текст .md": {
    "en": "Download text .md",
    "kk": ".md мәтінін жүктеп алу"
  },
  "гипотезы, не обвинения": {
    "en": "hypotheses, not accusations",
    "kk": "болжамдар, айыптаулар емес"
  },
  "Закрыть AI": {
    "en": "Close AI",
    "kk": "AI жабу"
  },
  "Спросить AI": {
    "en": "Ask AI",
    "kk": "AI сұрау"
  },
  "AI-ассистент": {
    "en": "AI assistant",
    "kk": "AI көмекшісі"
  },
  "AI-ассистент аналитика": {
    "en": "Analyst AI assistant",
    "kk": "Талдаушының AI көмекшісі"
  },
  "Вопрос и выбранные агентом факты передаются в OpenAI. Ответы — гипотезы для проверки.": {
    "en": "Your question and the facts selected by the agent are sent to OpenAI. Answers are hypotheses for review.",
    "kk": "Сұрақ пен агент таңдаған деректер OpenAI-ға жіберіледі. Жауаптар — тексеруге арналған болжамдар."
  },
  "Топ-10": {
    "en": "Top 10",
    "kk": "Үздік 10"
  },
  "Объяснить узел": {
    "en": "Explain node",
    "kk": "Түйінді түсіндіру"
  },
  "Новый разговор": {
    "en": "New conversation",
    "kk": "Жаңа әңгіме"
  },
  "Вопрос агенту": {
    "en": "Question for the agent",
    "kk": "Агентке сұрақ"
  },
  "Какие узлы проверить первыми?": {
    "en": "Which nodes should I review first?",
    "kk": "Алдымен қай түйіндерді тексеру керек?"
  },
  "Агент изучает данные…": {
    "en": "Agent is examining the data…",
    "kk": "Агент деректерді зерттеуде…"
  },
  "Отправить вопрос": {
    "en": "Send question",
    "kk": "Сұрақты жіберу"
  },
  "Локальный анализ · без LLM": {
    "en": "Local analysis · no LLM",
    "kk": "Жергілікті талдау · LLM қолданылмайды"
  },
  "AI · факты из инструментов": {
    "en": "AI · facts from tools",
    "kk": "AI · құралдардан алынған деректер"
  },
  "Ответ по снимку графа": {
    "en": "Answer from the graph snapshot",
    "kk": "Граф кескіні бойынша жауап"
  },
  "Инструменты агента": {
    "en": "Agent tools",
    "kk": "Агент құралдары"
  },
  "Время ожидания истекло.": {
    "en": "The request timed out.",
    "kk": "Күту уақыты аяқталды."
  },
  "Сервис недоступен": {
    "en": "Service unavailable",
    "kk": "Қызмет қолжетімсіз"
  },
  "API недоступен": {
    "en": "API unavailable",
    "kk": "API қолжетімсіз"
  },
  "Результат анализа сменился. Обновите данные сайта и повторите вопрос.": {
    "en": "The analysis has changed. Refresh the data and ask again.",
    "kk": "Талдау нәтижесі өзгерді. Деректерді жаңартып, сұрақты қайталаңыз."
  },
  "Выбери 10 приоритетных узлов": {
    "en": "Select 10 priority nodes. Answer in English.",
    "kk": "Басымдығы жоғары 10 түйінді таңда. Қазақ тілінде жауап бер."
  },
  "Объясни роль узла #{gid}": {
    "en": "Explain the role of node #{gid}. Answer in English.",
    "kk": "#{gid} түйінінің рөлін түсіндір. Қазақ тілінде жауап бер."
  },
  "Язык": {
    "en": "Language",
    "kk": "Тіл"
  },
  "Снимок изменился. Обновите данные и соберите досье заново.": {
    "en": "The snapshot changed. Refresh the data and rebuild the dossier.",
    "kk": "Кескін өзгерді. Деректерді жаңартып, досьені қайта жинаңыз."
  },
  "Для проверки хронологии не хватает дат. Показана только структура связей.": {
    "en": "Dates are missing for the chronology check. Only the connection structure is shown.",
    "kk": "Хронологияны тексеру үшін күндер жеткіліксіз. Тек байланыс құрылымы көрсетілген."
  },
  "Диапазоны дат не исключают последовательность. Агрегаты не подтверждают, что по цепочке прошли одни и те же деньги; нужна проверка отдельных операций.": {
    "en": "The date ranges do not rule out a sequence. Aggregates do not prove that the same money traveled along the path; individual transactions need review.",
    "kk": "Күндер аралығы реттілікті жоққа шығармайды. Жиынтық деректер тізбек арқылы бір қаражат өткенін растамайды; жеке операцияларды тексеру қажет."
  },
  "Хронология не сходится: на шаге {step} последний перевод был {last}, а предыдущие шаги требуют даты не раньше {earliest}. Эта цепочка не описывает последовательное движение средств в наблюдаемом периоде.": {
    "en": "Chronology conflict: at step {step}, the last transfer was on {last}, but previous steps require a date on or after {earliest}. This path does not describe sequential fund movement within the observed period.",
    "kk": "Хронология сәйкес емес: {step}-қадамдағы соңғы аударым {last} күні болған, ал алдыңғы қадамдар {earliest} күнінен ерте емес күнді талап етеді. Бұл тізбек бақыланған кезеңдегі қаражаттың ретімен қозғалуын сипаттамайды."
  },
  "Объясни направленную цепочку {path}. Проверь связи и даты инструментами. Проверка хронологии: {check}. Объясни ограничения и не утверждай, что это одни и те же деньги.": {
    "en": "Explain the directed path {path}. Verify connections and dates with tools. Chronology check: {check}. Explain limitations and do not claim these are the same funds. Answer in English.",
    "kk": "{path} бағытталған тізбегін түсіндір. Байланыстар мен күндерді құралдар арқылы тексер. Хронология тексерісі: {check}. Шектеулерді түсіндір, бұл бір қаражат деп тұжырымдама. Қазақ тілінде жауап бер."
  },
  "Настроен. Доступ к модели проверяется при отправке вопроса.": {
    "en": "Configured. Model access is checked when you send a question.",
    "kk": "Бапталған. Модельге қолжетімділік сұрақ жіберілгенде тексеріледі."
  },
  "AI-ассистент выключен: задайте ASSISTANT_ENABLED=1 в backend/.env": {
    "en": "AI assistant is disabled. Set ASSISTANT_ENABLED=1 in backend/.env.",
    "kk": "AI көмекшісі өшірулі. backend/.env ішінде ASSISTANT_ENABLED=1 орнатыңыз."
  },
  "Не задан OPENAI_API_KEY в backend/.env": {
    "en": "OPENAI_API_KEY is missing in backend/.env.",
    "kk": "backend/.env ішінде OPENAI_API_KEY көрсетілмеген."
  },
  "Не задан OPENAI_MODEL в backend/.env": {
    "en": "OPENAI_MODEL is missing in backend/.env.",
    "kk": "backend/.env ішінде OPENAI_MODEL көрсетілмеген."
  },
  "Установите зависимости backend/requirements-assistant.txt": {
    "en": "Install the dependencies in backend/requirements-assistant.txt.",
    "kk": "backend/requirements-assistant.txt тәуелділіктерін орнатыңыз."
  },
  "Нет результата анализа. Запустите pipeline и перечитайте снимок.": {
    "en": "No analysis result. Run the pipeline and reload the snapshot.",
    "kk": "Талдау нәтижесі жоқ. Есептеуді іске қосып, кескінді қайта жүктеңіз."
  },
  "Результат изменился во время загрузки. Обновите данные.": {
    "en": "The result changed while loading. Refresh the data.",
    "kk": "Жүктеу кезінде нәтиже өзгерді. Деректерді жаңартыңыз."
  },
  "Снимок сменился. Обновите данные сайта.": {
    "en": "The snapshot changed. Refresh the website data.",
    "kk": "Кескін өзгерді. Сайт деректерін жаңартыңыз."
  },
  "Узел": {
    "en": "Node",
    "kk": "Түйін"
  },
  "Направленная цепочка": {
    "en": "Directed path",
    "kk": "Бағытталған тізбек"
  },
  "Связь": {
    "en": "Connection",
    "kk": "Байланыс"
  }
}

export function translate(language: Language, text: string, values: Record<string, string | number> = {}): string {
  const template = language === "ru" ? text : interfaceCopy[text]?.[language] ?? text
  return template.replace(/\{(\w+)\}/g, (match, key) => String(values[key] ?? match))
}
