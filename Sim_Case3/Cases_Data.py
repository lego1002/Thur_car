from dataclasses import dataclass
from Helper import Helpers

@dataclass
class Case1:
    t1: float    
    t2: float    
    t3: float    
    vmax: float  # Maximum velocity
    omegamax: float  # Maximum Omega

    def v(self, t: float) -> float:
        if t < 0:
            return 0
        elif 0 <= t < self.t1:
            return Helpers._2Dlerp(0, self.t1, 0, self.vmax, t)
        elif self.t1 <= t < self.t2:
            return self.vmax
        elif self.t2 <= t < self.t3:
            return Helpers._2Dlerp(self.t2, self.t3, self.vmax, 0, t)
        else:
            return 0

    def w(self, t: float) -> float:
        return self.omegamax
    
@dataclass
class Case2:
    t1: float    
    t2: float    
    t3: float    
    t4: float
    t5: float
    t6: float
    t7: float
    t8: float
    t9: float
    vmax: float  # Maximum velocity
    omegamax: float  # Maximum Omega

    def v(self, t: float) -> float:
        if t < 0:
            return 0
        elif 0 <= t < self.t1:
            return Helpers._2Dlerp(0, self.t1, 0, self.vmax, t)
        elif self.t1 <= t < self.t2:
            return self.vmax
        elif self.t2 <= t < self.t3:
            return Helpers._2Dlerp(self.t2, self.t3, self.vmax, 0, t)
        elif self.t3 <= t < self.t6:
            return 0
        elif self.t6 <= t < self.t7:
            return Helpers._2Dlerp(0, self.t7, 0, self.vmax, t)
        elif self.t7 <= t < self.t8:
            return self.vmax
        elif self.t8 <= t < self.t9:
            return Helpers._2Dlerp(self.t8, self.t9, self.vmax, 0, t)
        else:
            return 0
        
    def w(self, t: float) -> float:
        if t < self.t3:
            return 0
        elif self.t3 <= t < self.t4:
            return Helpers._2Dlerp(self.t3, self.t4, 0, self.omegamax, t)
        elif self.t4 <= t < self.t5:
            return self.vmax
        elif self.t5 <= t < self.t6:
            return Helpers._2Dlerp(self.t5, self.t6, self.omegamax, 0, t)
        elif t > self.t6:
            return 0
        else:
            return 0
        
@dataclass
class Case3:
    t1: float    
    t2: float    
    t3: float    
    t4: float
    t5: float
    t6: float
    t7: float
    vmax: float  # Maximum velocity
    omegamax: float  # Maximum Omega

    def v(self, t: float) -> float:
        if t < 0:
            return 0
        elif 0 <= t < self.t1:
            return Helpers._2Dlerp(0, self.t1, 0, self.vmax, t)
        elif self.t1 <= t < self.t6:
            return self.vmax
        elif self.t6 <= t < self.t7:
            return Helpers._2Dlerp(self.t6, self.t7, self.vmax, 0, t)
        else:
            return 0
        
    def w(self, t: float) -> float:
        if t < self.t2:
            return 0
        elif self.t2 <= t < self.t3:
            return Helpers._2Dlerp(self.t2, self.t3, 0, self.omegamax, t)
        elif self.t3 <= t < self.t4:
            return self.vmax
        elif self.t4 <= t < self.t5:
            return Helpers._2Dlerp(self.t4, self.t5, self.omegamax, 0, t)
        elif t > self.t5:
            return 0
        else:
            return 0
    

    
    
