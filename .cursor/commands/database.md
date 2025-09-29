Use the Supabase MCP server to search and analyze database information. Connect to the configured Supabase project and perform comprehensive database operations including:

1. **Database Discovery**: List all tables, views, functions, and schemas in the database
2. **Table Analysis**: Examine table structures, column types, constraints, and relationships
3. **Data Exploration**: Query and analyze data patterns, distributions, and sample records
4. **Schema Insights**: Identify foreign key relationships, indexes, and database design patterns
5. **Performance Analysis**: Analyze query performance and suggest optimizations
6. **Data Quality Assessment**: Check for data consistency, null values, and potential issues

When executing this command, provide detailed insights about the database structure and data, including:

- Table schemas with column details and data types
- Relationship mappings between tables
- Data volume and distribution statistics
- Sample data from key tables (respecting privacy)
- Recommendations for database optimization or improvements

Always ensure proper data privacy and security practices when accessing and analyzing database information.

**IMPORTANT**: you only need to read tables from the `lahman` schema, nothing else.

## Output Format

Output should always be a list of SQL queries that were executed so that we can use them in a separate Python script.

```python
[
    "SELECT * FROM lahman.Master",
    "SELECT * FROM lahman.People",
    "SELECT Count(*) FROM lahman.Batting"
]
```
