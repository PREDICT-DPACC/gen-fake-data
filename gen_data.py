import pandas as pd
import numpy as np

# dfd is data dictionary
dfd= pd.read_csv(r'C:\Users\tashr\Downloads\AMPSCZFormRepository_DataDictionary_2021-05-21.csv')

# df is fake data, initialize it
df= pd.DataFrame(columns= dfd['Variable / Field Name'])

# append 100 empty rows here
N=100
df.record_id= np.random.randint(100,1000,N)

for var in dfd.iterrows():    
    
    var= var[1]
    
    # dfs is each row of df i.e. fake data of each subject
    all_cond_values= []
    for dfs in df.iterrows():
        
        given_cond= var['Choices, Calculations, OR Slider Labels']
        if given_cond is np.nan:
            all_cond_values.append('')
            continue
        
        # assign a three digit random ID
        # dfs.record_id= np.random.randint(100,1000)
        
        if var['Field Type']=='calc':
            
            if 'if(' in given_cond or 'sum(' in given_cond:
                all_cond_values.append('')
                continue
            
            given_cond= given_cond.replace(']','')
            given_cond= given_cond.replace('[','dfs[1].')
            given_cond= given_cond.replace('=','==')
            given_cond= given_cond.lower()
            
            '''
            # parse calculation
            tmp_plus=[]
            for str_plus in given_cond.split('+'):

                tmp_and=[]
                for str_and in str_plus.split('and'):
                    
                    tmp_or=[]
                    for cond in str_and.split('or'):
                        cond= cond.replace('if(',' ')
                        cond= cond.replace(')','')
                        
                        # evaluate condition and obtain result
                        print(cond)
                        try:
                            c,t,f=cond.split(',')
                        except:
                            print(c)
                            
                        # print(c)
                        if eval(c):
                            value= t
                        else:
                            value= f
                            
                        tmp_or.append(value)
                        

                    # rejoin the ors
                    cond_or_new= ' or '.join(tmp_or)
                    tmp_and.append(cond_or_new)
                
                # rejoin the ands
                cond_and_new= ' and '.join(tmp_and)
                tmp_plus.append(cond_and_new)

            # rejoin the pluses    
            cond_new= ' + '.join(tmp_plus)
            '''
            
            cond_value= eval(given_cond)
            
        elif var['Field Type'] in ['radio', 'checkbox', 'dropdown']:
            values= []
            for val_lab in given_cond.split(' | '):
                try:
                    values.append(int(val_lab.split(', ')[0]))
                except:
                    values.append(float(val_lab.split(', ')[0]))
            
            # randomize according to multinomial distribution
            L= len(values)
            prob= [1/L]*L
            cond_value= values[np.where(np.random.multinomial(1,prob))[0][0]]
        
        elif var['Field Type']=='yesno':
            cond_value= 1 if round(np.random.rand()) else 0
        
        
        # print(cond_value)
        
        # ENH randomization
        all_cond_values.append(cond_value)
    
    try:
        df[var['Variable / Field Name']]= all_cond_values
    except:
        print(all_cond_values)
    

df.to_csv(r'C:\Users\tashr\Downloads\fake_data.csv', index= False)
