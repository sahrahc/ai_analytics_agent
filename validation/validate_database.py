from datetime import datetime
import json
from langchain_core.runnables import RunnableConfig

from state import GraphState

# -----------------------------------
# Final validation against the database
# This is an expensive validation as
# it connects to the database, so
# static and semantic validations
# should be done first.
# -----------------------------------

LOG_FILE = "output/snowflake_response.log"


def validate_with_database(state: GraphState, config: RunnableConfig):

    db_connection = config.get("configurable", {}).get("db_connection")
    if not db_connection:
        raise RuntimeError("Database connection not found in config")

    cursor = db_connection.cursor()

    # output:
    validation_status = (
        state["validation_status"] + "\nStarting database validation (3 of 3). \n"
    )

    try:
        query = state["sql"]

        cursor.execute(f"EXPLAIN USING TEXT {query}")

        plan = cursor.fetchall()

        # -----------------------------------
        # Process explain plan
        # -----------------------------------

        explain_text = "\n".join(row[0] for row in plan)

        if "error" in explain_text.lower():
            validation_status += "ERROR found by database: \n"
            error = f"Database validation error: {explain_text}"
            print("Database Validation:", error)
            raise Exception(error)

        if "cartesian" in explain_text.lower():
            validation_status += "CARTESIAN join found by database: \n"

        if "full scan" in explain_text.lower():
            validation_status += "FULL table scan found by database: \n"

        # log results of explain plan for debugging
        timestamp = datetime.now()
        # TODO create class and reuse for consistent logging
        log_entry = {
            "timestamp": timestamp,
            "response_id": cursor.sfqid,  # snowflake query id
            "response_text": explain_text,
            # "full_response": null,  # no full response for database validation
        }

        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(log_entry, indent=2, default=str))
            f.write("\n\n")

        print(f"Snowflake Response logged to {LOG_FILE}")

        print("Database validation passed")

    finally:
        cursor.close()

    return {
        "validation_status": validation_status,
    }
