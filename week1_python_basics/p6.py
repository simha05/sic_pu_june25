#farmer problem
#The overall sales achieved by Mahesh from the 80 acres of land.

total_land = 80
div = total_land/5
tomato_land1 = (30/100*div)
tomato_land2 = (70/100*div)
tomato_sales = (tomato_land1*10000*7)+(tomato_land2*12000*7)
potato_sales = (div*10000)*20
cabbage_sales = (div*14000)*24
sunflower_sales = (div*700)*200
sugarcane_sales = (div*45000)*4000
total_sales = tomato_sales+potato_sales+cabbage_sales+sunflower_sales+sugarcane_sales
print('the overall sales achived by mahesh from the 80 acres of land' ,total_sales)

# Sales realisation from chemical-free farming at the end of 11 months?

vegetables_sales = tomato_sales+potato_sales+cabbage_sales
sugarcane_sales2 = sugarcane_sales/4
sales_realisation = vegetables_sales+sugarcane_sales2+sunflower_sales
print('slaes realisation from chemical-free farming at the end of 11 months' ,sales_realisation)