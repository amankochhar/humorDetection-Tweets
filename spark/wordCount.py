from __future__ import print_function

import sys
from operator import add
from pyspark.ml.feature import StringIndexer
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: wordcount <file>", file=sys.stderr)
        exit(-1)

    spark = SparkSession\
        .builder\
        .appName("PythonWordCount")\
        .getOrCreate()

    data = spark.read.text(sys.argv[1])

    # #renaming the columns in our data frame
    oldColumns = data.schema.names
    newColumns = ["tweets", "results"]

    df = reduce(lambda data, idx: data.withColumnRenamed(oldColumns[idx], newColumns[idx]), xrange(len(oldColumns)), data)

    # Split the data into train and test
    splits = df.randomSplit([0.7, 0.3], 1234)
    train = splits[0]
    test = splits[1]

    lines = train.rdd.map(lambda r: r[0])
    counts = lines.flatMap(lambda x: x.split(' ')) \
                  .map(lambda x: (x, 1))
    output = counts.collect()

    # spark.stop()

    # sc = SparkContext(appName="nlpProject")
    # df = sc.createDataFrame(output)

    # indexer = StringIndexer(inputCol="category", outputCol="categoryIndex")
    # indexed = indexer.fit(df).transform(df)
    # indexed.show()


    for (word, count) in output:
        print("%s: %i" % (word, count))

    spark.stop()