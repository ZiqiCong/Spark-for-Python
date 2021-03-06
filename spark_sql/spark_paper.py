# coding: utf-8
import sys
import os

pre_current_dir = os.path.dirname(os.getcwd())
sys.path.append(pre_current_dir)
from pyspark.sql.functions import broadcast
from spark_sql.spark_sql_base import SparkSql


class SparkPaper(object):
    def __init__(self):
        self.spark_sql = SparkSql()

    def get_paper_info(self, paper_id=None):
        # 读取表的dataframe
        sub_q_df = self.spark_sql.load_table_dataframe('paper_subtype_question')
        q_map_df = self.spark_sql.load_table_dataframe('question_cognition_map')

        df = broadcast(sub_q_df).filter(
            sub_q_df.paper_id == paper_id
        ).join(
            q_map_df, on=[
                sub_q_df.question_id == q_map_df.question_id
            ], how='left'
        ).select("cognition_map_num")

        # 统计排序
        res_df = df.groupBy(
            "cognition_map_num"
        ).count().sort('count', ascending=False)

        return res_df


paper = SparkPaper()
print(paper.get_paper_info("002114ec130d4e83b201667dc30af44e").toJSON().collect())
