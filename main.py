import json
import os
import datetime
import statistics
from flask import Flask, render_template_string, request, redirect, url_for
from threading import Thread
from flask import render_template

app = Flask(__name__)


@app.route('/login')
def login():
    return render_template('login.html')


DATA_FILE = "users_data.json"
LOG_FILE = "visitor_log.txt"
IP_CACHE_FILE = "ip_cache.json"

# List of approved admin Replit usernames
APPROVED_ADMINS = ["kindasus22345"]

default_users = [
    {
        "name": "Isaac",
        "score": 100,
        "history": [{
            "date": "2025-04-21",
            "score": 100
        }],
        "comments": [],
        "badges": []
    },
    {
        "name": "Anton",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Noah",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Kanatip",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Jaden",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Joshua",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Colin",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Ethan",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Harry",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Leon",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Nee obo",
        "score": 20,
        "history": [{
            "date": "2025-04-21",
            "score": 20
        }]
    },
    {
        "name": "Oliver",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Reuben",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Sadie",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Spike",
        "score": 2,
        "history": [{
            "date": "2025-04-21",
            "score": 2
        }]
    },
    {
        "name": "Stephan",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Oat",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Crystal",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Violette",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Zakary",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Lucas",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Ryan",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Camille",
        "score": 0,
        "history": [{
            "date": "2025-04-21",
            "score": 0
        }]
    },
    {
        "name": "Cairo",
        "score": 50,
        "history": [{
            "date": "2025-04-21",
            "score": 50
        }]
    },
    {
        "name": "bird ",
        "score": 1000,
        "history": [{
            "date": "2025-04-21",
            "score": 1000
        }]
    },
]

# Track unique visitors
visited_ips = {}
action_log = []


def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            users = json.load(f)
            # Ensure all users have a history field
            for user in users:
                if "history" not in user:
                    user["history"] = [{
                        "date":
                        datetime.datetime.now().strftime("%Y-%m-%d"),
                        "score":
                        user["score"]
                    }]
            return users
    return default_users


def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)


def award_weekly_badges():
    users = load_users()
    sorted_users = sorted(users, key=lambda x: x['score'], reverse=True)
    if sorted_users:
        today = datetime.datetime.now()
        if today.weekday() == 6:  # Sunday
            winner = sorted_users[0]
            if 'badges' not in winner:
                winner['badges'] = []
            winner['badges'].append({
                'type': 'weekly_winner',
                'date': today.strftime("%Y-%m-%d"),
                'score': winner['score']
            })
            save_users(users)


def load_ip_cache():
    global visited_ips
    if os.path.exists(IP_CACHE_FILE):
        with open(IP_CACHE_FILE, "r") as f:
            visited_ips = json.load(f)
    else:
        visited_ips = {}
    return visited_ips


def save_ip_cache():
    with open(IP_CACHE_FILE, "w") as f:
        json.dump(visited_ips, f, indent=4)


def log_action(action_type, user_name, details):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    action_log.append({
        "timestamp": timestamp,
        "type": action_type,
        "user": user_name,
        "details": details
    })

    # Keep log to a reasonable size (last 1000 actions)
    if len(action_log) > 1000:
        action_log.pop(0)


def log_visitor(ip_address, user_agent):
    global visited_ips

    # If IP already logged today, don't log again
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    if ip_address in visited_ips:
        # Check if we've logged this IP today
        last_visit_date = visited_ips[ip_address].split()[
            0]  # Extract date portion
        if last_visit_date == today:
            # Already logged today, so just return
            return False

    # Log new visitor
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    visited_ips[ip_address] = timestamp

    log_entry = f"{timestamp} - IP: {ip_address} - User-Agent: {user_agent}\n"

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

    print(f"New visitor logged: {ip_address} at {timestamp}")
    save_ip_cache()
    return True


def add_positive_action(user, points):
    user["score"] += points
    # Update history
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    user["history"].append({"date": today, "score": user["score"]})

    log_action("positive", user["name"],
               f"Score increased by {points} to {user['score']}")
    print(f"{user['name']}'s score increased by {points}.")


def add_negative_action(user, points):
    user["score"] -= points
    # Update history
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    user["history"].append({"date": today, "score": user["score"]})

    log_action("negative", user["name"],
               f"Score decreased by {points} to {user['score']}")
    print(f"{user['name']}'s score decreased by {points}.")


def view_score(user):
    print(f"{user['name']}'s current score is: {user['score']}")


def add_user(users, name, score=0):
    # Check if user already exists
    if find_user(users, name):
        print(f"Error: User '{name}' already exists.")
        return False

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    users.append({
        "name": name,
        "score": score,
        "history": [{
            "date": today,
            "score": score
        }]
    })

    log_action("add_user", name,
               f"New user added with initial score of {score}")
    print(f"User '{name}' added with initial score of {score}.")
    save_users(users)
    return True


def remove_user(users, name):
    user = find_user(users, name)
    if user:
        users.remove(user)
        log_action("remove_user", name, "User removed from system")
        print(f"User '{name}' removed successfully.")
        save_users(users)
        return True
    else:
        print(f"Error: User '{name}' not found.")
        return False


def view_logs():
    if not os.path.exists(LOG_FILE):
        print("No visitor logs found.")
        return

    print("\n--- Unique Visitors ---")
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
        # Show last 10 entries or all if less than 10
        for line in lines[-10:]:
            print(line.strip())
    print(f"\nTotal unique visitors logged: {len(lines)}")


def calculate_stats(users):
    if not users:
        return {
            "total": 0,
            "avg": 0,
            "median": 0,
            "max": 0,
            "min": 0,
            "active": 0
        }

    scores = [user["score"] for user in users]
    active_users = len([user for user in users if user["score"] > 0])

    stats = {
        "total": len(users),
        "avg": round(sum(scores) / len(scores), 2),
        "median": statistics.median(scores),
        "max": max(scores),
        "min": min(scores),
        "active": active_users,
        "inactive": len(users) - active_users
    }
    return stats


def show_menu():
    print("\n1. Add Positive Action")
    print("2. Add Negative Action")
    print("3. View Score")
    print("4. View Rankings")
    print("5. Add New User")
    print("6. Remove User")
    print("7. View Unique Visitors")
    print("8. View System Statistics")
    print("9. Access Admin Dashboard (Web)")
    print("10. Exit")


def find_user(users, name):
    for user in users:
        if user['name'].lower() == name.lower():
            return user
    return None


def print_rankings(users):
    sorted_users = sorted(users, key=lambda x: x['score'], reverse=True)
    print("\nRankings:")
    for rank, user in enumerate(sorted_users, 1):
        print(f"Rank {rank}: {user['name']} with score {user['score']}")


def print_stats(users):
    stats = calculate_stats(users)
    print("\n--- System Statistics ---")
    print(f"Total users: {stats['total']}")
    print(f"Active users (score > 0): {stats['active']}")
    print(f"Inactive users (score = 0): {stats['inactive']}")
    print(f"Average score: {stats['avg']}")
    print(f"Median score: {stats['median']}")
    print(f"Maximum score: {stats['max']}")
    print(f"Minimum score: {stats['min']}")

    # Check if we have visitor logs
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            visitor_count = len(f.readlines())
        print(f"Total unique visitors: {visitor_count}")

    # Recent activity
    print("\nRecent activity:")
    for action in action_log[-5:]:
        print(
            f"{action['timestamp']} - {action['type']} - {action['user']} - {action['details']}"
        )


# Initialize Flask app
app.secret_key = os.urandom(24)  # For session handling

from flask import session, redirect, url_for, render_template


@app.route('/googlelogin', methods=['POST', 'GET'])
def googlelogin():
    return render_template('Googlelogin.html')


@app.route('/select_user', methods=['POST'])
def select_user():
    selected_user = request.form.get('selected_user')
    if selected_user:
        session['selected_user'] = selected_user
    return redirect('/')


@app.route('/')
def web_rankings():
    # Log visitor information (only once per day)
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    log_visitor(ip_address, user_agent)

    # Get authenticated user info
    replit_user = request.headers.get('X-Replit-User-Name')

    # Display rankings
    users = load_users()
    sorted_users = sorted(users, key=lambda x: x['score'], reverse=True)

    # Get user stats if logged in
    user_stats = None
    if replit_user:
        user_stats = find_user(users, replit_user)

    selected_user = session.get('selected_user')
    if selected_user:
        user_stats = find_user(users, selected_user)

    return render_template('ranking.html',
                           users=sorted_users,
                           replit_user=replit_user,
                           selected_user=selected_user,
                           user_stats=user_stats)


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    error = None
    replit_user = request.headers.get('X-Replit-User-Name')
    is_admin = replit_user in APPROVED_ADMINS

    if request.method == 'POST':
        if is_admin:
            return redirect('/admin/dashboard')
        else:
            error = "Invalid password. Please try again."

    return render_template('admin_login.html',
                           error=error,
                           replit_user=replit_user,
                           is_admin=is_admin)


@app.route('/admin/dashboard')
def admin_dashboard():
    users = load_users()
    sorted_users = sorted(users, key=lambda x: x['score'], reverse=True)
    stats = calculate_stats(users)

    # Get visitor count
    visitor_count = 0
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            visitor_count = len(f.readlines())

    # Get recent actions
    recent_actions = action_log[-10:] if action_log else []

    return render_template('admin_dashboard.html',
                           users=users,
                           sorted_users=sorted_users,
                           stats=stats,
                           visitor_count=visitor_count,
                           recent_actions=recent_actions)


@app.route('/admin/add_user', methods=['POST'])
def admin_add_user():
    name = request.form.get('name')
    try:
        score = int(request.form.get('score', 0))
    except ValueError:
        score = 0

    users = load_users()
    add_user(users, name, score)
    return redirect('/admin/dashboard')


@app.route('/admin/update_score', methods=['POST'])
def admin_update_score():
    name = request.form.get('user')
    points = int(request.form.get('points', 0))
    action = request.form.get('action')

    users = load_users()
    user = find_user(users, name)

    if user:
        if action == 'add':
            add_positive_action(user, points)
        else:
            add_negative_action(user, points)
        save_users(users)

    return redirect('/admin/dashboard')


@app.route('/add_comment', methods=['POST'])
def add_comment():
    if 'selected_user' not in session:
        return redirect('/')

    comment_text = request.form.get('comment')
    if comment_text:
        users = load_users()
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comment = {
            'user': session['selected_user'],
            'date': today,
            'text': comment_text
        }

        for user in users:
            if 'comments' not in user:
                user['comments'] = []
            if user['name'] == session['selected_user']:
                user['comments'].append(comment)
                save_users(users)
                break
    return redirect('/')


@app.route('/admin/remove_user', methods=['POST'])
def admin_remove_user():
    name = request.form.get('user')
    users = load_users()
    remove_user(users, name)
    return redirect('/admin/dashboard')


@app.route('/submit_application', methods=['POST'])
def submit_application():
    if 'selected_user' not in session:
        return redirect('/')

    request_type = request.form.get('request_type')
    reason = request.form.get('reason')

    if request_type and reason:
        users = load_users()
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        application = {
            'user': session['selected_user'],
            'date': today,
            'type': request_type,
            'reason': reason
        }
        #In a real application, you would store this application data, likely in a database.
        #For this example, we'll just print it.
        print(
            f"Application received from {session['selected_user']}: {application}"
        )
    return redirect('/')


def run_web_server():
    app.run(host='0.0.0.0', port=5000)


def handle_user_input(_):
    users = load_users()

    # Load previously visited IPs
    load_ip_cache()

    # Start web server in the background
    web_thread = Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()

    print("Web rankings available at http://localhost:5000/")
    print("Admin dashboard available at http://localhost:5000/admin")
    print("IP logging enabled. Each visitor will be logged only once per day.")

    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter user name: ")
            points = int(input("Enter points for the action: "))
            user = find_user(users, name)
            if user:
                add_positive_action(user, points)
                save_users(users)
            else:
                print("User not found.")

        elif choice == "2":
            name = input("Enter user name: ")
            points = int(input("Enter points for the action: "))
            user = find_user(users, name)
            if user:
                add_negative_action(user, points)
                save_users(users)
            else:
                print("User not found.")

        elif choice == "3":
            name = input("Enter user name to view score: ")
            user = find_user(users, name)
            if user:
                view_score(user)
            else:
                print("User not found.")

        elif choice == "4":
            print_rankings(users)

        elif choice == "5":
            name = input("Enter new user name: ")
            try:
                initial_score = int(
                    input("Enter initial score (default 0): ") or "0")
                add_user(users, name, initial_score)
            except ValueError:
                print("Invalid score. Using default score of 0.")
                add_user(users, name, 0)

        elif choice == "6":
            name = input("Enter user name to remove: ")
            remove_user(users, name)

        elif choice == "7":
            view_logs()

        elif choice == "8":
            print_stats(users)

        elif choice == "9":
            print("Admin dashboard available at http://localhost:5000/admin")
            print("Use Replit authentication.")

        elif choice == "10":
            print("Exiting program.")
            save_users(users)
            save_ip_cache()
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    handle_user_input(default_users)
