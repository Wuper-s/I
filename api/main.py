import requests
from todo_api import TaskManager

API_KEY = 'TU_CLAVE_DE_API'
WEATHER_URL = f'http://api.openweathermap.org/data/2.5/weather?q=Buenos%20Aires,AR&units=metric&lang=es&appid={API_KEY}'

def show_weather():
    try:
        response = requests.get(WEATHER_URL)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            print(f"\nClima actual en Buenos Aires:")
            print(f"Temperatura: {temp}°C")
            print(f"Descripción: {description.capitalize()}")
            print(f"Humedad: {humidity}%")
            print(f"Velocidad del viento: {wind_speed} m/s\n")
        else:
            print("\nError al obtener el clima. Por favor, intenta más tarde.\n")
    except Exception as e:
        print(f"\nOcurrió un error: {e}\n")

def show_tasks(manager):
    tasks = manager.get_tasks()
    if not tasks:
        print("\nNo hay tareas disponibles.\n")
    else:
        print("\nTareas actuales:")
        for index, task in enumerate(tasks, start=1):
            status = "Completada" if task["completed"] else "Pendiente"
            print(f"{index}. Título: {task['title']}\n   Descripción: {task['description']}\n   Estado: {status}\n")
    return tasks

def add_task(manager):
    print("\n--- Agregar una nueva tarea ---")
    title = input("Título: ").strip()
    description = input("Descripción: ").strip()
    if title and description:
        task = manager.add_task(title, description)
        print(f"\nTarea agregada exitosamente: {task}\n")
    else:
        print("\nError: Título y descripción son obligatorios.\n")

def mark_task_done(manager):
    print("\n--- Marcar tarea como completada ---")
    tasks = show_tasks(manager)
    try:
        task_number = int(input("Ingresa el número de la tarea que deseas marcar como hecha: ").strip())
        if 1 <= task_number <= len(tasks):
            task_id = tasks[task_number - 1]["id"]
            task = manager.update_task(task_id, completed=True)
            print(f"\nTarea marcada como completada: {task}\n")
        else:
            print("\nError: Número de tarea inválido.\n")
    except ValueError:
        print("\nError: Por favor, ingresa un número válido.\n")

def reset_tasks(manager):
    confirm = input("\n¿Estás seguro de que quieres eliminar todas las tareas? (s/n): ").lower()
    if confirm == "s":
        manager.reset_tasks()
        print("\nTodas las tareas han sido eliminadas.\n")
    else:
        print("\nNo se realizaron cambios.\n")

def main_menu():
    manager = TaskManager()
    try:
        while True:
            print("\n--- Menú Principal ---")
            print("1. Ver todas las tareas")
            print("2. Agregar una nueva tarea")
            print("3. Marcar tarea como completada")
            print("4. Resetear todas las tareas")
            print("5. Mostrar clima actual en Buenos Aires")
            print("6. Salir")

            choice = input("Selecciona una opción (1-6): ").strip()

            if choice == "1":
                show_tasks(manager)
            elif choice == "2":
                add_task(manager)
            elif choice == "3":
                mark_task_done(manager)
            elif choice == "4":
                reset_tasks(manager)
            elif choice == "5":
                show_weather()
            elif choice == "6":
                print("\n¡Hasta luego!")
                break
            else:
                print("\nOpción inválida. Por favor, selecciona una opción válida.\n")
    finally:
        manager.close()

if __name__ == "__main__":
    main_menu()
