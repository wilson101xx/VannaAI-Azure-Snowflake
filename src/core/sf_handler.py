
from src.core.vanna import MyVanna
from src.config.local_env import AppConfig


def connect_to_snowflake(vn: MyVanna, account: str = AppConfig.SNOWFLAKE_ACCOUNT) -> MyVanna:
    """
    Connect Vanna.ai to Snowflake
    """

    print(AppConfig.SNOWFLAKE_ACCOUNT)
    vn.connect_to_snowflake(
        account=account,
        username=AppConfig.SNOWFLAKE_USER,
        password=AppConfig.SNOWFLAKE_PASSWORD,
        role=AppConfig.SNOWFLAKE_ROLE,
        database=AppConfig.SNOWFLAKE_DATABASE,
        warehouse=AppConfig.SNOWFLAKE_WAREHOUSE
    )
    return vn

if __name__ == "__main__":
    wokring = connect_to_snowflake()

