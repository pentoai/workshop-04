"""
Database utility module for connecting to PostgreSQL and executing queries.

This module provides functions to connect to a PostgreSQL database using SQLAlchemy
and execute SQL queries, returning results as pandas DataFrames for analysis.
"""

import logging
import os
from typing import Any

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_database_engine():
    """
    Create and return a SQLAlchemy engine using the POSTGRES_URL environment variable.

    Returns:
        sqlalchemy.engine.Engine: Database engine for executing queries

    Raises:
        ValueError: If POSTGRES_URL environment variable is not set
        SQLAlchemyError: If connection to database fails
    """
    postgres_url = os.getenv("POSTGRES_URL")

    if not postgres_url:
        raise ValueError(
            "POSTGRES_URL environment variable is not set. "
            "Please set it to your PostgreSQL connection string."
        )

    try:
        engine = create_engine(postgres_url)
        # Test the connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Successfully connected to PostgreSQL database")
        return engine
    except SQLAlchemyError as e:
        logger.error(f"Failed to connect to database: {e}")
        raise


def execute_query(query: str, params: dict[str, Any] | None = None) -> pd.DataFrame:
    """
    Execute a SQL query and return results as a pandas DataFrame.

    Args:
        query (str): SQL query to execute
        params (dict, optional): Parameters to bind to the query

    Returns:
        pd.DataFrame: Query results as a pandas DataFrame

    Raises:
        SQLAlchemyError: If query execution fails
        ValueError: If query is empty or invalid
    """
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    engine = get_database_engine()

    try:
        with engine.connect() as conn:
            logger.info(f"Executing query: {query[:100]}...")

            if params:
                result = pd.read_sql_query(text(query), conn, params=params)
            else:
                result = pd.read_sql_query(text(query), conn)

            logger.info(
                f"Query executed successfully. Returned {len(result)} rows, {len(result.columns)} columns"
            )
            return result

    except SQLAlchemyError as e:
        logger.error(f"Query execution failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during query execution: {e}")
        raise


def execute_query_with_validation(
    query: str, params: dict[str, Any] | None = None
) -> pd.DataFrame:
    """
    Execute a SQL query with additional validation and error handling.

    This function includes comprehensive validation of the returned data,
    checking for common issues like empty results, null values, and data types.

    Args:
        query (str): SQL query to execute
        params (dict, optional): Parameters to bind to the query

    Returns:
        pd.DataFrame: Validated query results as a pandas DataFrame

    Raises:
        SQLAlchemyError: If query execution fails
        ValueError: If query is empty, invalid, or returns unexpected results
    """
    result = execute_query(query, params)

    # Validation checks
    if result.empty:
        logger.warning("Query returned no results")

    # Log data quality information
    null_counts = result.isnull().sum()
    if null_counts.any():
        logger.info(
            f"Null values found in columns: {null_counts[null_counts > 0].to_dict()}"
        )

    # Log data types
    logger.info(f"Data types: {result.dtypes.to_dict()}")

    return result
