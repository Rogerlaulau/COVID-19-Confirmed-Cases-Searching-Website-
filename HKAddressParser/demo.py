# Import the components and use them
from components.core import Address
from components.util import Similarity

# Run the address parser with the address as param
temp = ""
#result = {"geo": ""}
for i in ["九龍城廣場", "", "宏業樓"]:
    
    try:
        address = Address(i)  #"宏業樓"
        result = address.ParseAddress()
        print(result)
        #print(f"{i}: {result['geo']}")
        print(type(result['geo']['Latitude']))
        temp += f"{i}: {result['geo']}" 
    except Exception as e:
        #print(f"\n{e}\n")
        print(i)
        print(e)
    #print(f">>> {result}")
    # print(result['chi'])
    # print(result['eng'])




print("\n=======================")
print(temp)
