import random

STORY_TEMPLATES = [
    {
        "title": "The Epic Space Adventure",
        "template": "Once upon a time, a {adjective1} astronaut named {name} was flying through space in a {adjective2} spaceship. Suddenly, they saw a {adjective3} {noun1} floating by! '{exclamation}!' shouted {name}, as they tried to {verb1} the mysterious object. The {noun1} started to {verb2} {adverb1}, which made {name} feel very {emotion}. After {number} minutes of {verb3}, {name} discovered that the {noun1} was actually a {adjective4} {noun2} from the planet {place}. The {noun2} taught {name} how to {verb4} like a {animal}, and they became {adjective5} friends forever!",
        "fields": ["adjective1", "name", "adjective2", "adjective3", "noun1", "exclamation", "verb1", "verb2", "adverb1", "emotion", "number", "verb3", "adjective4", "noun2", "place", "verb4", "animal", "adjective5"]
    },
    {
        "title": "The Mysterious Kitchen Catastrophe",
        "template": "Chef {name} was having a {adjective1} day in the kitchen when they decided to cook a {adjective2} {food}. They grabbed a {adjective3} {kitchen_tool} and started to {verb1} the ingredients {adverb1}. Suddenly, the {food} began to {verb2} and turn {color}! '{exclamation}!' screamed {name}, as {number} {animal}s came running into the kitchen. The {animal}s were {adjective4} and wanted to {verb3} the {color} {food}. After a {adjective5} chase around the {room}, everyone sat down and ate the {food} together. It tasted like {adjective6} {noun} and made everyone {verb4} with joy!",
        "fields": ["name", "adjective1", "adjective2", "food", "adjective3", "kitchen_tool", "verb1", "adverb1", "verb2", "color", "exclamation", "number", "animal", "adjective4", "verb3", "adjective5", "room", "adjective6", "noun", "verb4"]
    },
    {
        "title": "The Wacky School Day",
        "template": "It was a {adjective1} Monday morning when {name} arrived at {adjective2} Elementary School. Instead of their usual {subject} class, they found their teacher, Mr./Ms. {teacher_name}, {verb1} on the ceiling! The classroom was full of {adjective3} {noun1}s that were {verb2} around the room. '{exclamation}!' said {name}, pulling out their {adjective4} {school_supply}. All the students had to {verb3} {adverb1} to avoid the flying {noun1}s. When lunchtime came, the cafeteria was serving {adjective5} {food} with {adjective6} {condiment}. The whole school turned into a {adjective7} {noun2}, and everyone learned how to {verb4} in {language} by the end of the day!",
        "fields": ["adjective1", "name", "adjective2", "subject", "teacher_name", "verb1", "adjective3", "noun1", "verb2", "exclamation", "adjective4", "school_supply", "verb3", "adverb1", "adjective5", "food", "adjective6", "condiment", "adjective7", "noun2", "verb4", "language"]
    },
    {
        "title": "The Silly Pet Adventure",
        "template": "{name} had a {adjective1} pet {animal} named {pet_name}. One {adjective2} morning, {pet_name} learned how to {verb1} and decided to {verb2} to the {place}. At the {place}, {pet_name} met a {adjective3} {animal2} who was {verb3} a {adjective4} {object}. Together, they {verb4} {adverb1} until they found a {adjective5} treasure chest full of {noun}s. '{exclamation}!' barked/meowed/chirped {pet_name}, as {number} {adjective6} {creature}s appeared. Everyone {verb5} together and had a {adjective7} party that lasted {number2} hours!",
        "fields": ["name", "adjective1", "animal", "pet_name", "adjective2", "verb1", "verb2", "place", "adjective3", "animal2", "verb3", "adjective4", "object", "verb4", "adverb1", "adjective5", "noun", "exclamation", "number", "adjective6", "creature", "verb5", "adjective7", "number2"]
    }
]

def get_random_template():
    """Return a random story template"""
    return random.choice(STORY_TEMPLATES)

def get_template_by_index(index):
    """Return a specific story template by index"""
    if 0 <= index < len(STORY_TEMPLATES):
        return STORY_TEMPLATES[index]
    return get_random_template()

def get_all_templates():
    """Return all available story templates"""
    return STORY_TEMPLATES