from pyspark.sql import functions as F
from pyspark.sql.functions import lit
from pyspark.sql.functions import udf, array

# df
df = spark.createDataFrame([
    ("a", None, None),
    ("a", "code1", None),
    ("a", "code2", "name2"),
    ("b", "code3", "name3"),
    ("b", "code4", "name5"),
    ("b", "code5", "name2"),
    ("c", None, None),
    ("c", "code1", None),
    ("c", "code2", "name2"),
], ["id", "code", "name"])

df.show()

# add collect_set columns
dfc = (df.
 groupby("id").
 agg(F.collect_set("code"),
       F.collect_list("name")))

dfc = dfc.withColumn("ciao", lit("code1"))

dfc.show()

# create udf
def check(arr, code):
    return code in arr
check_udf = udf(check)

# apply udf
dfcc = (dfc
        .withColumn("prova", check_udf("collect_set(code)", "ciao")))

dfcc.show()