from cosmosdb_bulk_updater import BulkUpdater, Database


def update_document(document: dict):

    document['new_field'] = 'blah'
    return document


def run():
    d = Database(
        endpoint="[ENDPOINT]",
        key="[YOUR_KEY]",
        database="[DATABASE]",
        collection="[COLLECTION]"
    )

    u = BulkUpdater(
        database=d,
        query="SELECT TOP 500 VALUE c FROM c where NOT IS_DEFINED(c.new_field)"
    )

    u.execute_update(
        execute_fn=update_document
    )


if __name__ == '__main__':
    run()
