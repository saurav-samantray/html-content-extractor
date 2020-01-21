from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("RSP1").set("spark.cores.max", "4")
sc = SparkContext(conf = conf)
sc.setLogLevel("WARN")

print("Something happened")