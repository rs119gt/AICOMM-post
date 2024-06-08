from django.http import JsonResponse
from home.models import Review
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ReviewSerializer
import os
import pandas as pd
from django.conf import settings
from home.models import Product
from .serializers import ProductSerializer

#import matplotlib.pyplot as plt
import nltk
#import numpy as np
import pandas as pd
#import seaborn as sns
nltk.download('stopwords')

@api_view(['GET'])
def getRoutes(request):
    routes=['GET api/','GET api/reviews', 'GET api/allreviews']
    return Response(routes)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import Review
from .serializers import ReviewSerializer

@api_view(['GET'])
def getAllReviews(request):
     # Retrieve all reviews
     reviews = Review.objects.all()
    
     # Serialize the reviews with product details
     serializer = ReviewSerializer(reviews, many=True)

     # print(serializer.data.review_text)
     for review_data in serializer.data:
         print(review_data['review_text'],review_data['purchase_history_details']['product']['id'],review_data['purchase_history_details']['product']['sub_category']['category']['name'],review_data['purchase_history_details']['product']['sub_category']['sname'])
    
     # Return the serialized data
     return Response(serializer.data)



import os
import pandas as pd
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import Review
from .serializers import ReviewSerializer

@api_view(['GET'])
def getReviews(request):
    # Retrieve all reviews
    reviews = Review.objects.all()
    print(reviews)
    # Serialize the reviews
    serializer = ReviewSerializer(reviews, many=True)
    
    # Construct the path to the CSV file using Django settings
    csv_file_path = os.path.join(settings.STATICFILES_DIRS[0], 'review.csv')
    
    try:
        # Load the existing CSV file
        existing_df = pd.read_csv(csv_file_path)
        
        # Initialize a list to hold the new data
        new_data = []
        
        # Extract data from the API response
        for review_data in serializer.data:
            clothing_id = review_data['purchase_history_details']['product']['id']
            review_text = review_data['review_text']
            department_name = review_data['purchase_history_details']['product']['sub_category']['category']['name']
            class_name = review_data['purchase_history_details']['product']['sub_category']['sname']
            
            # Append the extracted data to new_data
            new_data.append([clothing_id, review_text, department_name, class_name])
        
        # Convert the new data to a DataFrame
        new_df = pd.DataFrame(new_data, columns=['Clothing ID', 'Review Text', 'Department Name', 'Class Name'])
        
        
        new_df.to_csv(csv_file_path)

   


        # df = pd.read_csv('Womens Clothing E-Commerce Reviews.csv')
        df=pd.read_csv(csv_file_path)

        # for column in ["Class Name","Review Text"]:
        #     df = df[df[column].notnull()]
        # df.drop(df.columns[0], inplace=True, axis=1)

        from nltk.corpus import stopwords
        #from nltk.stem.porter import PorterStemmer
        from nltk.tokenize import RegexpTokenizer

        #ps = PorterStemmer()

        tokenizer = RegexpTokenizer(r'\w+')
        stop_words = set(stopwords.words('english'))
        result=[]
        def preprocessing(data):
            txt = data.str.lower().str.cat(sep=' ') #1
            words = tokenizer.tokenize(txt) #2
            words = [w for w in words if not w in stop_words] #3
            return words

        nltk.download('vader_lexicon')

        from nltk.sentiment.vader import SentimentIntensityAnalyzer

        # Pre-Processing
        SIA = SentimentIntensityAnalyzer()
        df['Review Text']= df['Review Text'].astype(str)
        
        # Applying Model, Variable Creation
        df['Polarity Score'] = df['Review Text'].apply(lambda x: SIA.polarity_scores(x)['compound'])
        # df['Neutral Score'] = df['Review Text'].apply(lambda x: SIA.polarity_scores(x)['neu'])
        # df['Negative Score'] = df['Review Text'].apply(lambda x: SIA.polarity_scores(x)['neg'])
        # df['Positive Score'] = df['Review Text'].apply(lambda x: SIA.polarity_scores(x)['pos'])

        # Converting 0 to 1 Decimal Score to a Categorical Variable
        # df['Sentiment'] = ''
        # df.loc[df['Polarity Score'] > 0, 'Sentiment'] = 'Positive'
        # df.loc[df['Polarity Score'] == 0, 'Sentiment'] = 'Neutral'
        # df.loc[df['Polarity Score'] < 0, 'Sentiment'] = 'Negative'

        # df_recommended=df[(df['Sentiment']=='Positive')]
        # df_not_recommended=df[(df['Sentiment']=='Negative') | (df['Sentiment']=='Neutral')]
        df_recommended=df
     

        df_sweaters=df_recommended[df_recommended['Class Name']=='Sweaters']
        df_dresses=df_recommended[df_recommended['Class Name']=='Dresses']
        df_jackets=df_recommended[df_recommended['Class Name']=='Jackets']
        df_jeans=df_recommended[df_recommended['Class Name']=='Jeans']
        df_gauge=df_recommended[df_recommended['Class Name']=='Fine Gauge']
        df_pants=df_recommended[df_recommended['Class Name']=='Pants']
        df_skirts=df_recommended[df_recommended['Class Name']=='Skirts']

        #new category=footwear
        df_footwear=df_recommended[df_recommended['Class Name']=='Footwear']
        #df_footwear=df_recommended[df_recommended['Department Name']=='Footwear']

       

        df_pants_filtered=df_pants.groupby(['Clothing ID', 'Class Name'])['Polarity Score'].mean().reset_index()
        df_pants_filtered = df_pants_filtered[df_pants_filtered['Polarity Score'] > 0.7]

        df_skirts_filtered=df_skirts.groupby(['Clothing ID', 'Class Name'])['Polarity Score'].mean().reset_index()
        df_skirts_filtered = df_skirts_filtered[df_skirts_filtered['Polarity Score'] > 0.9]
        
        df_jeans_filtered=df_jeans.groupby(['Clothing ID', 'Class Name'])['Polarity Score'].mean().reset_index()
        df_jeans_filtered = df_jeans_filtered[df_jeans_filtered['Polarity Score'] > 0.8]

        df_sweaters_filtered=df_sweaters.groupby(['Clothing ID', 'Class Name'])['Polarity Score'].mean().reset_index()
        df_sweaters_filtered = df_sweaters_filtered[df_sweaters_filtered['Polarity Score'] > 0.2]

        df_gauge_filtered=df_gauge.groupby(['Clothing ID', 'Class Name'])['Polarity Score'].mean().reset_index()
        df_gauge_filtered = df_gauge_filtered[df_gauge_filtered['Polarity Score'] > 0.89]

        df_dresses_filtered=df_dresses.groupby(['Clothing ID', 'Class Name'])['Polarity Score'].mean().reset_index()
        df_dresses_filtered = df_dresses_filtered[df_dresses_filtered['Polarity Score'] > 0.9]

        df_jackets_filtered=df_jackets.groupby(['Clothing ID', 'Class Name'])['Polarity Score'].mean().reset_index()
        df_jackets_filtered = df_jackets_filtered[df_jackets_filtered['Polarity Score'] > 0.65]

        df_footwear_filtered=df_footwear.groupby(['Clothing ID', 'Class Name'])['Polarity Score'].mean().reset_index()
        df_footwear_filtered = df_footwear_filtered[df_footwear_filtered['Polarity Score'] > 0.6]
        
        print(df_sweaters_filtered)
        print(df_sweaters)
        print(df_skirts_filtered)
        print(df_jeans_filtered)
        print(df_pants_filtered)
        print(df_gauge_filtered)
        print(df_dresses_filtered)
        print(df_jackets_filtered)
        print(df_footwear_filtered)
        #print(df_footwear)
        print(".jsjdls ....................................................................")
        print("////////////////////")
        print("Mean Polarity score of Pants", df_pants['Polarity Score'].mean())
        print("////////////////////")
        recomended_clothing_id = df_sweaters_filtered['Clothing ID'].tolist() + df_skirts_filtered['Clothing ID'].tolist() + df_jeans_filtered['Clothing ID'].tolist() + df_pants_filtered['Clothing ID'].tolist() + df_dresses_filtered['Clothing ID'].tolist() + df_jackets_filtered['Clothing ID'].tolist() + df_gauge_filtered['Clothing ID'].tolist() + df_footwear_filtered['Clothing ID'].tolist()

        #df_sweaters_filtered = df_sweaters_filtered.reset_index()
        #df_skirts_filtered = df_skirts_filtered.reset_index()
        #sweater_ids = df_sweaters_filtered['index'].tolist()
        #skirt_ids = df_skirts_filtered['index'].tolist()

        #recomended_clothing_id = sweater_ids
        print(recomended_clothing_id)
        result.extend(recomended_clothing_id)
        print(result)
        print("-----------------result")
    except Exception as e:
       
        return Response({"error": f"An error occurred while processing the CSV file: {e}"}, status=500)
    
    product_queryset = Product.objects.filter(id__in=result)
    print(product_queryset)
        
    serializer = ProductSerializer(product_queryset, many=True)

       
    return Response(serializer.data)
