import csv
import io


def read_csv(content: bytes):
    decoded = content.decode('utf-8')
    return list(csv.DictReader(io.StringIO(decoded)))
