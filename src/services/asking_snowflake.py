from src.core.vanna import MyVanna
import pandas as pd

class VannaAsker:
    """
    Handles queries to Vanna and Snowflake.
    """

    def __init__(self, vn: MyVanna) -> None:
        """Initialize VannaAsker with a Vanna instance."""
        self.vn = vn

    def ask_question(self, question: str):
        """
        Queries Vanna and returns structured results.
        """
        response = self.vn.ask(question=question)

        if not isinstance(response, dict):
            raise ValueError(f"Unexpected response type: {type(response)}")

        sql = response.get("sql", "")
        data = response.get("data", [])

        if isinstance(data, pd.DataFrame):
            data = data.to_dict(orient="records")

        return {
            "sql": sql,
            "data": data,
            "summary": response.get("summary", ""),
            "followup_questions": response.get("followup_questions", []),
        }

    def get_suggested_questions(self):
        """Fetches suggested questions from Vanna."""
        return self.vn.generate_questions()
