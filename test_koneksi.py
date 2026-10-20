import os
from neo4j import GraphDatabase

URI = "bolt://127.0.0.1:7687"
USERNAME = "neo4j"
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = "uts"

if not PASSWORD:
    raise ValueError("Variabel NEO4J_PASSWORD belum diatur.")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

try:
    driver.verify_connectivity()
    with driver.session(database=DATABASE) as session:
        result = session.run(
            'RETURN "Python berhasil terhubung ke Neo4j!" AS status'
        )
        print(result.single()["status"])
except Exception as e:
    print("Koneksi gagal:", e)
finally:
    driver.close()
