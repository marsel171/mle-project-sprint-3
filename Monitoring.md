# Мониторинг

Графики на дашборде представляют временные ряды данных, метрики производительности и статистику использования модели. 


## Для мониторинга выбраны метрики нескольких слоев:

### Инфраструткурный слой:
- Метрика "Потребление RAM"

    Эта метрика нужна, чтобы отображать, сколько оперативной памяти занято именно сейчас.


### Метрики реального времени:
- Метрика "Квантили ответов модели"

    Эта метрика нужна, для того, чтобы отслеживать поведение модели. Показывает медианное предсказание модели, информацию о квантилях 0.95 и 0.05 модели, чтобы следить за выбросами предсказаний.

### Метрики прикладного уровня:
- Метрика "Динамика предсказаний"

    Эта метрика выбрана для отслеживания частоты запросов к модели.
    Может понадобится для отслеживания закономерностей в использовании сервисом, и в целом, потребности в такой модели. Возможно отслеживание косвенных признаков - внедрили новую фичу, запустили рекламу аффектного сервиса и т.д.

- Метрика "Гистограмма предсказанных цен"

    Эта метрика может показать как оценку адекватности модели, так и наиболее популярные объекты (ЦА), для которой модель должна предсказывать цены. Если какая-то корзина окажется намного больше остальных, то это повод обратить внимание как на качество модели, (возможно она устарела или сменился источник данных для отработки), либо модель используется только для узкой категории объектов недвижимости и возможно стоит переработать препроцессинг данных и выкинуть не целевые данные для обучения.