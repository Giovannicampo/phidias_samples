from phidias.Types import *
from phidias.Main import *
from phidias.Lib import *

class position(SingletonBelief): pass
class priority(SingletonBelief): pass
class moving(Belief): pass

class task(Belief): pass
class idle(Belief): pass

def_vars('A', 'Dest', 'N1', 'N2', 'P1', 'P2', 'Other')

class deadlock(Goal): pass
deadlock(A, Other) << (
    position(A, N1) & target(A, N2) &
    position(Other, N2) & target(Other, N1) & neq(A, Other)
)

class find_next_task(Procedure): pass
class execute_task(Procedure): pass

+idle(A) >> [ find_next_task(A) ]

find_next_task(A) / task(A, Dest) >> [
    show_line("\n[AUTO] Task trovato per ", A, ": andare a ", Dest),
    -task(A, Dest), 
    execute_task(A, Dest)
]

find_next_task(A) >> [
    show_line("[IDLE] Nessun task per ", A, ". In attesa..."),
    +idle(A) 
]

execute_task(A, Dest) >> [
    +target(A, Dest),
    +moving(A)
]

class reach_destination(Procedure): pass

+moving(A) / deadlock(A, Other) >> [
    show_line("[ALERT] Deadlock con ", Other, "! Valuto priorità..."),
    -moving(A),
    show_line("[LOG] ", A, " si ferma per sicurezza.")
]

+moving(A) >> [
    show_line("[INFO] ", A, " in viaggio..."),
    reach_destination(A)
]

reach_destination(A) / target(A, Dest) >> [
    show_line("[SUCCESS] ", A, " arrivato a ", Dest),
    +position(A, Dest), 
    -target(A, Dest),
    +idle(A)
]

if __name__ == '__main__':
    PHIDIAS.assert_belief(position('AGV_1', 'Stazione_Ricarica'))
    
    PHIDIAS.assert_belief(task('AGV_1', 'Punto_Carico_A'))
    PHIDIAS.assert_belief(task('AGV_1', 'Punto_Scarico_B'))
    PHIDIAS.assert_belief(task('AGV_1', 'Manutenzione_C'))

    PHIDIAS.run()
    
    PHIDIAS.assert_belief(idle('AGV_1'))
    
    PHIDIAS.shell(globals())