import requests
import matplotlib.pyplot as plt
from task_manager import TaskMan

API_KEY = 'b37659907a4e75eec905bb3022ba4355'
WEATHER_URL = f'http://api.openweathermap.org/data/2.5/weather?q=Buenos%20Aires,AR&units=metric&lang=es&appid={API_KEY}'

def show_weather():
    """
    Obtiene y muestra el clima actual de Buenos Aires usando la API de OpenWeatherMap.
    """
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
            print(f"\nError al obtener el clima. Código de estado: {response.status_code}")
            print(f"Detalle del error: {response.text}\n")
    except Exception as e:
        print(f"\nOcurrió un error: {e}\n")

def show_pending_tasks(manager):
    """
    Muestra todas las tareas pendientes.
    """
    tasks = manager.get_tasks()
    pending_tasks = [task for task in tasks if not task["completed"]]
    if not pending_tasks:
        print("\nNo hay tareas pendientes.\n")
    else:
        print("\nTareas pendientes:")
        for index, task in enumerate(pending_tasks, start=1):
            print(f"{index}. Título: {task['title']}\n   Descripción: {task['description']}\n")

def add_task(manager):
    """
    Permite al usuario agregar una nueva tarea.
    """
    print("\n--- Agregar una nueva tarea ---")
    title = input("Título: ").strip()
    description = input("Descripción: ").strip()
    if title and description:
        task = manager.add_task(title, description)
        print(f"\nTarea agregada exitosamente: {task}\n")
    else:
        print("\nError: Título y descripción son obligatorios.\n")

def mark_task_done(manager):
    """
    Permite al usuario marcar una tarea como completada.
    """
    print("\n--- Marcar tarea como completada ---")
    tasks = manager.get_tasks()
    pending_tasks = [task for task in tasks if not task["completed"]]
    if not pending_tasks:
        print("\nNo hay tareas pendientes para marcar como completadas.\n")
        return
    for index, task in enumerate(pending_tasks, start=1):
        print(f"{index}. Título: {task['title']}\n   Descripción: {task['description']}\n")
    try:
        task_number = int(input("Ingresa el número de la tarea que deseas marcar como hecha: ").strip())
        if 1 <= task_number <= len(pending_tasks):
            task_id = pending_tasks[task_number - 1]["id"]
            task = manager.update_task(task_id, completed=True)
            print(f"\nTarea marcada como completada: {task}\n")
        else:
            print("\nError: Número de tarea inválido.\n")
    except ValueError:
        print("\nError: Por favor, ingresa un número válido.\n")

def delete_incomplete_tasks(manager):
    """
    Elimina todas las tareas sin completar.
    """
    confirm = input("\n¿Estás seguro de que quieres eliminar todas las tareas sin completar? (s/n): ").lower()
    if confirm == "s":
        manager.delete_incomplete_tasks()
        print("\nTodas las tareas sin completar han sido eliminadas.\n")
    else:
        print("\nNo se realizaron cambios.\n")

def show_weekday_chart(manager):
    """
    Muestra un gráfico de barras de las tareas completadas agrupadas por día de la semana.
    """
    print("\n--- Gráfico de Tareas Completadas por Día de la Semana ---")
    data = manager.get_weekday_statistics()

    if data.empty:
        print("No hay tareas completadas para mostrar.\n")
    else:
        plt.figure(figsize=(10, 6))
        plt.bar(data["Día"], data["Total"], color="skyblue")
        plt.xlabel("Día de la Semana")
        plt.ylabel("Número de Tareas Completadas")
        plt.title("Tareas Completadas por Día de la Semana")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.show()

def show_completion_times_chart(manager):
    """
    Muestra un gráfico de barras de la cantidad de tareas completadas según el tiempo para completarlas.
    """
    print("\n--- Gráfico de Cantidad de Tareas por Tiempo de Finalización ---")
    data = manager.get_completion_times()

    if not data:
        print("No hay tareas completadas para mostrar.\n")
    else:
        times = [task["time_to_complete"] for task in data if task["time_to_complete"] > 0]

        if not times:
            print("No hay tiempos válidos para generar el gráfico.\n")
            return

        max_time = max(times)
        time_counts = [times.count(day) for day in range(1, max_time + 1)]

        plt.figure(figsize=(10, 6))
        plt.bar(range(1, max_time + 1), time_counts, color="orange")
        plt.xlabel("Días para Completar la Tarea")
        plt.ylabel("Cantidad de Tareas Completadas")
        plt.title("Cantidad de Tareas por Tiempo de Finalización")
        plt.xticks(range(1, max_time + 1))
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.show()

def main_menu():
    """
    Menú principal del programa con todas las opciones.
    """
    manager = TaskMan()
    try:
        while True:
            print("\n--- Menú Principal ---")
            print("1. Ver tareas pendientes")
            print("2. Agregar una nueva tarea")
            print("3. Marcar tarea como completada")
            print("4. Borrar tareas sin completar")
            print("5. Mostrar gráfico de tareas por día de la semana")
            print("6. Mostrar gráfico de tiempos para completar tareas")
            print("7. Mostrar clima actual en Buenos Aires")
            print("8. Salir")

            choice = input("Selecciona una opción (1-8): ").strip()

            if choice == "1":
                show_pending_tasks(manager)
            elif choice == "2":
                add_task(manager)
            elif choice == "3":
                mark_task_done(manager)
            elif choice == "4":
                delete_incomplete_tasks(manager)
            elif choice == "5":
                show_weekday_chart(manager)
            elif choice == "6":
                show_completion_times_chart(manager)
            elif choice == "7":
                show_weather()
            elif choice == "8":
                print("\n¡Hasta luego!")
                break
            else:
                print("\nOpción inválida. Por favor, selecciona una opción válida.\n")
    finally:
        manager.close()

if __name__ == "__main__":
    main_menu()
