# Auckland Aquarium Management System

This project is a Python console application for managing fish inventory in an Auckland aquarium.

The aquarium manages these fish:

- Goldfish
- Shark
- Angelfish
- Tuna
- Salmon

The system accepts input data, stores it in a SQLite database, and displays each fish category with the number of fish currently available.

## Technologies Used

- Python 3
- SQLite
- Factory design pattern
- Singleton design pattern

## Design Patterns

### Factory Pattern

The `FishFactory` class creates fish objects from user input. For example, if the user enters `Salmon`, the factory creates a `Salmon` object with its correct category.

This keeps object creation in one place and makes the program easier to extend.

### Singleton Pattern

The `DatabaseConnection` class uses the Singleton pattern. This means the program uses one shared database connection instead of creating many separate connections.

## Database

The application uses a SQLite database named `aquarium.db`.

The database table is `fish_inventory` and stores:

- `name`
- `category`
- `available_count`

The database is created automatically when the program runs.

The project includes seed data so the aquarium starts with sample inventory:

| Fish | Starting Count |
| --- | ---: |
| Goldfish | 25 |
| Shark | 2 |
| Angelfish | 18 |
| Tuna | 9 |
| Salmon | 14 |

## How to Run

From this folder, run:

```bash
python3 aquarium.py
```

## Menu Options

```text
Auckland Aquarium Management
1. Display all fish
2. Update fish count
3. Search fish
4. Exit
```

## Example

```text
Choose an option: 2
Enter fish name: Salmon
Enter available count: 12
Salmon count updated.

Choose an option: 1

Auckland Aquarium Fish Inventory
------------------------------------------------------------------------
Fish            Category                            Available Count
------------------------------------------------------------------------
Angelfish       Tropical ornamental fish                         18
Goldfish        Freshwater ornamental fish                        25
Salmon          Migratory fish                                    12
Shark           Large marine predator fish                        2
Tuna            Ocean fish                                        9
------------------------------------------------------------------------
```

## How to Run Tests

```bash
python3 -m unittest test_aquarium.py
```
