import uuid

import pycouchdb


class CouchDBClient:
    def __init__(self, host, port, username, password, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database_name = database
        self.server = None
        self.db = None
        self.partition_key = "courses"  # Default partition key

    def connect(self):
        try:
            url = f"http://{self.username}:{self.password}@{self.host}:{self.port}"
            self.server = pycouchdb.Server(url)
            self.db = self.server.database(self.database_name)
            print(f"Connected to CouchDB at {url}")
        except Exception as e:
            print(f"Failed to connect to CouchDB: {str(e)}")
            raise

    def get(self, doc_id):
        return self.db.get(doc_id)

    def insert(self, doc):
        # Generate a new UUID
        new_uuid = str(uuid.uuid4())
        # Create the document ID in the format "partition:id"
        doc['_id'] = f"{self.partition_key}:{new_uuid}"
        result = self.db.save(doc)
        return result['_id'], result['_rev']

    # def insert(self, doc):
    #     # Remove '_id' if it exists in the document
    #     doc.pop('_id', None)
    #     return self.db.save(doc)

    def update(self, doc):
        return self.db.save(doc)

    def delete(self, doc_id):
        doc = self.db.get(doc_id)
        return self.db.delete(doc)

    def query(self, view_name, **kwargs):
        # Add partition parameter to the query
        kwargs['partition'] = self.partition_key
        return self.db.query(view_name, **kwargs)

    def bulk_save(self, docs):
        return self.db.save_bulk(docs)

    def create_view(self, design_doc, view_name, map_func, reduce_func="_count"):
        design_doc_id = f"_design/{design_doc}"
        existing_doc = self.db.get(design_doc_id)
        if existing_doc:
            existing_doc['views'][view_name] = {
                "map": map_func,
                "reduce": reduce_func
            }
            self.db.save(existing_doc)
        else:
            self.db.save({
                "_id": design_doc_id,
                "views": {
                    view_name: {
                        "map": map_func,
                        "reduce": reduce_func
                    }
                },
                "options": {
                    "partitioned": True
                }
            },
            )
        return 'success'

    def query_course_by_partial_name(self, partial_name):
        view_name = 'courses/by_partial_name'
        options = {
            'partition': self.partition_key,
            'startkey': partial_name,
            'endkey': partial_name + '\ufff0',
            'reduce': False,  # Don't reduce the results
            'include_docs': True
        }
        results = self.db.query(view_name, **options)
        # Remove duplicates based on document ID
        unique_results = {result['doc']['_id']: result['doc'] for result in results}
        return list(unique_results.values())

    def delete_view(self, design_doc):
        design_doc_id = f"_design/{design_doc}"
        return self.db.delete(design_doc_id)

    def get_view(self, design_doc):
        design_doc_id = f"_design/{design_doc}"
        return self.db.get(design_doc_id)

    def get_all_docs(self):
        return self.db.all()

    def get_all_docs_by_view(self, view_name):
        return self.db.view(view_name)
