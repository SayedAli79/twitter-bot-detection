import numpy as np
#import scipy
from pandas import DataFrame 

class Entropy:

    def calc_entropy(X):
        """
        Calculate entropy given a pandas Series, list, or numpy array.
        """
        probabilities = [float(len(X[X == c]))/float(len(X)) for c in set(X)]
        
        # Initialize the entropy to 0.
        entropy = 0
        # Loop through the probabilities, and add each one to the total entropy.
        for prob in probabilities:
            if prob > 0:
                entropy += prob * math.log(prob, 2)
    
        return -entropy

    @classmethod    
    def df_fill(cls,sample1,sample2,name_col):
        total_len = len(sample1) + len(sample2) 
        target_df = DataFrame(columns=['user',name_col], index=range(total_len))
        target_df['user'] = list([0]*len(sample1)) + list([1]*len(sample2))
        target_df[name_col] = list(sample1) + list(sample2)
        return target_df

    def calc_information_gain(data, split_name, target_name):
        """
        Calculate information gain given a dataset, column to split on, and target.
        """
        # Calculate original entropy.
        original_entropy = calc_entropy(data[target_name])
    
        # Find the median of the column we're splitting.
        column = data[split_name]
        median = column.median()
    
        # Make two subsets of the data based on the median.
        left_split = data[column <= median]
        right_split = data[column > median]
    
        # Loop through the splits, and calculate the subset entropy.
        to_subtract = 0
        for subset in [left_split, right_split]:
            prob = (float(subset.shape[0]) / float(data.shape[0])) 
            to_subtract += prob * calc_entropy(subset[target_name])
    
        # Return information gain.
        return original_entropy - to_subtract

    @classmethod
    def information_gains(cls,Accountrep_human,Accountrep_bot,tweetdens_human,tweetdens_bot
               ,weekday_human,weekday_bot,mentions_human,mentions_bot
               ,voc_human,voc_bot,ratio_human,ratio_bot):

        
        df_accountreputation =  df_fill(Accountrep_human["accountreputation"],Accountrep_bot["accountreputation"],"accountreputation")
    
        df_tweetdens =  df_fill(tweetdens_human,tweetdens_bot,"tweeting density")
    
        df_weekday =  df_fill(weekday_human["prop"],weekday_bot["prop"],"tweets per week days")

        df_mentions = df_fill(mentions_human,mentions_bot,"avg_mentions_per_user")

        df_voc = df_fill(voc_human,voc_bot,"Vocabulary size per users")

        df_ratio = df_fill(ratio_human,ratio_bot,"follower / following ratio")


        list_metrics = ['Account reputation','Tweeting density','tweets per week days',
                 'avg_mentions_per_user','Vocabulary size per users','Follower / Following ratio'] 

        information_gains = DataFrame(columns=['metric','information gain'], index=range(len(list_metrics)))

        information_gains['metric'] = list_metrics
        information_gains['information gain'] = [calc_information_gain(df_accountreputation, "accountreputation", "user"),
        calc_information_gain(df_tweetdens, "tweeting density", "user"),
        calc_information_gain(df_weekday, "tweets per week days", "user"),
        calc_information_gain(df_mentions, "avg_mentions_per_user", "user"),
        calc_information_gain(df_voc, "Vocabulary size per users", "user"),
        calc_information_gain(df_ratio, "follower / following ratio", "user")]

        information_gains.sort_values('information gain',inplace = True,ascending = False)

        return information_gains


#from sklearn.tree import DecisionTreeClassifier


#    def decisiontree():

## Instantiate the classifier.
## Set random_state to 1 to keep results consistent.
#        clf = DecisionTreeClassifier(random_state=1)

#        clf.fit(df_voc['Vocabulary size per users'],df_voc['user'])


