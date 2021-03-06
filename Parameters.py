# In this script I define the class Param which can be used to initialise and save parameters or import and save them. 
# For the second model we covert the secondary network to a minimum spanning tree by using Kruskhal's algorithm on distance_matrix_SN.



import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree


# Defining the class Param


class Param:
    
# The __init__ function which is used to initalise an object of class Param

    def __init__(self, N = None,P = None ,L = None ,K = None, H = None ,ql = None, qk = None ,
                 rk = None , sk = None, rh = None ,sh = None , V = [], S = [], W= [], A = [],
                 Com = [], B = [], distance_matrix_PN  = [], distance_matrix_SN =[], demand =[],
                 m = [], g = [], f = [], Btc =[], Ch=[], Pa =[], subtrees =[], uprime = None, 
                 lprime = None):
        
        self.N = N     # Total number of vertices in the networks
        self.P = P     # Number of time periods 
        self.L = L     # Number of vehicles serving the primary network
        self.K = K     # Number of vehicles serving one tree in the secondary network
        self.H = H     # Numeber of trees in the secondary network     
        self.ql = ql   # Capacity of primary network vehicles
        self.qk = qk   # Capacity of secondary network vehciles
        self.rk = rk   # Maximum route time allowed for vehicle on secondary network
        self.sk = sk   # Average speed of a vehicle on secondary network
        self.rh = rh   # Maximum route time allowed for vehilcle on a prmary network
        self.sh = sh   # Average speed of a vehicle on primary network
        self.V = V     # Set of all vertices 
        self.S = S     # Set of vertices on a secondary network
        self.W = W     # Set of vertices in primary network
        self.A = A
        self.Com = Com  # Set of commodities part of relief supply
        self.B = B
        self.distance_matrix_PN = distance_matrix_PN  # Cost matrix of primary network
        self.distance_matrix_SN = distance_matrix_SN  # Cost matrix of secondary network
        self.demand = demand   # list containing demand of commodities at different vertices
        self.m = m   # list containing demand at different vertices for different commodities
        self.g = g   # service time for primary vehicles 
        self.f = f   # service time for secondary vehicles
        self.Btc = Btc  # list of availablity of commoditites in different time periods
        self.uprime = uprime
        self.lprime = lprime
        self.Ch = Ch  # List of list of childrens for each vertices
        self.Pa= Pa   # List of parents for each children 
        self.subrees = subtrees  # List of list of subtrees at each vertex
        
  # The method getParamModel1 is used to import data and process it to get the parameters for model 1

    def getParamModel1(self, PATH, sheetname1, sheetname2, sheetname3, sheetname4, sheetname5,sheetname6):
        
        df1 = pd.read_excel(PATH,sheetname= sheetname1,na_values=None)
        df2 = pd.read_excel(PATH,sheetname= sheetname2,na_values=None)
        df3 = pd.read_excel(PATH,sheetname= sheetname3,na_values=None)
        df4 = pd.read_excel(PATH,sheetname= sheetname4,na_values=None)
        df5 = pd.read_excel(PATH,sheetname= sheetname5,na_values=None)
        df6 = pd.read_excel(PATH,sheetname= sheetname6,na_values=None)
        
        self.N = df1[df1['Parmeters'] == 'N']['Values']
        self.P = df1[df1['Parmeters'] == 'P']['Values']
        self.L = df1[df1['Parmeters'] == 'L']['Values']
        self.K = df1[df1['Parmeters'] == 'K']['Values']
        self.H = df1[df1['Parmeters'] == 'H']['Values']
        self.ql = df1[df1['Parmeters'] == 'ql']['Values']
        self.qk = df1[df1['Parmeters'] == 'qk']['Values']
        self.rk = df1[df1['Parmeters'] == 'rk']['Values']
        self.sk = df1[df1['Parmeters'] == 'sk']['Values']
        self.rh = df1[df1['Parmeters'] == 'rh']['Values']
        self.sh = df1[df1['Parmeters'] == 'sh']['Values']

        self.V = df2['V']
        self.S = df2['S']
        self.W = df2['W']
        self.A = df2['A']
        self.Com = df2['Com']
        self.B = df2['B']
        self.g = df2['g']
        self.f = df2['f']
        
        self.Btc = df3.as_matrix().tolist()
        
        self.distance_matrix_PN = df4.as_matrix().tolist()
        for i in range(len(self.distance_matrix_PN)):
            for j in range(len(self.distance_matrix_PN[i])):
                self.distance_matrix_PN[i][j]= int(self.distance_matrix_PN[i][j])
        for i in range(len(self.distance_matrix_PN)):
            for j in range(len(self.distance_matrix_PN[i])):
                if self.distance_matrix_PN[i][j]==0:
                    self.distance_matrix_PN[i][j]=None
                if i>j:
                    self.distance_matrix_PN[i][j] = self.distance_matrix_PN[j][i]
                    
        self.distance_matrix_SN = df5.as_matrix().tolist()
        for i in range(len(self.distance_matrix_SN)):
            for j in range(self.distance_matrix_SN[i]):
                self.distance_matrix_SN[i][j]= int(self.distance_matrix_SN[i][j])
        for i in range(len(self.distance_matrix_SN)):
            for j in range(len(self.distance_matrix_SN[i])):
                if self.distance_matrix_SN[i][j]==0:
                    self.distance_matrix_SN[i][j]=1000000
                if i>j:
                    self.distance_matrix_SN[i][j] = self.distance_matrix_SN[j][i]
                    
        for t in range(self.P):       
            self.demand = df6.as_matrix().tolist()
        for t in range(self.P):
            for i in self.V: 
                for c in self.Com:
                    self.demand[t][i][c]= int(self.demand[t][i][c])
                    if self.demand[t][i][c]== 0:
                        self.demand[t][i][c]= None
        for i in self.V:
            for c in self.Com:
                for t in range(self.P):
                    self.m[i][t][c]=self.demand[t][i][c]
                    
        return self 

  # The method getParamModelTree is used to import data and process it to get the parameters for model 2 or the tree model  

        def getParamModelTree(self, PATH, sheetname1, sheetname2, sheetname3, sheetname4, sheetname5,sheetname6):
        
            df1 = pd.read_excel(PATH,sheetname= sheetname1,na_values=None)
            df2 = pd.read_excel(PATH,sheetname= sheetname2,na_values=None)
            df3 = pd.read_excel(PATH,sheetname= sheetname3,na_values=None)
            df4 = pd.read_excel(PATH,sheetname= sheetname7,na_values=None)
            df5 = pd.read_excel(PATH,sheetname= sheetname5,na_values=None)
            df6 = pd.read_excel(PATH,sheetname= sheetname6,na_values=None)
            
            self.N = df1[df1['Parmeters'] == 'N']['Values']
            self.P = df1[df1['Parmeters'] == 'P']['Values']
            self.L = df1[df1['Parmeters'] == 'L']['Values']
            self.K = df1[df1['Parmeters'] == 'K']['Values']
            self.H = df1[df1['Parmeters'] == 'H']['Values']
            self.ql = df1[df1['Parmeters'] == 'ql']['Values']
            self.qk = df1[df1['Parmeters'] == 'qk']['Values']
            self.rk = df1[df1['Parmeters'] == 'rk']['Values']
            self.sk = df1[df1['Parmeters'] == 'sk']['Values']
            self.rh = df1[df1['Parmeters'] == 'rh']['Values']
            self.sh = df1[df1['Parmeters'] == 'sh']['Values']
    
            self.V = df2['V']
            self.S = df2['S']
            self.W = df2['W']
            self.A = df2['A']
            self.Com = df2['Com']
            self.B = df2['B']
            self.g = df2['g']
            self.f = df2['f']
            self.Btc = df3.as_matrix().tolist()
            
            self.distance_matrix_PN = df4.as_matrix().tolist()
            for i in range(len(self.distance_matrix_PN)):
                for j in range(len(self.distance_matrix_PN[i])):
                    self.distance_matrix_PN[i][j]= int(self.distance_matrix_PN[i][j])
            for i in range(len(self.distance_matrix_PN)):
                for j in range(len(self.distance_matrix_PN[i])):
                    if self.distance_matrix_PN[i][j]==0:
                        self.distance_matrix_PN[i][j]=None
                    if i>j:
                        self.distance_matrix_PN[i][j] = self.distance_matrix_PN[j][i]
             
        # Getting the Minimum Spanning Tree of the secondary network using Krushkal's MST algorihm.
        
            self.distance_matrix_SN = df5.as_matrix()
            Tcsr = minimum_spanning_tree(self.distance_matrix_SN)
            self.distance_matrix_SN= Tcsr.toarray().astype(int)
            self.distance_matrix_SN= self.distance_matrix_SN.tolist()
            
            for i in range(len(self.distance_matrix_SN)):
                for j in range(len(self.distance_matrix_SN[i])):
                    self.distance_matrix_SN[i][j]= int(self.distance_matrix_SN[i][j])
            for i in range(len(self.distance_matrix_SN)):
                for j in range(len(self.distance_matrix_SN[i])):
                    if self.distance_matrix_SN[i][j]==0:
                        self.distance_matrix_SN[i][j]=None
                    if i>j:
                        self.distance_matrix_SN[i][j]=self.distance_matrix_SN[j][i]
                        
            for t in range(self.P):       
                self.demand = df6.as_matrix().tolist()
            for t in range(self.P):
                for i in self.V: 
                    for c in self.Com:
                        self.demand[t][i][c]= int(self.demand[t][i][c])
                        if self.demand[t][i][c]== 0:
                            self.demand[t][i][c]= None
                            
            for i in self.V:
                for c in self.Com:
                    for t in range(self.P):
                        self.m[i][t][c]=self.demand[t][i][c]
             
            # Getting Children Nodes for each node
                                    
            self.Ch= [None for x in self.V]
            j=1
            i=0
            a=1
            order_of_search=[]
            while len(order_of_search) < self.N-1:
                if i!=0 and max(order_of_search)<self.N:
                    a=max(order_of_search) + 1 
                order_of_search.append(a)
                while i < len(order_of_search) or i==0 :
                    j=1
                    b=order_of_search[i]
                    while j < len(self.distance_matrix_SN[b]):
                        if self.distance_matrix_SN[b][j] != None:
                            if self.Ch[b]== None:
                                if self.Ch[j]!= None:
                                    if self.Ch[j].count(b)==0:
                                        self.Ch[b]=[]
                                        self.Ch[b].append(j)
                                        order_of_search.append(j)
                                else:
                                    self.Ch[b]=[]
                                    self.Ch[b].append(j)
                                    order_of_search.append(j)
                            
                            elif self.Ch[b].count(j)==0:
                                if self.Ch[j]!= None:
                                    if self.Ch[j].count(b)==0:
                                        self.Ch[b].append(j)
                                        order_of_search.append(j)
                                else:
                                    self.Ch[b].append(j)
                                    order_of_search.append(j) 
                        j=j+1
                    i=i+1   
                        
            
            for i in range(len(self.distance_matrix_SN)):
                for j in range(len(self.distance_matrix_SN[i])):
                    if self.distance_matrix_SN[i][j]==None:
                        self.distance_matrix_SN[i][j]=1000000        
                       
             # Getting Parent Node of each child
            
            self.Pa = [None for x in self.V]
            for i in range(len(self.Ch)):
                if self.Ch[i] !=None:
                    for j in self.Ch[i]:
                        self.Pa[j]=i
                        
             # Getting subtrees in the tree
             
            self.subtrees = [None for x in self.V]
            for i in range(len(self.Ch)):
                if self.Ch[i]!= None:
                    j=0
                    self.subtrees[i]=self.Ch[i]
                    while j<len(self.subtrees[i]):
                        if self.Ch[self.subtrees[i][j]] != None:
                            self.subtrees[i]= self.subtrees[i]+ self.Ch[self.subtrees[i][j]]
                        j=j+1
                         
            return self
        
        
        
        

                        
             
                                
            
                        
        
                            

