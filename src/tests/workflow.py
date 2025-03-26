# Just using this to test stuff
import os
from src.core.vanna import MyVanna
from src.core.sf_handler import connect_to_snowflake
from dotenv import load_dotenv
from src.services.training import VannaTrainer

load_dotenv()

config = {
    "azure_search_endpoint": os.getenv("AZURE_AI_SEARCH_ENDPOINT"),
    "azure_search_api_key": os.getenv("AZURE_SEARCH_API_KEY"),
    "index_name": "test-vanna-index",
    "dimensions": 384,
    "model": os.getenv("MODEL")
}

vn_instance = MyVanna(config=config)  
vn_instance = connect_to_snowflake(vn_instance)  
# base_vn = vn_instance

trainer = VannaTrainer(vn_instance)

data = trainer.get_training_data()
print(data)
# trainer.train_base_data()


