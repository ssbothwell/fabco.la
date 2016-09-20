from cuttingstock.GreedySolver import *

class Strainer:    
    def __init__(self, x, y, thickness, quantity, fourQuarter, nineQuarter):
        self.x = x # In Inches
        self.y = y # In Inches
        self.thickness = thickness # In Inches
        self.roughThickness = thickness + 0.25
        self.yBraces = self.braceQuantity(self.x)
        self.xBraces = self.braceQuantity(self.y)

        self.yBraceLength = self.braceLength(self.y)
        self.xBraceLength = self.braceLength(self.x)
        
        self.xBF = self.boardFeet(self.x, 2.25, self.roughThickness, 2)
        self.yBF = self.boardFeet(self.y, 2.25, self.roughThickness, 2)
        self.xBraceBF = self.boardFeet(self.xBraceLength, 2.25, self.roughThickness, self.xBraces)
        self.yBraceBF = self.boardFeet(self.yBraceLength, 2.25, self.roughThickness, self.yBraces)
        self.braceBF = self.xBraceBF + self.yBraceBF
        self.barBF = self.xBF + self.yBF
        
        # Brace and Bar quantity dicts for stock cutting algorithm 
        self.bars = {x+1: quantity * 2, y+1: quantity * 2}
        self.braces = {self.xBraceLength: self.xBraces, self.yBraceLength: self.yBraces}
        
        self.fourQuarterStock = fourQuarter # In Feet
        self.nineQuarterStock = nineQuarter # In Feet
        
    def braceQuantity(self, barLength):
        """ Determines brace spacing """
        spacing = int
        for i in range(1, 20):
            if (barLength / i) <= 26:
                spacing = i - 1
                break
        return spacing

    def braceLength(self, barLength):
        """ Determine brace length """
        return barLength - 3.5
          
    def boardFeet(self, lengthInches, width, thickness, quantity):
        """ Generic board feet calculator """        
        return (((lengthInches/12) * width * thickness)/12)*quantity

    def boardsPerStockLength(self, dict):
        """ Input a Dict of board lengths/quantities and output the ideal cutting pattern """
        
        if __name__ == '__main__':
            #inputp={1380:22,1520:25,1560:12,1710:14,1820:18,1880:18,1930:20,2000:10,2050:12,2100:14,2140:16,2150:18,2200:20}
            #inputp={300:8,700:9,600:6,500:8,400:4}
            inputp=dict
            max_size=120
            a=GreedySolver(inputp,max_size)
            cutPatterns = a.getResult()
            i=1
            realwaste=0
            for combination in cutPatterns:
            	if(max_size-combination.getCombinationSize()<200):
            		realwaste+=max_size-combination.getCombinationSize()
                print str(i)+" " + combination.printCombi() #+" waste = ",max_size-combination.getCombinationSize()
                i+=1
            print "real waste = ",realwaste
        
    def printSpec(self):
        print "%s@%s x %s x %s\"" % (self.quantity, self.x, self.y, self.thickness)
        print ""
        print "Bars:"
        print " 2@ %s\" x %s x 9/4\"" % (self.x, self.thickness)
        print " 2@ %s\" x %s x 9/4\"" % (self.y, self.thickness)
        print ""
        print "Braces:"
        print " %s@ %s\" x 2.25\" x 4/4\"" % (self.xBraces, self.xBraceLength)
        print " %s@ %s\" x 2.25\" x 4/4\"" % (self.yBraces, self.yBraceLength)
        print ""
        print "Optimal Board Feet:"
        print "9/4: %s per unit, %s total" % (self.barBF, self.barBF*self.quantity)
        print "4/4: %s per unit, %s total" % (self.braceBF, self.braceBF*self.quantity)
        print ""
        print ""
        
strainer = Strainer(36, 48, 1.25, 1, 10, 10)
print strainer.boardsPerStockLength(strainer.bars)
#print strainer.boardsPerStockLength(strainer.braces)