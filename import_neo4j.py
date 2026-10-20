import os
import pandas as pd
from neo4j import GraphDatabase
from pathlib import Path

# Konfigurasi Neo4j
URI = "bolt://127.0.0.1:7687"
USERNAME = "neo4j"
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = "uts"

BATCH_SIZE = 1000


def import_batch(tx, records, periode):
    query = """
    UNWIND $records AS row
    MERGE (v:Visitor {visitorId: row.visitorid})
    MERGE (i:Item {itemId: row.itemid})
    WITH v, i, row
    CALL {
        WITH v, i, row
        WITH v, i, row WHERE row.event = 'view'
        CREATE (v)-[:VIEWED {
            timestamp: row.timestamp,
            periode: $periode
        }]->(i)
        RETURN count(*) AS n

        UNION ALL

        WITH v, i, row
        WITH v, i, row WHERE row.event = 'addtocart'
        CREATE (v)-[:ADDED_TO_CART {
            timestamp: row.timestamp,
            periode: $periode
        }]->(i)
        RETURN count(*) AS n

        UNION ALL

        WITH v, i, row
        WITH v, i, row WHERE row.event = 'transaction'
        CREATE (v)-[:BOUGHT {
            timestamp: row.timestamp,
            transactionId: row.transactionid,
            periode: $periode
        }]->(i)
        RETURN count(*) AS n
    }
    RETURN sum(n) AS imported
    """
    tx.run(query, records=records, periode=periode).consume()


def main():
    if not PASSWORD:
        raise ValueError(
            "Variabel lingkungan NEO4J_PASSWORD belum diatur."
        )

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD)
    )

    try:
        driver.verify_connectivity()

        with driver.session(database=DATABASE) as session:
            session.run("""
                CREATE CONSTRAINT visitor_id IF NOT EXISTS
                FOR (v:Visitor) REQUIRE v.visitorId IS UNIQUE
            """).consume()

            session.run("""
                CREATE CONSTRAINT item_id IF NOT EXISTS
                FOR (i:Item) REQUIRE i.itemId IS UNIQUE
            """).consume()

            for filename, periode in [
                ("P1.csv", "P1"),
                ("P2.csv", "P2"),
            ]:
                path = Path("data") / filename

                if not path.exists():
                    raise FileNotFoundError(
                        f"File tidak ditemukan: {path}"
                    )

                total = 0

                for chunk in pd.read_csv(
                    path,
                    chunksize=BATCH_SIZE
                ):
                    chunk["transactionid"] = (
                        chunk["transactionid"]
                        .fillna("")
                        .astype(str)
                    )

                    records = chunk.to_dict(orient="records")

                    session.execute_write(
                        import_batch,
                        records,
                        periode
                    )

                    total += len(records)

                    print(
                        f"{periode}: {total:,} baris diproses",
                        flush=True
                    )

                print(
                    f"Selesai mengimpor {periode}: {total:,} baris"
                )

    finally:
        driver.close()


if __name__ == "__main__":
    main()
