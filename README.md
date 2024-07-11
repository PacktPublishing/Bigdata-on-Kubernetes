# Big Data on Kubernetes

<a href="https://www.amazon.com/Big-Data-Kubernetes-practical-efficient/dp/1835462146/ref=tmm_pap_swatch_0?_encoding=UTF8&dib_tag=se&dib=eyJ2IjoiMSJ9.f-qgjQEcIcUJ87LXGDQGLtg8bYoODUh-eqkvU-Lk08Gl_Dehn2iyKELYaqXZj2j9zLVxCiWuGdfi-tpY0sA8AzZV9GrYd1fcc4_QobRvWovbWkHMmpfqitRy0NFcoit9QiwnQ8gXFGDd-HQqjgK1cA.6i1oTi7zW4AIDD_NCZwG5lcXrYhl5Ht0d5K1OPMZqNw&qid=1720678581&sr=1-3&utm_source=github&utm_medium=repository&utm_campaign=9781835082287"><img src="https://m.media-amazon.com/images/I/810h3uxswlL._SL1500_.jpg" alt="Shipping & Fee Details" height="256px" align="right"></a>

This is the code repository for [Big Data on Kubernetes](https://www.amazon.com/Big-Data-Kubernetes-practical-efficient/dp/1835462146/ref=tmm_pap_swatch_0?_encoding=UTF8&dib_tag=se&dib=eyJ2IjoiMSJ9.f-qgjQEcIcUJ87LXGDQGLtg8bYoODUh-eqkvU-Lk08Gl_Dehn2iyKELYaqXZj2j9zLVxCiWuGdfi-tpY0sA8AzZV9GrYd1fcc4_QobRvWovbWkHMmpfqitRy0NFcoit9QiwnQ8gXFGDd-HQqjgK1cA.6i1oTi7zW4AIDD_NCZwG5lcXrYhl5Ht0d5K1OPMZqNw&qid=1720678581&sr=1-3&utm_source=github&utm_medium=repository&utm_campaign=9781835082287), published by Packt.

**A practical guide to building efficient and 
scalable data solutions**

## What is this book about?
With step-by-step instructions and examples, this book will teach you the skills needed to build and deploy complex data pipelines on Kubernetes, resulting in efficient and scalable big data solutions.

This book covers the following exciting features:
Install and use Docker to run containers and build concise images
Gain a deep understanding of Kubernetes architecture and its components
Deploy and manage Kubernetes clusters on different cloud platforms
Implement and manage data pipelines using Apache Spark and Apache Airflow
Deploy and configure Apache Kafka for real-time data ingestion and processing
Build and orchestrate a complete big data pipeline using open-source tools
Deploy Generative AI applications on a Kubernetes-based architecture

If you feel this book is for you, get your [copy](https://www.amazon.com/dp/1835462146) today!

<a href="https://www.packtpub.com/?utm_source=github&utm_medium=banner&utm_campaign=GitHubBanner"><img src="https://raw.githubusercontent.com/PacktPublishing/GitHub/master/GitHub.png" 
alt="https://www.packtpub.com/" border="5" /></a>

## Instructions and Navigations
All of the code is organized into folders. For example, Chapter01.

The code will look like the following:
```
import pandas as pd
url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/
master/pima-indians-diabetes.data.csv'

df = pd.read_csv(url, header=None)

df["newcolumn"] = df[5].apply(lambda x: x*2)

print(df.columns)
print(df.head())
print(df.shape)

```

**Following is what you need for this book:**
If you are a data engineer, BI analyst, data team leader, data architect, or tech manager with a basic understanding of big data technologies, then this big data book is for you. Familiarity with the basics of Python programming, SQL queries, and YAML is required to understand the topics discussed in this book

With the following software and hardware list you can run all code files present in the book (Chapter 1-11).
### Software and Hardware List
| Chapter | Software required | OS required |
| -------- | ------------------------------------ | ----------------------------------- |
| 1-11 | Python>=3.9 | Windows, macOS, or Linux |
| 1-11 | Docker, the latest version available | Linux |
| 1-11 | Docker Desktop, the latest version available | Windows or macOS |
| 1-11 | Kubectl | Windows, macOS, or Linux |
| 1-11 | Awscli | Windows, macOS, or Linux |
| 1-11 | Eksctl | Windows, macOS, or Linux |
| 1-11 | DBeaver Community Edition | Windows, macOS, or Linux |

### Related products
* Data Engineering with Databricks Cookbook [[Packt]](https://www.packtpub.com/en-in/product/data-engineering-with-databricks-cookbook-9781837633357?type=subscription) [[Amazon]](https://www.amazon.com/dp/1837633355)

* Data Engineering with Scala and Spark [[Packt]](https://www.packtpub.com/en-in/product/data-engineering-with-scala-and-spark-9781804612583?type=subscription) [[Amazon]](https://www.amazon.com/dp/1804612588)


## Get to Know the Author
**Neylson Crepalde**
is a Generative AI Strategist at AWS. Prior to that, he was CTO at A3Data, a consulting company focused on Data, Analytics and Artificial Intelligence. He holds a PhD in Economic Sociology, a master in Sociology of Culture, an MBA in Cultural Management and a Bachelor in Orchestra Conducting. He has been working with data since 2015. He is committed to sharing knowledge with people of every professional level and helping data teams achieve their best. He is several times AWS certified, Spark certified, Neo4j certified and Airflow certified. Neylson has been teaching for 10+ years now in colleges and MBA programs and he gives regular talks and lectures on Data Architecture, AI strategy, Data Governance and Network Science.
