import datetime
import threading
import queue

from pydocumentdb.document_client import DocumentClient
from pydocumentdb import document_client
from pydocumentdb.query_iterable import QueryIterable


def do_update(client: DocumentClient, document, result_queue: queue.Queue):

    try:
        client.ReplaceDocument(document['_self'], document)
        result_queue.put({
            'id': document['id'],
            'updated': True
        })

    except Exception:
        result_queue.put({
            'id': document['id'],
            'updated': False
        })


class Database:

    def __init__(self, endpoint, key, database, collection ):
        self.endpoint = endpoint
        self.key = key
        self.database = database
        self.collection = collection


class BulkUpdater:

    def __init__(self, database: Database, query: str, threads=10):
        """
        BulkUpdater's constructor
        :param database: A database reference
        :param query: The query that will be executed until it returns zero result
        :param threads: The number of threads that will be executed default:10
        """
        self._endpoint = database.endpoint
        self._database = database.database
        self._collection = database.collection
        self._key = database.key
        self._threads = threads
        self._query = query
        self._result_queue = queue.Queue()

        self._client = document_client.DocumentClient(self._endpoint, {'masterKey': self._key})

    def _get_query(self, q: str) -> QueryIterable:
        """
        Generetes a QueryIterable from the string query
        :param q: The query
        :return: A QueryIterable
        """
        query = self._client.QueryDocuments(
            f'dbs/{self._database}/colls/{self._collection}',
            q
        )
        return query

    def _get_chunked_list(self, l: list, total_items: int) -> list:
        """
        Split the the list with total items size
        :param l: The list
        :param total_items: The total items
        :return: The list with list of total items size
        """
        for i in range(0, len(l), total_items):
            # Create an index range for l of n items:
            yield l[i:i + total_items]

    def execute_update(self, execute_fn):
        """
        Execute the update
        :param execute_fn: A function that returns the document updated
        """

        result = list(self._get_query(self._query))
        total_run = 0
        while len(result) > 0:
            threads = list()
            for document in result:
                updated_document = execute_fn(document)
                thread = threading.Thread(target=do_update, args=(self._client, updated_document, self._result_queue))
                threads.append(thread)

            pool = list(self._get_chunked_list(threads, self._threads))

            print(f'Number of pools: {len(pool)}')
            for thread_list in pool:
                print(f'Number of thread in this pool: {len(thread_list)}')
                # Start all threads
                [t.start() for t in thread_list]

                # Wait threads to finish
                [t.join() for t in thread_list]

            # Get all threads results
            all_results = [self._result_queue.get() for _ in range(self._result_queue.qsize())]
            success = [result for result in all_results if result['updated'] is True]
            errors = [result for result in all_results if result['updated'] is False]

            total_run = total_run + len(success)
            print(
                f"Total run in iteration: {len(success)} at {datetime.datetime.now()}")
            print(
                f"Total Documents.......: {total_run} at {datetime.datetime.now()}")

            for result in errors:
                print(f"not updated id..: {result['id']}")

            # Re execute the query
            print("Re executing the query")
            result = list(self._get_query(self._query))

