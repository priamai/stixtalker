# Stix Talker
This tool enables you to perform queries in natural language to a STIX database.

The training set is composed of:
* an extensive list of all the STIX 2.1 objects
* a documentation file in yaml that add more information

## Train

First train the tool:

```
python main.py -t
```


## Queries

Then for queries:

```
python main.py --query "How many indicators there are?"
```

Output example:
```
SQL Prompt: [{'role': 'system', 'content': 'You are a SQLite expert. Please help to generate a SQL query to answer the question. Your response should ONLY be based on the given context and follow the response guidelines and format instructions. \n===Tables \nCREATE TABLE "indicator" ("id" TEXT UNIQUE,"created_by_ref" TEXT,"created" TEXT,"modified" TEXT,"name" TEXT,"indicator_types" TEXT,"pattern" TEXT,"pattern_type" TEXT,"pattern_version" TEXT,"valid_from" TEXT, "description" TEXT, "granular_markings" TEXT)\n\nCREATE TABLE "process" ("id" TEXT UNIQUE,"pid" BIGINT,"x_aslr_enabled" BIGINT,"x_dep_enabled" BIGINT,"x_priority" TEXT,"x_owner_sid" TEXT, "command_line" TEXT, "image_ref" TEXT, "x_service_name" TEXT, "x_display_name" TEXT, "x_start_type" TEXT, "x_service_type" TEXT, "x_service_status" TEXT, "created_time" TEXT)\n\nCREATE TABLE "observed-data" ( "id" TEXT UNIQUE, "created_by_ref" TEXT, "created" TEXT, "modified" TEXT, "first_observed" TEXT, "last_observed" TEXT, "number_observed" BIGINT)\n\nCREATE TABLE "marking-definition" ("id" TEXT UNIQUE,"created" TEXT,"definition_type" TEXT,"name" TEXT,"definition.tlp" TEXT, "definition.statement" TEXT)\n\nCREATE TABLE "sighting" ("id" TEXT UNIQUE,"created_by_ref" TEXT,"created" TEXT,"modified" TEXT,"first_seen" TEXT,"last_seen" TEXT,"count" BIGINT,"sighting_of_ref" TEXT)\n\nCREATE TABLE "intrusion-set" ("id" TEXT UNIQUE,"created" TEXT,"modified" TEXT,"name" TEXT,"description" TEXT,"aliases" TEXT,"first_seen" TEXT,"goals" TEXT,"resource_level" TEXT,"primary_motivation" TEXT,"secondary_motivations" TEXT)\n\nCREATE TABLE "intrusion-set" ("id" TEXT UNIQUE,"created" TEXT,"modified" TEXT,"name" TEXT,"description" TEXT,"aliases" TEXT,"first_seen" TEXT,"goals" TEXT,"resource_level" TEXT,"primary_motivation" TEXT,"secondary_motivations" TEXT, "created_by_ref" TEXT)\n\nCREATE TABLE "location" ("id" TEXT UNIQUE,"created_by_ref" TEXT,"created" TEXT,"modified" TEXT,"region" TEXT, "country" TEXT, "administrative_area" TEXT, "postal_code" TEXT, "latitude" REAL, "longitude" REAL)\n\n\n===Additional Context \n\n===Response Guidelines \n1. If the provided context is sufficient, please generate a valid SQL query without any explanations for the question. \n2. If the provided context is almost sufficient but requires knowledge of a specific string in a particular column, please generate an intermediate SQL query to find the distinct strings in that column. Prepend the query with a comment saying intermediate_sql \n3. If the provided context is insufficient, please explain why it can\'t be generated. \n4. Please use the most relevant table(s). \n5. If the question has been asked and answered before, please repeat the answer exactly as it was given before. \n'}, {'role': 'user', 'content': 'How many indicators are in total?'}, {'role': 'assistant', 'content': 'SELECT COUNT(*) FROM indicator'}, {'role': 'user', 'content': 'How many IOCs are available?'}, {'role': 'assistant', 'content': 'SELECT COUNT(*) FROM indicator'}, {'role': 'user', 'content': 'How many indicators there are?'}]
Using model gpt-4o for 702.5 tokens (approx)
LLM Response: SELECT COUNT(*) FROM indicator
Auto generated SQL
SELECT COUNT(*) FROM indicator
Executing statement
   COUNT(*)
0         7
```

## Version
This is pretty much a work in progress.