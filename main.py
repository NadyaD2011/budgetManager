import json
import argparse


def add_expense(expenses, description, amount, budget):
    if budget < amount:
        print('Не возможно добавить такую трата. Укажите точный бюджет.')
        return budget
    else:
        expenses.append(
            {
                "description": description,
                "amount": amount
            }
        )
        print(f'Успешно добавлена трата. {description} - {amount}')
        return budget - amount


def get_total_expenses(expenses):
    total_expenses = 0
    for expense in expenses:
        total_expenses += expense['amount']
    return total_expenses


def show_budget_details(first_budget, budget, expenses, add_budget):
    print(f'Изначальный бюджет: {first_budget}')
    print('Траты:')
    for expense in expenses:
        print(f' - {expense['description']} : {expense['amount']};')
    print(f'Всего потрачено: {get_total_expenses(expenses)}')
    print(f'Всего добавлено: {sum(add_budget)}')
    print(f'Текущий бюджет: {budget}')


def save_budget_details(filepath, initial_budget, expenses, first_budget):
    data = {
        "first_budget": first_budget,
        "initial_budget": initial_budget,
        "expenses": expenses
    }

    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)


def load_budget_data(filepath):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            return (
                data['initial_budget'],
                data['expenses'],
                data['first_budget']
            )
    except (FileNotFoundError, json.JSONDecodeError):
        return 0, [], 0


def update_budget(budget, add_budget):
    add_money = float(input('Введите количество добавленных денег: '))
    add_budget.append(add_money)
    return budget + add_money


def main():
    parser = argparse.ArgumentParser(
        description="В этой рограмме вы можете отслеживать ваши финансы."
    )
    parser.add_argument(
        "-file",
        "--filepath",
        help="Введите путь до файла",
        type=str,
        default='budget_data.json'
    )
    args = parser.parse_args()
    filepath = args.filepath

    print('Добро пожаловать! Здесь вы можете отслеживать ваши финансы.')

    inital_budget, expenses, first_budget = load_budget_data(filepath)
    if inital_budget == 0:
        inital_budget = float(input('Введите имеющиеся количество денег: '))
        first_budget = inital_budget
    budget = inital_budget
    add_budget = []

    while True:

        print("\nЧтобы вы хотел сделать ?\n1. Добавить траты\n2. Показать \
              оставшийся бюджет\n3. Обновить бюджет\n4. Выход")
        choice = int(input("Выберите действие (1/2/3/4): "))

        if choice == 1:
            description = input("Введите краткое описание траты: ")
            amount = float(input("Введите количество потраченных денег: "))
            budget = add_expense(expenses, description, amount, budget)
        elif choice == 2:
            show_budget_details(first_budget, budget, expenses, add_budget)
        elif choice == 3:
            budget = update_budget(budget, add_budget)
        elif choice == 4:
            inital_budget = budget
            save_budget_details(
                filepath,
                inital_budget,
                expenses,
                first_budget
            )
            print('Спасибо, что воспользовались нашим приложением!')
            break
        else:
            print('Произошла ошибка, попробуйте снова.')


if __name__ == "__main__":
    main()
