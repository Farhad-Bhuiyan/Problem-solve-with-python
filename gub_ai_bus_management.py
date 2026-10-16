
import json
import os
from collections import deque
from copy import deepcopy

# ============================================================
# AI-BASED UNIVERSITY BUS MANAGEMENT SYSTEM
# Green University of Bangladesh
#
# Console only - NO GUI
#
# AI / Algorithm usage:
#   Graph            -> Stops, roads, routes, conflicts
#   BFS              -> Shortest route, alternative route
#   DFS              -> Network exploration
#   Graph Coloring   -> Conflict-free time-slot assignment
#   CSP/Backtracking -> Bus assignment, capacity assignment,
#                       schedule generation, conflict checking
#
# NOTE:
# The supplied GUB schedule does not provide total passenger
# capacity for every bus. Therefore, the initial capacities
# below are LAB-SIMULATION values and can be updated from menu.
# ============================================================


DATA_DIR = "gub_bus_data"
STOPS_FILE = os.path.join(DATA_DIR, "stops.json")
ROADS_FILE = os.path.join(DATA_DIR, "roads.json")
ROUTES_FILE = os.path.join(DATA_DIR, "routes.json")
BUSES_FILE = os.path.join(DATA_DIR, "buses.json")
STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
SCHEDULE_FILE = os.path.join(DATA_DIR, "schedule.json")


# ============================================================
# DEFAULT DATA FROM THE PROVIDED GUB SCHEDULE
# ============================================================

DEFAULT_ROUTES = {
    "Route 01": {
        "name": "Shewrapara to GUB via Mirpur 12",
        "stops": [
            "Shewrapara", "Mirpur-10", "Mirpur-12",
            "Kalshi", "ECB Chattor", "Kuril", "GUB Campus"
        ],
        "pickup_times": {
            "Shewrapara": "07:00",
            "Mirpur-10": "07:05",
            "Mirpur-12": "07:10",
            "Kalshi": "07:15",
            "ECB Chattor": "07:17",
            "Kuril": "07:30"
        },
        "campus_departures": ["13:45", "16:45"]
    },

    "Route 02": {
        "name": "Shewrapara to GUB via Mohakhali",
        "stops": [
            "Shewrapara", "Agargaon", "Mohakhali",
            "Banani", "MES", "Kuril", "GUB Campus"
        ],
        "pickup_times": {
            "Shewrapara": "07:15",
            "Agargaon": "07:20",
            "Mohakhali": "07:35",
            "Banani": "07:45",
            "MES": "07:50",
            "Kuril": "07:55"
        },
        "campus_departures": ["16:45"]
    },

    "Route 03_1": {
        "name": "Shyamoli to GUB via Majar Road",
        "stops": [
            "Shyamoli", "Technical Mor", "Gabtoli",
            "Majar Road", "Mirpur 1", "Mirpur 2",
            "Mirpur 11", "Kalshi", "Kuril", "GUB Campus"
        ],
        "pickup_times": {
            "Shyamoli": "07:00",
            "Technical Mor": "07:05",
            "Gabtoli": "07:10",
            "Majar Road": "07:15",
            "Mirpur 1": "07:20",
            "Mirpur 2": "07:25",
            "Mirpur 11": "07:30",
            "Kalshi": "07:45",
            "Kuril": "07:55"
        },
        "campus_departures": ["16:45"]
    },

    "Route 03_2": {
        "name": "Shyamoli to GUB via Technical Mor",
        "stops": [
            "Shyamoli", "Technical Mor", "Mirpur 1",
            "Mirpur 2", "Mirpur 11", "Kalshi",
            "Kuril", "GUB Campus"
        ],
        "pickup_times": {
            "Shyamoli": "07:10",
            "Technical Mor": "07:15",
            "Mirpur 1": "07:25",
            "Mirpur 2": "07:30",
            "Mirpur 11": "07:35",
            "Kalshi": "07:45",
            "Kuril": "07:55"
        },
        "campus_departures": ["16:45"]
    },

    "Route 04_1": {
        "name": "Azimpur to GUB via Dhanmondi 27-Farmgate",
        "stops": [
            "Azimpur", "New Market", "City College",
            "Dhanmondi 27", "Khamar Bari", "Farmgate",
            "Mohakhali", "Banani", "Kuril", "GUB Campus"
        ],
        "pickup_times": {
            "Azimpur": "07:00",
            "New Market": "07:05",
            "City College": "07:07",
            "Dhanmondi 27": "07:10",
            "Khamar Bari": "07:15",
            "Farmgate": "07:20",
            "Mohakhali": "07:25",
            "Banani": "07:30",
            "Kuril": "07:35"
        },
        "campus_departures": ["16:45"]
    },

    "Route 05_1": {
        "name": "Motijheel to GUB via Malibagh",
        "stops": [
            "Motijheel", "Komlapur", "Basabo", "Khilgaon",
            "Malibag", "Abul Hotel", "Rampura", "Badda",
            "Natun Bazar", "Kuril", "GUB Campus"
        ],
        "pickup_times": {
            "Motijheel": "07:00",
            "Komlapur": "07:05",
            "Basabo": "07:10",
            "Khilgaon": "07:12",
            "Malibag": "07:18",
            "Abul Hotel": "07:22",
            "Rampura": "07:27",
            "Badda": "07:35",
            "Natun Bazar": "07:40",
            "Kuril": "07:50"
        },
        "campus_departures": ["13:45", "16:45"]
    },

    "Route 05_2": {
        "name": "Malibagh to GUB via Rampura",
        "stops": [
            "Malibag", "Abul Hotel", "Rampura",
            "Badda", "Natun Bazar", "Kuril", "GUB Campus"
        ],
        "pickup_times": {
            "Malibag": "07:10",
            "Abul Hotel": "07:15",
            "Rampura": "07:20",
            "Badda": "07:30",
            "Natun Bazar": "07:35",
            "Kuril": "07:45"
        },
        "campus_departures": ["16:45"]
    },

    "Route 06_1": {
        "name": "Gulistan to GUB via Staff Quarter",
        "stops": [
            "Gulistan", "Tikatuli", "Doyaganj", "Jonopath Mor",
            "Jatrabari", "Vangga Press", "Mridhabari", "Konapara",
            "Staff Quarter", "Tarabo", "Rupshi", "Bhulta",
            "GUB Campus"
        ],
        "pickup_times": {
            "Gulistan": "06:45",
            "Tikatuli": "06:55",
            "Doyaganj": "06:57",
            "Jonopath Mor": "06:59",
            "Jatrabari": "07:00",
            "Vangga Press": "07:02",
            "Mridhabari": "07:03",
            "Konapara": "07:10",
            "Staff Quarter": "07:12",
            "Tarabo": "07:15",
            "Rupshi": "07:20",
            "Bhulta": "07:35"
        },
        "campus_departures": ["16:45"]
    },

    "Route 06_2": {
        "name": "Jatrabari to GUB via Staff Quarter",
        "stops": [
            "Jatrabari", "Vangga Press", "Mridhabari",
            "Konapara", "Staff Quarter", "Tarabo",
            "Rupshi", "Bhulta", "GUB Campus"
        ],
        "pickup_times": {
            "Jatrabari": "07:05",
            "Vangga Press": "07:07",
            "Mridhabari": "07:10",
            "Konapara": "07:15",
            "Staff Quarter": "07:20",
            "Tarabo": "07:25",
            "Rupshi": "07:30",
            "Bhulta": "07:40"
        },
        "campus_departures": ["16:45"]
    },

    "Route 07": {
        "name": "Shonir Akhra to GUB via Kanchpur",
        "stops": [
            "Shonir Akhra", "Rayerbagh", "Matuail",
            "Sign Board", "CTG Road", "Kachpur",
            "Tarabo", "Rupshi", "Bhulta", "GUB Campus"
        ],
        "pickup_times": {
            "Shonir Akhra": "06:50",
            "Rayerbagh": "06:52",
            "Matuail": "06:55",
            "Sign Board": "07:00",
            "CTG Road": "07:10",
            "Kachpur": "07:15",
            "Tarabo": "07:20",
            "Rupshi": "07:25",
            "Bhulta": "07:50"
        },
        "campus_departures": ["13:45", "16:45"]
    },

    "Route 08_1": {
        "name": "Chashara to GUB via CTG Road",
        "stops": [
            "Chashara", "Nobiganj", "Chowdhuri Bari",
            "Adomjhee EPZ", "CTG Road", "Kachpur",
            "Tarabo", "Rupshi", "Murapara", "GUB Campus"
        ],
        "pickup_times": {
            "Chashara": "06:35",
            "Nobiganj": "06:40",
            "Chowdhuri Bari": "06:45",
            "Adomjhee EPZ": "06:55",
            "CTG Road": "07:05",
            "Kachpur": "07:10",
            "Tarabo": "07:20",
            "Rupshi": "07:25",
            "Murapara": "07:30"
        },
        "campus_departures": ["16:45"]
    },

    "Route 08_2": {
        "name": "Chashara to GUB via Sign Board",
        "stops": [
            "Chashara", "Shibu Market", "Jalkuri", "Bhuighar",
            "Mamudpar", "Sign Board", "Shanarpar", "CTG Road",
            "Kachpur", "Tarabo", "Rupshi", "Murapara",
            "GUB Campus"
        ],
        "pickup_times": {
            "Chashara": "06:45",
            "Shibu Market": "06:50",
            "Jalkuri": "06:55",
            "Bhuighar": "06:57",
            "Mamudpar": "07:00",
            "Sign Board": "07:10",
            "Shanarpar": "07:15",
            "CTG Road": "07:20",
            "Kachpur": "07:25",
            "Tarabo": "07:35",
            "Rupshi": "07:40",
            "Murapara": "07:50"
        },
        "campus_departures": ["13:45", "16:45"]
    },

    "Route 09_1": {
        "name": "Narsingdi (Velanagar) to GUB via Bhulta",
        "stops": [
            "Narsingdi Velanagar", "Shahe Protap",
            "Panchdona", "Madhopdi", "Bhulta", "GUB Campus"
        ],
        "pickup_times": {
            "Narsingdi Velanagar": "07:00",
            "Shahe Protap": "07:10",
            "Panchdona": "07:20",
            "Madhopdi": "07:30",
            "Bhulta": "07:45"
        },
        "campus_departures": ["13:45", "16:45"]
    },

    "Route 09_2": {
        "name": "Narsingdi (Ghorashal) to GUB via Bhulta",
        "stops": [
            "Ghorashal", "Panchdona",
            "Madhopdi", "Bhulta", "GUB Campus"
        ],
        "pickup_times": {
            "Ghorashal": "07:00",
            "Panchdona": "07:10",
            "Madhopdi": "07:20",
            "Bhulta": "07:35"
        },
        "campus_departures": ["16:45"]
    },

    "Route 10_1": {
        "name": "Bypass (Gazipur) to GUB via Abdullahpur",
        "stops": [
            "Gazipur Bypass", "Abdullahpur", "Azompur",
            "Rajlakshmi", "Airport", "Khilkhet",
            "Kuril", "GUB Campus"
        ],
        "pickup_times": {
            "Gazipur Bypass": "06:45",
            "Abdullahpur": "07:00",
            "Azompur": "07:05",
            "Rajlakshmi": "07:10",
            "Airport": "07:15",
            "Khilkhet": "07:18",
            "Kuril": "07:22"
        },
        "campus_departures": ["16:45"]
    },

    "Route 10_2": {
        "name": "Chowrasta (Gazipur) to GUB via Mirer Bazar",
        "stops": [
            "Gazipur Chowrasta", "Gazipur Bypass",
            "Meghdubi", "Mirer Bazar", "Ulukhola",
            "Zinda Park", "Kanchon", "GUB Campus"
        ],
        "pickup_times": {
            "Gazipur Chowrasta": "06:45",
            "Gazipur Bypass": "06:47",
            "Meghdubi": "06:55",
            "Mirer Bazar": "07:00",
            "Ulukhola": "07:05",
            "Zinda Park": "07:10",
            "Kanchon": "07:20"
        },
        "campus_departures": ["16:45"]
    },

    "Route 11": {
        "name": "Sonargaon to GUB via Madanpur-Noyapur",
        "stops": [
            "Mograpara", "Langalbond", "Madanpur",
            "Noyapur", "Bostail", "Gawsia", "GUB Campus"
        ],
        "pickup_times": {
            "Mograpara": "07:00",
            "Langalbond": "07:05",
            "Madanpur": "07:10",
            "Noyapur": "07:15",
            "Bostail": "07:30",
            "Gawsia": "07:40"
        },
        "campus_departures": ["16:45"]
    },

    "Route 11_12": {
        "name": "Sonargaon Baradi to GUB via Araihazar",
        "stops": [
            "Sonargaon-Baradi", "Ladhurchor", "Mahazampur",
            "Taltola", "Eidbardi", "Araihazar Chowrasta",
            "Kalibari Bazar", "Duptara", "Gawsia", "GUB Campus"
        ],
        "pickup_times": {
            "Sonargaon-Baradi": "07:00",
            "Ladhurchor": "07:10",
            "Mahazampur": "07:12",
            "Taltola": "07:20",
            "Eidbardi": "07:25",
            "Araihazar Chowrasta": "07:30",
            "Kalibari Bazar": "07:35",
            "Duptara": "07:40",
            "Gawsia": "07:45"
        },
        "campus_departures": ["16:45"]
    },

    "Route 12": {
        "name": "Araihazar (Bishnandi Ferry Ghat) to GUB",
        "stops": [
            "Bishnandi Ferry Ghat", "Bishnandi Taltola Bazar",
            "Ramchandri", "Kalirhat", "Dokkhinpara Tharibarimor",
            "Ferighat Bypass Road", "Araihazar Chowrasta",
            "Kalibari Bazar", "Duptara", "Gawsia", "GUB Campus"
        ],
        "pickup_times": {
            "Bishnandi Ferry Ghat": "07:15",
            "Bishnandi Taltola Bazar": "07:16",
            "Ramchandri": "07:17",
            "Kalirhat": "07:18",
            "Dokkhinpara Tharibarimor": "07:20",
            "Ferighat Bypass Road": "07:25",
            "Araihazar Chowrasta": "07:27",
            "Kalibari Bazar": "07:30",
            "Duptara": "07:35",
            "Gawsia": "07:40"
        },
        "campus_departures": ["16:45"]
    }
}


DEFAULT_BUSES = {
    "DM BA 13-0861": {
        "capacity": 40,
        "driver": "Rajib",
        "assigned_route": None
    },
    "DM BA 12-1500": {
        "capacity": 40,
        "driver": "Wazkuruni",
        "assigned_route": None
    },
    "DM BA 11-9044": {
        "capacity": 40,
        "driver": "Alam",
        "assigned_route": None
    },
    "DM BA 11-9053": {
        "capacity": 40,
        "driver": "Mahtab",
        "assigned_route": None
    },
    "DM JHA 11-1146": {
        "capacity": 40,
        "driver": "Alamin",
        "assigned_route": None
    },
    "DM BA 15-4884": {
        "capacity": 40,
        "driver": "Kalam",
        "assigned_route": None
    },
    "DM BA 13-1390": {
        "capacity": 40,
        "driver": "Manik",
        "assigned_route": None
    },
    "DM BA 11-0049": {
        "capacity": 40,
        "driver": "Rahim",
        "assigned_route": None
    },
    "DM BA 15-7715": {
        "capacity": 40,
        "driver": "Arif",
        "assigned_route": None
    },
    "DM SA-11-0700": {
        "capacity": 40,
        "driver": "Rasel",
        "assigned_route": None
    },
    "DM BA 15-9418": {
        "capacity": 40,
        "driver": "Hannan",
        "assigned_route": None
    },
    "DM BA 11-7202": {
        "capacity": 40,
        "driver": "Mizan",
        "assigned_route": None
    },
    "DM SA-11-0735": {
        "capacity": 40,
        "driver": "Aminul",
        "assigned_route": None
    },
    "DM BA 11-3868": {
        "capacity": 40,
        "driver": "Rabbi",
        "assigned_route": None
    },
    "DM BA 14-4066": {
        "capacity": 40,
        "driver": "Rakibul",
        "assigned_route": None
    },
    "DM SA 11-0734": {
        "capacity": 40,
        "driver": "Usman",
        "assigned_route": None
    },
    "DM BA 13-0680": {
        "capacity": 40,
        "driver": "Jahangir",
        "assigned_route": None
    },
    "DM SA 11-0737": {
        "capacity": 40,
        "driver": "Masud",
        "assigned_route": None
    },
    "DM BA 13-0563": {
        "capacity": 40,
        "driver": "Mahbub",
        "assigned_route": None
    },
    "DM BA 11-9782": {
        "capacity": 40,
        "driver": "Abul",
        "assigned_route": None
    }
}


DEFAULT_STUDENTS = {
    "221001": {"name": "Ayan", "pickup_stop": "Shewrapara", "assigned_bus": None},
    "221002": {"name": "Borna", "pickup_stop": "Kuril", "assigned_bus": None},
    "221003": {"name": "Cynthia", "pickup_stop": "Kalshi", "assigned_bus": None},
    "221004": {"name": "Dipto", "pickup_stop": "Rampura", "assigned_bus": None},
    "221005": {"name": "Faria", "pickup_stop": "Tarabo", "assigned_bus": None},
    "221006": {"name": "Hira", "pickup_stop": "Gawsia", "assigned_bus": None},
    "221007": {"name": "Jannat", "pickup_stop": "Chashara", "assigned_bus": None},
    "221008": {"name": "Lamia", "pickup_stop": "Dhanmondi 27", "assigned_bus": None}
}


TIME_SLOTS = [
    "06:30", "06:45", "07:00", "07:15",
    "07:30", "07:45", "08:00", "08:15",
    "13:45", "15:15", "16:30", "16:45"
]


# ============================================================
# FILE / DATA HELPERS
# ============================================================

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_json(path, default):
    if not os.path.exists(path):
        save_json(path, default)
        return deepcopy(default)

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def build_default_stops_and_roads(routes):
    stops = set()
    roads = {}

    for route in routes.values():
        route_stops = route["stops"]

        for stop in route_stops:
            stops.add(stop)
            roads.setdefault(stop, [])

        for i in range(len(route_stops) - 1):
            a = route_stops[i]
            b = route_stops[i + 1]

            if b not in roads[a]:
                roads[a].append(b)

            if a not in roads[b]:
                roads[b].append(a)

    return sorted(stops), roads


def initialize_data():
    os.makedirs(DATA_DIR, exist_ok=True)

    default_stops, default_roads = build_default_stops_and_roads(DEFAULT_ROUTES)

    load_json(STOPS_FILE, default_stops)
    load_json(ROADS_FILE, default_roads)
    load_json(ROUTES_FILE, DEFAULT_ROUTES)
    load_json(BUSES_FILE, DEFAULT_BUSES)
    load_json(STUDENTS_FILE, DEFAULT_STUDENTS)
    load_json(SCHEDULE_FILE, {})


def load_all():
    stops = load_json(STOPS_FILE, [])
    roads = load_json(ROADS_FILE, {})
    routes = load_json(ROUTES_FILE, {})
    buses = load_json(BUSES_FILE, {})
    students = load_json(STUDENTS_FILE, {})
    schedule = load_json(SCHEDULE_FILE, {})

    return stops, roads, routes, buses, students, schedule


# ============================================================
# BASIC INPUT HELPERS
# ============================================================

def normalize_lookup(value, options):
    value = value.strip().lower()

    for item in options:
        if item.lower() == value:
            return item

    return None


def pause():
    input("\nPress Enter to continue...")


def print_header(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


# ============================================================
# FEATURE 1 - BUS STOP MANAGEMENT
# ============================================================

def bus_stop_management():
    while True:
        stops, roads, routes, buses, students, schedule = load_all()

        print_header("BUS STOP MANAGEMENT")
        print("1. Add Stop")
        print("2. Update/Rename Stop")
        print("3. Delete Stop")
        print("4. View All Stops")
        print("0. Back")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            name = input("New stop name: ").strip()

            if not name:
                print("Stop name cannot be empty.")
                continue

            if normalize_lookup(name, stops):
                print("Stop already exists.")
                continue

            stops.append(name)
            stops.sort()
            roads[name] = []

            save_json(STOPS_FILE, stops)
            save_json(ROADS_FILE, roads)

            print("Stop added successfully.")

        elif choice == "2":
            old = input("Existing stop name: ").strip()
            old_name = normalize_lookup(old, stops)

            if not old_name:
                print("Stop not found.")
                continue

            new_name = input("New stop name: ").strip()

            if not new_name:
                print("New name cannot be empty.")
                continue

            if normalize_lookup(new_name, stops):
                print("Another stop with that name already exists.")
                continue

            stops[stops.index(old_name)] = new_name

            roads[new_name] = roads.pop(old_name, [])

            for stop in list(roads.keys()):
                roads[stop] = [
                    new_name if x == old_name else x
                    for x in roads[stop]
                ]

            for route in routes.values():
                route["stops"] = [
                    new_name if x == old_name else x
                    for x in route["stops"]
                ]

                if old_name in route.get("pickup_times", {}):
                    route["pickup_times"][new_name] = route["pickup_times"].pop(old_name)

            for student in students.values():
                if student["pickup_stop"] == old_name:
                    student["pickup_stop"] = new_name

            save_json(STOPS_FILE, sorted(stops))
            save_json(ROADS_FILE, roads)
            save_json(ROUTES_FILE, routes)
            save_json(STUDENTS_FILE, students)

            print("Stop updated successfully.")

        elif choice == "3":
            name = input("Stop to delete: ").strip()
            stop_name = normalize_lookup(name, stops)

            if not stop_name:
                print("Stop not found.")
                continue

            confirm = input(
                f"Delete '{stop_name}' from graph and routes? (y/n): "
            ).strip().lower()

            if confirm != "y":
                continue

            stops.remove(stop_name)

            roads.pop(stop_name, None)

            for stop in list(roads.keys()):
                roads[stop] = [x for x in roads[stop] if x != stop_name]

            for route in routes.values():
                route["stops"] = [x for x in route["stops"] if x != stop_name]
                route.get("pickup_times", {}).pop(stop_name, None)

            for student in students.values():
                if student["pickup_stop"] == stop_name:
                    student["pickup_stop"] = None
                    student["assigned_bus"] = None

            save_json(STOPS_FILE, stops)
            save_json(ROADS_FILE, roads)
            save_json(ROUTES_FILE, routes)
            save_json(STUDENTS_FILE, students)

            print("Stop deleted.")

        elif choice == "4":
            print("\nAll Stops:")
            for i, stop in enumerate(sorted(stops), start=1):
                print(f"{i:3}. {stop}")

        elif choice == "0":
            return

        else:
            print("Invalid choice.")


# ============================================================
# FEATURE 2 - ROAD / ROUTE CONNECTION MANAGEMENT
# ============================================================

def road_management():
    while True:
        stops, roads, routes, buses, students, schedule = load_all()

        print_header("ROAD / CONNECTION MANAGEMENT")
        print("1. Add Connection")
        print("2. Delete Connection")
        print("3. View Connections")
        print("0. Back")

        choice = input("\nChoice: ").strip()

        if choice in ["1", "2"]:
            first = input("First stop: ").strip()
            second = input("Second stop: ").strip()

            a = normalize_lookup(first, stops)
            b = normalize_lookup(second, stops)

            if not a or not b:
                print("One or both stops do not exist.")
                continue

            if a == b:
                print("A stop cannot connect to itself.")
                continue

            if choice == "1":
                roads.setdefault(a, [])
                roads.setdefault(b, [])

                if b not in roads[a]:
                    roads[a].append(b)

                if a not in roads[b]:
                    roads[b].append(a)

                save_json(ROADS_FILE, roads)
                print(f"Connection created: {a} <-> {b}")

            else:
                if b in roads.get(a, []):
                    roads[a].remove(b)

                if a in roads.get(b, []):
                    roads[b].remove(a)

                save_json(ROADS_FILE, roads)
                print(f"Connection removed: {a} <-> {b}")

        elif choice == "3":
            print("\nNetwork Connections:")
            for stop in sorted(roads):
                neighbours = ", ".join(sorted(roads[stop])) or "None"
                print(f"{stop:30} -> {neighbours}")

        elif choice == "0":
            return

        else:
            print("Invalid choice.")


# ============================================================
# FEATURE 3 - BFS ROUTE FINDER
# ============================================================

def bfs_shortest_path(graph, start, goal, blocked_stops=None, blocked_edges=None):
    blocked_stops = blocked_stops or set()
    blocked_edges = blocked_edges or set()

    if start in blocked_stops or goal in blocked_stops:
        return None, 0

    queue = deque([(start, [start])])
    visited = {start}
    explored = 0

    while queue:
        node, path = queue.popleft()
        explored += 1

        if node == goal:
            return path, explored

        for neighbour in sorted(graph.get(node, [])):
            edge = tuple(sorted((node, neighbour)))

            if neighbour in blocked_stops:
                continue

            if edge in blocked_edges:
                continue

            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, path + [neighbour]))

    return None, explored


def bfs_route_finder():
    stops, roads, routes, buses, students, schedule = load_all()

    print_header("BFS SHORTEST ROUTE FINDER")

    start_input = input("Start location: ").strip()
    goal_input = input("Destination: ").strip()

    start = normalize_lookup(start_input, stops)
    goal = normalize_lookup(goal_input, stops)

    if not start or not goal:
        print("Invalid start or destination.")
        return

    path, explored = bfs_shortest_path(roads, start, goal)

    if not path:
        print("No route found.")
        return

    print("\nShortest route:")
    print(" -> ".join(path))
    print("Number of stop links:", len(path) - 1)
    print("Explored nodes:", explored)


# ============================================================
# FEATURE 4 - DFS NETWORK EXPLORER
# ============================================================

def dfs_order(graph, start):
    visited = set()
    stack = [start]
    order = []

    while stack:
        node = stack.pop()

        if node in visited:
            continue

        visited.add(node)
        order.append(node)

        for neighbour in sorted(graph.get(node, []), reverse=True):
            if neighbour not in visited:
                stack.append(neighbour)

    return order


def dfs_network_explorer():
    stops, roads, routes, buses, students, schedule = load_all()

    print_header("DFS NETWORK EXPLORER")

    start_input = input("Start stop: ").strip()
    start = normalize_lookup(start_input, stops)

    if not start:
        print("Stop not found.")
        return

    order = dfs_order(roads, start)

    print("\nDFS exploration:")
    print(" -> ".join(order))
    print("\nReachable stops:", len(order))


# ============================================================
# FEATURE 5 - ROUTE CONFLICT DETECTION
# ============================================================

def detect_route_conflicts(routes):
    conflicts = {}
    route_names = list(routes.keys())

    for route_name in route_names:
        conflicts[route_name] = {}

    for i in range(len(route_names)):
        for j in range(i + 1, len(route_names)):
            a = route_names[i]
            b = route_names[j]

            shared_stops = set(routes[a]["stops"]) & set(routes[b]["stops"])
            shared_stops.discard("GUB Campus")

            same_departure = (
                set(routes[a].get("campus_departures", []))
                & set(routes[b].get("campus_departures", []))
            )

            # Route conflict if they share a non-campus stop.
            if shared_stops:
                details = {
                    "shared_stops": sorted(shared_stops),
                    "same_departure": sorted(same_departure)
                }

                conflicts[a][b] = details
                conflicts[b][a] = details

    return conflicts


def route_conflict_detection():
    _, _, routes, _, _, _ = load_all()

    print_header("ROUTE CONFLICT DETECTION")

    conflicts = detect_route_conflicts(routes)

    any_conflict = False

    for route in sorted(conflicts):
        if conflicts[route]:
            any_conflict = True
            print(f"\n{route} conflicts with:")

            for other, detail in sorted(conflicts[route].items()):
                print(
                    f"  - {other} | Shared stops: "
                    f"{', '.join(detail['shared_stops'])}"
                )

    if not any_conflict:
        print("No route conflicts detected.")


# ============================================================
# FEATURE 6 - GRAPH COLORING TIME-SLOT ASSIGNMENT
# ============================================================

def build_conflict_graph(routes):
    details = detect_route_conflicts(routes)

    graph = {route: set() for route in routes}

    for route in details:
        for other in details[route]:
            graph[route].add(other)

    return graph


def is_color_safe(node, color, coloring, graph):
    for neighbour in graph[node]:
        if coloring.get(neighbour) == color:
            return False
    return True


def color_graph(graph, colors):
    nodes = sorted(
        graph,
        key=lambda node: len(graph[node]),
        reverse=True
    )

    coloring = {}

    def backtrack(index):
        if index == len(nodes):
            return True

        node = nodes[index]

        for color in colors:
            if is_color_safe(node, color, coloring, graph):
                coloring[node] = color

                if backtrack(index + 1):
                    return True

                del coloring[node]

        return False

    if backtrack(0):
        return coloring

    return None


def automatic_time_slot_assignment():
    _, _, routes, _, _, _ = load_all()

    print_header("AUTOMATIC TIME-SLOT ASSIGNMENT - GRAPH COLORING")

    graph = build_conflict_graph(routes)

    coloring = color_graph(graph, TIME_SLOTS)

    if coloring is None:
        print("Not enough time slots to color the route conflict graph.")
        return None

    print("\nAssigned time slots:")

    for route in sorted(coloring):
        print(f"{route:12} -> {coloring[route]}")

    return coloring


# ============================================================
# FEATURE 7 - BUS ASSIGNMENT USING CSP
# ============================================================

def route_student_demand(routes, students):
    demand = {route: 0 for route in routes}

    for student in students.values():
        pickup = student.get("pickup_stop")

        if not pickup:
            continue

        possible_routes = [
            route for route, info in routes.items()
            if pickup in info["stops"]
        ]

        if possible_routes:
            # Count demand against the student's first possible route
            # only for demand estimation.
            demand[possible_routes[0]] += 1

    return demand


def assign_buses_csp(routes, buses, students, time_slots=None):
    demand = route_student_demand(routes, students)

    route_names = list(routes.keys())

    # Most difficult routes first: higher demand first.
    route_names.sort(key=lambda r: demand[r], reverse=True)

    assignment = {}
    used_buses_by_slot = {}

    def backtrack(index):
        if index == len(route_names):
            return True

        route = route_names[index]
        required_capacity = demand[route]

        candidates = sorted(
            buses.keys(),
            key=lambda bus: buses[bus]["capacity"]
        )

        for bus in candidates:
            if buses[bus]["capacity"] < required_capacity:
                continue

            slot = time_slots.get(route) if time_slots else None

            if slot is not None:
                already_used = used_buses_by_slot.setdefault(slot, set())

                if bus in already_used:
                    continue

            assignment[route] = bus

            if slot is not None:
                used_buses_by_slot[slot].add(bus)

            if backtrack(index + 1):
                return True

            if slot is not None:
                used_buses_by_slot[slot].remove(bus)

            del assignment[route]

        return False

    success = backtrack(0)

    if success:
        return assignment, demand

    return None, demand


def bus_assignment():
    _, _, routes, buses, students, _ = load_all()

    print_header("BUS ASSIGNMENT - CSP")

    conflict_graph = build_conflict_graph(routes)
    time_slots = color_graph(conflict_graph, TIME_SLOTS)


    assignment, demand = assign_buses_csp(
        routes,
        buses,
        students,
        time_slots
    )

    if assignment is None:
        print("No valid bus assignment found.")
        return

    for route in sorted(assignment):
        bus = assignment[route]

        print(
            f"{route:12} -> {bus:15} | "
            f"Capacity: {buses[bus]['capacity']:3} | "
            f"Estimated demand: {demand[route]}"
        )

    for bus in buses:
        buses[bus]["assigned_route"] = None

    for route, bus in assignment.items():
        buses[bus]["assigned_route"] = route

    save_json(BUSES_FILE, buses)

    print("\nBus assignments saved.")


# ============================================================
# FEATURE 8 - CAPACITY MANAGEMENT / STUDENT ASSIGNMENT
# ============================================================

def student_route_domains(routes, students):
    domains = {}

    for student_id, student in students.items():
        pickup = student.get("pickup_stop")

        domains[student_id] = []

        if not pickup:
            continue

        for route, info in routes.items():
            if pickup in info["stops"]:
                domains[student_id].append(route)

    return domains


def assign_students_to_buses_csp(routes, buses, students):
    domains = student_route_domains(routes, students)

    route_to_bus = {}

    for bus_no, bus in buses.items():
        route = bus.get("assigned_route")

        if route:
            route_to_bus[route] = bus_no

    student_ids = sorted(
        students.keys(),
        key=lambda sid: len(domains.get(sid, []))
    )

    remaining_capacity = {
        bus_no: buses[bus_no]["capacity"]
        for bus_no in buses
    }

    assignment = {}

    def backtrack(index):
        if index == len(student_ids):
            return True

        sid = student_ids[index]

        for route in domains.get(sid, []):
            bus = route_to_bus.get(route)

            if not bus:
                continue

            if remaining_capacity[bus] <= 0:
                continue

            assignment[sid] = bus
            remaining_capacity[bus] -= 1

            if backtrack(index + 1):
                return True

            remaining_capacity[bus] += 1
            del assignment[sid]

        return False

    success = backtrack(0)

    if success:
        return assignment, domains

    return None, domains


def capacity_management():
    _, _, routes, buses, students, _ = load_all()

    print_header("CAPACITY MANAGEMENT - CSP")

    assignment, domains = assign_students_to_buses_csp(
        routes,
        buses,
        students
    )

    if assignment is None:
        print("No valid student-to-bus assignment found.")
        print("Make sure buses are assigned to routes first.")
        return

    load_count = {bus: 0 for bus in buses}

    for sid, bus in assignment.items():
        students[sid]["assigned_bus"] = bus
        load_count[bus] += 1

    save_json(STUDENTS_FILE, students)

    for sid in sorted(assignment):
        student = students[sid]
        print(
            f"{sid} | {student['name']:15} | "
            f"{student['pickup_stop']:22} -> {assignment[sid]}"
        )

    print("\nCapacity usage:")

    for bus in sorted(buses):
        if load_count[bus] > 0:
            print(
                f"{bus:15}: "
                f"{load_count[bus]}/{buses[bus]['capacity']}"
            )


# ============================================================
# FEATURE 9 - SCHEDULE GENERATION
# ============================================================

def generate_schedule_data(routes, buses, students):
    conflict_graph = build_conflict_graph(routes)
    time_slots = color_graph(conflict_graph, TIME_SLOTS)

    if time_slots is None:
        return None, "Time-slot assignment failed."

    bus_assignment_data, demand = assign_buses_csp(
        routes,
        buses,
        students,
        time_slots
    )

    if bus_assignment_data is None:
        return None, "Bus assignment failed."

    schedule = {}

    for route in routes:
        bus = bus_assignment_data[route]

        schedule[route] = {
            "route_name": routes[route]["name"],
            "time_slot": time_slots[route],
            "bus": bus,
            "driver": buses[bus]["driver"],
            "capacity": buses[bus]["capacity"],
            "estimated_demand": demand[route]
        }

    return schedule, None


def schedule_generation():
    _, _, routes, buses, students, _ = load_all()

    print_header("FULL DAILY SCHEDULE GENERATION - CSP + COLORING")

    schedule, error = generate_schedule_data(
        routes,
        buses,
        students
    )

    if error:
        print(error)
        return

    save_json(SCHEDULE_FILE, schedule)

    print(
        f"{'Route':12} {'Time':8} {'Bus':16} "
        f"{'Driver':14} {'Demand/Cap':12}"
    )
    print("-" * 70)

    for route in sorted(schedule):
        item = schedule[route]

        print(
            f"{route:12} {item['time_slot']:8} "
            f"{item['bus']:16} {item['driver']:14} "
            f"{item['estimated_demand']}/{item['capacity']}"
        )

    print("\nSchedule saved.")


# ============================================================
# FEATURE 10 - CONFLICT CHECKING
# ============================================================

def conflict_checking():
    _, _, _, _, _, schedule = load_all()

    print_header("SCHEDULE CONFLICT CHECKING")

    if not schedule:
        print("No saved schedule. Generate a schedule first.")
        return

    conflicts = []

    route_names = list(schedule.keys())

    for i in range(len(route_names)):
        for j in range(i + 1, len(route_names)):
            a = route_names[i]
            b = route_names[j]

            same_bus = schedule[a]["bus"] == schedule[b]["bus"]
            same_time = schedule[a]["time_slot"] == schedule[b]["time_slot"]

            if same_bus and same_time:
                conflicts.append((a, b, schedule[a]["bus"], schedule[a]["time_slot"]))

    if conflicts:
        print("Conflicts found:")

        for a, b, bus, time in conflicts:
            print(
                f"{a} and {b} use {bus} at the same time {time}"
            )

    else:
        print("PASS: No bus is assigned to two routes at the same time.")


# ============================================================
# FEATURE 11 - ALTERNATIVE ROUTE
# ============================================================

def alternative_route():
    stops, roads, _, _, _, _ = load_all()

    print_header("ALTERNATIVE ROUTE FINDER - BFS")

    start_input = input("Start stop: ").strip()
    goal_input = input("Destination: ").strip()

    start = normalize_lookup(start_input, stops)
    goal = normalize_lookup(goal_input, stops)

    if not start or not goal:
        print("Invalid start or destination.")
        return

    print("\n1. Block a stop")
    print("2. Block a road/connection")
    print("3. No blockage")

    choice = input("Choice: ").strip()

    blocked_stops = set()
    blocked_edges = set()

    if choice == "1":
        blocked_input = input("Unavailable stop: ").strip()
        blocked = normalize_lookup(blocked_input, stops)

        if not blocked:
            print("Stop not found.")
            return

        blocked_stops.add(blocked)

    elif choice == "2":
        a_input = input("Road first stop: ").strip()
        b_input = input("Road second stop: ").strip()

        a = normalize_lookup(a_input, stops)
        b = normalize_lookup(b_input, stops)

        if not a or not b:
            print("Invalid road stops.")
            return

        blocked_edges.add(tuple(sorted((a, b))))

    path, explored = bfs_shortest_path(
        roads,
        start,
        goal,
        blocked_stops=blocked_stops,
        blocked_edges=blocked_edges
    )

    if path:
        print("\nAlternative route:")
        print(" -> ".join(path))
        print("Stop links:", len(path) - 1)
        print("Explored nodes:", explored)
    else:
        print("No alternative route exists.")


# ============================================================
# FEATURE 12 - ROUTE VISUALIZATION (CONSOLE)
# ============================================================

def route_visualization():
    _, roads, _, _, _, _ = load_all()

    print_header("BUS NETWORK VISUALIZATION - CONSOLE GRAPH")

    for stop in sorted(roads):
        neighbours = sorted(roads[stop])

        if neighbours:
            print(f"[{stop}]")
            for neighbour in neighbours:
                print(f"   |-- {neighbour}")
        else:
            print(f"[{stop}] -> No connection")


# ============================================================
# FEATURE 13 - SEARCH BUS STOP
# ============================================================

def search_bus_stop():
    stops, roads, routes, _, _, _ = load_all()

    print_header("SEARCH BUS STOP")

    query = input("Stop name: ").strip().lower()

    matches = [
        stop for stop in stops
        if query in stop.lower()
    ]

    if not matches:
        print("No matching stop found.")
        return

    for stop in matches:
        print(f"\nStop: {stop}")
        print(
            "Connected stops:",
            ", ".join(sorted(roads.get(stop, []))) or "None"
        )

        serving_routes = [
            route for route, info in routes.items()
            if stop in info["stops"]
        ]

        print(
            "Serving routes:",
            ", ".join(serving_routes) or "None"
        )


# ============================================================
# FEATURE 14 - BUS INFORMATION MANAGEMENT
# ============================================================

def bus_information():
    while True:
        _, _, _, buses, _, _ = load_all()

        print_header("BUS INFORMATION")
        print("1. View All Buses")
        print("2. Add Bus")
        print("3. Update Bus")
        print("4. Delete Bus")
        print("0. Back")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            for bus_no in sorted(buses):
                bus = buses[bus_no]

                print(
                    f"{bus_no:16} | "
                    f"Capacity: {bus['capacity']:3} | "
                    f"Driver: {bus['driver']:15} | "
                    f"Route: {bus.get('assigned_route')}"
                )

        elif choice == "2":
            bus_no = input("Bus number: ").strip()

            if not bus_no:
                print("Bus number required.")
                continue

            if bus_no in buses:
                print("Bus already exists.")
                continue

            driver = input("Driver name: ").strip()

            try:
                capacity = int(input("Seat capacity: "))
            except ValueError:
                print("Invalid capacity.")
                continue

            buses[bus_no] = {
                "capacity": capacity,
                "driver": driver,
                "assigned_route": None
            }

            save_json(BUSES_FILE, buses)
            print("Bus added.")

        elif choice == "3":
            bus_no = input("Bus number to update: ").strip()

            if bus_no not in buses:
                print("Bus not found.")
                continue

            driver = input(
                f"Driver [{buses[bus_no]['driver']}]: "
            ).strip()

            capacity_text = input(
                f"Capacity [{buses[bus_no]['capacity']}]: "
            ).strip()

            if driver:
                buses[bus_no]["driver"] = driver

            if capacity_text:
                try:
                    buses[bus_no]["capacity"] = int(capacity_text)
                except ValueError:
                    print("Invalid capacity.")
                    continue

            save_json(BUSES_FILE, buses)
            print("Bus updated.")

        elif choice == "4":
            bus_no = input("Bus number to delete: ").strip()

            if bus_no not in buses:
                print("Bus not found.")
                continue

            del buses[bus_no]
            save_json(BUSES_FILE, buses)
            print("Bus deleted.")

        elif choice == "0":
            return

        else:
            print("Invalid choice.")


# ============================================================
# FEATURE 15 - STUDENT / PASSENGER INFORMATION
# ============================================================

def student_information():
    while True:
        stops, _, _, _, students, _ = load_all()

        print_header("STUDENT / PASSENGER INFORMATION")
        print("1. View Students")
        print("2. Add Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("0. Back")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            for sid in sorted(students):
                student = students[sid]

                print(
                    f"{sid:10} | "
                    f"{student['name']:18} | "
                    f"Pickup: {str(student['pickup_stop']):24} | "
                    f"Bus: {student.get('assigned_bus')}"
                )

        elif choice == "2":
            sid = input("Student ID: ").strip()

            if sid in students:
                print("Student ID already exists.")
                continue

            name = input("Student name: ").strip()
            pickup_input = input("Pickup stop: ").strip()
            pickup = normalize_lookup(pickup_input, stops)

            if not pickup:
                print("Pickup stop not found.")
                continue

            students[sid] = {
                "name": name,
                "pickup_stop": pickup,
                "assigned_bus": None
            }

            save_json(STUDENTS_FILE, students)
            print("Student added.")

        elif choice == "3":
            sid = input("Student ID: ").strip()

            if sid not in students:
                print("Student not found.")
                continue

            name = input(
                f"Name [{students[sid]['name']}]: "
            ).strip()

            pickup_input = input(
                f"Pickup [{students[sid]['pickup_stop']}]: "
            ).strip()

            if name:
                students[sid]["name"] = name

            if pickup_input:
                pickup = normalize_lookup(pickup_input, stops)

                if not pickup:
                    print("Pickup stop not found.")
                    continue

                students[sid]["pickup_stop"] = pickup
                students[sid]["assigned_bus"] = None

            save_json(STUDENTS_FILE, students)
            print("Student updated.")

        elif choice == "4":
            sid = input("Student ID: ").strip()

            if sid not in students:
                print("Student not found.")
                continue

            del students[sid]
            save_json(STUDENTS_FILE, students)
            print("Student deleted.")

        elif choice == "0":
            return

        else:
            print("Invalid choice.")


# ============================================================
# FEATURE 16 - DAILY TIMETABLE
# ============================================================

def daily_timetable():
    _, _, _, _, _, schedule = load_all()

    print_header("DAILY UNIVERSITY BUS TIMETABLE")

    if not schedule:
        print("No schedule generated yet.")
        return

    sorted_items = sorted(
        schedule.items(),
        key=lambda item: item[1]["time_slot"]
    )

    print(
        f"{'Time':8} {'Route':12} {'Bus':16} "
        f"{'Driver':14} {'Demand/Capacity':16}"
    )
    print("-" * 78)

    for route, item in sorted_items:
        print(
            f"{item['time_slot']:8} "
            f"{route:12} "
            f"{item['bus']:16} "
            f"{item['driver']:14} "
            f"{item['estimated_demand']}/{item['capacity']}"
        )


# ============================================================
# EXTRA: ROUTE DATA VIEW
# ============================================================

def view_routes():
    _, _, routes, _, _, _ = load_all()

    print_header("UNIVERSITY ROUTES")

    for route in sorted(routes):
        info = routes[route]

        print(f"\n{route}: {info['name']}")
        print("Stops:")
        print(" -> ".join(info["stops"]))


# ============================================================
# MAIN MENU
# ============================================================

def main():
    initialize_data()

    while True:
        print("\n")
        print("=" * 80)
        print(" AI-BASED UNIVERSITY BUS MANAGEMENT SYSTEM - GUB")
        print("=" * 80)

        print("""
 1. Bus Stop Management
 2. Road / Connection Management
 3. BFS Route Finder
 4. DFS Network Explorer
 5. Route Conflict Detection
 6. Automatic Time-slot Assignment
 7. Bus Assignment
 8. Capacity Management / Student Assignment
 9. Schedule Generation
10. Conflict Checking
11. Alternative Route
12. Route Visualization
13. Search Bus Stop
14. Bus Information
15. Student / Passenger Information
16. Daily Timetable
17. View University Routes
 0. Exit
""")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            bus_stop_management()

        elif choice == "2":
            road_management()

        elif choice == "3":
            bfs_route_finder()
            pause()

        elif choice == "4":
            dfs_network_explorer()
            pause()

        elif choice == "5":
            route_conflict_detection()
            pause()

        elif choice == "6":
            automatic_time_slot_assignment()
            pause()

        elif choice == "7":
            bus_assignment()
            pause()

        elif choice == "8":
            capacity_management()
            pause()

        elif choice == "9":
            schedule_generation()
            pause()

        elif choice == "10":
            conflict_checking()
            pause()

        elif choice == "11":
            alternative_route()
            pause()

        elif choice == "12":
            route_visualization()
            pause()

        elif choice == "13":
            search_bus_stop()
            pause()

        elif choice == "14":
            bus_information()

        elif choice == "15":
            student_information()

        elif choice == "16":
            daily_timetable()
            pause()

        elif choice == "17":
            view_routes()
            pause()

        elif choice == "0":
            print("\nProgram closed.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
