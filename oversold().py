def oversold(fleet_data, daily_data):
    ''' 
    [[Plane 1 model, Number of business seats, Number of
    economy seats, Total number of seats, Gate, Destination,
    Arrival status, Maximum baggage weight allowed per
    passenger], [Plane 2 model,...etc.],...etc.]

    [[Gate, Number of business passengers, Number of economy
    passengers], [Gate,...etc.],...etc.]


    for econ and busniess 

    [[Plane 1 model, Number of oversold economy seats], [Plane
    2 model,...etc.],...etc.]
    '''
    # defining variables 
    results_econ = [] #empty list will update with results   
    results_business = [] 

    econ_oversold = 0 
    business_oversold = 0

    #processing 
    for i in range(len(fleet_data)): # using range() and len() to cycle through the indexes of the list basedf on the number of entries in fleet_data()

        #defining varibles that will change for each iteration using 2d list indexing 
        model = fleet_data[i][0] 
        business_seats = fleet_data[i][1] #i represents the sublist while the 1 represents the index of the data of intrest in the sublist 
        econ_seats = fleet_data[i][2]
        gate = fleet_data[i][4]

        for ii in range(len(daily_data)): ## nested for loop to cycle through daily data 
            if daily_data[ii][0] == gate: #compare gate number of fleet data to the item in the location of gate (index 0 of sublist) of the current sublist

                #if True, assign variuables for tickets sold by indexing the current sublist 
                business_sold = daily_data[ii][1]
                econ_sold = daily_data[ii][2]

                #compare number of seats sold vs number avaible for both types of seats 

                ##business oversold 
                if business_seats<business_sold:#if we have more sold seats than spaces available 
                    business_oversold  = business_sold- business_seats  #then the difference is the nukber of oversold seats
                else:                                                   #otherwise there are no oversold seats 
                    business_oversold = 0 #! what are we supposed to to if undersold? 
                ## economy oversold 
                if econ_seats<econ_sold:
                    econ_oversold = econ_sold - econ_seats 

                else:
                    econ_oversold = 0
        #update result list with new sublist for each plane 
        results_econ.append([model, econ_oversold]) 
        results_business.append([model, business_oversold])
    #output 
    return results_econ, results_business # return both lists of results  
'''
test 1 
fleet_data = [
    ["Boeing 737", 20, 150, 170, "A1", "New York", "On Time", 23.0],
    ["Airbus A320", 15, 140, 155, "B2", "Toronto", "Delayed", 25.0],
    ["Boeing 777", 30, 250, 280, "C3", "London", "On Time", 30.0],
    ["Bombardier Q400", 10, 70, 80, "D4", "Montreal", "On Time", 20.0]
]


daily_data = [
    ["A1", 160, 1],
    ["B2", 0, 1],
    ["C3", 260, 1],
    ["D4", 100, 1]
]


print(oversold (fleet_data, daily_data))

''' 