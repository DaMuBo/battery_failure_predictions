import pandas as pd
import numpy as np
import logging





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
            tmp = df[selector].groupby(groupby, observed=True).expanding().mean().reset_index().sort_index()
        elif function == 'median':
            tmp = df[selector].groupby(groupby, observed=True).expanding().median().reset_index().sort_index()  
        elif function == 'std':
            tmp = df[selector].groupby(groupby, observed=True).expanding().std().reset_index().sort_index()
            #.agg(np.std, ddof=1)  
        elif function == 'min':
            tmp = df[selector].groupby(groupby, observed=True).expanding().min().reset_index().sort_index()  
        elif function == 'max':
            tmp = df[selector].groupby(groupby, observed=True).expanding().max().reset_index().sort_index()  
        elif function == 'count':
            tmp = df[selector].groupby(groupby, observed=True).expanding().count().reset_index().sort_index()  
        elif function == 'sum':
            tmp = df[selector].groupby(groupby, observed=True).expanding().sum().reset_index().sort_index()  
        else:
            raise ValueError("""Unknown function provided. Select one of the defined functions. 
                             For more Information see description of Function""")
        tmp[columns] = tmp[columns].apply(pd.to_numeric, downcast="float")
    else:
        logging.info("Das hier ist nur ein dummy - das Framing muss noch ergänzt werden")
        return df
    
    tmp.rename( new_names, axis=1,inplace=True)
    tmp.drop("level_2",axis=1,inplace=True)
    
    for value in new_names.values():
        df[value] = tmp[value]

    logging.info(f"<<< Added new feature function {function} to columns {columns} >>>")
    return df




def target_creator(df,column = 'relativeTime',groupby= ['batteryname','zyklus'] , target = "target"):
    """
    Function takes a dataframe and calculates an target variable on it
    
    Inputs
    ---------------
    
        df : DataFrame
            The Input Dataframe with the core data
        
        column : String
            The column name which defines the target variable
        
        groupby : List
            The grouping function to get the max value out of it 
        
        target : String
            Defined the name of the column where the value will be stored
        
        

    
    Outputs
    ---------------
    
        Returns the input Dataframe with the desired target column applied
    
    """
    selector = groupby +[column]
    tmp = df[selector].groupby(groupby, observed=True).max().reset_index().sort_index()
    
    data = df.merge(tmp, how='inner',on=groupby)
    data[target] = data[f"{column}_y"] - data[f"{column}_x"]
    
    logging.info(f"<<< Created target value out of {column} >>>")
    
    return data['target']