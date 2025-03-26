from src.api.routers.query import VannaAsker
from dotenv import load_dotenv

load_dotenv()

def generate_questions_cached(vn: VannaAsker):
    return vn.generate_questions()

def generate_sql_cached(vn: VannaAsker, question: str):
    return vn.generate_sql(question=question, allow_llm_to_see_data=True)

def is_sql_valid_cached(vn: VannaAsker, sql: str):
    return vn.is_sql_valid(sql=sql)

def run_sql_cached(vn: VannaAsker, sql: str):
    return vn.run_sql(sql=sql)

def should_generate_chart_cached(vn: VannaAsker, question, sql, df):
    return vn.should_generate_chart(df=df)

def generate_plotly_code_cached(vn: VannaAsker, question, sql, df):
    code = vn.generate_plotly_code(question=question, sql=sql, df=df)
    return code

def generate_plot_cached(vn: VannaAsker, code, df):
    return vn.get_plotly_figure(plotly_code=code, df=df)

def generate_followup_cached(vn: VannaAsker, question, sql, df):
    return vn.generate_followup_questions(question=question, sql=sql, df=df)

def generate_summary_cached(vn: VannaAsker, question, df):
    return vn.generate_summary(question=question, df=df)
