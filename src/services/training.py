from src.core.vanna import MyVanna
from src.services import ddl
import pandas as pd
import numpy as np

class VannaTrainer:
    """
    Class for training Vanna.ai
    """

    def __init__(self, vn: MyVanna) -> None:
        """
        Constructor

        Args:
            vn (MyVanna): Vanna.ai instance
        """
        self.vn = vn

    def train_base_data(self) -> None:
        """
        Trains Vanna.ai with base training data from Snowflake
        """
        # train info schema
        df_information_schema = self.vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")
        information_schema_plan = self.vn.get_training_plan_generic(df_information_schema)
        print(information_schema_plan)
        self.vn.train(plan=information_schema_plan)
        print("Information schema data loaded to vector db")
        
        # train business rules 
        df_business_rules = self.vn.run_sql("SELECT * FROM DOCUMENTS.BUSINESS_RULES")
        for rule in df_business_rules['CONTEXT'].tolist():
            self.vn.train(documentation=rule)
        print(f"{len(df_business_rules)} business rules loaded to vector db")
        
        # train prompt and sql pairs
        df_pairs = self.vn.run_sql("SELECT * FROM DOCUMENTS.PROMPTS_AND_SQL_QUERIES")
        for row in df_pairs.itertuples():
            self.vn.train(question=row[1], sql=row[2])
        print(f"{len(df_pairs)} (prompt, sql) pairs loaded to vector db")
    
    def train_data_info_schema(self) -> None:
        """
        Trains Vanna.ai with the information schema data
        """
        df_information_schema = self.vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")
        plan = self.vn.get_training_plan_generic(df_information_schema)
        self.vn.train(plan=plan)

    def train_data_ddl(self) -> None:
        """
        Trains Vanna.ai on DDL queries/DB architecture,

        for the purpose of this, you can save a file called ddl with a function
        ddl_data() with example data to import

        NOT IMPLEMENTED YET! WILL RAISE ERROR!
        """
        ddl_data = ddl.ddl_data()
        self.vn.train(ddl=ddl_data)
        return True



    def train_data_documents(self, document: str) -> str:
        """
        Trains Vanna.ai on business context and documentation
        """
        record_id = self.vn.train(documentation=document)
        return record_id

    def train_data_prompt_sql_pairs(self, question: str, sql: str) -> str:
        """
        Trains Vanna.ai on prompt and SQL query pairs
        """
        record_id = self.vn.train(question=question, sql=sql)
        return record_id

    def _train_data_reporting(self) -> None:
        """
        Trains Vanna.ai on reporting data

        NOTE: I don't think we will expose this in the API,
        probably going to be an internal function.

        NOTE: Assumes you are using the DeepScout_ChromaDB_VectorStore
        object with the MyVanna class.
        """
        df_tableau_metadta = self.vn.run_sql("SELECT * FROM REPORTING.TABLEAU_REPORTS")
        for _, row in df_tableau_metadta.iterrows():
            self.vn.add_reporting(row['WORKBOOK_NAME'], row['WORKBOOK_URL'])

    def get_training_data(self):
        """
        Retrieves training data and ensures JSON-safe serialization.
        """
        data = self.vn.get_training_data()

        if isinstance(data, pd.DataFrame):
            # Replace inf/-inf with np.nan, then fill with None for JSON safety
            data = data.replace([np.inf, -np.inf], np.nan).where(pd.notnull(data), None)
            return data.to_dict(orient="records")

        elif isinstance(data, (list, tuple, set)):
            return list(data)

        elif isinstance(data, dict):
            def safe_value(val):
                if isinstance(val, float) and (np.isnan(val) or np.isinf(val)):
                    return None
                elif isinstance(val, (dict, list, str, int, float)):
                    return val
                return str(val)

            return {k: safe_value(v) for k, v in data.items()}

        else:
            return str(data)