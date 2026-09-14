"""Reusable JSON persistence with error handling."""

import json
from pathlib import Path


class JsonStorage:
    def __init__(self, file_path):
        # Store the JSON file location.
        self.file_path = Path(file_path)

        # Create the parent folder if it doesn't exist.
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # Create an empty JSON list for a new storage file.
        if not self.file_path.exists():
            self.save([])

    def load(self):
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError) as error:
            raise RuntimeError(
                f"Could not load {self.file_path.name}: {error}"
            ) from error

        if not isinstance(data, list):
            raise RuntimeError(
                f"{self.file_path.name} must contain a JSON list."
            )

        return data

    def save(self, records):
        # Save the records to the JSON file.
        try:
            with self.file_path.open("w", encoding="utf-8") as file:
                json.dump(records, file, indent=4)

        # Convert file errors into a clear application error.
        except OSError as error:
            raise RuntimeError(
                f"Could not save {self.file_path.name}: {error}"
            ) from error

    def next_id(self):
        # Generate the next available ID.
        records = self.load()

        return max(
            (record.get("id", 0) for record in records),
            default=0
        ) + 1

    def add(self, record):
        # Add a new record and save the updated list.
        records = self.load()
        records.append(record)
        self.save(records)

        return record

    def find_by_id(self, record_id):
        # Find and return one record using its ID.
        return next(
            (
                item
                for item in self.load()
                if item.get("id") == record_id
            ),
            None,
        )

    def update(self, record_id, new_record):
        # Find a record and replace it with the updated version.
        records = self.load()

        for index, record in enumerate(records):
            if record.get("id") == record_id:
                records[index] = new_record
                self.save(records)
                return True

        # Return False when the ID does not exist.
        return False

    def delete(self, record_id):
        # Remove the record with the matching ID.
        records = self.load()

        remaining = [
            item for item in records
            if item.get("id") != record_id
        ]

        # Nothing was deleted if the list size stayed the same.
        if len(remaining) == len(records):
            return False

        # Save the list after removing the record.
        self.save(remaining)
        return True