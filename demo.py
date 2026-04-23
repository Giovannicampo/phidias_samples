from phidias.Types import *
from phidias.Main import *
from phidias.Lib import *

class position(Belief): pass   
class target(Belief): pass     
class priority(Belief): pass  
class moving(Belief): pass              

def_vars('AgentX', 'AgentY', 'NodeA', 'NodeB', 'Px', 'Py')

class deadlock(Goal): pass
deadlock(AgentX, AgentY, NodeA, NodeB) << (
    position(AgentX, NodeA) & target(AgentX, NodeB) &
    position(AgentY, NodeB) & target(AgentY, NodeA) &
    neq(AgentX, AgentY)
)

class set_target(Procedure): pass
class go(Procedure): pass
class resolve_conflict(Procedure): pass
class start_demo(Procedure): pass
class arrive(Procedure): pass

set_target(AgentX, NodeB) >> [
    show_line("\n>>> [INFO] TARGET: ", AgentX, " intends to move to ", NodeB),
    +target(AgentX, NodeB)
]

go(AgentX) / target(AgentX, NodeB) >> [
    show_line(">>> [ACTION] MOTORS: Starting engines for ", AgentX, " towards ", NodeB, "..."),
    +moving(AgentX) 
]

go(AgentX) >> [
    show_line("[ERROR] MOTORS: Cannot start ", AgentX, " - No target destination set!")
]

+moving(AgentX) / deadlock(AgentX, AgentY, NodeA, NodeB) >> [
    show_line("[WARNING] DEADLOCK: Frontal collision risk between ", AgentX, " and ", AgentY, "!"),
    resolve_conflict(AgentX, AgentY)
]

+moving(AgentX) >> [
    show_line("[INFO] PATH: Route is clear for ", AgentX, ".")
]

resolve_conflict(AgentX, AgentY) / (priority(AgentX, Px) & priority(AgentY, Py) & lt(Px, Py) & target(AgentX, NodeB)) >> [
    show_line("[INFO] RESOLUTION: ", AgentX, " (Priority ", Px, ") YIELDS to ", AgentY, " (Priority ", Py, ")."),
    -moving(AgentX),
    -target(AgentX, NodeB),
    show_line("[ACTION] ", AgentX, " stops and clears its current route.")
]

resolve_conflict(AgentX, AgentY) / (priority(AgentX, Px) & priority(AgentY, Py) & gt(Px, Py)) >> [
    show_line("[INFO] RESOLUTION: ", AgentX, " (Priority ", Px, ") HAS RIGHT OF WAY over ", AgentY, " (Priority ", Py, ")."),
    show_line("[ACTION] ", AgentX, " maintains its trajectory.")
]

arrive(AgentX) / (target(AgentX, NodeB) & position(AgentX, NodeA)) >> [
    show_line("\n<<< [SUCCESS] ", AgentX, " has physically arrived at ", NodeB, " (departed from ", NodeA, ")."),
    -position(AgentX, NodeA),  
    +position(AgentX, NodeB),  
    -target(AgentX, NodeB),    
    -moving(AgentX)            
]

arrive(AgentX) >> [
    show_line("\n<<< [ERROR] ", AgentX, " could not arrive at the target.")
]

start_demo() >> [
    set_target('AGV_2', 'North'),
    set_target('AGV_1', 'South'),
    show_line("\n--- [INFO] INTENTIONS DECLARED, STARTING MOVEMENT ---"),
    go('AGV_2'),
    go('AGV_1')
]

if __name__ == '__main__':
    PHIDIAS.assert_belief(position('AGV_1', 'North'))
    PHIDIAS.assert_belief(priority('AGV_1', 10)) 
    
    PHIDIAS.assert_belief(position('AGV_2', 'South'))
    PHIDIAS.assert_belief(priority('AGV_2', 50)) 

    print("\n--- AUTO DEADLOCK DEMO ---")
    PHIDIAS.run(start_demo())
    PHIDIAS.shell(globals())