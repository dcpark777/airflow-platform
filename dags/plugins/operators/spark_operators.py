from airflow.models.baseoperator import BaseOperator
from maestro.maestro import maestro

@maestro("spark-scala-action")
class SparkScalaOperator(BaseOperator):
    def __init__(self, class_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_name = class_name
    
    def execute(self, context):
        print(f"Running {self.class_name}")


class SparkPythonOperator(BaseOperator):
    def __init__(self, pyfile: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pyfile = pyfile
    
    def execute(self, context):
        print(f"Running {self.pyfile}")