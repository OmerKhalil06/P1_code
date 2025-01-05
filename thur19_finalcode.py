def passenger_data():
    """sorts out individual passenger's information from a txt document.
    
    """
    file = open("passenger_data_v1 1.txt")
    passenger_data = [] #creat an empty list
    for line in file: #loop thru each line of the file
        line = line.strip("\n") #get rid of the line-continuation character
        line = line.split(",") #convert string into list
        passenger_data.append(line) #append each passenger into overall list
        
    file.close()
    return passenger_data

passenger_data1 = (passenger_data())

def fleet_data():
    """"
    Reads and processes fleet data from a text file.
    
    Parameter: 
        filename (str): filename of the fleet data file.
    
    Returns:
        list: A 2D list with commas separating each sublist, where each represents a line from the file.
        
    No outputs.

    """
    file = open("fleet_data.txt")
    # Initialize an empty list to store fleet data
    fleet_data = []
    
    for line in file:
        line = line.strip("\n")
        line = line.split(",")
        fleet_data.append(line) # Append processed data to fleet_data
            
    file.close()
    return fleet_data

fleet_data1 = fleet_data()

def daily_data(passenger_data, fleet_data): #! add parameter here
    """
    Passenger and fleet data is used to count business and economy seats per gate.

    Parameters:
        passenger_data (2D list): passenger data
        fleet_data (2D list): fleet data

    Returns:
        output (2D list): list of lists containing [Gate, Business Count, Economy Count].
        
    No outputs.
    """
    # Initialize a list to hold gate info
    gate_summary = []
    
    for plane_info in fleet_data:
            gate = plane_info[4] # Extract gate info
            gate_summary.append([gate, 0, 0]) # Initialize gate entry and initialize business and economy counts as 0

    for passenger_info in passenger_data:
        gate = passenger_info[2] # Extract gate info
        passenger_class = passenger_info[3] # Extract passenger class

        for gate_info in gate_summary:
            if gate_info[0] == gate:   # Find the matching gate in gate_summary
                if passenger_class == "Business":
                    gate_info[1] += 1  # Increment Business Count
                elif passenger_class == "Economy":
                    gate_info[2] += 1  # Increment Economy Count
                break

    return gate_summary
daily_data1=daily_data(passenger_data1,fleet_data1)

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
oversoldE, oversoldB  = oversold(passenger_data1, fleet_data1) #! add fleet data here 

def overweight(passenger_data, fleet_data):
    """Analyzes passenger baggage data and identifies those who exceed the allowed weight limit 
    for their flight's plane model.
    Parameters: passenger_data: passenger data (2D list)
                fleet_data: fleet data (2D list)
    Returns: list of lists containing [Passenger first name, First letter of last name, Gate, Exceeded weight]
             list of lists containing [Plane 1 model, Number of passengers with overweight baggage]
    """
    
    fleet_overweight = [["Boeing 777-300ER",0],["Boeing 777-200LR",0],["Airbus A330-300",0],["Embraer A330-300",0],["Airbus A319-100",0],["Boeing 737 MAX",0],["Airbus A321-200",0]]
    passenger_overweight = []

    for fleet in fleet_data: 
        for passenger in passenger_data:
            if passenger[2] == fleet[4]:#passenger's plane by checking gate
                if float(passenger[6]) > float(fleet[7]): #check if luggage exceeds max weight
                    fleet_overweight[fleet_data.index(fleet)][1] += 1 #fleet-2D list
                    passenger_overweight.append([passenger[0], passenger[1], passenger[2], round(float(passenger[6]) - float(fleet[7]),2)]) #passenger 2D list
    
    return fleet_overweight, passenger_overweight

fleet_overweight, passenger_overweight = overweight(passenger_data,fleet_data)

overweight1 = overweight(passenger_data1, fleet_data1)

#layover function
def layover(passenger_data, fleet_data):
    """
    Processes passenger and fleet data function to find layover passengers and planes with layover passengers
    
    Parameters:
        passenger_data (list): 2D list of passenger data
        fleet_data (list): 2D list of fleet data
        
    Returns:
        Two 2D lists/tuples - list of layover passengers and list of planes with layover passengers
    """
    
    #intializes lists for output
    layover_passengers = []
    layover_plane = []

    #extract layover passengers data from passenger data 
    for passenger in passenger_data:
        #finds data using entry numbers corresponding to needed piece of data, then defines in variable 
        first_name = passenger[0]
        last_name = passenger[1]
        passenger_gate = passenger[2]
        
        #if statement to see if layover status = true
        if len(passenger) >= 8 and passenger[7].strip().lower() == 'layover':
            #appends data for list if condition is met
            layover_passengers.append([first_name, last_name, passenger_gate])

    #determine number of layover passengers per plane
    for fleet in fleet_data:
        #assigns variables for entries in fleet_data
        plane_model = fleet[0]
        gate = fleet[4]
        arrival_status = fleet[6]
        destination = fleet[5]
        num_of_layover_passengers = 0
        
        for passenger in passenger_data:
            #if gate, arrival status, and passenger destination are the same in both fleet_data, and passenger_data, plane layover status = true
            if (passenger[2] == gate and passenger[5] == arrival_status and passenger[4] == destination):
                num_of_layover_passengers += 1
        #appends to second list (for layover plane info)
        layover_plane.append([plane_model, num_of_layover_passengers])
    
    #return both lists
    return layover_passengers, layover_plane


layover_passengers, layover_plane = layover(passenger_data, fleet_data)
layover1 =layover(passenger_data1, fleet_data1)


def graphical_thur19(oversold, overweight, layover):        

    '''this function summarizes information of oversold(),overweight(), layover() and time_delay() functions 
        1. oversold business and economy seats
        2. passengers with overweight bags
        3. passengers that are going to layover
        4. passengers that are going to arrive late and have to layover
        
        and outputs this information intoa graphical interface that is easy to read 
        '''
    
    ### Turtle Graphics ### 
    # Import the turtle module
    import turtle

    ### Process information ### 
    #processing plane information 
    output_strings = ['','Oversold Economy Tickets:','Oversold Business Tickets:',
                      'Overweight Bags:','Layover Passengers:'] # list of strings used in the output, corresponding to different data 
    oversoldE = oversold[0]
    oversoldB = oversold[1]

    plane_data = [] #2d list of each planes information  
    for i in oversoldE: #cycle through sublists in one of the lists of data 
        model = i[0] #take model number 
        oversold_econ = i[1]  #take oversold econ seats 
        result = [model, oversold_econ] #put these avalues into a list to hold the planes information 

        # get other values from each 2d list 
        for index in oversoldB: #cycle through each sublist 
            if index[0] == model: #if the model number is the same 
                result.append(index[1]) # add the corresponding information needed to the result list using indexing and append 

        for index in overweight:
            if index[0] == model:
                result.append(index[1])
        
        for index in layover:
            if index[0] == model:
                result.append(index[1])

        plane_data.append(result)#append the entire sublist 

    # Constants  
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT= 500
    WINDOW_TITLE = 'Graphical_Thur19'

    # Variables 
    box_colours = ['pink', 'light blue', 'orange', 'white'] #list of colours to cycle through when creating graphics 
    x = -400 #initial x coordinate for turtle to start 
    
    # Set up the screen object
    turtle.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = turtle.Screen()
    screen.title(WINDOW_TITLE)
    screen.bgcolor('light grey') 
    screen.tracer(0)

    # Create the turtle object
    t = turtle.Turtle()
    t.hideturtle()

    ## draw boxes 
    colour_index = 0
    for i in plane_data: #cycle through sublists 
        t.fillcolor(box_colours[colour_index]) #change fill colour 
        colour_index+=1 
        y=180 #set/reset height 

        #reposition turtle 
        t.up()
        t.goto(x, y)
        t.down()
        #create box 
        for _ in range (2):
            t.begin_fill()
            t.forward(170)
            t.right(90)
            t.forward(60)
            t.right(90)
            t.end_fill()
        
        t.up()
        t.goto(x+85, y-35)
        t.down()

        #write text 
        t.write(f'{i[0]}', font = ('Times New Roman',12, 'bold'), align = 'center')

        #update variables 
        y-=70
        x+=10

        #cycle through items in sublist and write them 
        counter = 1
        while counter != len(i):
            y-=25 #change y to be 25 down for next movement 

            t.up()
            t.goto(x,y)
            t.down()
            #write informaton 
            t.write(f'{output_strings[counter]} {i[counter]}', font = ('Times New Roman',10, 'normal'),align = 'left')
            counter+=1 #update counter 

        x+=200 # move 200 over for next plane information 

    ##  draw line barriers 
    #define initial position 
    t.right(90)
    x = -207.5
    y = 180
    
    for _ in range(3):
        t.width(4)
        t.up()
        t.goto(x,y)
        t.down()
        t.forward(200)
        x+=212.5 #move 212.5 to the right on next line  

    ## Draw Title 
    #write title 
    t.up()
    t.goto(0,200)
    t.down()
    t.write('Flight Information', font= ('Times New Roman',16, 'bold'),align = 'center' )

    #create underline 
    t.up()
    t.goto(-100,195)
    t.down()
    t.left(90)
    t.forward(200)
    ## create Team ID 
    t.up()
    t.goto(380,-230)
    t.down
    t.write('Thur-19', font = ('Time New Roman', 12, 'bold'))
    # End of code 
    screen.exitonclick() 
    turtle.done()
graphical_thur19(oversoldE, oversoldB,overweight1,layover1)
