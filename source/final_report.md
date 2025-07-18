# Финален отчет / Final Report

## Описание на проекта / Project Description

[Кратко описание на проекта.]

## Постигнати резултати / Achieved Results

[Опишете постигнатите резултати.]

## Метрики за оценка на модела / Model Evaluation Metrics

В проекта за класификация използвахме следните метрики за оценка на логистичната регресия:

- **Precision (Точност):** Дял на правилно предсказаните положителни примери от всички предсказани като положителни. Високата стойност означава малко фалшиви положителни.
- **Recall (Чувствителност):** Дял на правилно предсказаните положителни примери от всички реално положителни. Високата стойност означава малко фалшиви отрицателни.
- **F1-Score:** Хармонично средно между precision и recall. Подходяща метрика при небалансирани класове.
- **Accuracy (Точност на класификация):** Дял на правилно класифицираните примери от всички примери.
- **Confusion Matrix (Матрица на объркванията):** Показва броя на правилно и неправилно класифицираните примери за всеки клас.
- **Log Loss (Ентропия):** Мери несигурността на предсказанията. По-ниска стойност означава по-добра калибрация на вероятностите.
- **Information Gain (Информационна печалба):** Оценява важността на всяка входна характеристика (feature) за задачата. Използвахме mutual information за да оправдаем избора на входни характеристики.

### Как са използвани метриките в проекта

- Всички метрики се изчисляват автоматично след трениране на логистичната регресия и се визуализират в сайта на страницата "Logistic Regression Results".
- Information gain се използва, за да се покаже кои характеристики (напр. x, y) са най-информативни за класификацията.
- Logloss се използва като обективна мярка за качеството на вероятностните предсказания.

### Примерни изводи от използването на метриките

- Ако precision и recall са високи, моделът успешно разпознава и двата класа без много грешки.
- Високата accuracy показва, че моделът се справя добре с общата класификация.
- F1-score е полезен при небалансирани класове – ако е висок, моделът не пренебрегва малкия клас.
- Нисък logloss означава, че вероятностните предсказания са добре калибрирани.
- Матрицата на объркванията показва дали има класове, които често се бъркат.
- Information gain показва, че характеристиката X (или Y) е по-важна за класификацията, ако нейната стойност е по-висока. Това оправдава избора на входни характеристики.

## Разпределение на задачите / Task Distribution

[Кой какво е правил.]

## ERD диаграма / ERD Diagram

![ERD](erd_diagram.png)

## Sequence UML диаграма / Sequence UML Diagram

![Sequence](sequence_diagram.png)

## UML Use Case диаграма / UML Use Case Diagram

![Use Case](use_case_diagram.png)

## UML диаграми на таблиците / UML Class Diagrams

### Role
![Role](uml_role.png)

### User
![User](uml_user.png)

### ClassifiedPoint
![ClassifiedPoint](uml_classifiedpoint.png)

---

## Приложения / Appendices

[Добавете други материали, ако е нужно.] 