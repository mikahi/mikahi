# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 09:59:44 2016

@author: mikalimcaoco
"""

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

#find intercept

loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')


loansData['Interest.Rate'] = loansData['Interest.Rate'].map(lambda x: x.rstrip('%'))
loansData['Interest.Rate'] = loansData['Interest.Rate'].astype(float)
loansData['Loan.Length'] = loansData['Loan.Length'].map(lambda x: x.rstrip('months'))

loansData['FICO.Score'] = loansData['FICO.Range']
loansData['FICO.Score'] = loansData['FICO.Range'].map(lambda x: x.split('-'))
loansData['FICO.Score'] = loansData['FICO.Score'].map(lambda x: int(x[0]))

ir_tf = [0 if x < 12 else 1 for x in loansData['Interest.Rate'].tolist()]
loansData['IR_TF'] = ir_tf

intercept = [1.0] * len(loansData)
loansData['Intercept'] = intercept

#why is intercept always 1

ind_vars = ['Intercept', 'Amount.Requested', 'FICO.Score']

logit = sm.Logit(loansData['IR_TF'], loansData[ind_vars])
result = logit.fit()
coeff = result.params
print(coeff)
e= 2.71


def logistic_function(FicoScore, LoanAmount,coeff):
    prob = 1/(1+e**(coeff[0]+coeff[2]*FicoScore+coeff[1]*LoanAmount))
    if prob >0.7:
        p=1
    else:
        p=0
    return prob, p
    # dont understadn what happens after this 
prob = logistic_function (720, 10000, coeff)[0]
decision = logistic_function(720, 10000,coeff)[1]


Fico = range(550,950,10)
p_plus = []
p_minus = []
p=[]
for j in Fico:
    p_plus.append(1/(1+e**(coeff[0]+coeff[2]*j+coeff[1]*10000)))
    p_minus.append(1/(1+e**(-coeff[0]-coeff[2]*j-coeff[1]*10000)))
    p.append(logistic_function(j, 10000,coeff)[1])
    
plt.plot(Fico, p_plus, label = 'p(x) = 1/(1+e**(b+mx))', color = 'blue')
plt.hold(True)
plt.plot(Fico, p_minus, label = 'p(x) = 1/(1+e**(-b-mx))', color = 'green')    
plt.hold(True)
plt.plot(Fico, p, 'ro', label = 'Decision for 10000 USD')
plt.legend(loc='upper right')
plt.xlabel('Fico Score')
plt.ylabel('Probability and decision, yes = 1, no = 0')
    
