from pymongo import MongoClient
import csv
from multiprocessing import Process

def worker(worker_id, start, end):
    max_lines = 1000
    client = MongoClient('localhost', 27019)
    db = client['big_data_db']
    collection = db['vessels']
    with open('aisdk-2023-05-01.csv', 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i < start:
                continue
            if i > end:
                break
            print(f'Worker {worker_id}: Processing line {i}')
            collection.insert_one({
                'timestamp': row[0],
                'type_of_mobile': row[1],
                'mmsi': row[2],
                'latitude': row[3],
                'longitude': row[4],
                'navigational_status': row[5],
                'rot': row[6],
                'sog': row[7],
                'cog': row[8],
                'heading': row[9],
                'imo': row[10],
                'callsign': row[11],
                'name': row[12],
                'ship_type': row[13],
                'cargo_type': row[14],
                'width': row[15],
                'length': row[16],
                'type_of_position_fixing_device': row[17],
                'draught': row[18],
                'destination': row[19],
                'eta': row[20],
                'data_source_type': row[21],
                'a': row[22],
                'b': row[23],
                'c': row[24],
                'd': row[25]
            })

if __name__ == '__main__':
    # We will insert 60,000 records in total, because my computer can't handle more
    p1 = Process(target=worker, args=(1, 0, 10000))
    p2 = Process(target=worker, args=(2, 10001, 20000))
    p3 = Process(target=worker, args=(3, 20001, 30000))
    p4 = Process(target=worker, args=(4, 30001, 40000))
    p5 = Process(target=worker, args=(5, 40001, 50000))
    p6 = Process(target=worker, args=(6, 50001, 60000))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()