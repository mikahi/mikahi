# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 16:23:41 2016

@author: mikalimcaoco
"""


import pandas as pd
import numpy as np 
import statsmodels.api as sm


loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

loansData['Interest.Rate'] = loansData['Interest.Rate'].map(lambda x: x.rstrip('%'))
loansData['Interest.Rate'] = loansData['Interest.Rate'].astype(float)
loansData['Loan.Length'] = loansData['Loan.Length'].map(lambda x: x.rstrip('months'))

loansData['FICO.Score'] = loansData['FICO.Range']
loansData['FICO.Score'] = loansData['FICO.Range'].map(lambda x: x.split('-'))
loansData['FICO.Score'] = loansData['FICO.Score'].map(lambda x: int(x[0]))

intrate = loansData['Interest.Rate']
intrate[np.isnan(intrate)]=0
loanamt = loansData['Amount.Requested']
loanamt[np.isnan(loanamt)] =0
fico = loansData['FICO.Score']
fico[np.isnan(fico)] = 0
monthly_income = loansData['Monthly.Income']
monthly_income[np.isnan(monthly_income)] = 0
house_ownership = loansData['Home.Ownership']
house_ownership = [4 if x == 'OWN' else 3 if x == 'MORTGAGE' else 2 if x == 'RENT' else 1 if x == 'OTHER' else 0 for x in house_ownership]



y = np.matrix(intrate).transpose()
x1 = np.matrix(fico).transpose()
x2= np.matrix(loanamt).transpose()
x3=np.matrix(monthly_income).transpose()
x4=np.matrix(house_ownership).transpose()


#need this stuff onwards explained

x = np.column_stack([x1,x2,x3,x4])

X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()


#what is f.params[xy]
print 'Coefficients: ', f.params[0:2]
print 'Intercept: ', f.params[2]
print 'P-Values: ', f.pvalues
print 'R-Squared: ', f.rsquared
