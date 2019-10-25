import cvxpy as cp

requests = [
  {"name":'Firewall', "nPoP":'c1', "cost":10},
  {"name":'DPI', "nPoP":'c1', "cost": 8},
  {"name":'DNS', "nPoP":'c1', "cost": 1},
  {"name":'Firewall', "nPoP":'c2', "cost": 8},
  {"name":'LoadBalancer', "nPoP":'c2', "cost": 7},
  {"name":'IPSec', "nPoP":'c2', "cost": 6}
]

capacities = [
  {"nPoP": 'c1', "capacity": 9},
  {"nPoP": 'c2', "capacity": 9}
]

#Add a variable to each item in requests
for w in requests:
    w['var'] = cp.Variable(boolean=True)

#Add up all the cost variables from each category
requests_summed_by_nPoP = dict()
for w in requests:
    if w['nPoP'] in requests_summed_by_nPoP:
        requests_summed_by_nPoP[w['nPoP']] += w['cost']*w['var']
    else:
        requests_summed_by_nPoP[w['nPoP']] = w['cost']*w['var']

#Create a list of capacity constraints from the summed cost variables
constraints = []
for d in capacities:
    if d['nPoP'] in requests_summed_by_nPoP:
        constraints.append(requests_summed_by_nPoP[d['nPoP']]<=d['capacity'])

#Create the objective function
obj = cp.Maximize(cp.sum([requests_summed_by_nPoP[d['nPoP']] for d in capacities]))

#Create a problem instance
prob = cp.Problem(obj, constraints)

#Solve the problem and catch the optimal value of the objective
val = prob.solve()

#Print the amount assigned to each cost
for w in requests:
    print("Allocate  {0} {1}".format(int(round(w['var'].value)), w['name']))