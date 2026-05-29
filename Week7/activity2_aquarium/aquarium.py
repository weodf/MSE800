from __future__ import annotations

import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path


DATABASE_PATH = Path(__file__).with_name("aquarium.db")

SEED_FISH_COUNTS = {
    "Goldfish": 25,
    "Shark": 2,
    "Angelfish": 18,
    "Tuna": 9,
    "Salmon": 14,
}


class Fish(ABC):
    def __init__(self, name: str, category: str) -> None:
        self.name = name
        self.category = category

    @abstractmethod
    def description(self) -> str:
        pass


class Goldfish(Fish):
    def __init__(self) -> None:
        super().__init__("Goldfish", "Freshwater ornamental fish")

    def description(self) -> str:
        return "A small freshwater fish often kept in home aquariums."


class Shark(Fish):
    def __init__(self) -> None:
        super().__init__("Shark", "Large marine predator fish")

    def description(self) -> str:
        return "A large marine predator fish."


class Angelfish(Fish):
    def __init__(self) -> None:
        super().__init__("Angelfish", "Tropical ornamental fish")

    def description(self) -> str:
        return "A tropical fish known for its flat body and bright pattern."


class Tuna(Fish):
    def __init__(self) -> None:
        super().__init__("Tuna", "Ocean fish")

    def description(self) -> str:
        return "A fast-swimming ocean fish."


class Salmon(Fish):
    def __init__(self) -> None:
        super().__init__("Salmon", "Migratory fish")

    def description(self) -> str:
        return "A migratory fish that can live in fresh and salt water."


class FishFactory:
    _fish_classes = {
        "goldfish": Goldfish,
        "shark": Shark,
        "angelfish": Angelfish,
        "tuna": Tuna,
        "salmon": Salmon,
    }

    @classmethod
    def create_fish(cls, fish_name: str) -> Fish:
        fish_class = cls._fish_classes.get(fish_name.strip().lower())
        if fish_class is None:
            valid_names = ", ".join(fish().name for fish in cls._fish_classes.values())
            raise ValueError(f"Unknown fish type. Please choose: {valid_names}")
        return fish_class()

    @classmethod
    def all_fish(cls) -> list[Fish]:
        return [fish_class() for fish_class in cls._fish_classes.values()]


class DatabaseConnection:
    _instance: DatabaseConnection | None = None

    def __new__(cls, database_path: Path = DATABASE_PATH) -> DatabaseConnection:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.database_path = database_path
            cls._instance.connection = sqlite3.connect(database_path)
            cls._instance.connection.row_factory = sqlite3.Row
        return cls._instance

    def get_connection(self) -> sqlite3.Connection:
        return self.connection

    def close(self) -> None:
        self.connection.close()
        type(self)._instance = None


class AquariumRepository:
    def __init__(self, database: DatabaseConnection | None = None) -> None:
        self.database = database or DatabaseConnection()
        self.connection = self.database.get_connection()

    def setup_database(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS fish_inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                available_count INTEGER NOT NULL CHECK (available_count >= 0)
            )
            """
        )
        self.connection.commit()

    def seed_default_fish(self) -> None:
        for fish in FishFactory.all_fish():
            self.connection.execute(
                """
                INSERT OR IGNORE INTO fish_inventory (name, category, available_count)
                VALUES (?, ?, ?)
                """,
                (fish.name, fish.category, SEED_FISH_COUNTS[fish.name]),
            )
        self.connection.commit()

    def update_fish_count(self, fish_name: str, available_count: int) -> None:
        if available_count < 0:
            raise ValueError("Available count cannot be negative.")

        fish = FishFactory.create_fish(fish_name)
        self.connection.execute(
            """
            INSERT INTO fish_inventory (name, category, available_count)
            VALUES (?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                category = excluded.category,
                available_count = excluded.available_count
            """,
            (fish.name, fish.category, available_count),
        )
        self.connection.commit()

    def get_all_fish(self) -> list[sqlite3.Row]:
        cursor = self.connection.execute(
            """
            SELECT name, category, available_count
            FROM fish_inventory
            ORDER BY name
            """
        )
        return cursor.fetchall()

    def get_fish(self, fish_name: str) -> sqlite3.Row | None:
        fish = FishFactory.create_fish(fish_name)
        cursor = self.connection.execute(
            """
            SELECT name, category, available_count
            FROM fish_inventory
            WHERE name = ?
            """,
            (fish.name,),
        )
        return cursor.fetchone()


def display_fish(rows: list[sqlite3.Row]) -> None:
    if not rows:
        print("No fish records found.")
        return

    print("\nAuckland Aquarium Fish Inventory")
    print("-" * 72)
    print(f"{'Fish':<15} {'Category':<35} {'Available Count':>15}")
    print("-" * 72)
    for row in rows:
        print(f"{row['name']:<15} {row['category']:<35} {row['available_count']:>15}")
    print("-" * 72)


def read_count() -> int:
    while True:
        raw_count = input("Enter available count: ").strip()
        try:
            count = int(raw_count)
            if count < 0:
                print("Please enter a number that is 0 or higher.")
                continue
            return count
        except ValueError:
            print("Please enter a whole number.")


def run_menu() -> None:
    repository = AquariumRepository()
    repository.setup_database()
    repository.seed_default_fish()

    while True:
        print("\nAuckland Aquarium Management")
        print("1. Display all fish")
        print("2. Update fish count")
        print("3. Search fish")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            display_fish(repository.get_all_fish())
        elif choice == "2":
            fish_name = input("Enter fish name: ").strip()
            try:
                count = read_count()
                repository.update_fish_count(fish_name, count)
                print(f"{fish_name.title()} count updated.")
            except ValueError as error:
                print(error)
        elif choice == "3":
            fish_name = input("Enter fish name: ").strip()
            try:
                fish = repository.get_fish(fish_name)
                if fish is None:
                    print("Fish has not been added to the aquarium database yet.")
                else:
                    display_fish([fish])
            except ValueError as error:
                print(error)
        elif choice == "4":
            repository.database.close()
            print("Goodbye.")
            break
        else:
            print("Please choose a valid option.")


if __name__ == "__main__":
    run_menu()
