'''
IPL class is to address the IPL bench problem.
we are formulating this in teh form of a adjacency matrix graph

'''
class IPL:

    '''
    Below function is mainly to initilize memeber variables of the the IPL class
    '''
    def __init__(self,inputfile):            
        self.PlayerTeam =  []
        # Check the number of players & franchises in the input file to dynamically allocate the adjacency matrix array.    
        self.masterLst =[]
        with open(inputfile, "r") as fp: 
            Lines = fp.readlines() 
            for line in Lines:
                for word in (line.strip().split("/")):
                    self.masterLst.append(word.strip())
        self.masterLst = list(set(self.masterLst))
        self.max_vertex = len(self.masterLst)
        self.edges = [[0] * self.max_vertex for _ in range(self.max_vertex)]    # Matrix to store directed edges (association)
        self.num_of_vertex = 0                                                    # Number of the vertexes
        self.file_out = "outputPS10.txt"
        f = open(self.file_out, 'w')
        f.close()
        
    '''
    Insertng a vertex to the given array
    counting the total vertex added in a array
    '''
    def insert_vertex(self, vertex):                                   
        if vertex not in self.PlayerTeam: 
            self.PlayerTeam.append(vertex)
            self.num_of_vertex += 1
            
    '''
    provide index of the vertex
    '''
    def fetch_vertex_index(self, key):
        return self.PlayerTeam.index(key)
       
    '''
    insert edges to 2D array
    '''
    def insert_edge(self, from_key, to_key):       
        self.insert_vertex(to_key)
        self.edges[self.fetch_vertex_index(from_key)][self.fetch_vertex_index(to_key)] = 1      
   
    '''
    Reading the input file from the
    '''
    def readInputfile(self, inputfile):
        with open(inputfile) as input_file_reader:
            line = input_file_reader.readline()
            while line != '':
                player_team = [team.strip() for team in line.split('/')]                                
                self.insert_vertex(player_team[0])
                for item in player_team[1:]:  
                    self.insert_edge (player_team[0], item)                             
                line = input_file_reader.readline()
            input_file_reader.close()      

    '''
    Prompt file is used as input to read teh instructions and then provide the necessary output
    ''' 
    def readPromptsfile(self, inputfile):
        with open(inputfile) as input_file_reader:
            line = input_file_reader.readline()
            while line != '':
                prompt = [prompts.strip() for prompts in line.split(':')]              
                if (prompt[0] == "findFranchise"):                    
                    iplobj.displayFranchises(prompt[1])
                if (prompt[0] == "listPlayers"):                    
                    iplobj.displayPlayers(prompt[1])
                if (prompt[0] == "franchiseBuddies"):                    
                    iplobj.franchiseBuddies(prompt[1], prompt[2] )    
                if (prompt[0] == "playerConnect"):                    
                    iplobj.findPlayerConnect(prompt[1], prompt[2] )  
                line = input_file_reader.readline()
        input_file_reader.close()      
    
    '''
    Display the name of franchise and the players
    '''
    def displayAll(self):
        list_franchise= []
        list_players = []
        num_of_franchise = 0
        num_of_players = 0
        
        for i in range(self.num_of_vertex):
            found_player = 0
            for j in range(self.num_of_vertex):
                if (self.edges[i][j] != 0):
                    list_players.append(self.PlayerTeam[j])
                    found_player = 1
                    num_of_players += 1
            if (found_player):
                list_franchise.append(self.PlayerTeam[i])
                num_of_franchise += 1
         
        with open(self.file_out,"a") as fp:            
            fp.write ("\n--------Function displayAll--------")
            fp.write ("\nTotal no. of franchises: {0}".format(num_of_franchise))
            fp.write ("\nTotal no. of players: {0}".format(num_of_players))        
            fp.write ("\nList of Franchises:\n")
            fp.write ('\n'.join(list_franchise))        
            fp.write ("\n\nList of players:\n")
            fp.write ('\n'.join(list_players))
            fp.write ("\n-----------------------------------")
        fp.close()
        
    '''
    display the franchise name for the given input player. 
    '''
    def displayFranchises(self, player):    
        franchise_list = []
        player_index = self.fetch_vertex_index(player)       
        for i in range(self.num_of_vertex):
            for j in range(self.num_of_vertex):
                if (self.edges[i][j] != 0 and j == player_index):
                    if self.PlayerTeam[i] not in franchise_list: 
                        franchise_list.append(self.PlayerTeam[i])                       
        with open(self.file_out,"a") as fp:                        
            fp.write ("\n\n--------Function displayFranchises --------")
            fp.write ("\nPlayer name: {0}".format(player))
            fp.write ("\nList of Franchises:\n")
            fp.write ('\n'.join(franchise_list))
            fp.write ("\n-------------------------------------------")
        fp.close()
    
    '''
    display the player names for the given franchise
    '''
    def displayPlayers(self, franchise):
        players_list = []
        
        player_index = self.fetch_vertex_index(franchise)
        
        
        for j in range(self.num_of_vertex):
            if (self.edges[player_index][j] != 0):
                if self.PlayerTeam[j] not in players_list: 
                    players_list.append(self.PlayerTeam[j])
        
        with open(self.file_out,"a") as fp:
            fp.write ("\n\n--------Function displayPlayers --------")
            fp.write ("\nPlayer name: {0}".format(franchise))
            fp.write ("\nList of players:\n")
            fp.write ('\n'.join(players_list))
            fp.write ("\n-------------------------------------------")
        fp.close()    
   
    '''
    provides  the team index value
    
    '''
    def fetchTeamIndexForPlayers(self, playerA, playerB):
        player_a_index = self.fetch_vertex_index(playerA)
        player_b_index = self.fetch_vertex_index(playerB)
        
        playerA_teams = [None]*2
        playerB_teams = [None]*2
        for i in range(self.num_of_vertex):
            if (self.edges[i][player_a_index]):
                if (playerA_teams[0] == None) :
                    playerA_teams[0] = i
                else :
                    playerA_teams[1] = i
            if (self.edges[i][player_b_index]):
                if (playerB_teams[0] == None) :
                    playerB_teams[0] = i
                else :
                    playerB_teams[1] = i
        return playerA_teams, playerB_teams
        
    '''
    identify if the players are in the same franchise
    '''
    def franchiseBuddies(self, playerA, playerB):
        player_a_index = self.fetch_vertex_index(playerA)
        player_b_index = self.fetch_vertex_index(playerB)
        count = 0;
        team_buddy = []
        for i in range(self.num_of_vertex):
            if (self.edges[i][player_a_index] and self.edges[i][player_b_index]):
                team_buddy.append(self.PlayerTeam[i])
                count += 1              
        
        with open(self.file_out,"a") as fp:
            fp.write ("\n\n--------Function franchiseBuddies --------")
            fp.write ("\nPlayer A: {0}".format(playerA))
            fp.write ("\nPlayer B: {0}".format(playerB))
            if (count):
                fp.write ("\nFranchise Buddies: Yes, ")
                fp.write ('\n'.join(team_buddy))
            else :
                fp.write ("\nThey never playered together")
            fp.write ("\n------------------------------------------")
        fp.close() 
    '''
    Verify if the players are connected based on other player who shares the two same franchises.
    '''
    def findPlayerConnect(self, playerA, playerB):  
        playerA_teams, playerB_teams = self.fetchTeamIndexForPlayers(playerA, playerB)      
        found_player = False;
        
        with open(self.file_out,"a") as fp:
            fp.write  ("\n--------Function findPlayerConnect --------")
            fp.write  ("\nPlayer A: {0}".format(playerA))
            fp.write  ("\nPlayer B: {0}".format(playerB))
        fp.close()          
        for player_a in range (2) :
            if (playerA_teams[player_a] == None): 
                continue                        
            for player_b in range(2) :
                if (playerB_teams[player_b] == None): 
                    continue    
                for edge in range(self.num_of_vertex):
                    if (self.edges[playerA_teams[player_a]][edge] and self.edges[playerB_teams[player_b]][edge]):
                        with open(self.file_out,"a") as fp:
                            fp.write  ('\nRelated: Yes, {0} > {1} > {2} > {3} > {4}'.format(playerA, self.PlayerTeam[playerA_teams[player_a]],self.PlayerTeam[edge], self.PlayerTeam[playerB_teams[player_b]], playerB))
                        fp.close()     
                        found_player = True

        if (False == found_player):
            with open(self.file_out,"a") as fp:
                fp.write  ("\nNo common player found between planyers {0} and {1}".format(playerA, playerB))
            fp.close()     

        with open(self.file_out,"a") as fp:            
            fp.write  ("\n-------------------------------------------")
        fp.close() 
        
if __name__ == "__main__":
    iplobj = IPL("inputPS10.txt")
    iplobj.readInputfile("inputPS10.txt")
    iplobj.readPromptsfile("promptsPS10.txt")
    iplobj.displayAll()

    