"""Booking desk for small events: create events, register guests, save data."""

import json
import secrets
import subprocess  # nosec B404 - used only with a fixed argument list, no shell
from datetime import date

events = {}


def create_event(event_name, venue, capacity=50, guests=None):
    """Create an event with a venue, capacity and optional guest list."""
    if guests is None:
        guests = []
    events[event_name] = {"venue": venue, "capacity": capacity,
                          "guests": guests}
    return events[event_name]


def register_guest(event_name, guest):
    """Add a guest to an event if it exists and has space."""
    event = events.get(event_name)
    if event is None:
        print("No such event:", event_name)
        return False
    if len(event["guests"]) >= event["capacity"]:
        print(event_name, "is full, cannot add", guest)
        return False
    event["guests"].append(guest)
    return True


def seats_left(event_name):
    """Return the number of free seats for an event."""
    event = events[event_name]
    return event["capacity"] - len(event["guests"])


def event_status(event_date):
    """Return 'Upcoming' or 'Completed' based on the event date."""
    if event_date >= date.today():
        return "Upcoming"
    return "Completed"


def guest_report(event_name):
    """Return the event's guest names, sorted, as one comma-separated string."""
    names = sorted(events[event_name]["guests"])
    return ", ".join(names)


def save_events(file_name="events.json"):
    """Save all events to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)


def load_events(file_name="events.json"):
    """Load events from a JSON file and return them."""
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)


def print_badges(event_name):
    """Send the badge file for an event to the printer."""
    # Helper kept for the lab: not called by the demo
    cmd = ["lp", f"badges_{event_name}.txt"]
    subprocess.run(cmd, check=True)  # nosec B603 B607 - fixed args, no shell


def main():
    """Run a short demonstration of the booking desk."""
    create_event("Tech Meetup", "Hall A", 3)
    create_event("Alumni Dinner", "Rooftop", 2)
    register_guest("Tech Meetup", "Asha")
    register_guest("Tech Meetup", "Ravi")
    register_guest("Alumni Dinner", "Meena")
    register_guest("Workshop", "Kiran")
    left = seats_left("Tech Meetup")
    print("Seats left at Tech Meetup:", left)
    print("Seats left at Alumni Dinner:", seats_left("Alumni Dinner"))
    print("Tech Meetup guests:", guest_report("Tech Meetup"))
    print("Tech Meetup is", event_status(date(2099, 1, 15)))
    print("Alumni Dinner is", event_status(date(2020, 5, 1)))
    guests = events["Tech Meetup"]["guests"]
    if guests:
        winner = secrets.choice(guests)
        print("Lucky draw winner:", winner)
    save_events()
    restored = load_events()  # reload to confirm the save worked
    print("Events restored from file:", len(restored))
    print("Venues:", [e["venue"] for e in restored.values()])


if __name__ == "__main__":
    main()