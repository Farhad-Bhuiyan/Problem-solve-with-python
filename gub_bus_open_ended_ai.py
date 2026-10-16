"""
GUB University Bus Route & Student Assignment
Open-Ended AI Lab Project (Console Only / No GUI)

AI techniques:
1. BFS  -> shortest number of scheduled stop-to-stop links
2. DFS  -> explore all reachable stops
3. CSP  -> assign students to suitable university bus routes
4. Graph Coloring -> create conflict-free dispatch groups for overlapping routes

Important:
- Route names, stop order, pickup times, and campus departure times are based on
  the provided Green University of Bangladesh Saturday-Wednesday bus schedule.
- Some spelling variants are normalized so that shared stops match correctly
  (for example Kachpur/Kanchpur -> Kachpur).
- The PDF does NOT state total student capacity for each vehicle. Therefore
  DEMO_ROUTE_CAPACITY below is a LAB-SIMULATION constraint, not an official
  GUB bus capacity.
- BFS minimizes the NUMBER OF SCHEDULED STOP LINKS, not real road distance,
  because distance/traffic data are not available in the supplied schedule.
"""

from collections import deque
from datetime import datetime

CAMPUS = "GUB Campus"

# ---------------------------------------------------------------------------
# REAL ROUTE DATA (normalized from the supplied Saturday-Wednesday schedule)
# Each stop item is: (area / normalized stop name, first listed pickup time)
# ---------------------------------------------------------------------------

ROUTES = {
    "Route 01": {
        "title": "Shewrapara to GUB via Mirpur 12",
        "stops": [
            ("Shewrapara", "07:00"),
            ("Mirpur-10", "07:05"),
            ("Mirpur-12", "07:10"),
            ("Kalshi", "07:15"),
            ("ECB Chattor", "07:17"),
            ("Kuril", "07:30"),
            (CAMPUS, None),
        ],
        "campus_departures": ["13:45", "16:45"],
    },

    "Route 02": {
        "title": "Shewrapara to GUB via Mohakhali",
        "stops": [
            ("Shewrapara", "07:15"),
            ("Agargaon", "07:20"),
            ("Mohakhali", "07:35"),
            ("Banani", "07:45"),
            ("MES", "07:50"),
            ("Kuril", "07:55"),
            (CAMPUS, None),
        ],
        "campus_departures": ["16:45"],
    },

    "Route 03_1": {
        "title": "Shyamoli to GUB via Majar Road",
        "stops": [
            ("Shyamoli", "07:00"),
            ("Technical Mor", "07:05"),
            ("Gabtoli", "07:10"),
            ("Majar Road", "07:15"),
            ("Mirpur 1", "07:20"),
            ("Mirpur 2", "07:25"),
            ("Mirpur 11", "07:30"),
            ("Kalshi", "07:45"),
            ("Kuril", "07:55"),
            (CAMPUS, None),
        ],
        "campus_departures": ["16:45"],
    },

    "Route 03_2": {
        "title": "Shyamoli to GUB via Technical Mor",
        "stops": [
            ("Shyamoli", "07:10"),
            ("Technical Mor", "07:15"),
            ("Mirpur 1", "07:25"),
            ("Mirpur 2", "07:30"),
            ("Mirpur 11", "07:35"),
            ("Kalshi", "07:45"),
            ("Kuril", "07:55"),
            (CAMPUS, None),
        ],
        "campus_departures": ["16:45"],
    },

    "Route 04_1": {
        "title": "Azimpur to GUB via Dhanmondi 27-Farmgate",
        "stops": [
            ("Azimpur", "07:00"),
            ("New Market", "07:05"),
            ("City College", "07:07"),
            ("Dhanmondi 27", "07:10"),
            ("Khamar Bari", "07:15"),
            ("Farmgate", "07:20"),
            ("Mohakhali", "07:25"),
            ("Banani", "07:30"),
            ("Kuril", "07:35"),
            (CAMPUS, None),
        ],
        "campus_departures": ["16:45"],
    },

    "Route 05_1": {
        "title": "Motijheel to GUB via Malibagh",
        "stops": [
            ("Motijheel", "07:00"),
            ("Komlapur", "07:05"),
            ("Basabo", "07:10"),
            ("Khilgaon", "07:12"),
            ("Malibag", "07:18"),
            ("Abul Hotel", "07:22"),
            ("Rampura", "07:27"),
            ("Badda", "07:35"),
            ("Natun Bazar", "07:40"),
            ("Kuril", "07:50"),
            (CAMPUS, None),
        ],
        "campus_departures": ["13:45", "16:45"],
    },

    "Route 05_2": {
        "title": "Malibagh to GUB via Rampura",
        "stops": [
            ("Malibag", "07:10"),
            ("Abul Hotel", "07:15"),
            ("Rampura", "07:20"),
            ("Badda", "07:30"),
            ("Natun Bazar", "07:35"),
            ("Kuril", "07:45"),
            (CAMPUS, None),
        ],
        "campus_departures": ["16:45"],
    },

    "Route 06_1": {
        "title": "Gulistan to GUB via Staff Quarter",
        "stops": [
            ("Gulistan", "06:45"),
            ("Tikatuli", "06:55"),
            ("Doyaganj", "06:57"),
            ("Jonopath Mor", "06:59"),
            ("Jatrabari", "07:00"),
            ("Vangga Press", "07:02"),
            ("Mridhabari", "07:03"),
            ("Konapara", "07:10"),
            ("Staff Quarter", "07:12"),
            ("Tarabo", "07:15"),
            ("Rupshi", "07:20"),
            ("Bhulta", "07:35"),
            (CAMPUS, None),
        ],
        "campus_departures": ["16:45"],
    },

    "Route 06_2": {
        "title": "Jatrabari to GUB via Staff Quarter",
        "stops": [
            ("Jatrabari", "07:05"),
            ("Vangga Press", "07:07"),
            ("Mridhabari", "07:10"),
            ("Konapara", "07:15"),
            ("Staff Quarter", "07:20"),
            ("Tarabo", "07:25"),
            ("Rupshi", "07:30"),
            ("Bhulta", "07:40"),
            (CAMPUS, None),
        ],
        "campus_departures": ["16:45"],
    },

    "Route 07": {
        "title": "Shonir Akhra to GUB via Kanchpur",
        "stops": [
            ("Shonir Akhra", "06:50"),
            ("Rayerbagh", "06:52"),
            ("Matuail", "06:55"),
            ("Sign Board", "07:00"),
            ("CTG Road", "07:10"),
            ("Kachpur", "07:15"),
            ("Tarabo", "07:20"),
            ("Rupshi", "07:25"),
            ("Bhulta", "07:50"),
            (CAMPUS, None),
        ],
        "campus_departures": ["13:45", "16:45"],
    },

    "Route 08_1": {
        "title": "Chashara to GUB via CTG Road",
        "stops": [
            ("Chashara", "06:35"),
            ("Nobiganj", "06:40"),
            ("Chowdhuri Bari", "06:45"),
            ("Adomjhee EPZ", "06:55"),
            ("CTG Road", "07:05"),
            ("Kachpur", "07:10"),
            ("Tarabo", "07:20"),
            ("Rupshi", "07:25"),
            ("Murapara", "07:30"),
            (CAMPUS, None),
        ],
        "campus_departures": ["16:45"],
    },

    "Route 08_2": {
        "title": "Chashara to GUB via Sign Board",
        "stops": [
            ("Chashara", "06:45"),
            ("Shibu Market", "06:50"),
            ("Jalkuri", "06:55"),
            ("Bhuighar", "06:57"),
            ("Mamudpar", "07:00"),
            ("Sign Board", "07:10"),
            ("Shanarpar", "07:15"),
            ("CTG Road", "07:20"),
            ("Kachpur", "07:25"),
            ("Tarabo", "07:35"),
            ("Rupshi", "07:40"),
            ("Murapara", "07:50"),
            (CAMPUS, None),
        ],
        "campus_departures": ["13:45", "16:45"],
    },

    "Route 09_1": {
        "title": "Narsingdi (Velanagar) to GUB via Bhulta",
        "stops": [
            ("Narsingdi Velanagar", "07:00"),
            ("Shahe Protap", "07:10"),
            ("Panchdona", "07:20"),
            ("Madhopdi", "07:30"),
            ("Bhulta", "07:45"),
            (CAMPUS, None),
        ],
        "campus_departures": ["13:45", "16:45"],
    },

    "Route 09_2": {
        "title": "Narsingdi (Ghorashal) to GUB via Bhulta",
        "stops": [
            ("Ghorashal", "07:00"),
            ("Panchdona", "07:10"),
            ("Madhopdi", "07:20"),
            ("Bhulta", "07:35"),
            (CAMPUS, None),
        ],
        "campus_departures": ["16:45"],
    },

    "Route 10_1": {
        "title": "Bypass (Gazipur) to GUB via Abdullahpur",
        "stops": [
            ("Gazipur Bypass", "06:45"),
            ("Abdullahpur", "07:00"),
            ("Azompur", "07:05"),
            ("Rajlakshmi", "07:10"),
            ("Airport", "07:15"),
            ("Khilkhet", "07:18"),
            ("Kuril", "07:22"),
            (CAMPUS, None),
        ],
        "campus_departures": ["16:45"],
    },

    "Route 10_2": {
        "title": "Chowrasta (Gazipur) to GUB via Mirer Bazar",
        "stops": [
            ("Gazipur Chowrasta", "06:45"),
            ("Gazipur Bypass", "06:47"),
            ("Meghdubi", "06:55"),
            ("Mirer Bazar", "07:00"),
            ("Ulukhola", "07:05"),
            ("Zinda Park", "07:10"),
            ("Kanchon", "07:20"),
            (CAMPUS, None),
        ],
        "campus_departures": ["16:45"],
    },

    "Route 11": {
        "title": "Sonargaon to GUB via Madanpur-Noyapur",
        "stops": [
            ("Mograpara", "07:00"),
            ("Langalbond", "07:05"),
            ("Madanpur", "07:10"),
            ("Noyapur", "07:15"),
            ("Bostail", "07:30"),
            ("Gawsia", "07:40"),
            (CAMPUS, None),
        ],
        "campus_departures": ["16:45"],
    },

    "Route 11_12": {
        "title": "Sonargaon Baradi to GUB via Poraporde-Araihazar",
        "stops": [
            ("Sonargaon-Baradi", "07:00"),
            ("Ladhurchor", "07:10"),
            ("Mahazampur", "07:12"),
            ("Taltola", "07:20"),
            ("Eidbardi", "07:25"),
            ("Araihazar Chowrasta", "07:30"),
            ("Kalibari Bazar", "07:35"),
            ("Duptara", "07:40"),
            ("Gawsia", "07:45"),
            (CAMPUS, None),
        ],
        "campus_departures": ["16:45"],
    },

    "Route 12": {
        "title": "Araihazar (Bishnandi Ferry Ghat) to GUB",
        "stops": [
            ("Bishnandi Ferry Ghat", "07:15"),
            ("Bishnandi Taltola Bazar", "07:16"),
            ("Ramchandri", "07:17"),
            ("Kalirhat", "07:18"),
            ("Dokkhinpara Tharibarimor", "07:20"),
            ("Ferighat Bypass Road", "07:25"),
            ("Araihazar Chowrasta", "07:27"),
            ("Kalibari Bazar", "07:30"),
            ("Duptara", "07:35"),
            ("Gawsia", "07:40"),
            (CAMPUS, None),
        ],
        "campus_departures": ["16:45"],
    },
}


# ---------------------------------------------------------------------------
# LAB-SIMULATION CAPACITY (NOT AN OFFICIAL GUB CAPACITY)
# ---------------------------------------------------------------------------

DEMO_ROUTE_CAPACITY = 2


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def time_to_minutes(time_text):
    """Convert HH:MM 24-hour time text to minutes after midnight."""
    if time_text is None:
        return None
    hour, minute = map(int, time_text.split(":"))
    return hour * 60 + minute


def route_stop_names(route_name):
    return [stop for stop, _ in ROUTES[route_name]["stops"]]


def pickup_time(route_name, stop_name):
    for stop, time_text in ROUTES[route_name]["stops"]:
        if stop == stop_name:
            return time_text
    return None


def all_stop_names():
    result = set()
    for route_name in ROUTES:
        result.update(route_stop_names(route_name))
    return result


# ---------------------------------------------------------------------------
# GRAPH CONSTRUCTION
# ---------------------------------------------------------------------------

def build_transport_graph():
    """
    Build an UNDIRECTED graph from consecutive scheduled stops.

    The official schedule states the services operate vice versa from campus,
    so using an undirected connectivity graph is reasonable for this lab model.
    """
    graph = {stop: set() for stop in all_stop_names()}

    for route_name in ROUTES:
        stops = route_stop_names(route_name)

        for i in range(len(stops) - 1):
            a = stops[i]
            b = stops[i + 1]

            graph[a].add(b)
            graph[b].add(a)

    return graph


TRANSPORT_GRAPH = build_transport_graph()


# ---------------------------------------------------------------------------
# 1. BFS - SHORTEST NUMBER OF SCHEDULED STOP LINKS
# ---------------------------------------------------------------------------

def bfs_shortest_path(start, goal):
    """
    Return:
        path           -> shortest path by number of graph edges
        explored_count -> number of nodes removed/processed from the queue
    """
    if start not in TRANSPORT_GRAPH or goal not in TRANSPORT_GRAPH:
        return None, 0

    queue = deque([(start, [start])])
    visited = {start}
    explored_count = 0

    while queue:
        node, path = queue.popleft()
        explored_count += 1

        if node == goal:
            return path, explored_count

        for neighbour in sorted(TRANSPORT_GRAPH[node]):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, path + [neighbour]))

    return None, explored_count


# ---------------------------------------------------------------------------
# 2. DFS - EXPLORE REACHABLE STOPS
# ---------------------------------------------------------------------------

def dfs_explore(start):
    """
    Iterative DFS.
    Returns the order in which reachable stops are explored.
    """
    if start not in TRANSPORT_GRAPH:
        return []

    visited = set()
    order = []
    stack = [start]

    while stack:
        node = stack.pop()

        if node in visited:
            continue

        visited.add(node)
        order.append(node)

        # Reverse-sorted so alphabetically smaller items are visited first.
        for neighbour in sorted(TRANSPORT_GRAPH[node], reverse=True):
            if neighbour not in visited:
                stack.append(neighbour)

    return order


# ---------------------------------------------------------------------------
# ROUTE LOOKUP
# ---------------------------------------------------------------------------

def routes_serving_stop(stop_name, latest_pickup=None):
    """
    Return possible routes serving a student's pickup point.
    If latest_pickup is supplied, only routes arriving at/before that time remain.
    """
    possible = []
    latest_minutes = time_to_minutes(latest_pickup) if latest_pickup else None

    for route_name in ROUTES:
        t = pickup_time(route_name, stop_name)

        if t is None:
            continue

        if latest_minutes is None or time_to_minutes(t) <= latest_minutes:
            possible.append(route_name)

    return possible


# ---------------------------------------------------------------------------
# 3. CSP - STUDENT -> ROUTE ASSIGNMENT
# ---------------------------------------------------------------------------

def build_student_domains(students):
    """
    CSP:
      Variables    = students
      Domain       = routes serving the student's pickup stop
      Constraints:
        1) route must serve pickup stop
        2) pickup time must be <= student's latest acceptable pickup time
        3) lab-simulation capacity must not be exceeded
    """
    domains = {}

    for student in students:
        domains[student["name"]] = routes_serving_stop(
            student["pickup"],
            student.get("latest_pickup")
        )

    return domains


def solve_student_assignment(students, capacity=DEMO_ROUTE_CAPACITY):
    domains = build_student_domains(students)

    # Fail early if any student has no valid route.
    for student_name, domain in domains.items():
        if not domain:
            return None, domains, {}

    # Most-constrained-variable heuristic:
    # assign students with fewer choices first.
    ordered_students = sorted(
        students,
        key=lambda s: len(domains[s["name"]])
    )

    assignment = {}
    load = {route_name: 0 for route_name in ROUTES}

    def backtrack(index):
        if index == len(ordered_students):
            return True

        student = ordered_students[index]
        name = student["name"]

        # Try less-loaded routes first.
        candidate_routes = sorted(
            domains[name],
            key=lambda route: (load[route], route)
        )

        for route in candidate_routes:
            if load[route] >= capacity:
                continue

            assignment[name] = route
            load[route] += 1

            if backtrack(index + 1):
                return True

            # Backtrack
            load[route] -= 1
            del assignment[name]

        return False

    success = backtrack(0)

    if not success:
        return None, domains, load

    return assignment, domains, load


# ---------------------------------------------------------------------------
# 4. GRAPH COLORING - ROUTE CONFLICT GROUPS
# ---------------------------------------------------------------------------

def build_route_conflict_graph():
    """
    Two routes conflict when:
      1) they share at least one non-campus stop, AND
      2) they have at least one common official campus departure time.

    The graph-coloring result is a LAB dispatch grouping.
    It does NOT replace the official university schedule.
    """
    conflict_graph = {route: set() for route in ROUTES}
    conflict_details = {}

    route_names = list(ROUTES.keys())

    for i in range(len(route_names)):
        for j in range(i + 1, len(route_names)):
            a = route_names[i]
            b = route_names[j]

            shared_stops = (
                set(route_stop_names(a))
                & set(route_stop_names(b))
                - {CAMPUS}
            )

            shared_departures = (
                set(ROUTES[a]["campus_departures"])
                & set(ROUTES[b]["campus_departures"])
            )

            if shared_stops and shared_departures:
                conflict_graph[a].add(b)
                conflict_graph[b].add(a)

                conflict_details[(a, b)] = {
                    "shared_stops": sorted(shared_stops),
                    "shared_departures": sorted(shared_departures),
                }

    return conflict_graph, conflict_details


def can_use_color(node, color, coloring, graph):
    for neighbour in graph[node]:
        if coloring.get(neighbour) == color:
            return False
    return True


def try_color_graph(graph, max_colors):
    """
    Backtracking graph coloring using degree ordering.
    """
    nodes = sorted(graph, key=lambda n: len(graph[n]), reverse=True)
    coloring = {}

    def backtrack(index):
        if index == len(nodes):
            return True

        node = nodes[index]

        for color in range(1, max_colors + 1):
            if can_use_color(node, color, coloring, graph):
                coloring[node] = color

                if backtrack(index + 1):
                    return True

                del coloring[node]

        return False

    if backtrack(0):
        return coloring

    return None


def minimum_route_coloring():
    graph, details = build_route_conflict_graph()

    for color_count in range(1, len(graph) + 1):
        coloring = try_color_graph(graph, color_count)

        if coloring is not None:
            return coloring, color_count, graph, details

    return None, 0, graph, details


# ---------------------------------------------------------------------------
# TEST DATA FOR THE OPEN-ENDED LAB
# ---------------------------------------------------------------------------

TEST_STUDENTS = [
    {"name": "Ayan",    "pickup": "Shewrapara",           "latest_pickup": "07:20"},
    {"name": "Borna",   "pickup": "Kuril",                "latest_pickup": "08:00"},
    {"name": "Cynthia", "pickup": "Kalshi",               "latest_pickup": "08:00"},
    {"name": "Dipto",   "pickup": "Rampura",              "latest_pickup": "08:00"},
    {"name": "Emon",    "pickup": "Rampura",              "latest_pickup": "08:00"},
    {"name": "Faria",   "pickup": "Tarabo",               "latest_pickup": "08:00"},
    {"name": "Galib",   "pickup": "Bhulta",               "latest_pickup": "08:00"},
    {"name": "Hira",    "pickup": "Gawsia",               "latest_pickup": "08:00"},
    {"name": "Imran",   "pickup": "Araihazar Chowrasta",  "latest_pickup": "08:00"},
    {"name": "Jannat",  "pickup": "Chashara",             "latest_pickup": "07:00"},
    {"name": "Kamal",   "pickup": "Mirpur 1",             "latest_pickup": "07:30"},
    {"name": "Lamia",   "pickup": "Dhanmondi 27",         "latest_pickup": "07:15"},
    {"name": "Mahin",   "pickup": "Narsingdi Velanagar",  "latest_pickup": "07:05"},
]

IMPOSSIBLE_TEST = [
    {"name": "Test Student", "pickup": "Unknown Area", "latest_pickup": "08:00"}
]


# ---------------------------------------------------------------------------
# OUTPUT / DEMONSTRATION
# ---------------------------------------------------------------------------

def print_route_summary():
    print("=" * 78)
    print("GUB UNIVERSITY BUS ROUTE & STUDENT ASSIGNMENT - OPEN-ENDED AI LAB")
    print("=" * 78)
    print(f"Day routes loaded     : {len(ROUTES)}")
    print(f"Unique graph stops    : {len(TRANSPORT_GRAPH)}")
    print("Schedule coverage     : Saturday to Wednesday")
    print("Interface             : Console output only (NO GUI)")
    print()


def demo_bfs():
    print("\n[1] BFS TEST - SHORTEST STOP-LINK PATH")
    print("-" * 78)

    tests = [
        ("Shewrapara", CAMPUS),
        ("Chashara", CAMPUS),
    ]

    for start, goal in tests:
        path, explored = bfs_shortest_path(start, goal)

        print(f"\nStart: {start}")
        print(f"Goal : {goal}")

        if path:
            print("Path :", " -> ".join(path))
            print("Stop links (edges):", len(path) - 1)
            print("Explored nodes    :", explored)
        else:
            print("No path found.")


def demo_dfs():
    print("\n[2] DFS TEST - EXPLORE REACHABLE BUS STOPS")
    print("-" * 78)

    start = "GUB Campus"
    order = dfs_explore(start)

    print("Start            :", start)
    print("Reachable stops  :", len(order))
    print("Exploration order:")
    print(" -> ".join(order))


def demo_csp():
    print("\n[3] CSP TEST - STUDENT TO BUS-ROUTE ASSIGNMENT")
    print("-" * 78)
    print(
        f"Lab simulation capacity = {DEMO_ROUTE_CAPACITY} students per route "
        "(NOT official bus capacity)"
    )

    assignment, domains, load = solve_student_assignment(TEST_STUDENTS)

    print("\nStudent domains:")
    for student in TEST_STUDENTS:
        name = student["name"]
        print(
            f"{name:8} | pickup={student['pickup']:<24} "
            f"| latest={student['latest_pickup']} "
            f"| domain={domains[name]}"
        )

    if assignment is None:
        print("\nNo valid CSP assignment found.")
        return

    print("\nValid CSP assignment:")
    for student in TEST_STUDENTS:
        name = student["name"]
        route = assignment[name]
        stop = student["pickup"]
        print(
            f"{name:8} -> {route:11} | "
            f"{stop:<24} | pickup time {pickup_time(route, stop)}"
        )

    used_routes = {r: count for r, count in load.items() if count > 0}
    print("\nSatisfied constraints:")
    print("- Every assigned route serves the student's pickup stop.")
    print("- Every assigned pickup time satisfies the student's latest time.")
    print("- No route exceeds the lab-simulation capacity.")
    print("Used route loads:", used_routes)

    # Negative test
    bad_assignment, bad_domains, _ = solve_student_assignment(IMPOSSIBLE_TEST)
    print("\nNegative test:")
    print("Input pickup stop = 'Unknown Area'")
    print("Domain            =", bad_domains["Test Student"])
    print("Expected result   = No valid assignment")
    print("Actual result     =", "No valid assignment" if bad_assignment is None else bad_assignment)


def demo_graph_coloring():
    print("\n[4] GRAPH COLORING TEST - ROUTE CONFLICT GROUPS")
    print("-" * 78)

    coloring, color_count, graph, details = minimum_route_coloring()

    edge_count = sum(len(v) for v in graph.values()) // 2

    print("Conflict rule:")
    print("Two routes are adjacent if they share a non-campus stop AND")
    print("also share at least one official campus departure time.")
    print()
    print("Conflict edges :", edge_count)
    print("Colors used    :", color_count)

    print("\nColor / dispatch-group assignment:")
    for route in sorted(coloring):
        print(
            f"{route:11} -> Color {coloring[route]} | {ROUTES[route]['title']}"
        )

    print("\nSample conflict evidence:")
    for index, ((a, b), info) in enumerate(sorted(details.items())):
        if index == 8:
            break

        print(
            f"{a} <-> {b} | shared stops={info['shared_stops']} "
            f"| common campus departure={info['shared_departures']}"
        )

    # Verify coloring
    valid = True
    for route in graph:
        for neighbour in graph[route]:
            if coloring[route] == coloring[neighbour]:
                valid = False

    print("\nColoring validation:", "PASS" if valid else "FAIL")
    print(
        "Interpretation: conflicting route pairs are placed in different "
        "lab dispatch groups."
    )


def main():
    print_route_summary()
    demo_bfs()
    demo_dfs()
    demo_csp()
    demo_graph_coloring()

    print("\n" + "=" * 78)
    print("RESULT SUMMARY")
    print("=" * 78)
    print("BFS  : reports shortest stop-link path and explored-node count.")
    print("DFS  : reports all reachable stops and exploration order.")
    print("CSP  : reports domains, valid assignments, constraints, and a failure test.")
    print("Color: reports conflict edges, number of colors, groups, and validation.")
    print("=" * 78)


if __name__ == "__main__":
    main()
