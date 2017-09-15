import pandas as pd
from scipy.stats import norm
import seaborn as sns
import MySQLdb as mdb
import matplotlib.pyplot as plt
import time

scriptStart = time.time()


sym = ["S&P500"]


#connect to MySQL
def connect_DB():
    db_host = '127.0.0.1'
    db_user = 'root'
    db_pass = '8h^=GP655@740u9'
    db_name = 'lean'
    
    con = mdb.connect(db_host, db_user, db_pass, db_name)
    
    return con


#disconnect from database
def disconnect(con):
    # disconnect from server
    con.close()

    
#get data
def req_sql(sym, con):
    # Select all of the historic close data
    sql = """SELECT DATE_TIME, CLOSE FROM `""" + sym + """` WHERE PERIOD = 1440 ORDER BY DATE_TIME ASC;"""

     #create a pandas dataframe
    df = pd.read_sql_query(sql, con=con, index_col='DATE_TIME')

    return df


#using THE MULTIVARIATE NORMAL VARIANCE–COVARIANCE APPROACH
def VaR(value, confidence_level, returns_mean, returns_volatility):
    alpha = norm.ppf(1-confidence_level, mean, volatility)
    return value - value*(alpha + 1)


if __name__ == "__main__":
    con = connect_DB()
    
    returns = req_sql(sym[0], con).pct_change()
     
    investment_value = 1000
    confidence_level = 0.99
    mean = pd.rolling_mean(returns, window=252)
    volatility = pd.rolling_std(returns, window=252)

    var = VaR(investment_value, confidence_level, mean, volatility)
    var_to_df = pd.DataFrame(var, index=returns.index, columns=["VaR"])
    
    plt.plot(var_to_df)
    plt.show()
    
    disconnect(con)

    timeused = (time.time()-scriptStart)/60

    print("Done in ",timeused, " minutes")  
