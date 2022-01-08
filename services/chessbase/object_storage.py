import pickle
import os.path
import time
import threading
import os
import sys
import datetime

lock = threading.Lock()


class ObjectStorage(dict):
    def __init__(self):
        super().__init__()
        self[str(len(self))] = len(self)

    def add_object(self, obj_id, obj):
        with lock:
            self[obj_id] = obj

    def list_objects_ids(self):
        return self.keys()


storage = None
if not os.path.isfile("storage/storage.db"):
    storage = ObjectStorage()
else:
    with open("storage/storage.db", mode="rb") as db_bytes:
        possible_load = pickle.load(db_bytes)
        if not possible_load["0"]:
            print(f'[{datetime.datetime.now().isoformat(sep=" ")}] Successfully restored db')
            storage = possible_load
        else:
            print(f'[{datetime.datetime.now().isoformat(sep=" ")}] Broken storage, cleaning up')
            storage = ObjectStorage()


def save_every_60_secs():
    while True:
        try:
            save_db_once()
        finally:
            time.sleep(60)


def save_db_once():
    try:
        with lock:
            with open("storage/storage.db", mode="wb") as db_bytes:
                pickle.dump(storage, db_bytes)
                print(f'[{datetime.datetime.now().isoformat(sep=" ")}] Pickled db size {os.stat("storage/storage.db").st_size / 1024} kb')
                print(f'[{datetime.datetime.now().isoformat(sep=" ")}] Inmemory db size {sys.getsizeof(storage) / 1024} kb')
                print(f'[{datetime.datetime.now().isoformat(sep=" ")}] Saved db')
    except Exception as e:
        print(f'[{datetime.datetime.now().isoformat(sep=" ")}] Error while saving db, {e}')


save_thread = threading.Thread(target=save_every_60_secs, daemon=True)
save_thread.start()
print(f'[{datetime.datetime.now().isoformat(sep=" ")}] Started saving daemon with {save_thread.name}')
