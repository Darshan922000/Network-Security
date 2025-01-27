parameter={
    "Decision Tree": {
        'criterion':['gini', 'entropy', 'log_loss'],
    },

    "Random Forest":{
        'n_estimators': [8,16,32,64,128,256]
    },

    "Gradiant Boosting":{
        'learning_rate':[.1,.01,.05,.001],
        'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
        'n_estimators': [8,16,32,64,128,256]
    },

    "Logistic Regression":{},

    "Adaboost":{
        'learning_rate':[.1,.01,0.5,.001],
        'n_estimators': [8,16,32,64,128,256]
    }
}