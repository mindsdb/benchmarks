## OpenML - [Amazon Employee Access](https://www.openml.org/d/4135) 

Author:  Source: [Kaggle Amazon Employee Access Challenge](https://www.kaggle.com/c/amazon-employee-access-challenge)  

### Description  
The data consists of real historical data collected from 2010 & 2011. Employees are manually allowed or denied access to resources over time.  The data is used to create an algorithm capable of learning from this historical data to predict approval/denial for an unseen set of employees.  

### Dataset Information  
When an employee at any company starts work, they first need to obtain the computer access necessary to fulfill their role. This access may allow an employee to read/manipulate resources through various applications or web portals. It is assumed that employees fulfilling the functions of a given role will access the same or similar resources. It is often the case that employees figure out the access they need as they encounter roadblocks during their daily work (e.g. not able to log into a reporting portal). A knowledgeable supervisor then takes time to manually grant the needed access in order to overcome access obstacles. As employees move throughout a company, this access discovery/recovery cycle wastes a non-trivial amount of time and money.  There is a considerable amount of data regarding an employee’s role within an organization and the resources to which they have access. Given the data related to current employees and their provisioned access, models can be built that automatically determine access privileges as employees enter and leave roles within a company. These auto-access models seek to minimize the human involvement required to grant or revoke employee access.  The original training and test set were merged.  

### Attributes Information  
* ACTION [target]: ACTION is 1 if the resource was approved, 0 if the resource was not  
* RESOURCE: An ID for each resource  
* MGR_ID: The EMPLOYEE ID of the manager of the current EMPLOYEE ID record; an employee may have only one manager at a time  
* ROLE_ROLLUP_1: Company role grouping category id 1 (e.g. US Engineering)  
* ROLE_ROLLUP_2: Company role grouping category id 2 (e.g. US Retail)  
* ROLE_DEPTNAME: Company role department description (e.g. Retail)  
* ROLE_TITLE: Company role business title description (e.g. Senior Engineering Retail Manager)  
* ROLE_FAMILY_DESC: Company role family extended description (e.g. Retail Manager, Software Engineering)  
* ROLE_FAMILY: Company role family description (e.g. Retail Manager)  
* ROLE_CODE: Company role code; this code is unique to each role (e.g. Manager)