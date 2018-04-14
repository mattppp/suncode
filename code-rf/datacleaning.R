library(dplyr)


setwd("~/Involvement/Suncode 2018/suncode/data/census")

files<- (Sys.glob("*.csv"))
all_df = lapply(files, read.csv)
files


educ = all_df[[2]] %>% 
  mutate(Total = rowSums(.[3:26]),
         `HS.or.Below` = rowSums(.[3:19] )/Total, 
         Undergrad.or.Below =  rowSums(.[20:23] )/Total,
         Graduate.School = rowSums(.[24:26]/Total)) %>%     
  filter(Total >0) %>% 
  select(ZIP, HS.or.Below, Undergrad.or.Below, Graduate.School) 
  
incpop = all_df[[5]] %>% 
  mutate(Median.Income = as.numeric(Median.Income),
         Population = as.numeric(Population)) 


full_census = all_df[[1]] %>% 
  full_join(educ) %>% 
  full_join(all_df[[4]]) %>% 
  full_join(incpop) %>% 
  mutate(Zip = as.factor(ZIP)) %>% 
  select(Zip, everything(), -ZIP) %>% 
  filter(!is.na(Median.Income)) 

write.csv(full_census,"../CensusZIP.csv", row.names = FALSE)
  

install_cancel = read.csv("../../data_combined.csv")
zillow = read.csv("../Zillow Data.csv")
insol = read.csv("../Insolation_by_Zip.csv")
yearSun = read.csv("../Google Sunroof_Yearly_Sunlight_by_State.csv")

joined = zillow %>% 
  select(JobId, Zip, Latitude, Longitude, AverageTilt, PaymentType, GrossPrice, FederalTaxCredit, Bedroom, HomeSqFoot, HeatingType, Heating, CoolingType, Cooling, YearBuilt) %>% 
  mutate(Zip = as.factor(Zip)) %>% 
  left_join(install_cancel, by = "JobId") %>% 
select(Zip = Zip.x,  everything(), -Zip.y) %>% 
  left_join(insol %>% 
              mutate(Zip = as.factor(Zip))) %>% 
  left_join(yearSun) %>% 
  mutate(Zip = as.numeric(Zip)) %>% 
  left_join(full_census%>% 
              mutate(Zip = as.numeric(Zip)) ) %>% 
  filter(!is.na(Status)) %>% 
  select(-X)
View(joined)

#number of installs and cancels
joined %>% 
  group_by(Status) %>% 
  count()

install_cancel %>% 
  group_by(Status) %>% 
  count()


write.csv(joined,"../../all_joined.csv", row.names = FALSE)
  
library(ggplot2)
library(GGally)
install.packages("car", dependencies = TRUE)
library(car) # for VIF
library(caTools)
library(ROCR)
library(ggplot2)
set.seed(144)
df = joined %>% 
  mutate(YearBuilt = as.factor(YearBuilt), Avg.Value = as.numeric(Avg.Value))
df$split = sample.split(df$Status, SplitRatio = 0.7)

df.train <- filter(df, split == TRUE) # is split a variable in loans?
df.test <- filter(df, split == FALSE)
table(df.train$Status)

mod <- glm(Status ~ AverageTilt + RoofType +  HS.or.Below +Avg.Value + Median.Income +
           Insolation + NumStories + AverageShading + RoofSqFoot + OldBill, data=df.train, family="binomial")
summary(mod)
