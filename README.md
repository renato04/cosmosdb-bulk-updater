# CosmosDB bulk updater

A package to update a tons of documents in Microsoft CosmosDB

**How it works?**

It executes a query and iterate all the items executing an update function defined by the user. This query
will be executed until it return any result

**Installing**

`pip install cosmosdb-bulk-updater`

**Usage**

The sample bellow show how to add a new field into the all database documents

```python
from cosmosdb_bulk_updater import BulkUpdater, Database


def update_document(document: dict):

    document['new_field'] = 'blah'
    return document


def run():
    database = Database(
        endpoint="[ENDPOINT]",
        key="[YOUR_KEY]",
        database="[DATABASE]",
        collection="[COLLECTION]"
    )

    updater = BulkUpdater(
        database=database,
        query="SELECT TOP 500 VALUE c FROM c where NOT IS_DEFINED(c.new_field)"
    )

    updater.execute_update(
        execute_fn=update_document
    )


if __name__ == '__main__':
    run()

```