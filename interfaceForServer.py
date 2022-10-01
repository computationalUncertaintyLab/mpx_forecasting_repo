#mcandrew

class interfaceForServer (object):
    def __init__(self):
        self.clients = []
        self.comm = { "qid":[]           # question id 
                     , "DOA":[]          # Date of access
                     , "interval" :[]    # Support of random variable
                      ,"densityValue":[] # Densit value contained in interval
                      ,"created_time":[]
                      ,"published_time":[]
                      ,"resolve_time":[]
                      #,"target_end_date":[]
                      #,"location_name":[]
                      ,"community_prediction":[]
                      ,"b":[]
                      ,"exponent":[]
                     }
    def today(self):
        from datetime import date
        return date.today().strftime("%Y-%m-%d")

    def extractCommunityPrediction(self,metac,comm):
        N = len(metac.xs)
        self.comm["qid"].extend( [metac.data["id"]]*N )
        self.comm["DOA"].extend( [self.today()]*N )
        self.comm["interval"].extend( metac.xs)
        self.comm["densityValue"].extend( metac.dens )
        self.comm["created_time"].extend( [metac.data["created_time"]]*N )
        self.comm["published_time"].extend( [metac.data["publish_time"]]*N )
        self.comm["resolve_time"].extend( [metac.data["resolve_time"]]*N )
        #self.comm["target_end_date"].extend( [metac.extract_target_end_date()]*N )
        #self.comm["location_name"].extend( [metac.extract_location()]*N )
        self.comm["community_prediction"].extend( [comm]*N)
        self.comm["b"].extend( [metac.b]*N)
        self.comm["exponent"].extend( [metac.exponent]*N )

    def communityPredictions2DF(self):
        import pandas as pd
        predictions = pd.DataFrame(self.comm)
        self.predictions = predictions

    def out(self,quants=False):
        import os

        if os.path.isdir("datalog"):
            pass
        else:
            os.mkdir("datalog")

        if quants:
            self.allQuants.to_csv("./communityquantiles.csv",index=False)
            self.allQuants.to_csv("datalog/{:s}--communityquantiles.csv".format(self.today()) ,index=False)
        else: 
            self.predictions.to_csv("./communitypredictions.csv",index=False)
            self.predictions.to_csv("datalog/{:s}--communitypredictions.csv".format(self.today()) ,index=False)

    def collectAllQuestionIds(self):
        import requests
        client = requests.get("https://www.metaculus.com/api2/questions/?project=1322").json()

        qids= []
        while True:
            for question in client["results"]:
                question = dict(question)
                id = question["id"]
                qids.append(id)
            
            if client["next"] is None:
                break
            else:
                client = requests.get(client["next"]).json()
        return qids
            
    def quantiles(self):
        import numpy as np
        return np.array([0.010, 0.025, 0.050, 0.100, 0.150, 0.200, 0.250, 0.300, 0.350, 0.400, 0.450, 0.500
                        ,0.550, 0.600, 0.650, 0.700, 0.750, 0.800, 0.850, 0.900, 0.950, 0.975, 0.990])
        
    def computeQuantiles(self,DF=None,xvalues=None,yvalues=None,qs=None):
        import numpy as np
        from scipy.optimize import root_scalar as groot
        from interpolator import interpolator
        import pandas as pd
        
        if qs is None:
            qs = self.quantiles()

        if DF is None:
            pass
        else:
            realxvalues, yvalues = list(DF.interval.values), list(DF.densityValue.values)
            xvalues = np.linspace(0,1,201) 
            b, exponent = DF.iloc[0]["b"], DF.iloc[0]["exponent"] 
            
        f = interpolator(xvalues,yvalues)

        def computeCumualtive(mn,f,x):
            from scipy.integrate import quad
            y,err = quad(f,mn,x)
            return y

        mnx = xvalues[0]
        pieces = []
        for x0,x1 in zip(xvalues[:-1],xvalues[1:]):
            pieces.append( computeCumualtive(x0,f,x1) )
        ttl = sum(pieces) # total area under curve
        cdf = np.cumsum(pieces)/ttl

        g = interpolator(xvalues,[0]+list(cdf))
            
        def cumul(x,g,q):
            return g(x) - q

        def findBracket(xvalues,g,q):
            bracket = [ xvalues[0] ]
            for x in xvalues[1:]:
                lowerbracket = bracket[0]

                if cumul(lowerbracket,g,q)* cumul(x,g,q) < 0:
                    bracket.append(x)
                    break
                else:
                    bracket[0] = x
            return bracket

        quantiles = {"quantile":[],"value":[]}
        for q in qs:

            bracket = findBracket(xvalues,g,q)
            
            G = lambda x: cumul(x,g,q)
            comp = groot(G, bracket=bracket, method="ridder" )

            quantiles["quantile"].append(q)
            if exponent==0:
                 quantiles["value"].append( 0 + b*comp.root )
            else:
                quantiles["value"].append( 0 + b* np.exp( exponent*comp.root) )
            
        return pd.DataFrame(quantiles)

    def computeAllQuantiles(self):
        self.allQuants = self.predictions.groupby(["qid"]).apply( lambda d: self.computeQuantiles(d) )
        return self.allQuants

    def mergeQuantilesAndPredictions(self):
        #keys = self.predictions[["qid","DOA","created_time","published_time","resolve_time","target_end_date","location_name"]].drop_duplicates()
        keys = self.predictions[["qid","DOA","created_time","published_time","resolve_time"]].drop_duplicates()
        self.allQuants = self.allQuants.merge(keys,on="qid")
        return self.allQuants
            
if __name__ == "__main__":
    pass

