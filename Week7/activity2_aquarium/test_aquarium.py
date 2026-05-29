import tempfile
import unittest
from pathlib import Path

from aquarium import AquariumRepository, DatabaseConnection, FishFactory, SEED_FISH_COUNTS


class AquariumTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "test_aquarium.db"
        self.database = DatabaseConnection(self.database_path)
        self.repository = AquariumRepository(self.database)
        self.repository.setup_database()
        self.repository.seed_default_fish()

    def tearDown(self) -> None:
        self.database.close()
        self.temp_dir.cleanup()

    def test_factory_creates_goldfish(self) -> None:
        fish = FishFactory.create_fish("goldfish")
        self.assertEqual(fish.name, "Goldfish")
        self.assertEqual(fish.category, "Freshwater ornamental fish")

    def test_repository_updates_and_reads_fish_count(self) -> None:
        self.repository.update_fish_count("Salmon", 12)
        fish = self.repository.get_fish("salmon")
        self.assertIsNotNone(fish)
        self.assertEqual(fish["name"], "Salmon")
        self.assertEqual(fish["available_count"], 12)

    def test_seed_data_adds_default_counts(self) -> None:
        fish = self.repository.get_fish("Shark")
        self.assertIsNotNone(fish)
        self.assertEqual(fish["available_count"], SEED_FISH_COUNTS["Shark"])

    def test_unknown_fish_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            FishFactory.create_fish("Snapper")


if __name__ == "__main__":
    unittest.main()
