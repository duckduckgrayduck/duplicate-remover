"""
DocumentCloud Add-On that removes duplicates by their hash value
"""
import csv
from documentcloud.addon import AddOn
from documentcloud.exceptions import APIError

class DuplicateRemover(AddOn):
    """An example Add-On for DocumentCloud."""

    def main(self):
        """The main add-on functionality goes here."""
        confirm = self.data.get("confirm", False)
        if confirm is False:
            self.set_message("You did not check the confirmation box to delete duplicates, keeping all duplicate files.")
        to_tag = self.data.get("to_tag", False)
        known_hashes = {}
        to_delete = []

        # Loop through all documents
        for document in self.get_documents():
            file_hash = document.file_hash
            if file_hash in known_hashes:
                # If file_hash is already known, add it to to_delete
                try:
                    if confirm is True:
                        document.delete()
                    else:
                        if to_tag is True:
                            document.data["duplicate"] = True
                            document.data["hash"] = document.file_hash
                            document.save()
                            clone = self.client.documents.get({known_hashes[file_hash]})
                            clone.data["duplicate"] = True
                            clone.data["hash"] = clone.file_hash
                            clone.save() 
                    to_delete.append({
                        'deleted_id': document.id,
                        'reason': f"Document has the same hash as document with id {known_hashes[file_hash]}"
                    })
                except APIError:
                    self.set_message(
                        "Could not delete some documents due to insufficient permissions." 
                        "You can only delete documents you own."
                    )
                    to_delete.append({
                        'deleted_id': document.id,
                        'reason': "Failed to delete due to insufficient permissions"
                    })

            else:
                # Otherwise, add file_hash and document id to known_hashes dictionary
                known_hashes[file_hash] = document.id
        # Print the list of deletions with reasons
        # print(known_hashes)

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
