import sys
import statistics
# import MathNet
List=sys.argv
# Calculate the mean, SD, Median, Sum, Double the list
StandardDev=statistics.stdev(List) 

Mean=statistics.mean(List)
Median=statistics.median(List)
Sum=sum(List)
res = [ele + ele for ele in List]

print("List: ", List)
print("Double: ", res)
print("Sum: ", Sum)
print("Median: ", Median)
print("Mean: ", Mean)
print("Standard Deviation: ", StandardDev)