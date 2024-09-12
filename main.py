from repository.json_repository import read_pilots_from_json, read_aircraft_from_json, read_targets_from_json
from service import mission_service
from service.mission_service import get_recommendations, save_recommendations_to_csv

# Declare global variables
pilots = []
aircraft = []
targets = []

def display_menu():
    print("\n--- Air Strike Simulation Menu ---")
    print("1. Load files (Pilots, Aircraft, Targets) from JSON")
    print("2. Display mission recommendations")
    print("3. Save mission recommendations to CSV")
    print("4. Exit")

def load_files():
    global pilots, aircraft, targets
    pilots = read_pilots_from_json('./assets/pilots.json')
    print(pilots)
    aircraft = read_aircraft_from_json('./assets/aircraft.json')
    print(aircraft)
    targets = read_targets_from_json('./assets/targets.json','./assets/city_coordinates.json')
    print(targets)
    mission_service.load_data(pilots, aircraft, targets)
    print("Files loaded successfully!")

def display_mission_recommendations():
    if not pilots or not aircraft or not targets:
        print("Please load the files first!")
        return

    recommendations = get_recommendations()

    if recommendations:
        print("\n--- Mission Recommendations ---")
        for recommendation in recommendations:
            print(recommendation)
    else:
        print("No recommendations available.")

def save_mission_recommendations_to_csv():
    if not pilots or not aircraft or not targets:
        print("Please load the files first!")
        return
    filename = "./assets/recommend_missions.csv"
    saved_filename = save_recommendations_to_csv(filename)
    print(f"Recommendations saved to {saved_filename}")

def main():
    while True:
        display_menu()
        choice = input("Select an option (1-4): ")
        if choice == '1':
            load_files()
        elif choice == '2':
            display_mission_recommendations()
        elif choice == '3':
            save_mission_recommendations_to_csv()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == '__main__':
    main()
