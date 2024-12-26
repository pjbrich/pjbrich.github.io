#Created by Benjamin Richards - 12/24/24
#this is to solve making a list of all the infiltration measurements in the data set

userchoice = ""


while userchoice == "y" or userchoice == "":

    #input total number of GEPS units
    totalGEPS = int(input("Enter the total number of GEPS units: "))
    #Gal/hour = (total GEPS units) * 50 = total gallons per hour
    galOverHour = totalGEPS * 50    
    #Gal/hour -> Cubic feet per hour = (total gallons per hour) / 7.48 = total cubic feet per hour
    cubicOverHour = galOverHour / 7.48
    #input the total Volume of water in cubic feet

    #input the surface area of the water
    surfaceArea = float(input("Enter the surface area of the water in square feet: "))
    #input the depth of the water
    depth = float(input("Enter the depth of the water in feet: "))

    #Volume of water in cubic feet = (surface area of the water) * (depth of the water)
    waterVolumeCF = surfaceArea * depth

    #Volume of water in cubic feet / total cubic feet per hour = total hours of infiltration
    timeToInfiltrate = waterVolumeCF / cubicOverHour
    #output the total hours of infiltration
    print(f"\nTotal GEPS units: {totalGEPS}")
    print(f"Total Gallons per Hour: {galOverHour}")
    print(f"Total Cubic Feet per Hour: {cubicOverHour:.2f}")
    print (f"Water Volume in Cubic Feet: {waterVolumeCF:.2f}")
    print(f"Total hours of infiltration: {timeToInfiltrate:.2f}")
    userchoice = input("Would you like to calculate the total hours of infiltration? (y/n):")
    
print("Thank you for using the Infiltration Estimator!")


