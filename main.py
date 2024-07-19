"""
DocumentCloud Add-On that removes duplicates by their hash value
"""
import csv
import sys
from documentcloud.addon import AddOn

class DuplicateRemover(AddOn):
    """An example Add-On for DocumentCloud."""

    def main(self):
        """The main add-on functionality goes here."""
        confirm = self.data.get("confirm", False)
        if confirm is False:
            self.set_message("You did not check the confirmation box to run this Add-On")
            sys.exit(0)
        known_hashes = {}
        to_delete = []

        # Loop through all documents
        for document in self.get_documents():
            file_hash = document.file_hash
            if file_hash in known_hashes:
                # If file_hash is already known, add it to to_delete
                to_delete.append({
                    'deleted_id': document.id,
                    'reason': f"Deleted because it has the same hash as {known_hashes[file_hash]}"
                })
            else:
                # Otherwise, add file_hash and document id to known_hashes dictionary
                known_hashes[file_hash] = document.id
        # Print the list of deletions with reasons
        # print(known_hashes)
        for deletion in to_delete:
            print(f"Deleted document {deletion['deleted_id']} - {deletion['reason']}")

        csv_filename = "deleted_documents.csv"
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['deleted_id', 'reason']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for deletion in to_delete:
                writer.writerow(deletion)
        self.upload_file(open(csv_filename, encoding='utf-8'))

if __name__ == "__main__":
    DuplicateRemover().main()
