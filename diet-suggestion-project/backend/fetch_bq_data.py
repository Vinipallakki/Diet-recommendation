from google.cloud import bigquery

def get_user_weekly_food_data(project_id, dataset, table):
    client = bigquery.Client(project=project_id)

    query = f"""
        SELECT *
        FROM `{project_id}.{dataset}.{table}`
        ORDER BY recorded_date DESC
        LIMIT 7
    """

    query_job = client.query(query)
    results = [dict(row) for row in query_job.result()]
    return results
