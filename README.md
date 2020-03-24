# A simple demonstration create a blockchain application on Alibaba Cloud Function Compute 

I have studied the work of blockchain by [Daniel van Flymen](https://medium.com/@vanflymen/learn-blockchains-by-building-one-117428612f46) through his [source code](https://github.com/dvf/blockchain). 

Refer to Ken Formm's [study](https://read.acloud.guru/blockchain-and-serverless-processing-similarities-differences-and-how-they-fit-together-c12142373287), serverless and blockchain can be used together. 

Here I would like to share my experience developing a serverless application based on Daniel and deploy to Alibaba Cloud Function Compute.

Step 1 Create a new function at Function Compute
As the sample is currently implement with Flask framework, the simple way is create a new function (Function Compute > Service-Function > Create Function) by selecting the "Template Function" (as follow)

![alt text][screen1]
[screen1]: https://github.com/JediAzta/FCBlockChain/tree/master/img/01createfunction.png
