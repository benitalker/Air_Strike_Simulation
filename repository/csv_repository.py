import csv

def write_missions_to_csv(recommendations, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Target', 'Aircraft', 'Pilot', 'Score', 'Execution Time'])
        for mission in recommendations:
            writer.writerow([mission.target.city, mission.aircraft.type, mission.pilot.name,
                             mission.score, mission.execution_time])
    return filename