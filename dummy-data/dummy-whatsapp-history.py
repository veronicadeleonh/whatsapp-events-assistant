import random
from datetime import datetime, timedelta

# List of players in the group
players = [
    "Maria", "Sofia", "Ana", "Laura", "Carmen",
    "Julia", "Elena", "Isabel", "Paula", "Victoria"
]

# Football locations
locations = {
    "formal": ["Urban Football Center", "Sports Complex Downtown", "Indoor Soccer Arena"],
    "colloquial": ["the usual spot", "our regular field", "the indoor court"],
    "vague": ["somewhere central", "that new place", "where we played last time"],
    "incomplete": ["the center", "the complex", "the field"]
}

# Football-related messages
meeting_messages = [
    "Who's up for a 5v5 match?",
    "Ladies, shall we organize a game this week?",
    "I'm trying to arrange a match, who's in?",
    "Anyone free for a game?",
    "Time for our weekly football match!",
    "Missing our football sessions, let's plan one!",
    "The weather is perfect for a match, who's joining?",
    "We need 10 players for a proper 5v5, who's available?",
    "Haven't played in a while, let's organize something!",
    "The pitch is booked, who's coming to play?"
]

# Regular chat messages related to football
regular_messages = [
    "Did you watch the Women's World Cup match yesterday?",
    "That goal by {player} was incredible!",
    "Anyone got spare football boots size 38?",
    "I found this great sports store with women's football gear!",
    "My muscles are still sore from our last game 😅",
    "We're getting better each time we play!",
    "Should we get matching team shirts?",
    "Who's watching the Champions League final?",
    "Need to practice my penalties 😫",
    "Best football session ever yesterday! 🎉"
]

def get_location_reference(formality='formal'):
    """Generate a location reference based on desired formality"""
    if formality == 'mixed':
        formality = random.choice(['formal', 'colloquial', 'vague', 'incomplete'])
    return random.choice(locations[formality])

def get_relative_date_expression(target_date, message_date):
    """Generate a natural date expression based on the difference between dates"""
    delta = target_date.date() - message_date.date()
    days_diff = delta.days
    
    if days_diff == 0:
        return "today"
    elif days_diff == 1:
        return "tomorrow"
    elif days_diff == -1:
        return "yesterday"
    elif 0 < days_diff <= 7:
        return target_date.strftime("%A")  # e.g., "Friday"
    elif -7 <= days_diff < 0:
        return f"last {target_date.strftime('%A')}"
    elif 7 < days_diff <= 14:
        return f"next {target_date.strftime('%A')}"
    else:
        return target_date.strftime("%Y-%m-%d")  # fallback to exact date

def generate_random_date():
    # Generate a date between 3 months ago and 2 months in the future
    today = datetime.now()
    start_date = today - timedelta(days=90)  # 3 months ago
    end_date = today + timedelta(days=60)    # 2 months in future
    delta = end_date - start_date
    return start_date + timedelta(days=random.randint(0, delta.days))

def generate_clean_discussion(base_datetime, include_location=True, include_time=True, 
                            use_natural_dates=True, location_formality='formal'):
    discussion = []
    organizer = random.choice(players)
    
    # Initial message
    discussion.append((base_datetime, organizer, "Who's up for a match?"))
    
    # Propose details
    current_datetime = base_datetime + timedelta(minutes=5)
    game_datetime = base_datetime + timedelta(days=random.randint(1, 7))
    is_future = game_datetime > datetime.now()
    
    # Build date expression
    if use_natural_dates and random.random() < 0.7:  # 70% chance to use natural date
        date_expr = get_relative_date_expression(game_datetime, current_datetime)
    else:
        date_expr = game_datetime.strftime("%Y-%m-%d")
    
    # Build proposal message
    if is_future:
        proposal = f"How about {date_expr}"
        if include_time:
            proposal += f" at {random.randint(17,20)}:00"
        if include_location:
            proposal += f" at {get_location_reference(location_formality)}"
        proposal += "?"
    else:
        proposal = f"We played {date_expr}"
        if include_location:
            proposal += f" at {get_location_reference(location_formality)}"
        proposal += ". Good memories!"
    
    discussion.append((current_datetime, organizer, proposal))
    
    # Location discussion (sometimes)
    if include_location and random.random() < 0.3:
        current_datetime += timedelta(minutes=random.randint(2, 8))
        discussion.append((current_datetime, random.choice(players), 
            random.choice([
                "Is that the one near the mall?",
                "Which entrance should we use?",
                "Is parking available there?",
                "Can you send the location?"
            ])))
        
        current_datetime += timedelta(minutes=random.randint(2, 5))
        discussion.append((current_datetime, organizer,
            random.choice([
                "Yes, that's the one!",
                "I'll send the location in a bit",
                "Same entrance as last time",
                "Plenty of parking available"
            ])))
    
    # Responses
    confirmed_players = [organizer]
    for player in players:
        if player != organizer:
            current_datetime += timedelta(minutes=random.randint(3, 15))
            if random.random() < 0.8:
                response = "Count me in! 👍" if is_future else "Yes, it was fun! 👍"
                confirmed_players.append(player)
            else:
                response = "Can't make it 😢" if is_future else "Missed it 😢"
            discussion.append((current_datetime, player, response))
    
    # Final confirmation
    current_datetime += timedelta(minutes=5)
    if is_future:
        final_message = f"Perfect! Players: {', '.join(confirmed_players)}"
    else:
        final_message = f"It was great playing with {', '.join(confirmed_players)}!"
    discussion.append((current_datetime, organizer, final_message))
    
    return discussion

def generate_ambiguous_discussion(base_datetime):
    discussion = []
    organizer = random.choice(players)
    is_future = base_datetime > datetime.now()
    
    # More varied ambiguous messages
    initial_msgs = [
        "Anyone free soon?",
        "Shall we arrange something?",
        "Time for another match?",
        "Missing our games!",
        "Should we meet up again?"
    ]
    
    discussion.append((base_datetime, organizer, random.choice(initial_msgs)))
    
    current_datetime = base_datetime + timedelta(minutes=5)
    discussion.append((current_datetime, "Sofia", 
        random.choice(["When?", "Which day?", "I might be free", "Yes, let's play!"])))
    
    current_datetime += timedelta(minutes=random.randint(2, 10))
    discussion.append((current_datetime, organizer, 
        random.choice(["Maybe later this week?", "How about soon?", "When are you all free?"])))
    
    current_datetime += timedelta(minutes=random.randint(2, 10))
    discussion.append((current_datetime, "Ana", 
        random.choice(["Where?", "The usual spot?", "Which field?"])))
    
    current_datetime += timedelta(minutes=random.randint(2, 10))
    discussion.append((current_datetime, "Laura", 
        random.choice(["Same time as always?", "Afternoon?", "Evening works better"])))
    
    current_datetime += timedelta(minutes=random.randint(2, 10))
    discussion.append((current_datetime, organizer, 
        random.choice(["Let's figure it out later", "I'll check and let you know", "Will keep you posted"])))
    
    return discussion

def save_chat_history(discussions, filename):
    whatsapp_history = []
    for discussion in discussions:
        for msg_datetime, sender, message in discussion:
            whatsapp_history.append(f"[{msg_datetime.strftime('%d/%m/%y, %H:%M:%S')}] {sender}: {message}")
    
    # Sort by datetime
    whatsapp_history.sort()
    
    with open(filename, "w", encoding='utf-8') as file:
        file.write("\n".join(whatsapp_history))
    
    return len(whatsapp_history)

# Generate 2-event chat (clean data)
two_event_discussions = [
    generate_clean_discussion(generate_random_date(), location_formality='mixed')
    for _ in range(2)
]
msg_count = save_chat_history(two_event_discussions, "dummy_whatsapp_2_events.txt")
print(f"Generated {msg_count} messages in 2-event chat")

# Generate 5-event chat (mixed formality)
five_event_discussions = [
    generate_clean_discussion(
        generate_random_date(),
        location_formality=random.choice(['formal', 'colloquial', 'mixed'])
    )
    for _ in range(5)
]
msg_count = save_chat_history(five_event_discussions, "dummy_whatsapp_5_events.txt")
print(f"Generated {msg_count} messages in 5-event chat")

# Generate 10-event chat with mixed/incomplete data
mixed_discussions = []
for _ in range(10):
    if random.random() < 0.6:  # 60% chance for clean but incomplete data
        mixed_discussions.append(
            generate_clean_discussion(
                generate_random_date(),
                include_location=random.random() > 0.3,
                include_time=random.random() > 0.3,
                use_natural_dates=True,
                location_formality=random.choice(['formal', 'colloquial', 'vague', 'incomplete'])
            )
        )
    else:  # 40% chance for ambiguous discussion
        mixed_discussions.append(generate_ambiguous_discussion(generate_random_date()))

msg_count = save_chat_history(mixed_discussions, "dummy_whatsapp_ambiguous.txt")
print(f"Generated {msg_count} messages in ambiguous chat")