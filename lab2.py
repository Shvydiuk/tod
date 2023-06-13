from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

def main():
    #1 Завантажуємо набір даних Iris 
    iris = load_iris()
    X = iris.data
    y = iris.target

    #2: Ділимо його на тренувальну та тестову вибірки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #3: Створюємо пайплайн
    pipeline = Pipeline([
        ('scaler', StandardScaler()),   # Крок попередньої обробки: StandardScaler
        ('pca', PCA()),  #Крок відбору ознак: PCA
        ('classifier', LogisticRegression())  # Модель класифікації: Logistic Regression
    ])

    #4: Визначення гіперпараметрів та значення для GridSearchCV
    param_grid = {
        'pca__n_components': [2, 3],
        'classifier__C': [0.1, 1, 10] 
    }

    #5: Налаштування гіперпараметрів моделі та вибір функцій за допомогою GridSearchCV
    grid_search = GridSearchCV(pipeline, param_grid, cv=5)
    grid_search.fit(X_train, y_train)

    #6: Навчимо пайплайн на тренувальній вибірці та оцінимо його роботу на тестовій вибірці
    y_pred = grid_search.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

    #7: Порівняння результатів пайплайну з базовою моделлю, яка не використовує пайплайн
    baseline_model = LogisticRegression(max_iter=1000)
    baseline_model.fit(X_train, y_train)
    y_pred_baseline = baseline_model.predict(X_test)
    accuracy_baseline = accuracy_score(y_test, y_pred_baseline)
    print("Baseline Accuracy:", accuracy_baseline)

    #8: Збереження навченого пайплайну
    returnText = input ("Enter any symbol to stop execution of programm: ")
    joblib.dump(grid_search, 'trained_pipeline.pkl')

if __name__ == '__main__':
    main()