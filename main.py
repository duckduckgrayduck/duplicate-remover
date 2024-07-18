"""
DocumentCloud Add-On that removes duplicates by their hash value
"""

from documentcloud.addon import AddOn


class DuplicateRemover(AddOn):
    """An example Add-On for DocumentCloud."""

    def main(self):
        """The main add-on functionality goes here."""

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
        print(known_hashes)
        for deletion in to_delete:
            print(f"Deleted document {deletion['deleted_id']} - {deletion['reason']}")


if __name__ == "__main__":
    DuplicateRemover().main()
