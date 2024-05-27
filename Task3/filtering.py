from pymongo import MongoClient
from multiprocessing import Process

def worker(worker_id, start, count):
    client = MongoClient('localhost', 27019)
    db = client['big_data_db']
    collection = db['vessels'].find().skip(start).limit(count)
    filtered_collection = db['filtered_vessels']

    for i, vessel in enumerate(collection):
        print(f'Worker {worker_id}: Processing vessel {i}')
        # Filter out vessels with missing data. We only filter by these fields because they are needed for the task.
        if 'timestamp' not in vessel or 'mmsi' not in vessel or 'latitude' not in vessel or 'longitude' not in vessel or vessel['timestamp'] == '' or vessel['mmsi'] == '' or vessel['latitude'] == '' or vessel['longitude'] == '':
            continue
        filtered_collection.insert_one(vessel)

if __name__ == '__main__':
    p1 = Process(target=worker, args=(1, 0, 20000))
    p2 = Process(target=worker, args=(2, 20001, 20000))
    p3 = Process(target=worker, args=(3, 40001, 20000))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    client = MongoClient('localhost', 27019)
    db = client['big_data_db']
    collection = db['filtered_vessels']
    pipeline = [
        {
            '$group': {
                '_id': '$mmsi',
                'count': {'$sum': 1}
            }
        },
        {
            '$match': {
                'count': {'$gte': 100}
            }
        }
    ]
    mmsi = list(collection.aggregate(pipeline))
    mmsi = [m['_id'] for m in mmsi]
    collection.delete_many({'mmsi': {'$nin': mmsi}})