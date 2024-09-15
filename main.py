from repository.json_repository import read_pilots_from_json, read_aircraft_from_json, read_targets_from_json
from service import mission_service
from service.mission_service import get_recommendations, save_recommendations_to_csv
from toolz import curry, pipe, compose, pluck, get_in, assoc, partition, first, second, nth
from toolz.curried import map, filter, reduce

# Global variables
global_data = {'pilots': [], 'aircraft': [], 'targets': []}

menu_options = {
    '1': ('Load files (Pilots, Aircraft, Targets) from JSON', 'load_files'),
    '2': ('Display mission recommendations', 'display_mission_recommendations'),
    '3': ('Save mission recommendations to CSV', 'save_mission_recommendations_to_csv'),
    '4': ('Exit', 'exit')
}

@curry
def load_file(reader_func, file_path, *extra_args):
    return reader_func(file_path, *extra_args)

def load_files():
    file_loaders = [
        ('pilots', load_file(read_pilots_from_json, './assets/pilots.json')),
        ('aircraft', load_file(read_aircraft_from_json, './assets/aircraft.json')),
        ('targets', load_file(read_targets_from_json, './assets/targets.json', './assets/city_coordinates.json'))
    ]

    global global_data
    global_data = reduce(lambda acc, item: assoc(acc, first(item), second(item)), file_loaders, {})

    mission_service.load_data(**global_data)
    print("Files loaded successfully!")

def display_mission_recommendations():
    if not all(global_data.values()):
        print("Please load the files first!")
        return

    recommendations = get_recommendations()

    if recommendations:
        print("\n--- Mission Recommendations ---")
        pipe(
            recommendations,
            map(str),
            '\n'.join,
            print
        )
    else:
        print("No recommendations available.")

def save_mission_recommendations_to_csv():
    if not all(global_data.values()):
        print("Please load the files first!")
        return
    filename = "./assets/recommend_missions.csv"
    saved_filename = save_recommendations_to_csv(filename)
    print(f"Recommendations saved to {saved_filename}")

def display_menu():
    print("\n--- Air Strike Simulation Menu ---")
    pipe(
        menu_options.items(),
        map(lambda item: f"{item[0]}. {item[1][0]}"),
        '\n'.join,
        print
    )

def get_menu_choice():
    return input("Select an option (1-4): ")

def execute_menu_choice(choice):
    if choice == '4':
        print("Exiting the program.")
        return False
    
    action = get_in([choice, 1], menu_options)
    if action:
        globals()[action]()
    else:
        print("Invalid choice. Please select a valid option.")
    return True

def main():
    while True:
        display_menu()
        if not execute_menu_choice(get_menu_choice()):
            break

if __name__ == '__main__':
    main()