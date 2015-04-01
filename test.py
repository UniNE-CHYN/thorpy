from thorpy.comm.discovery import discover_stages

if __name__ == '__main__':
    from thorpy.message import *
    
    stages = list(discover_stages())
    print(stages)
    s = stages[0]
    
    s.home()
    
    s.print_state()
    
    import IPython
    IPython.embed()
    
    #del s, stages
