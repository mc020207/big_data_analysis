from pyspark.ml.fpm import FPGrowth
from pyspark import SparkContext
from pyspark.sql import SparkSession
# df = spark.createDataFrame([
#     (0, [1, 2, 5]),
#     (1, [1, 2, 3, 5]),
#     (2, [1, 2])
# ], ["id", "items"])
sc = SparkContext(appName="FPGrowth")
spark = SparkSession(sc)
data = sc.textFile("/mydata/data")
transactions = data.map(lambda line: (line.strip().split(' '),))
df = transactions.toDF(["items",])
fpGrowth = FPGrowth(itemsCol="items", minSupport=4e-6, minConfidence=0.4)
model = fpGrowth.fit(df)

# Display frequent itemsets.
# model.freqItemsets.show()

# Display generated association rules.
answer=model.associationRules
from pyspark.sql.types import *
from pyspark.sql.functions import udf
def str_to_arr(my_list):
    my_list.sort()
    return  '+'.join([str(elem) for elem in my_list]) 
str_to_arr_udf = udf(str_to_arr,StringType())
answer = answer.withColumn("antecedent",str_to_arr_udf(answer["antecedent"]))
answer = answer.withColumn("consequent",str_to_arr_udf(answer["consequent"]))
answer.write.option("header",True).csv("/mydata/output")

# transform examines the input items against all the association rules and summarize the
# consequents as prediction
#model.transform(df).show()
spark.stop()