# Entryway of the script to get scripts to connect to twitter api
# with certain parameters.
import sys

class cli_parser:
    def __init__(self, query, parameters):
        self.query = query
        self.parms = parameters


# total arguments
n = len(sys.argv)

# if n != 3:
#     print("The correct way of using the script is: python3 main.py <query> <parameters>")
#     sys.exit(1)

sys.argv.append("test")
sys.argv.append(44196397)
sys.argv.append("test")
query = sys.argv[1]
parameters = sys.argv[2]
     
print("query: " + str(query))
print("parameters: " + str(parameters))

# TODO: start main with query paramaters