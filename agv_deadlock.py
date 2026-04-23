from phidias.Types import *
from phidias.Main import *
from phidias.Lib import *

class position(SingletonBelief): pass
class target(SingletonBelief): pass
class priority(SingletonBelief): pass

class moving(Belief): pass

def_vars('AgentX', 'AgentY', 'NodeA', 'NodeB', 'Px', 'Py')

class deadlock(Goal): pass

deadlock(AgentX, AgentY) << (
    position(AgentX, NodeA) & target(AgentX, NodeB) &
    position(AgentY, NodeB) & target(AgentY, NodeA) &
    neq(AgentX, AgentY)
)

class route_to(Procedure): pass
class resolve_conflict(Procedure): pass

route_to(AgentX, NodeB) >> [
    show_line("\n[COMMAND] Routing ", AgentX, " to ", NodeB),
    +target(AgentX, NodeB),
    +moving(AgentX)
]

+moving(AgentX) / deadlock(AgentX, AgentY) >> [
    show_line("[ALERT] Deadlock detected between ", AgentX, " and ", AgentY, "!"),
    resolve_conflict(AgentX, AgentY)
]

+moving(AgentX) >> [
    show_line("[INFO] Path is clear. ", AgentX, " is moving.")
]

resolve_conflict(AgentX, AgentY) / (priority(AgentX, Px) & priority(AgentY, Py) & lt(Px, Py)) >> [
    show_line("   -> ", AgentX, " yields to ", AgentY, " (Priority: ", Px, " < ", Py, ")"),
    -moving(AgentX),
    show_line("   -> ", AgentX, " halts and waits for clearance.")
]

resolve_conflict(AgentX, AgentY) / (priority(AgentX, Px) & priority(AgentY, Py) & gt(Px, Py)) >> [
    show_line("   -> ", AgentX, " asserts right-of-way over ", AgentY, " (Priority: ", Px, " > ", Py, ")"),
    show_line("   -> ", AgentX, " flashes lights and waits for ", AgentY, " to yield.")
]

resolve_conflict(AgentX, AgentY) >> [
    show_line("   -> STANDOFF! Both agents have equal priority. Requesting central orchestration...")
]

if __name__ == '__main__':
    PHIDIAS.assert_belief(position('AGV_1', 'Corridor_North'))
    PHIDIAS.assert_belief(priority('AGV_1', 10))
    
    PHIDIAS.assert_belief(position('AGV_2', 'Corridor_South'))
    PHIDIAS.assert_belief(priority('AGV_2', 50))

    # Start the engine
    PHIDIAS.run()
    
    print("\n--- PHIDIAS AGV SYSTEM INITIALIZED ---")
    print("Welcome to the interactive shell. Type your commands!")
    
    # Start the interactive shell to show live commands
    PHIDIAS.shell(globals())