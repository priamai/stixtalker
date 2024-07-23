# Stix Talker
Conversational query language for your stix needs!

```
SQL Prompt: [{'role': 'system', 'content': "You are a SQLite expert. Please help to generate a SQL query to answer the question. Your response should ONLY be based on the given context and follow the response guidelines and format instructions. ===Response Guidelines \n1. If the provided context is sufficient, please generate a valid SQL query without any explanations for the question. \n2. If the provided context is almost sufficient but requires knowledge of a specific string in a particular column, please generate an intermediate SQL query to find the distinct strings in that column. Prepend the query with a comment saying intermediate_sql \n3. If the provided context is insufficient, please explain why it can't be generated. \n4. Please use the most relevant table(s). \n5. If the question has been asked and answered before, please repeat the answer exactly as it was given before. \n"}, {'role': 'user', 'content': 'How many indicators do we have?'}, {'role': 'assistant', 'content': 'SELECT COUNT(*) FROM indicator'}, {'role': 'user', 'content': 'How many indicators are in total?'}, {'role': 'assistant', 'content': 'SELECT COUNT(*) FROM indicator'}, {'role': 'user', 'content': 'How many indicators do we have?'}]
Using model gpt-4o for 251.0 tokens (approx)


Ran 2 tests in 8.085s

OK
LLM Response: SELECT COUNT(*) FROM indicator
   COUNT(*)
0         1
```

