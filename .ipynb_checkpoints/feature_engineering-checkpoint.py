import pandas as pd
import numpy as np




def feature_creator(df, columns,groupby, function = 'mean',frame='all'):
    """
    Function takes a dataframe and adds the defined features
    
    Inputs
    ---------------
    
        df : DataFrame
            The Input Dataframe with the core data
        
        columns : String / List 
            A String with the column name or a list of column names 
            on which the desired function should be applied

        groupby : String / List
            A String with the column name or a list of column names
            which should be taken for the grouping
            
        function : String
            The Function which should be applied on the columns 
            
        frame : String
            Defines the frame in the group over which the function should be calculated
    
    Outputs
    ---------------
    
        Returns the input Dataframe with the desired function applied
    
    """
    
    selector = []
    new_names = {}
    if isinstance(columns,list):
        for c in columns:
            new_names[c] = f"{function}_{c}_{frame}"
    else:
        new_names[columns] = f"{function}_{columns}_{frame}"
        
        
    if isinstance(columns,list) and isinstance(groupby,list):
        selector = columns + groupby
    elif isinstance(columns,list):
        selector.extend(columns)
        selector.append(groupby)
    elif isinstance(groupby,list):
        selector.extend(groupby)
        selector.append(columns)
    else:
        selector = [columns,groupby]
        
        
    if frame == 'all':
        if function == 'mean':
            tmp = df[selector].groupby(groupby).mean().reset_index()    
        elif function == 'median':
            tmp = df[selector].groupby(groupby).median().reset_index()
        elif function == 'std':
            tmp = df[selector].groupby(groupby).agg(np.std, ddof=1).reset_index()
        elif function == 'min':
            tmp = df[selector].groupby(groupby).min().reset_index()
        elif function == 'max':
            tmp = df[selector].groupby(groupby).max().reset_index()
        elif function == 'count':
            tmp = df[selector].groupby(groupby).size().reset_index()
            new_names[0] = f"{function}_entrys_{frame}"
        elif function == 'sum':
            tmp = df[selector].groupby(groupby).sum().reset_index()
        else:
            raise ValueError("""Unknown function provided. Select one of the defined functions. 
                             For more Information see description of Function""")
    else:
        print("Das hier ist nur ein dummy - das Framing muss noch ergänzt werden")
        return df
    
    
    tmp.rename( new_names, axis=1,inplace=True)
    
    if isinstance(columns,list):
        for value in new_names.values():
            if value in df.columns:
                df.drop(value,axis=1 , inplace=True)
                
                
    elif new_names[columns] in df.columns:
        df.drop(new_names[columns], axis=1 , inplace=True)   
    df = df.merge(tmp, how='inner', on=groupby)
    
    
    return df