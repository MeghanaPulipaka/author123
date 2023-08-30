import json
from neo4j import GraphDatabase

# Assuming you have set up the Neo4j driver and session
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

# Function to get the top N co-authors with the highest degree of connection
def get_top_co_authors(session, author_id, top_n):
    query = f"""
    MATCH (a:Author)-[:CO_AUTHORED]->(b:Author)
    WHERE a.author_id = '{author_id}'
    WITH COLLECT(b.author_id) AS co_author_ids
    WITH co_author_ids, SIZE(co_author_ids) AS degree
    ORDER BY degree DESC
    LIMIT {top_n}
    RETURN co_author_ids
    """
    result = session.run(query)
    top_co_authors = result.single()["co_author_ids"]
    return top_co_authors

# Function to get authors connected to given authors
def get_connected_authors(session, author_ids):
    query = f"""
    MATCH (a:Author)-[:CO_AUTHORED]->(b:Author)
    WHERE a.author_id IN {author_ids} AND a.author_id <> b.author_id
    RETURN DISTINCT b.author_id AS connected_author_id
    """
    result = session.run(query, author_ids=author_ids)
    connected_authors = [record["connected_author_id"] for record in result]
    return connected_authors

top_n = 5  # Number of top co-authors to select

def get_connected_authors_final(input_author_id):
    with driver.session() as session:
        top_co_authors = get_top_co_authors(session, input_author_id, top_n)
        connected_authors = set(top_co_authors)  # Use a set to store connected authors
        
        while len(connected_authors) < top_n:
            new_connected_authors = get_connected_authors(session, list(connected_authors))
            connected_authors.update(new_connected_authors)

            if len(connected_authors) >= top_n:
                break
        
        connected_authors = list(connected_authors)[:top_n]  # Convert set back to list and truncate if needed
        
        output_data = []
        for rank, co_author_id in enumerate(connected_authors, start=1):
            output_data.append({
                "authorID": co_author_id,
                "likeliness": 1,
                "rank": rank
                })
        json_output = json.dumps(output_data, indent=4)
        return json_output
